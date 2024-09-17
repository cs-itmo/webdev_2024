from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def sample_template(request: Request):
    user = {"is_authenticated": True, "name": "John Doe"}
    products = [{"name": "Laptop", "price": 999}, {"name": "Phone", "price": 799}]
    articles = [{"title": "FastAPI Tips", "date": datetime(2023, 1, 15)},
                {"title": "Python Best Practices", "date": datetime(2023, 2, 10)}]
    about_us_html = "<p>We are <img src=''> <strong>the best</strong> at what we do!</p>"
    recommended_items = [{"name": "Headphones", "price": 199}, {"name": "Monitor", "price": 299}]
    
    return templates.TemplateResponse("sample_template.html", {
        "request": request,
        "title": "Jinja2 Template Demo",
        "user": user,
        "products": products,
        "articles": articles,
        "about_us_html": about_us_html,
        "recommended_items": recommended_items
    })

@app.get("/about/", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "About Us"})