import os
from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException


app = FastAPI()
items = {
    1: {"name": "Item 1", "description": "This is item 1"},
    2: {"name": "Item 2", "description": "This is item 2"},
    3: {"name": "Item 3", "description": "This is item 3"},
}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id in items:
        return items[item_id]
    return {"error": "Item not found"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid document type")

    contents = await file.read()
    file_path = f"uploads/{file.filename}"
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(contents)

    return {"message": "PDF uploaded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
#http://127.0.0.1:8000/docs#/default/upload_pdf_upload_post
#uvicorn main:app --reload