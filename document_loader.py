"""
Document Loader - Handles PDF fetching and text extraction
"""
import os
import tempfile
from typing import List
import requests
from pypdf import PdfReader

from config import Config


class DocumentLoader:
    """Loads and processes PDF documents."""
    
    def __init__(self, url: str = None):
        self.url = url or Config.RESUME_URL
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP
    
    def fetch_pdf(self) -> str:
        """Download PDF from URL and return local path."""
        if not self.url:
            raise ValueError("No resume URL configured")
        
        print(f"📥 Downloading PDF from {self.url}")
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        
        pdf_path = os.path.join(tempfile.gettempdir(), "resume.pdf")
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ PDF saved to {pdf_path}")
        return pdf_path
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract all text from PDF."""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                if last_period > self.chunk_size // 2:
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
        
        return [c for c in chunks if c]  # Remove empty chunks
    
    def load_and_process(self) -> List[str]:
        """Main method: fetch PDF, extract text, chunk it."""
        pdf_path = self.fetch_pdf()
        text = self.extract_text(pdf_path)
        chunks = self.chunk_text(text)
        print(f"📄 Processed {len(chunks)} chunks from resume")
        return chunks
