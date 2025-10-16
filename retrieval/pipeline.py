from dataclasses import dataclass
from typing import List, Dict, Optional, Iterable, Tuple
import pandas as pd
import numpy as np
from .retriever import TfidfRetriever, BM25Retriever, Product, Retriever

@dataclass
class RetrievalPipeline:
    model: str = "tfidf"  # "tfidf" or "bm25"
    retriever: Optional[Retriever] = None

    def _make_retriever(self) -> Retriever:
        if self.model == "tfidf" or self.model == "tfidf_char_word":
            return TfidfRetriever()
        elif self.model == "bm25":
            return BM25Retriever()
        else:
            raise ValueError(f"Unknown model: {self.model}")

    def fit(self, products_df: pd.DataFrame):
        products = [Product(str(r["product_id"]), r.get("title",""), r.get("description",""))
                    for _, r in products_df.iterrows()]
        self.retriever = self._make_retriever()
        self.retriever.fit(products)
        return self

    def search(self, queries: List[str], k: int=10) -> List[List[str]]:
        idx = self.retriever.search(queries, k=k)
        ids = np.array(self.retriever.ids)
        return [ids[row].tolist() for row in idx]
