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
    
    # Add the item name to a set for indexing
    if await redis_client.hexists("item_names", item.name):
        existing_item_ids = set(json.loads(await redis_client.hget("item_names", item.name)))
        existing_item_ids |= set([item_id,])
        await redis_client.hset("item_names", item.name, json.dumps(list(existing_item_ids)))
    else:
        await redis_client.hset("item_names", item.name, json.dumps([item_id,]))
    return item

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    redis_client = app.state.redis_client

    # Fetch the item from Redis
    item_data = await redis_client.hget("items", item_id)
    if not item_data:
        raise HTTPException(status_code=404, detail="Item not found")

    return json.loads(item_data)

@app.get("/items", response_model=List[Item])
async def list_items(name: Optional[str] = None):
    redis_client = app.state.redis_client

    if await redis_client.hexists("item_names", name):
        existing_item_ids = set(json.loads(await redis_client.hget("item_names", name)))
        items = []
        for item_id in existing_item_ids:
            item_data = await redis_client.hget("items", item_id)
            items.append(json.loads(item_data))
        return items
    else:
        raise HTTPException(status_code=404, detail="Item not found")

