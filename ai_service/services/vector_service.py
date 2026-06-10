import hashlib
import numpy as np
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from ai_service.config import settings

class VectorService:
    def __init__(self):
        self.host = settings.QDRANT_HOST
        self.port = settings.QDRANT_PORT
        self.collection_name = settings.QDRANT_COLLECTION
        
        # Initialize client
        try:
            self.client = QdrantClient(host=self.host, port=self.port)
            self._ensure_collection()
        except Exception as e:
            print(f"Error connecting to Qdrant at {self.host}:{self.port} - {e}. Vector search will run in mock mode.")
            self.client = None
            
        # Try initializing sentence-transformers locally
        self.encoder = None
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            print("Loaded SentenceTransformer locally.")
        except Exception as e:
            print(f"SentenceTransformer not loaded: {e}. Falling back to mock embeddings (size 384).")

    def _ensure_collection(self):
        if not self.client:
            return
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=384,  # matches all-MiniLM-L6-v2
                        distance=models.Distance.COSINE
                    )
                )
                print(f"Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            print(f"Error checking/creating Qdrant collection: {e}")

    def generate_embeddings(self, text: str) -> List[float]:
        # If local sentence-transformers encoder is available, use it
        if self.encoder:
            try:
                embedding = self.encoder.encode(text)
                return embedding.tolist()
            except Exception as e:
                print(f"SentenceTransformer encoding failed: {e}")
                
        # Mock embeddings (size 384) using a stable random generator seeded with the text hash
        sha = hashlib.sha256(text.encode('utf-8')).digest()
        np.random.seed(int.from_bytes(sha[:4], byteorder='big'))
        vec = np.random.randn(384)
        vec /= np.linalg.norm(vec)  # normalize
        return vec.tolist()

    def upsert_article(self, article_id: str, text: str, metadata: Dict[str, Any]):
        if not self.client:
            print("Qdrant not connected. Skipping upsert.")
            return False
            
        try:
            vector = self.generate_embeddings(text)
            
            # Simple integer ID generation or hash for Qdrant compatibility
            # Qdrant accepts UUID string or integer IDs. Let's make sure it's a valid ID format.
            # We can convert a UUID string or generic string to a UUID format or numeric
            qdrant_id = None
            try:
                import uuid
                # Check if already a valid UUID
                uuid.UUID(article_id)
                qdrant_id = article_id
            except ValueError:
                # Generate stable UUID from string
                qdrant_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, article_id))

            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=qdrant_id,
                        vector=vector,
                        payload={
                            "article_id": article_id,
                            "text": text,
                            **metadata
                        }
                    )
                ]
            )
            return True
        except Exception as e:
            print(f"Qdrant upsert failed: {e}")
            return False

    def search_similar_articles(self, text: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not self.client:
            print("Qdrant not connected. Returning empty list.")
            return []
            
        try:
            vector = self.generate_embeddings(text)
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=limit
            )
            
            return [
                {
                    "id": r.id,
                    "score": r.score,
                    "payload": r.payload
                } for r in results
            ]
        except Exception as e:
            print(f"Qdrant search failed: {e}")
            return []
