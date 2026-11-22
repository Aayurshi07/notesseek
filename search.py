import os, sqlite3
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

db = sqlite3.connect("notesseek.db")
rows = db.execute("SELECT source, text, embedding FROM chunks").fetchall()
sources = [r[0] for r in rows]
texts = [r[1] for r in rows]
matrix = np.vstack([np.frombuffer(r[2], dtype=np.float32) for r in rows])
matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)

def embed_query(q):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=q,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768,
        ),
    )
    v = np.array(result.embeddings[0].values, dtype=np.float32)
    return v / np.linalg.norm(v)

def search(query, k=3):
    scores = matrix @ embed_query(query)
    top = np.argsort(scores)[::-1][:k]
    return [{"source": sources[i], "text": texts[i], "score": float(scores[i])} for i in top]

if __name__ == "__main__":
    q = input("Ask a question: ")
    for r in search(q):
        print(f"\n[{r['source']}] score={r['score']:.3f}")
        print(r["text"][:300])