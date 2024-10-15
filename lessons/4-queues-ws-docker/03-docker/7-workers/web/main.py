from fastapi import FastAPI, Form
from celery import Celery
from fastapi.responses import HTMLResponse
from datetime import datetime
import time

app = FastAPI()

# Initialize Celery
celery = Celery(__name__)
celery.conf.broker_url = "redis://redis:6379/0"
celery.conf.result_backend = "redis://redis:6379/0"

@celery.task(name="write_notification")
def write_notification(email: str, message: str = ""):
    time.sleep(5)
    with open("log.txt", mode="a+") as email_file:
        content = f"notification for {email}: {message} saved. Timestamp: {datetime.now()}\n"
        email_file.write(content)
    return f"Notification sent to {email}"

@app.post("/send-notification")
async def send_notification(email: str = Form(), message: str = Form()):
    task = write_notification.delay(email, message=message)
    return {"task_id": task.id, "message": "Notification sent in the background"}

@app.get("/")
async def root():
    return HTMLResponse("<form action='/send-notification' method='post'><input name='email' type='email' value='demo@lms.itmo.xyz'><br><textarea name='message'>Message</textarea><br><br><button>Send notification</button></form>")
