from fastapi import FastAPI
from backend.app.rag.query import query_assistant

app = FastAPI(title="Enterprise AI Assistant")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
def chat(payload: dict):
    user_query = payload.get("query")
    return query_assistant(user_query)
