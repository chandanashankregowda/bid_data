from fastapi import FastAPI
from sqlalchemy import create_engine, text, inspect
import pandas as pd

app = FastAPI()

# Connect to your SQLite database
engine = create_engine("sqlite:///bid.db")

# Home route
@app.get("/")
def home():
    return {
        "message": "Bid database API is running"
    }

# Show all table names
@app.get("/tables")
def get_tables():
    inspector = inspect(engine)
    return {
        "tables": inspector.get_table_names()
    }

# Get data from any table
@app.get("/{table_name}")
def get_table_data(table_name: str, limit: int = 50):

    query = f"SELECT * FROM {table_name} LIMIT {limit}"

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return df.to_dict(orient="records")
