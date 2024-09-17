from typing import Annotated
from fastapi import Cookie, FastAPI, Response
from pydantic import BaseModel
import httpx

def get_cat(api_key):
    return httpx.get(f"https://api.thecatapi.com/v1/images/search?api_key={api_key}").json()[0]

class AuthRequest(BaseModel):
    api_key: str

app = FastAPI()

@app.post("/auth/")
async def auth(response: Response, auth_request: AuthRequest):
    response.set_cookie(key="api_key", value=auth_request.api_key)
    return {"message": "Your API key has been set as a cookie"}

@app.get("/cats/")
async def get_cats(api_key: Annotated[str, Cookie(alias="api_key")]):
    return get_cat(api_key)

@app.get("/cats/{cat_id}")
async def get_cats(cat_id: str):
    cat = httpx.get(f"https://cdn2.thecatapi.com/images/{cat_id}.jpg").content
    return Response(content=cat, media_type="image/jpeg")