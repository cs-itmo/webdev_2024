from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


app = FastAPI()

# Create SQLite database connection
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

# Define base class for models
Base = declarative_base()

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a simple model to store items
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Initialize the database
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI + SQLAlchemy demo"}
