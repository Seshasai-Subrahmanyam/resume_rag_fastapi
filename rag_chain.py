"""
RAG Chain - Anthropic Claude integration for Q&A
"""
from typing import Dict, Any, Optional
from anthropic import Anthropic

from config import Config, SYSTEM_PROMPT
from vector_store import VectorStore


class RAGChain:
    """RAG chain using Claude for question answering."""
    
    # Persona modifiers for different user types
    PERSONA_MODIFIERS = {
        "hr": "\n\nNote: Respond formally, focusing on qualifications, certifications, and professional achievements.",
        "peer": "\n\nNote: Be casual and technical, mention specific technologies and implementation details.",
        "founder": "\n\nNote: Focus on business impact, leadership, and project outcomes.",
        "default": ""
    }
    
    def __init__(self):
        self.vector_store = VectorStore()
        self._client: Optional[Anthropic] = None
    
    @property
    def client(self) -> Anthropic:
        """Lazy-load Anthropic client."""
        if self._client is None:
            if not Config.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            self._client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        return self._client
    
    def query(self, question: str, persona: str = "default") -> Dict[str, Any]:
        """
        Query the RAG system.
        
        Args:
            question: User's question
            persona: 'hr', 'peer', 'founder', or 'default'
            
        Returns:
            Dict with answer and metadata
        """
        # Auto-rebuild if vector store is empty
        if not self.vector_store.is_initialized:
            print("⚠️ Vector store empty, auto-rebuilding...")
            self.rebuild_index()
        
        # Get relevant context from vector store
        context_chunks = self.vector_store.search(question, n_results=4)
        
        # If still no chunks after rebuild attempt, return error
        if not context_chunks:
            return {
                "answer": "I couldn't find any resume information. Please check your RESUME_URL configuration.",
                "persona": persona,
                "sources_count": 0
            }
        
        # Build context string
        context = "\n\n---\n\n".join(context_chunks)
        
        # Adjust system prompt for persona
        persona_modifier = self.PERSONA_MODIFIERS.get(persona, "")
        system = SYSTEM_PROMPT + persona_modifier
        
        # Build user message with context
        user_message = f"""Based on the following resume information:

{context}

Question: {question}

Please provide a helpful answer based only on the information above. If the information isn't in the resume, say so politely."""
        
        # Call Claude API
        response = self.client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user_message}]
        )
        
        answer = response.content[0].text
        
        return {
            "answer": answer,
            "persona": persona,
            "sources_count": len(context_chunks)
        }
    
    def rebuild_index(self) -> Dict[str, Any]:
        """Rebuild the vector store from resume URL."""
        from document_loader import DocumentLoader
        
        loader = DocumentLoader()
        chunks = loader.load_and_process()
        count = self.vector_store.add_documents(chunks)
        
        return {
            "status": "success",
            "documents_indexed": count
        }
    
    @property
    def is_ready(self) -> bool:
        """Check if RAG system is ready for queries."""
        return self.vector_store.is_initialized


# Global instance
rag_chain = RAGChain()
