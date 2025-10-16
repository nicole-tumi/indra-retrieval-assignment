from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np
from .vectorizers import HybridTfidf, BM25

@dataclass
class Product:
    product_id: str
    title: str
    description: str

class Retriever:
    def fit(self, products: List[Product]): ...
    def search(self, queries: List[str], k: int=10) -> np.ndarray: ...
    @property
    def ids(self) -> List[str]: ...

class TfidfRetriever(Retriever):
    def __init__(self):
        self.hybrid = HybridTfidf()
        self._ids: List[str] = []
        self._titles: List[str] = []
        self._descs: List[str] = []

    def fit(self, products: List[Product]):
        self._ids    = [p.product_id for p in products]
        self._titles = [p.title for p in products]
        self._descs  = [p.description for p in products]
        self.hybrid.fit(self._titles, self._descs)
        return self

    def search(self, queries: List[str], k: int=10) -> np.ndarray:
        return self.hybrid.cosine_search(queries, k=k)

    @property
    def ids(self) -> List[str]:
        return self._ids

class BM25Retriever(Retriever):
    def __init__(self):
        self.bm25 = BM25()
        self._ids: List[str] = []
        self._titles: List[str] = []
        self._descs: List[str] = []

    def fit(self, products: List[Product]):
        self._ids    = [p.product_id for p in products]
        self._titles = [p.title for p in products]
        self._descs  = [p.description for p in products]
        self.bm25.fit(self._titles, self._descs)
        return self

    def search(self, queries: List[str], k: int=10) -> np.ndarray:
        return self.bm25.search(queries, k=k)

    @property
    def ids(self) -> List[str]:
        return self._ids
