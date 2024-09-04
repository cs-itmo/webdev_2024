from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uuid
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn.info")

users_db = {}
tokens_db = {}
security = HTTPBearer()

class UserRequest(BaseModel):
    username: str
    password: str

class User(UserRequest):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


def authenticate_user(username: str, password: str) -> User|None:
    user = users_db.get(username)
    if user and user.password == password:
        return user
    return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = tokens_db.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = next((user for user in users_db.values() if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.post("/register")
async def register(user: UserRequest):
    logger.info("Registering user %s", user.username)
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_id = str(uuid.uuid4())
    users_db[user.username] = User(id=user_id, **user.model_dump())
    return {"msg": "User registered successfully", "id": user_id}

@app.post("/auth", response_model=Token)
async def auth(user: UserRequest) -> Token:
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = str(uuid.uuid4())
    tokens_db[token] = authenticated_user.id
    return {"access_token": token}

@app.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "id": current_user.id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)