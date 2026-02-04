from fastapi import FastAPI
import chromadb
from chromadb.config import Settings
import os

app = FastAPI(title="FastAPI + ChromaDB API")

# Render persistent disk path
PERSIST_DIR = os.getenv("CHROMA_DIR", "/opt/render/project/chroma_db")
os.makedirs(PERSIST_DIR, exist_ok=True)

client = chromadb.Client(
    Settings(
        persist_directory=PERSIST_DIR,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection("my_collection")

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/add")
def add_text(text: str):
    collection.add(
        documents=[text],
        ids=[str(collection.count() + 1)]
    )
    client.persist()
    return {"message": "Text added"}

@app.get("/count")
def count():
    return {"count": collection.count()}
