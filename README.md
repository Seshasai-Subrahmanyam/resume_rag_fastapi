# Resume RAG

AI-powered Q&A for Seshasai Nagadevara's resume using ChromaDB and Claude.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY and RESUME_URL

# Start server
python server.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/api/query` | POST | Ask a question |
| `/api/rebuild` | POST | Rebuild index from PDF |
| `/docs` | GET | Swagger documentation |

## Usage

```bash
# Rebuild index (first time)
curl -X POST http://localhost:8000/api/rebuild

# Ask a question
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the Flutter experience?", "persona": "peer"}'
```

## Personas

- **default** - Balanced, professional
- **hr** - Formal, qualification-focused
- **peer** - Casual, technical
- **founder** - Business impact focused

## Architecture

```
config.py          → Configuration & prompts
document_loader.py → PDF fetching & chunking
vector_store.py    → ChromaDB with built-in embeddings
rag_chain.py       → Claude API integration
server.py          → FastAPI endpoints
```
