import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

postgres_url = os.getenv("DATABASE_URL")
if not postgres_url:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
