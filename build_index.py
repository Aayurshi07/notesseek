import os, time, sqlite3
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from ingest import read_pdf, chunk_text

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

db = sqlite3.connect("notesseek.db")
db.execute("""CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    text TEXT,
    embedding BLOB
)""")

def embed_batch(texts):
    while True:
        try:
            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=texts,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                    output_dimensionality=768,
                ),
            )
            return [np.array(e.values, dtype=np.float32) for e in result.embeddings]
        except Exception as e:
            if "429" in str(e):
                print("Rate limit hit, waiting 60 seconds...")
                time.sleep(60)
            else:
                raise

for filename in os.listdir("pdfs"):
    if not filename.endswith(".pdf"):
        continue
    done = db.execute("SELECT COUNT(*) FROM chunks WHERE source=?", (filename,)).fetchone()[0]
    if done:
        print("Skipping", filename)
        continue
    chunks = chunk_text(read_pdf(os.path.join("pdfs", filename)))
    for i in range(0, len(chunks), 20):
        batch = chunks[i:i + 20]
        vectors = embed_batch(batch)
        for text, vec in zip(batch, vectors):
            db.execute("INSERT INTO chunks (source, text, embedding) VALUES (?, ?, ?)",
                       (filename, text, vec.tobytes()))
        db.commit()
        time.sleep(2)
    print("Indexed", filename, len(chunks), "chunks")

print("Done. Total rows:", db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0])