import os
from pypdf import PdfReader

CHUNK_SIZE = 800
OVERLAP = 100

def read_pdf(path):
    reader = PdfReader(path)
    return " ".join((page.extract_text() or "") for page in reader.pages)

def chunk_text(text, size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

if __name__ == "__main__":
    total = 0
    for filename in os.listdir("pdfs"):
        if filename.endswith(".pdf"):
            text = read_pdf(os.path.join("pdfs", filename))
            chunks = chunk_text(text)
            total += len(chunks)
            print(filename, "->", len(chunks), "chunks")
    print("Total chunks:", total)