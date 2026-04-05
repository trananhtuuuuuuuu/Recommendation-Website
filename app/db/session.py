# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#TEMPLATE_DATABASE_URL = '"postgresql://user:password@localhost/db"'
DATABASE_URL = "postgresql://postgres:123456@localhost:8386/rw-db"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)