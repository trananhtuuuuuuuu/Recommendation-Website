from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

try:
  conn = psycopg2.connect(host="localhost", port=8386, database="rw-db", user="postgres", password="123456", cursor_factory=RealDictCursor)
  cursor = conn.cursor()
  print(f"Database connection successful")
except Exception as error:
  print(f"Database connection failed")


class Item(BaseModel):
  name: str
  description: str | None = None
  price: float
  tax: float | None = None


@app.post("/items")
async def create_item(item: Item):
  return item

