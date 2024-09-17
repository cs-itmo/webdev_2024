from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserRequest(BaseModel):
    username: str

class TokenRequest(BaseModel):
    token: str

@app.post("/get_token")
def get_token(input_data: UserRequest):
    data = {
        "sub": input_data.username,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iss": "http://localhost"
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token}

@app.post("/verify_token")
def verify_token(token_request: TokenRequest):
    try:
        payload = jwt.decode(token_request.token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token validation failed")
        
        return {"message": f"Token is valid for user {username}", "payload": payload}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def read_root():
    return {"message": "JWT Demo App"}
