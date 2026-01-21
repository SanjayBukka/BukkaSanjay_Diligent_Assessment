import os
import requests
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

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = "llama3.2:latest"

def query_assistant(user_query: str) -> dict:
    query_embedding = model.encode(user_query).tolist()

    result = index.query(
        vector=query_embedding,
        top_k=1,
        include_metadata=True
    )

    context = ""
    if result.matches:
        context = result.matches[0].metadata["text"]

    prompt = f"""
You are an enterprise AI assistant designed for internal knowledge support.

CRITICAL RULES (NON-NEGOTIABLE):
1. You MUST answer ONLY using the retrieved context provided to you.
2. You are NOT allowed to use your pretrained knowledge, assumptions, or general world knowledge.
3. If the retrieved context is empty, insufficient, or unrelated, you MUST respond with:
   "I don't have that information in my knowledge base."
4. You must NEVER guess, infer, or fabricate facts.
5. If the user question is outside the scope of the retrieved context, refuse politely using rule #3.

ROLE:
- You represent an enterprise SaaS assistant.

- Accuracy is more important than helpfulness.
- A wrong answer is worse than no answer.

Retrieved Context:
{context}

User Question:
{user_query}

OUTPUT REQUIREMENTS:
- Base your answer strictly on the retrieved context.
- Keep the response concise and factual.
- Do not add extra explanations unless present in the context.
- Do not mention the words "context", "vector database", or "Pinecone" in your response.
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
