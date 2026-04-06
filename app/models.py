from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    source_document: str

class UploadResponse(BaseModel):
    message: str
    filename: str
    pages: int
    chunks: int