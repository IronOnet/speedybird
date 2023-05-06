from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base, sessionmaker 

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3" 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Session = sessionmaker(bind=engine, autoflush=False) 

Base = declarative_base() 