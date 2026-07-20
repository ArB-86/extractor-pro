from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
from pathlib import Path

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

INDEX_PATH = Path("datasets/search_index.pkl")
index = []

@app.on_event("startup")
def load_index():
    global index
    if INDEX_PATH.exists():
        with open(INDEX_PATH, "rb") as f:
            index = pickle.load(f)

class SearchResult(BaseModel):
    question_text: str
    chapter: str | None
    question_number: str | None
    source_page: int | None
    answer: str | None

@app.get("/search", response_model=list[SearchResult])
def search(q: str = Query(..., min_length=1)):
    if not index:
        return []
    results = []
    for item in index:
        text = item.get("question_text", "").lower()
        if q.lower() in text:
            results.append(item)
            if len(results) >= 20:
                break
    return results

@app.get("/stats")
def stats():
    return {"total_questions": len(index)}
