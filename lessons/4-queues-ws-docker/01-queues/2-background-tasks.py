from fastapi import BackgroundTasks, FastAPI, Form
from asyncio import sleep
from fastapi.responses import HTMLResponse
from datetime import datetime
app = FastAPI()


async def write_notification(email: str, message: str = ""):
    await sleep(5)
    with open("log.txt", mode="a+") as email_file:
        content = f"notification for {email}: Message '{message}' saved. Timestamp: {datetime.now()}\n"
        email_file.write(content)


@app.post("/send-notification/")
async def send_notification(background_tasks: BackgroundTasks, email: str = Form(), message: str = Form()):
    background_tasks.add_task(write_notification, email, message)
    return {"message": "Notification sent in the background"}


@app.get("/")
async def root():
    return HTMLResponse("<form action='/send-notification' method='post'><input name='email' type='email' value='demo@lms.itmo.xyz'><br><textarea name='message'>Message</textarea><br><br><button>Send notification</button></form>")
