from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from .text import normalize_text

@dataclass
class Corpus:
    ids: List[str]
    texts: List[str]

class HybridTfidf:
    """
    Word-level + char-level TF-IDF with optional field weighting.
    """
    def __init__(self,
                 word_ngram_range: Tuple[int,int]=(1,2),
                 char_ngram_range: Tuple[int,int]=(3,5),
                 title_weight: float=2.0,
                 desc_weight: float=1.0,
                 max_features_word: Optional[int]=50000,
                 max_features_char: Optional[int]=80000):
        self.word_vec = TfidfVectorizer(
            analyzer="word",
            ngram_range=word_ngram_range,
            max_features=max_features_word,
            preprocessor=normalize_text
        )
        self.char_vec = TfidfVectorizer(
            analyzer="char",
            ngram_range=char_ngram_range,
            max_features=max_features_char,
            preprocessor=normalize_text
        )
        self.title_weight = title_weight
        self.desc_weight = desc_weight
        self._doc_matrix = None
        self._query_word = None
        self._query_char = None

    def _compose_text(self, title: str, description: str) -> str:
        # simple field weighting by repeating title tokens
        title = normalize_text(title or "")
        desc  = normalize_text(description or "")
        title_boost = (" " + title) * int(max(1, self.title_weight))
        desc_boost  = (" " + desc)  * int(max(1, self.desc_weight))
        return (title_boost + " " + desc_boost).strip()

    def fit(self, titles: List[str], descriptions: List[str]):
        docs = [self._compose_text(t or "", d or "") for t, d in zip(titles, descriptions)]
        self._doc_word = self.word_vec.fit_transform(docs)   # sparse
        self._doc_char = self.char_vec.fit_transform(docs)
        # cache
        self._doc_matrix = (self._doc_word, self._doc_char)
        return self

    def transform_queries(self, queries: List[str]):
        qnorm = [normalize_text(q) for q in queries]
        self._query_word = self.word_vec.transform(qnorm)
        self._query_char = self.char_vec.transform(qnorm)
        return (self._query_word, self._query_char)

    def cosine_search(self, queries: List[str], k: int=10) -> np.ndarray:
        qw, qc = self.transform_queries(queries)
        dw, dc = self._doc_matrix
        sims = (qw @ dw.T).toarray() + (qc @ dc.T).toarray()  # simple sum fusion
        topk = np.argpartition(-sims, kth=min(k, sims.shape[1]-1), axis=1)[:, :k]
        # sort each row’s top-k
        rows = np.arange(sims.shape[0])[:, None]
        sorted_idx = np.argsort(-sims[rows, topk])
        return topk[rows, sorted_idx]

class BM25:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.df = {}
        self.idf = {}
        self.doc_lens = []
        self.avgdl = 0.0
        self.docs_tokens = []

    def _tokenize(self, s: str):
        from .text import normalize_text
        return normalize_text(s).split()

    def fit(self, titles, descriptions):
        import numpy as np
        def _safe(x):
            try:
                return "" if x is None or x != x else str(x)
            except Exception:
                return ""
        docs = [f"{_safe(t)} {_safe(d)}" for t, d in zip(titles, descriptions)]
        N = len(docs)
        self.docs_tokens = [self._tokenize(x) for x in docs]
        self.doc_lens = [len(toks) for toks in self.docs_tokens]
        self.avgdl = float(np.mean(self.doc_lens)) if self.doc_lens else 0.0

        # df
        self.df = {}
        for toks in self.docs_tokens:
            for w in set(toks):
                self.df[w] = self.df.get(w, 0) + 1

        # idf (Okapi)
        self.idf = {w: float(np.log(1 + (N - df + 0.5) / (df + 0.5))) for w, df in self.df.items()}
        return self

    def search(self, queries, k: int = 10):
        import numpy as np
        results = []
        for q in queries:
            q_toks = self._tokenize(q)
            scores = np.zeros(len(self.docs_tokens), dtype=float)
            for i, toks in enumerate(self.docs_tokens):
                len_i = len(toks)
                if len_i == 0:
                    continue
                # term frequencies
                tf = {}
                for w in toks:
                    tf[w] = tf.get(w, 0) + 1
                score = 0.0
                for w in q_toks:
                    tfw = tf.get(w, 0)
                    if tfw == 0:
                        continue
                    idf = self.idf.get(w, 0.0)
                    numerator = tfw * (self.k1 + 1.0)
                    denom = tfw + self.k1 * (1 - self.b + self.b * (len_i / (self.avgdl + 1e-8)))
                    score += idf * (numerator / (denom + 1e-8))
                scores[i] = score
            if len(scores) == 0:
                results.append(np.array([], dtype=int))
                continue
            topk = np.argpartition(-scores, kth=min(k, max(1, len(scores)) - 1))[:k]
            topk = topk[np.argsort(-scores[topk])]
            results.append(topk)
        return np.vstack(results)


