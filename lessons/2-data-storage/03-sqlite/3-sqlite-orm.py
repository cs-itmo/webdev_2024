from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship, sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session

app = FastAPI()
DATABASE_URL = "sqlite:///./test.db"

# Create SQLite engine
engine = create_engine(DATABASE_URL)

# Define the base class for our models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Model Definitions ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    # One-to-Many relationship: User can have multiple posts
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

    # Foreign key to link posts to users
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to User
    owner = relationship("User", back_populates="posts")

# Initialize the database tables
Base.metadata.create_all(bind=engine)

# Test endpoint
@app.get("/")
def read_root(db: Session = Depends(get_db)):
    random_post = db.query(Post).order_by(func.random()).first()
    raw_query = str(db.query(Post).order_by(func.random()).statement.compile(compile_kwargs={"literal_binds": True}))
    return {"random_post": random_post, "raw_query": raw_query}

@app.get("/init/")
def init_db():
    from faker import Faker
    fake = Faker()
    db = SessionLocal()
    # clear the database
    db.query(User).delete()
    db.query(Post).delete()
    for _ in range(10):
        user = User(name=fake.name(), email=fake.email())
        db.add(user)
        db.commit()
        for _ in range(5):
            post = Post(title=fake.sentence(), content=fake.text(), owner=user)
            db.add(post)
        db.commit()