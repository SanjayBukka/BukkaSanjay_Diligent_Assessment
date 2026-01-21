import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(name, default=None):
    value = os.getenv(name, default)
    if value and isinstance(value, str):
        return value.strip("'").strip('"')
    return value

PINECONE_API_KEY = get_env_var("PINECONE_API_KEY")
PINECONE_INDEX_NAME = get_env_var("PINECONE_INDEX_NAME")
PINECONE_HOST = get_env_var("PINECONE_HOST")
