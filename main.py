import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import shutil
from pathlib import Path


app = FastAPI()


UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)


ALLOWED_FILE_TYPES = {
    "application/json": ".json",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx"
}


def get_file_extension(content_type: str):
    return ALLOWED_FILE_TYPES.get(content_type)

@app.post("/file/upload")
def upload_file(file: UploadFile = File(...)):
   
    file_extension = get_file_extension(file.content_type)
    if not file_extension:
        raise HTTPException(status_code=415, detail="Invalid file type. Only JSON, PPTX, DOCX, and XLSX files are allowed.")
    
 
    file_path = UPLOAD_DIR / f"{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "message": "File uploaded successfully."}

@app.post("/file/uploaddownloaded")
def upload_and_download_file(file: UploadFile = File(...)):

    file_extension = get_file_extension(file.content_type)
    if not file_extension:
        raise HTTPException(status_code=415, detail="Invalid file type. Only JSON, PPTX, DOCX, and XLSX files are allowed.")
    
   
    file_path = UPLOAD_DIR / f"{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
   
    return FileResponse(file_path, filename=file.filename, headers={"Content-Type": file.content_type})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  
