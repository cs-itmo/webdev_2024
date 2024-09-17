from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionLocal, engine, Base, get_db
from schemas import UserCreate, Token, UserResponse
from utils import verify_password, get_password_hash
from auth import create_access_token, get_current_user
from database import User

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# User registration route
@app.post("/register/", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password and create the user
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# User login route
@app.post("/login/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate JWT token for authentication
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Protected route to check JWT token validity
@app.get("/me/", response_model=UserResponse)
def access_cabinet(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome to your cabinet, {current_user.email}!", "user": current_user}


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Auth Demo"}
