from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Template

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_input():
    """
    This route displays a form where a user can input some data.
    """
    return """
    <html>
    <head><title>SSTI Demo</title></head>
    <body>
        <h1>FastAPI SSTI Demo</h1>
        <form action="/submit" method="post">
            <label for="user_input">Enter some data:</label>
            <input type="text" id="user_input" name="user_input">
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """


@app.post("/submit", response_class=HTMLResponse)
async def submit_form(user_input: str = Form(...)):
    """
    This route demonstrates SSTI by rendering user input using a raw template string.
    The user input is directly interpreted as a Jinja2 template, which is dangerous.
    """
    template = Template(user_input)
    rendered_result = template.render()

    return f"""
    <html>
    <head><title>SSTI Result</title></head>
    <body>
        <h1>SSTI Result</h1>
        <p>You entered (rendered): {rendered_result}</p>
    </body>
    </html>
    """
