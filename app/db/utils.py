from sqlalchemy import text
from sqlalchemy.engine import Engine

def check_db_connection(engine: Engine):
    """Mission: Verify the database is alive and reachable."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database connection already")
    except Exception as e:
        print(f"CRITICAL: Could not connect to database: {e}")
        raise e