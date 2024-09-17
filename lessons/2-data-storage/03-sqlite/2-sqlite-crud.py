from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from sqlalchemy.orm import Session

Base = declarative_base()
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class ItemCreate(BaseModel):
    name: str

class ItemRead(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI + SQLAlchemy demo"}

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> ItemRead:
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

@app.get("/items/")
def read_items(db: Session = Depends(get_db)) -> list[ItemRead]:
    items = db.query(Item).all()
    return items

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    raw_query = str(db.query(Item).filter(Item.id == item_id).statement.compile(compile_kwargs={"literal_binds": True}))
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return raw_query

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} deleted"}