from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

# SQLite (local file)  # (commented out now)
# DATABASE_URL = "sqlite:///./starwars.sqlite"

# Use MySQL (ensure schema 'starwarsDB' exists): CREATE DATABASE starwarsDB;
# Activate venv before using: .\.venv\Scripts\Activate.ps1
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/starwarsDB"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def test_connection():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Connection successful!")

def load_models():
    # Import to register tables with Base.metadata
    import orm_models  # noqa: F401

# Usage to import models elsewhere:
# from orm_models import Franchise, Film, Character
# session = SessionLocal()
# ...existing code...
