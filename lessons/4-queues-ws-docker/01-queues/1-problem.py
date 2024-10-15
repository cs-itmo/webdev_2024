from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from asyncio import sleep
from datetime import datetime
app = FastAPI()


@app.get("/")
async def root():
    return HTMLResponse("<form action='/send-notification' method='post'><input name='email' type='email' value='demo@lms.itmo.xyz'><br><textarea name='message'>Message</textarea><br><br><button>Send notification</button></form>")


@app.post("/send-notification/")
async def send_notification(email: str = Form(), message: str = Form()):
    await sleep(5)
    with open("log.txt", mode="a+") as email_file:
        content = f"notification for {email}: {message} saved. Timestamp: {datetime.now()}\n"
        email_file.write(content)
    return {"message": "Notification sent"}