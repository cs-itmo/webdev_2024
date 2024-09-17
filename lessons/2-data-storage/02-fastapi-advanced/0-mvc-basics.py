from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home Page"})

@app.get("/items/")
async def read_items():
    return [{"name": "Item 1", "price": 10.5}, {"name": "Item 2", "price": 20.0}]

@app.get("/about/", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "About Us"})