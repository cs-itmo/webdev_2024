from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import redis.asyncio as redis
import json
import uuid
from models import Item
from typing import List, Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    try:
        app.state.redis_client = redis_client
        yield
    finally:
        await redis_client.close()

app = FastAPI(lifespan=lifespan)

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    redis_client = app.state.redis_client

    # Generate a unique ID if not provided
    item_id = item.id or str(uuid.uuid4())
    item.id = item_id

    # Store the item in Redis as a JSON string
    await redis_client.hset("items", item_id, json.dumps(item.model_dump()))
    return item

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    redis_client = app.state.redis_client

    # Fetch the item from Redis
    item_data = await redis_client.hget("items", item_id)
    if not item_data:
        raise HTTPException(status_code=404, detail="Item not found")

    return json.loads(item_data)

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    redis_client = app.state.redis_client

    # Check if the item exists
    if not await redis_client.hexists("items", item_id):
        raise HTTPException(status_code=404, detail="Item not found")

    # Update the item
    item.id = item_id
    await redis_client.hset("items", item_id, json.dumps(item.model_dump()))
    return item

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    redis_client = app.state.redis_client

    # Delete the item from Redis
    if not await redis_client.hdel("items", item_id):
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted successfully"}

@app.get("/items", response_model=List[Item])
async def list_items(name: Optional[str] = None):
    redis_client = app.state.redis_client

    # Fetch all items from Redis
    all_items = await redis_client.hvals("items")
    items = [json.loads(item) for item in all_items]

    # If a search query is provided, filter the items
    if name:
        items = [item for item in items if name.lower() in item["name"].lower()]

    return items
