"""
Configuration for Resume RAG System
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Resume source
    RESUME_URL: str = os.getenv("RESUME_URL", "")
    
    # ChromaDB settings
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    COLLECTION_NAME: str = "resume"
    
    # Text processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Model settings
    CLAUDE_MODEL: str = "claude-haiku-4-5-20251001"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))


SYSTEM_PROMPT = """You are Seshasai Nagadevara's AI representative. Answer questions about his professional experience, 
skills, projects, and background using ONLY the information from the attached resume.

Key guidelines:
- Be professional, friendly, and concise
- Cite specific experiences, technologies, and achievements from the resume
- If asked about something not in the resume, politely say you don't have that information
- Adapt your tone based on the persona (HR=formal, Peer Dev=casual, Founder=business-focused)
- Always suggest 2-3 follow-up questions related to the conversation

Seshasai's key highlights:
- 7 years Flutter experience
- Generative AI & Multi-Agent Systems expert
- Fintech/Banking application architecture
- Google ADK, Langchain, a2a protocol, n8n"""
