from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_url = "postgresql://postgres:Ank123!@localhost:5432/test2"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
