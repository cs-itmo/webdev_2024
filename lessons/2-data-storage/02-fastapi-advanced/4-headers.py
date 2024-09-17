from typing import Annotated
from fastapi import Header, FastAPI, Response, Cookie, Request
from pydantic import BaseModel
import httpx

def get_cat(api_key):
    return httpx.get(f"https://api.thecatapi.com/v1/images/search?api_key={api_key}").json()[0]

app = FastAPI()

@app.get("/remind/")
async def auth(response: Response, api_key: Annotated[str, Cookie()] = None):
    if api_key:
        response.headers["X-Cat"] = api_key
        return {"message": "Your API key has been found and set as a header"}
    else:
        return {"message": "No API key found"}

@app.get("/cats/")
async def get_cats(api_key: Annotated[str, Header(alias='X-Cat')]):
    return get_cat(api_key)

@app.get("/cats/{cat_id}")
async def get_cats(cat_id: str):
    cat = httpx.get(f"https://cdn2.thecatapi.com/images/{cat_id}.jpg").content
    return Response(content=cat, media_type="image/jpeg")