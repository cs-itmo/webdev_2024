# Flask minimal app
from flask import Flask
flask_app = Flask(__name__)
@flask_app.route('/')
def hello_world():
    return 'Hello, World!'

# Django wsgi.py
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
application = get_wsgi_application()

# FastAPI minimal app
from fastapi import FastAPI
fastapi_app = FastAPI()
@fastapi_app.get("/")
def read_root():
    return {"Hello": "World"}
