# Indra Retrieval Assignment — Reference Scaffold

This repo gives you a **clean, OOP-based baseline** to improve MAP@10 and ship a **FastAPI** microservice.

> Works with: `pandas==1.5.3`, `scikit-learn==1.3.2`, `numpy==1.23.*`, `fastapi==0.110.*`, `uvicorn==0.29.*`

## What’s inside

```
indra_retrieval_assignment/
├─ README.md
├─ requirements.txt
├─ retrieval/
│  ├─ __init__.py
│  ├─ text.py               # cleaning, tokenization
│  ├─ vectorizers.py        # TF-IDF (word+char), BM25
│  ├─ retriever.py          # Retriever interface + concrete implementations
│  ├─ pipeline.py           # End-to-end: fit, search, batch-eval
├─ metrics/
│  ├─ __init__.py
│  ├─ ranking.py            # MAP@K + graded MAP@K (partial matches)
├─ service/
│  ├─ __init__.py
│  ├─ app.py                # FastAPI app
│  ├─ schemas.py            # pydantic models
│  ├─ logging_conf.py
├─ evaluation/
│  ├─ __init__.py
│  ├─ run_eval.py           # CLI to evaluate MAP@10 + graded MAP@10
├─ tests/
│  ├─ test_metrics.py
│  ├─ test_vectorizers.py
├─ Dockerfile
├─ run_api.sh
└─ run_eval.sh
```

## Quickstart

1) **Install**:

```bash
pip install -r requirements.txt
```

2) **Expected CSVs** (Wayfair WANDS shaped):
- `products.csv`: `product_id,title,description`
- `queries.csv`: `query,relevant_product_ids` (pipe `|` separated)

3) **Evaluate**:

```bash
python -m evaluation.run_eval --products ./data/products.csv --queries ./data/queries.csv --model tfidf_char_word --k 10
```

4) **Run API**:

```bash
bash run_api.sh
# http://127.0.0.1:8000/docs
```
