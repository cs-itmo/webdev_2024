from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from typing import List
from fastapi.templating import Jinja2Templates
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_binary(self, binary_data: bytes):
        for connection in self.active_connections:
            await connection.send_bytes(binary_data)

manager = ConnectionManager()

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse(request=request, name="advanced.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await manager.send_personal_message("Welcome to the WebSocket server!", websocket)
        while True:
            try:
                data = await websocket.receive()
                logger.info(f"Received data: {data}")
                if "text" in data and isinstance(data['type'], str):
                    await manager.broadcast(f"{data['text']}")
                elif "bytes" in data and isinstance(data['bytes'], bytes):
                    await manager.broadcast_binary(data['bytes'])
            except WebSocketDisconnect:
                manager.disconnect(websocket)
                break
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                await websocket.close(reason=str(e))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
