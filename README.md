# Resume RAG API

AI-powered resume Q&A API using **ChromaDB** for vector search and **Claude** for intelligent responses. Includes structured resume data endpoint.

## Features

- 🔍 **Semantic Search** — ChromaDB with built-in embeddings (all-MiniLM-L6-v2)
- 🤖 **AI-Powered Answers** — Claude Haiku for contextual Q&A
- 👥 **Persona Support** — Tailored responses for HR, peers, and founders
- 📄 **Resume JSON API** — Serve structured resume data directly
- ⚡ **Auto-Rebuild** — Vector store auto-initializes on first query

## Quick Start

```bash
# Create virtual environment (Python 3.12 recommended)
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
touch .env
# Edit .env with your ANTHROPIC_API_KEY and RESUME_URL

# Start server
python server.py
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `RESUME_URL` | URL to your resume PDF |
| `CHROMA_PERSIST_DIR` | ChromaDB storage path (default: `./chroma_db`) |
| `HOST` | Server host (default: `0.0.0.0`) |
| `PORT` | Server port (default: `8000`) |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and status |
| `/health` | GET | Health check |
| `/api/query` | POST | Ask a question about the resume |
| `/api/resume` | GET | Get structured resume JSON data |
| `/api/rebuild` | POST | Rebuild vector store from PDF |
| `/docs` | GET | Swagger API documentation |

## Usage Examples

### Ask a Question
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the Flutter experience?", "persona": "peer"}'
```

### Get Resume Data
```bash
curl http://localhost:8000/api/resume
```

### Rebuild Index
```bash
curl -X POST http://localhost:8000/api/rebuild
```

## Personas

| Persona | Description |
|---------|-------------|
| `default` | Balanced, professional responses |
| `hr` | Formal, qualification-focused |
| `peer` | Casual, technical details |
| `founder` | Business impact and outcomes |

## Project Structure

```
resume-rag/
├── assets/
│   └── resume.json      # Structured resume data
├── config.py            # Configuration & prompts
├── document_loader.py   # PDF fetching & chunking
├── vector_store.py      # ChromaDB with built-in embeddings
├── rag_chain.py         # Claude API + auto-rebuild logic
├── server.py            # FastAPI endpoints
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (not committed)
```

## Tech Stack

- **FastAPI** — Modern Python web framework
- **ChromaDB** — Vector database with built-in embeddings
- **Anthropic Claude** — LLM for intelligent Q&A
- **PyPDF** — PDF parsing

## License

MIT
