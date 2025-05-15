from sqlmodel import SQLModel, create_engine, Session
from config import settings

DATABASE_URL = settings.DB_URI
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    return Session(engine)
