import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI
from google import genai
from search import search

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="NotesSeek")

@app.get("/")
def home():
    return {"message": "NotesSeek is running"}

@app.get("/search")
def search_endpoint(q: str, k: int = 3):
    return {"query": q, "results": search(q, k)}

@app.get("/ask")
def ask_endpoint(q: str, k: int = 3):
    results = search(q, k)
    context = "\n\n".join(f"[{r['source']}]\n{r['text']}" for r in results)
    prompt = (
        "Answer the question using ONLY the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {q}"
    )
    response = None
    for attempt in range(5):
        try:
            response = client.models.generate_content(
               model="gemini-3.5-flash-lite",
                contents=prompt,
            )
            break
        except Exception as e:
            if "503" in str(e) or "429" in str(e):
                time.sleep(5)
            else:
                raise
    if response is None:
        return {"error": "Gemini is busy right now, please try again in a minute."}
    return {
        "question": q,
        "answer": response.text,
        "sources": sorted({r["source"] for r in results}),
    }