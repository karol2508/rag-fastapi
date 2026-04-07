# RAG PDF Chatbot API

A production-ready REST API that lets you upload PDF documents and ask questions 
about their content using Retrieval-Augmented Generation (RAG).

## How it works

1. Upload a PDF via the `/upload-pdf` endpoint
2. The API splits the document into chunks and creates vector embeddings
3. Ask a question via `/ask` — the API retrieves relevant context and generates an answer
4. Get a structured JSON response with the answer and source document

## Tech Stack

- **FastAPI** — REST API framework
- **LangChain** — LLM orchestration
- **OpenAI API** — GPT-3.5-turbo for answer generation + embeddings
- **FAISS** — Vector database for semantic search
- **Docker** — Containerization
- **Pydantic** — Data validation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and available endpoints |
| GET | `/health` | Health check |
| POST | `/upload-pdf` | Upload and process a PDF |
| POST | `/ask` | Ask a question about the uploaded PDF |

## Installation & Usage

### Local
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker
```bash
docker-compose up --build
```

Add your OpenAI API key in `.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

## Interactive Documentation

Once running, visit `http://localhost:8000/docs` for the full Swagger UI.

## Skills demonstrated

- REST API design with FastAPI
- RAG (Retrieval Augmented Generation)
- Vector databases (FAISS)
- Docker containerization
- LangChain framework
- OpenAI API integration
- Pydantic data validation
