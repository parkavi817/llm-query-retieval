import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.services.document_parser import extract_text_from_pdf, extract_text_from_docx, extract_text_from_email
from app.routes import routes

app = FastAPI()

# CORS middleware (allow all origins for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routes with /api/v1 prefix
app.include_router(routes.router, prefix="/api/v1")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    if ".." in filename or filename.startswith("/"):
        return JSONResponse(status_code=400, content={"error": "Invalid filename."})

    allowed_exts = [".pdf", ".docx", ".txt", ".eml"]
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_exts:
        return JSONResponse(status_code=400, content={"error": f"Unsupported file type: {ext}"})

    save_path = os.path.join(UPLOAD_DIR, filename)

    try:
        contents = await file.read()
        with open(save_path, "wb") as f:
            f.write(contents)
        return JSONResponse(content={"message": f"Uploaded {filename} successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.post("/parse/")
async def parse_uploaded_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx", ".eml", ".msg", ".txt"]:
        return JSONResponse(status_code=400, content={"error": f"Unsupported file type: {ext}"})

    try:
        contents = await file.read()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        tmp.write(contents)
        tmp.close()

        text = ""
        if ext == ".pdf":
            text = extract_text_from_pdf(tmp.name)
        elif ext == ".docx":
            text = extract_text_from_docx(tmp.name)
        elif ext in [".eml", ".msg"]:
            text = extract_text_from_email(tmp.name)
        elif ext == ".txt":
            text = contents.decode('utf-8', errors='ignore')

        os.unlink(tmp.name)
        return {"text": text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
