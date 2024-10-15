# server.py
import json
import uuid
from typing import Dict, Any
from fastapi import FastAPI
import redis

app = FastAPI()

# Инициализация Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Очередь задач
QUEUE_NAME = "task_queue"

# Функция для добавления задачи в очередь
def enqueue_task(task_data: Dict[str, Any]):
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "data": task_data,
        "status": "pending"
    }
    redis_client.rpush(QUEUE_NAME, json.dumps(task))
    redis_client.set(f"task:{task_id}", json.dumps(task))
    return task_id

# Эндпоинт для добавления задачи
@app.post("/add-task/")
async def add_task(task: Dict[str, Any]):
    task_id = enqueue_task(task)
    return {"task_id": task_id, "message": "Task added to queue"}

# Эндпоинт для проверки статуса задачи
@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task_json = redis_client.get(f"task:{task_id}")
    if task_json:
        task = json.loads(task_json)
        return {"task_id": task_id, "status": task["status"]}
    return {"task_id": task_id, "status": "not found"}
