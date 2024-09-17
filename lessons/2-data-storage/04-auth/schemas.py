from pydantic import BaseModel

# Pydantic model for user registration
class UserCreate(BaseModel):
    email: str
    password: str

# Pydantic model for the JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str

class UserResponse(BaseModel):
    message: str
    user: User
