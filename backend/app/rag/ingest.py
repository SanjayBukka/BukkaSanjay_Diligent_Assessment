from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from backend.app.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_HOST
)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME, host=PINECONE_HOST)

model = SentenceTransformer("all-MiniLM-L6-v2")

def ingest_text(text: str, doc_id: str):
    embedding = model.encode(text).tolist()
    index.upsert([
        {
            "id": doc_id,
            "values": embedding,
            "metadata": {"text": text}
        }
    ])
