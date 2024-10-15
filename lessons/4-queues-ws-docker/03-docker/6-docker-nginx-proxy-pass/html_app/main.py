from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI with WebSocket</title>
    </head>
    <body>
        <h1>Hello, FastAPI!</h1>
        <button onclick="fetchRandomNumber()">Fetch Random Number</button>
        <p id="random-number"></p>
        <script>
            function fetchRandomNumber() {
                const ws = new WebSocket("ws://" + window.location.host + "/ws/random");
                ws.onmessage = function(event) {
                    document.getElementById('random-number').innerText = "Random number: " + event.data;
                    ws.close();
                };
                ws.onerror = function(error) {
                    console.error("WebSocket error:", error);
                };
            }
        </script>
    </body>
    </html>
    """
