import argparse
import pandas as pd
from retrieval.pipeline import RetrievalPipeline
from metrics.ranking import map_at_k, graded_map_at_k

def parse_gold(s: str):
    if pd.isna(s): return []
    return [x.strip() for x in str(s).split("|") if x.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--products", required=True)
    ap.add_argument("--queries", required=True)
    ap.add_argument("--model", default="tfidf_char_word", choices=["tfidf_char_word","bm25","tfidf"])
    ap.add_argument("--k", type=int, default=10)
    args = ap.parse_args()

    products = pd.read_csv(args.products)
    queries = pd.read_csv(args.queries)

    pipe = RetrievalPipeline(model=args.model).fit(products)

    q_list = queries["query"].astype(str).tolist()
    preds = pipe.search(q_list, k=args.k)

    gold = [parse_gold(s) for s in queries["relevant_product_ids"].tolist()]

    base_map = map_at_k(preds, gold, k=args.k)

    # id2text for graded eval (use title+desc)
    id2text = {str(r["product_id"]): f"{r.get('title','')} {r.get('description','')}" for _,r in products.iterrows()}
    gmap = graded_map_at_k(preds, gold, queries=q_list, id2text=id2text, k=args.k)

    print(f"MAP@{args.k}: {base_map:.4f}")
    print(f"Graded MAP@{args.k} (partial-match aware): {gmap:.4f}")

if __name__ == "__main__":
    main()
