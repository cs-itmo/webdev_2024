from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, FastAPI
from faker import Faker

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: int

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

fake = Faker()
users = [User(name=fake.name(), email=fake.email(), age=fake.random_int(18, 100)) for _ in range(10)]
items = [Item(name=fake.word(), price=fake.random_int(1000, 10000) / 100) for _ in range(10)]

async def common_parameters(q: str = "", skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    found_items = [item for item in items if commons["q"] in item.name]
    return {"items": [item for item in found_items[commons["skip"] : commons["skip"] + commons["limit"]]]}


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    found_users = [user for user in users if commons["q"] in user.name]
    return {"users": [user for user in found_users[commons["skip"] : commons["skip"] + commons["limit"]]]}