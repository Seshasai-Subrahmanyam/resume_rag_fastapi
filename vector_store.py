"""
Vector Store - ChromaDB with built-in embeddings
"""
import os
import shutil
from typing import List, Optional
import chromadb
from chromadb.config import Settings

from config import Config


class VectorStore:
    """Manages ChromaDB vector store with built-in embeddings."""
    
    def __init__(self):
        self.persist_dir = Config.CHROMA_PERSIST_DIR
        self.collection_name = Config.COLLECTION_NAME
        self._client: Optional[chromadb.ClientAPI] = None
        self._collection = None
    
    @property
    def client(self) -> chromadb.ClientAPI:
        """Lazy-load ChromaDB client."""
        if self._client is None:
            os.makedirs(self.persist_dir, exist_ok=True)
            self._client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )
        return self._client
    
    @property
    def collection(self):
        """Get or create the collection."""
        if self._collection is None:
            # Uses ChromaDB's default embedding function (all-MiniLM-L6-v2)
            self._collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Resume document chunks"}
            )
        return self._collection
    
    def add_documents(self, chunks: List[str]) -> int:
        """Add document chunks to the vector store."""
        if not chunks:
            return 0
        
        # Generate IDs for each chunk
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Clear existing data first
        self.clear()
        
        # Add new documents (ChromaDB handles embedding automatically)
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=[{"index": i} for i in range(len(chunks))]
        )
        
        print(f"✅ Added {len(chunks)} chunks to vector store")
        return len(chunks)
    
    def search(self, query: str, n_results: int = 2) -> List[str]:
        """Search for relevant document chunks."""
        if self.collection.count() == 0:
            return []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count())
        )
        
        return results.get("documents", [[]])[0]
    
    def clear(self) -> None:
        """Clear the collection."""
        try:
            self.client.delete_collection(self.collection_name)
            self._collection = None
        except Exception:
            pass  # Collection might not exist
    
    def delete(self) -> None:
        """Delete the entire vector store."""
        if os.path.exists(self.persist_dir):
            shutil.rmtree(self.persist_dir)
            self._client = None
            self._collection = None
            print("🗑️ Vector store deleted")
    
    @property
    def count(self) -> int:
        """Get number of documents in store."""
        try:
            return self.collection.count()
        except Exception:
            return 0
    
    @property
    def is_initialized(self) -> bool:
        """Check if vector store has documents."""
        return self.count > 0
