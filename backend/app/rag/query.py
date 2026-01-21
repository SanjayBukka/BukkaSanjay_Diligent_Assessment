import pinecone
import requests
from sentence_transformers import SentenceTransformer
from backend.app.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME
)
import os

pinecone.init(api_key=PINECONE_API_KEY)
index = pinecone.Index(PINECONE_INDEX_NAME)

model = SentenceTransformer("all-MiniLM-L6-v2")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = "llama3.1:8b-instruct"

def query_assistant(user_query: str) -> dict:
    query_embedding = model.encode(user_query).tolist()

    result = index.query(
        vector=query_embedding,
        top_k=1,
        include_metadata=True
    )

    context = ""
    if result["matches"]:
        context = result["matches"][0]["metadata"]["text"]

    prompt = f"""
You are an enterprise AI assistant.
Answer the question using ONLY the context below.

Context:
{context}

Question:
{user_query}
"""

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    answer = response.json().get("response", "")

    return {
        "answer": answer.strip(),
        "source": context
    }
