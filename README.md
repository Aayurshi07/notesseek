# NotesSeek

A small search and Q&A tool for academic PDFs. You ask a question, it finds the most relevant parts of the papers, and Gemini answers using only those parts.

Live API: https://notesseek.onrender.com (free plan, so the first request after a break can take about a minute)
Docs page: https://notesseek.onrender.com/docs

I built it to understand how RAG works end to end, so I kept each part simple.

## How it works

1. Each PDF is read with pypdf and cut into chunks of 800 characters (100 overlap).
2. Every chunk is embedded with Gemini (gemini-embedding-001, 768 dimensions) and stored in SQLite.
3. A question is embedded the same way, and the 3 closest chunks are found by cosine similarity.
4. Those chunks go to Gemini, which answers using only that text.

## Endpoints

- `GET /search?q=...` returns the top matching chunks with scores
- `GET /ask?q=...` returns an answer and the source PDFs

## Evaluation

I wrote two test sets and measure Recall@3 (is the right result in the top 3?).

- Easy set, 15 questions: pass if the right paper is in the top 3. Score: 15/15.
- Hard set, 15 questions: pass only if a top-3 chunk contains the exact phrase that answers the question, like "152 layers" or "0.999". Score: 13/15.

The two misses on the hard set are "What is the deepest ResNet tested on ImageNet?" and "What does the alignment model avoid compressing a sentence into?". The answers are in the PDFs, but the search doesn't rank those chunks in the top 3.

Chunk size 800 and 1200 both scored 13/15 on the hard set. One of my test phrases first failed only because the PDF writes "fixed-length" with a joined "fi" letter, so I fixed the test and not the search.

## Run it locally

    pip install -r requirements.txt

Put your Gemini key in a `.env` file:

    GEMINI_API_KEY=your_key

Add PDFs to a `pdfs` folder, then:

    python build_index.py
    uvicorn main:app --reload

## Deployment

Docker image built from the Dockerfile and deployed on Render's free plan. The key is set as an environment variable on Render, not in the repo. The SQLite database is included in the repo (it only holds text from public arXiv papers).

## Stack

Python, FastAPI, Gemini API, SQLite, NumPy, Docker, Render