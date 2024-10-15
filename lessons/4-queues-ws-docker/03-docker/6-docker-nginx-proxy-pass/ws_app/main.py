import random
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws/random")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    random_number = random.randint(1, 100)
    await websocket.send_text(str(random_number))
    await websocket.close()
