import os
import uuid
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}

def allowed_file_extension(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS

@app.post("/upload/")
async def create_upload_file(file: UploadFile):
    if not allowed_file_extension(file.filename):
        raise HTTPException(status_code=400, detail="File extension not allowed.")

    _, ext = os.path.splitext(file.filename)
    file_name = f"{str(uuid.uuid4())}{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    try:
        with open(file_path, "wb") as w:
            w.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save the file.") from e

    return JSONResponse(content={"filename": file_name})

@app.get("/image/{filename}")
async def get_upload_file(filename: str):
    safe_filename = Path(filename).name
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(file_path, filename=safe_filename, content_disposition_type="inline")