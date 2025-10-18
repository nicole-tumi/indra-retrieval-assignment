# Indra Retrieval Assignment — Product Search Prototype

Hi! I wanted to build a **working end-to-end baseline** for product retrieval, focusing more on **clarity and execution** than on over-engineering.

I tried to keep things simple:

-   Make sure the **pipeline runs reliably**.
-   Document everything clearly so **someone else (or future me)** can continue improving it.

This project implements a simple e-commerce product search engine based on the **WANDS dataset (Wayfair)**.  
The goal was **not** to achieve a state-of-the-art model, but to:

-   Improve the baseline **MAP@10 score (>0.30)** through a reasonable modeling decision.
-   Add support for **partial relevance scoring** via a **Graded MAP@10** metric.
-   **Refactor** the original notebook code into an **extensible OOP structure**.
-   Expose the retrieval pipeline as a **production-ready FastAPI microservice** (with error handling, logging hooks, and modular retrievers).

## Overview

-   **Baseline model provided:** TF-IDF (word-only) with MAP@10 ≈ **0.29**
-   **Improved models implemented:**
    -   TF-IDF (word-only baseline reproduction)
    -   TF-IDF hybrid (word + char n-grams → improves partial match robustness)
    -   BM25 baseline (comparison)
-   **Evaluation metrics:**
    -   `MAP@10`: strict relevance
    -   `Graded MAP@10`: **gives partial credit** when a product is not an exact match but is still close (e.g., "blue velvet chair" vs "navy velvet seat")

## Final Results (WANDS Dataset - Local Run)

| Model              | MAP@10 | Graded MAP@10 |
| ------------------ | :----: | :-----------: |
| TF-IDF (word-only) | 0.4434 |    0.5028     |
| TF-IDF char+word   | 0.4434 |    0.5028     |
| BM25               | 0.4261 |    0.4682     |

✅ **Target >0.30 achieved**  
✅ **Graded MAP@10 > strict MAP@10**, which shows that **partial matches were actually being recognized**

## Why I Added Graded MAP?

At first, the baseline judged relevance as **binary** (right or wrong).  
But in e-commerce, users **don’t always type exact product names**, and **near matches still matter**.

Example idea I followed:

> If the user searches for _“brown leather chair”_, ranking _“dark leather armchair”_ slightly lower is fine — but completely discarding it felt too harsh.

So I introduced **Graded MAP@10**, which:

-   rewards **close lexical overlap** using n-grams,
-   keeps the implementation simple enough for a baseline,
-   gives a metric that **feels more “fair”** than strict MAP.

## Repository Structure (Kept Clean for Learning & Extension)

```
indra-retrieval-assignment/
│
├── retrieval/ # Core OOP search pipeline
│ ├── pipeline.py # High-level retrieval pipeline wrapper
│ ├── retriever.py # Abstraction over different retrieval backends
│ ├── vectorizers.py # TF-IDF, BM25, hybrid encoders
│ └── text.py # Normalization, tokenization, n-gram utils
│
├── metrics/ # MAP@k and Graded MAP@k
│
├── service/ # FastAPI microservice layer
│
├── evaluation/ # CLI eval script (run_eval.py)
│
└── data/ # products_clean.csv and queries_clean.csv
```

## Running the Microservice (FastAPI)

I exposed the pipeline via a **small FastAPI app** so it could act like a microservice:

```
uvicorn service.app:app --reload --port 8000
```

### Sample Request:

```
curl -X POST "http://127.0.0.1:8000/search" -H "Content-Type: application/json" -d '{"queries": ["blue chair"], "k": 3}'
```

### Sample Response:

```
{
    "results": [
        [
            "1234",
            "991",
            "812"
        ]
    ]
}
```

## Evaluation via CLI

```
python -m evaluation.run_eval --products ./data/products_clean.csv --queries ./data/queries_clean.csv --model tfidf_char_word --k 10
```

## What I Would Explore Next (If I Had More Time)

| Idea                                     | Reason                                         |
| ---------------------------------------- | ---------------------------------------------- |
| ✅ Weight title more than description    | Quick improvement without heavy refactor       |
| ✅ Keep char n-grams                     | Helps with typos and short queries             |
| 🚧 Fuse BM25 + TF-IDF                    | Could increase both recall and ranking quality |
| 🚧 Add a light reranker using embeddings | Only on top-k, to keep things efficient        |
| 🚧 Use click logs or user signals        | A better long-term ranking objective           |

## Deliverables

-   ✔ MAP@10 improved above the required **0.30**
-   ✔ Added a Graded MAP metric to fairly evaluate partial matches
-   ✔ Code refactored into modular OOP components to allow future extensions
-   ✔ Working FastAPI microservice responding to search queries
-   ✔ Left the structure ready for future improvements

> 💡 A Spanish version (`README_ES.md`) is included for accessibility.
