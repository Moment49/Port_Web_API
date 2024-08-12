from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./portfolio_app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Instantiate the session class
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Defines the base which the models will inherit from
Base = declarative_base()

def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

