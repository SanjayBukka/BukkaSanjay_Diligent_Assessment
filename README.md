# Enterprise AI Assistant

## 1. Overview
The Enterprise AI Assistant is a specialized tool designed to provide factual answers based on internal company documentation. It leverages a Retrieval-Augmented Generation (RAG) pipeline to ensure responses are grounded in specific enterprise knowledge rather than general training data.

## 2. Problem
Enterprises often struggle with information discovery across vast internal knowledge bases. General-purpose LLMs are prone to hallucinations and lack access to private, up-to-date company data, making them unreliable for internal support.

## 3. Solution
This project implements a RAG-based approach. It indexes enterprise documents into a vector database and retrieves the most relevant context for every user query. This context is then provided to a local LLM to generate a precise, grounded response.

## 4. Architecture
*   **UI**: Streamlit-based chat interface for user interaction.
*   **Backend**: FastAPI server handling query processing and orchestration.
*   **Vector DB**: Pinecone for high-performance semantic search and document retrieval.
*   **LLM**: Llama 3.2 (running via Ollama) for local, secure text generation.

## 5. Key Features
*   **Grounded Answers**: Responses are strictly limited to the provided context.
*   **Context Refusal**: The system explicitly states when information is missing from the knowledge base.
*   **Semantic Retrieval**: Uses vector embeddings to find relevant information even without exact keyword matches.

## 6. Tech Stack
*   **Backend**: Python, FastAPI, Uvicorn
*   **LLM**: Ollama (Llama 3.2)
*   **Vector DB**: Pinecone
*   **Frontend**: Streamlit
*   **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)

## 7. How Hallucination Is Prevented
Hallucination is prevented through strict system prompting and context enforcement. The LLM is instructed to ignore its pre-trained knowledge and only use the retrieved snippets. If the retrieved context is insufficient, the model is programmed to return a standard "information not found" response.

## 8. Setup
1.  **Environment**: Create and activate a virtual environment.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
2.  **Dependencies**: Install required packages.
    ```bash
    pip install -r backend/requirements.txt
    ```
3.  **Environment Variables**: Configure `.env` based on `.env.example`.
    *   `PINECONE_API_KEY`
    *   `PINECONE_INDEX_NAME`
    *   `PINECONE_HOST`
4.  **Run Backend**:
    ```bash
    python -m uvicorn backend.app.main:app --port 8000
    ```
5.  **Run Frontend**:
    ```bash
    streamlit run frontend/app.py
    ```

## 9. Example
*   **Question**: "What are Diligent's key product areas?"
*   **Expected Behavior**: The assistant retrieves the "company.txt" context and lists: board management, risk management, audit, compliance tracking, and ESG reporting.

## 10. Limitations
*   **Single Chunk Retrieval**: Currently retrieves only the top-1 most relevant document chunk.
*   **Local LLM Dependency**: Performance and latency are dependent on the host machine's hardware for running Ollama.
*   **Static Ingestion**: Document ingestion is currently a manual process rather than an automated sync.
