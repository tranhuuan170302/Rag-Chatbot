from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://postgres:admin123@localhost:5432/auth_service_db"

engine = create_engine(DB_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()