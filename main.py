from fastapi import FastAPI
import chromadb
from chromadb.config import Settings
import os

app = FastAPI(title="FastAPI + ChromaDB API")

# This will be "chroma_db" locally
# and "/app/chroma_db" on Railway
PERSIST_DIR = os.getenv("CHROMA_DIR", "chroma_db")

# THIS LINE CREATES THE FOLDER IF IT DOESN'T EXIST
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
