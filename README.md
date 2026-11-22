\# NotesSeek



A small search and Q\&A tool for academic PDFs. You ask a question, it finds the most relevant parts of the papers and gives an answer based only on those.



I built it to understand how RAG works end to end, so I kept each part simple.



\## How it works



1\. Each PDF is read with pypdf and cut into chunks of 800 characters (100 overlap).

2\. Every chunk is turned into an embedding using Gemini and stored in SQLite.

3\. A question is embedded the same way, and the 3 closest chunks are found by cosine similarity.

4\. Those chunks are passed to Gemini, which answers using only that text.



\## Endpoints



\- `GET /search?q=...` returns the top matching chunks

\- `GET /ask?q=...` returns an answer and the source PDFs



\## Run it locally



&#x20;   pip install fastapi uvicorn google-genai pypdf numpy python-dotenv



Put your Gemini key in a `.env` file:



&#x20;   GEMINI\_API\_KEY=your\_key



Add PDFs to a `pdfs` folder, then:



&#x20;   python build\_index.py

&#x20;   uvicorn main:app --reload



\## Evaluation



I wrote 15 questions with the PDF each answer should come from and check if that PDF shows up in the top 3 (Recall@3). Run it with `python evaluate.py`.



\## Stack



Python, FastAPI, Gemini API, SQLite, NumPy

