import mongoengine as me
from pydantic import BaseModel

# MongoDB connection setup
DATABASE_URL = "mongodb://mongodb:27017/itmo"
me.connect(host=DATABASE_URL)

# MongoEngine User model
class User(me.Document):
    email = me.StringField(required=True, unique=True)
    hashed_password = me.StringField(required=True)

    meta = {'collection': 'users'}

# Pydantic model for response serialization
class UserResponse(BaseModel):
    id: str
    email: str

