import time
from search import search
from eval_set import EVAL_SET

hits = 0
for question, expected in EVAL_SET:
    results = search(question, k=3)
    found = expected in [r["source"] for r in results]
    hits += found
    print("PASS" if found else "FAIL", "|", question)
    time.sleep(1)

print(f"\nRecall@3: {hits}/{len(EVAL_SET)} = {hits / len(EVAL_SET):.2f}")