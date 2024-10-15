from fastapi import FastAPI, Depends, HTTPException
from database import User, UserResponse

app = FastAPI()

@app.post("/users/", response_model=UserResponse)
async def create_user(email: str, password: str):
    if User.objects(email=email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(email=email, hashed_password=password)
    user.save()
    
    return UserResponse(id=str(user.id), email=user.email)

@app.get("/users/{email}", response_model=UserResponse)
async def get_user(email: str):
    user = User.objects(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=str(user.id), email=user.email)
