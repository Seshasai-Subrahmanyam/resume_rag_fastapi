"""
FastAPI Server - Production-ready API for Resume RAG
"""
import json
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import Config
from rag_chain import rag_chain


# === Request/Response Models ===

class QueryRequest(BaseModel):
    """Query request model."""
    question: str = Field(..., description="Question about the resume")
    persona: Optional[str] = Field("default", description="Persona: 'hr', 'peer', 'founder', or 'default'")


class QueryResponse(BaseModel):
    """Query response model."""
    answer: str
    persona: str
    sources_count: int


class StatusResponse(BaseModel):
    """Status response model."""
    status: str
    message: str


class RebuildResponse(BaseModel):
    """Rebuild response model."""
    status: str
    documents_indexed: int


# === Application Setup ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    print("🚀 Starting Resume RAG Server...")
    if rag_chain.is_ready:
        print("✅ Vector store loaded with existing data")
    else:
        print("⚠️ Vector store empty - call POST /api/rebuild to initialize")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title="Resume RAG API",
    description="AI-powered resume Q&A for Seshasai Nagadevara",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Endpoints ===

@app.get("/")
async def root():
    """API info and endpoints."""
    return {
        "name": "Resume RAG API",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check",
            "POST /api/query": "Ask a question",
            "POST /api/rebuild": "Rebuild vector store",
            "GET /docs": "API documentation"
        },
        "personas": ["default", "hr", "peer", "founder"],
        "ready": rag_chain.is_ready
    }


@app.get("/health", response_model=StatusResponse)
async def health():
    """Health check endpoint."""
    return StatusResponse(
        status="healthy",
        message=f"Ready: {rag_chain.is_ready}"
    )


@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the resume using RAG."""
    try:
        result = rag_chain.query(
            question=request.question,
            persona=request.persona or "default"
        )
        return QueryResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/api/rebuild", response_model=RebuildResponse)
async def rebuild():
    """Rebuild vector store from resume URL."""
    try:
        result = rag_chain.rebuild_index()
        return RebuildResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rebuild failed: {str(e)}")


@app.get("/api/resume")
async def get_resume():
    """Get resume data from assets/resume.json."""
    resume_path = Path(__file__).parent / "assets" / "resume.json"
    
    if not resume_path.exists():
        raise HTTPException(status_code=404, detail="resume.json not found in assets folder")
    
    try:
        with open(resume_path, "r", encoding="utf-8") as f:
            resume_data = json.load(f)
        return resume_data
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read resume: {str(e)}")


# === Main Entry Point ===

if __name__ == "__main__":
    import uvicorn
    
    print(f"🌐 Server: http://{Config.HOST}:{Config.PORT}")
    print(f"📚 Docs: http://{Config.HOST}:{Config.PORT}/docs")
    
    uvicorn.run(
        "server:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=False,
        workers=2
    )
