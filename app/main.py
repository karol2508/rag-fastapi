from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models import QuestionRequest, AnswerResponse, UploadResponse
from app.rag import process_pdf, get_answer
import shutil
import os

app = FastAPI(
    title="RAG PDF Chatbot API",
    description="Upload a PDF and ask questions about its content using RAG",
    version="1.0.0"
)

UPLOAD_DIR = "docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {
        "message": "RAG PDF Chatbot API",
        "endpoints": {
            "upload": "/upload-pdf",
            "ask": "/ask",
            "health": "/health"
        }
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = process_pdf(file_path)
    
    return UploadResponse(
        message="PDF uploaded and processed successfully",
        filename=file.filename,
        pages=result["pages"],
        chunks=result["chunks"]
    )

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    result = get_answer(request.question)
    
    return AnswerResponse(
        question=request.question,
        answer=result["answer"],
        source_document=result["source"]
    )