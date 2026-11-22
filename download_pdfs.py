import os, time, requests

os.makedirs("pdfs", exist_ok=True)

papers = {
    "attention_is_all_you_need": "1706.03762",
    "bert": "1810.04805",
    "rag": "2005.11401",
    "resnet": "1512.03385",
    "adam": "1412.6980",
    "gpt3": "2005.14165",
    "word2vec": "1301.3781",
    "batchnorm": "1502.03167",
    "gans": "1406.2661",
    "bahdanau_attention": "1409.0473",
}

for name, arxiv_id in papers.items():
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    r = requests.get(url, timeout=60, allow_redirects=True)
    with open(f"pdfs/{name}.pdf", "wb") as f:
        f.write(r.content)
    print("Downloaded", name)
    time.sleep(3)