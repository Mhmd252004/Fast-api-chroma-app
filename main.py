from fastapi import FastAPI
import chromadb
from chromadb.config import Settings
import os

app = FastAPI(title="FastAPI + ChromaDB API")

# في Vercel، المسار الوحيد المتاح للكتابة هو /tmp
PERSIST_DIR = "/tmp/chroma_db"
os.makedirs(PERSIST_DIR, exist_ok=True)

client = chromadb.PersistentClient(path=PERSIST_DIR)
collection = client.get_or_create_collection("my_collection")

@app.get("/")
def root():
    return {"status": "API is running on Vercel"}

@app.post("/add")
def add_text(text: str):
    collection.add(
        documents=[text],
        ids=[str(collection.count() + 1)]
    )
    # ملاحظة: في النسخ الحديثة من Chroma، الحفظ يتم تلقائيًا في PersistentClient
    return {"message": f"Text added to /tmp"}

@app.get("/count")
def count():
    return {"count": collection.count()}