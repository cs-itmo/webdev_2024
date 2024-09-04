from fastapi import FastAPI, Query
from datetime import datetime

app = FastAPI()


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False, timestamp: datetime | None = Query(None, example="2023-08-28T14:30:00Z"),
):
    item = {"item_id": item_id, "owner_id": user_id, "timestamp": datetime.now()}    
    if q:
        item.update({"q": q})
    if timestamp:
        item.update({"timestamp": timestamp})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item