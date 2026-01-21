import pinecone
from sentence_transformers import SentenceTransformer
from backend.app.config import PINECONE_API_KEY, PINECONE_INDEX_NAME

pinecone.init(api_key=PINECONE_API_KEY)
index = pinecone.Index(PINECONE_INDEX_NAME)

model = SentenceTransformer("all-MiniLM-L6-v2")

def ingest_text(text: str, doc_id: str):
    embedding = model.encode(text).tolist()
    index.upsert([
        (doc_id, embedding, {"text": text})
    ])
