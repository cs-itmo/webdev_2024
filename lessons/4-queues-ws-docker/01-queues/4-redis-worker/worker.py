import json
import time
import redis
from datetime import datetime

# Инициализация Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Очередь задач
QUEUE_NAME = "task_queue"

# Функция для выполнения задачи
def process_task(task_data):
    # Здесь выполняется задача
    time.sleep(5)  # Имитация длительной работы
    print(f"Task processed: {task_data}")

# Функция воркера
def worker():
    print("Worker started")
    while True:
        # Получаем задачу из очереди
        _, task_json = redis_client.blpop(QUEUE_NAME)
        task = json.loads(task_json)
        
        # Обновляем статус задачи
        task["status"] = "processing"
        task["started_at"] = datetime.now().isoformat()
        redis_client.set(f"task:{task['id']}", json.dumps(task))
        
        # Выполняем задачу
        process_task(task["data"])
        
        # Обновляем статус задачи
        task["status"] = "completed"
        task["finished_at"] = datetime.now().isoformat()
        redis_client.set(f"task:{task['id']}", json.dumps(task))

if __name__ == "__main__":
    worker()