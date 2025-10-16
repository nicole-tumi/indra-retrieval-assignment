from typing import List, Set, Dict, Iterable, Tuple
import numpy as np
from retrieval.text import tokenize, char_ngrams, normalize_text

def _precision_at_k(retrieved: List[str], gold: Set[str], k: int) -> float:
    hits = 0
    total = 0
    for i, pid in enumerate(retrieved[:k], start=1):
        total += 1
        if pid in gold:
            hits += 1
    return hits / max(1, total)

def average_precision_at_k(retrieved: List[str], gold: Set[str], k: int) -> float:
    hits = 0
    precisions = []
    for i, pid in enumerate(retrieved[:k], start=1):
        if pid in gold:
            hits += 1
            precisions.append(hits / i)
    return float(np.mean(precisions)) if precisions else 0.0

def map_at_k(all_retrieved: List[List[str]], all_gold: List[Iterable[str]], k: int=10) -> float:
    ap = []
    for preds, gold_ids in zip(all_retrieved, all_gold):
        ap.append(average_precision_at_k(preds, set(map(str, gold_ids)), k))
    return float(np.mean(ap)) if ap else 0.0

# --------- Graded (partial-match-aware) ---------

def token_jaccard(a: str, b: str) -> float:
    ta, tb = set(tokenize(a)), set(tokenize(b))
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / max(1, union)

def char_overlap(a: str, b: str, ns=(3,4,5)) -> float:
    a_grams = set()
    b_grams = set()
    for n in ns:
        a_grams |= set(char_ngrams(a, n))
        b_grams |= set(char_ngrams(b, n))
    if not a_grams or not b_grams:
        return 0.0
    inter = len(a_grams & b_grams)
    union = len(a_grams | b_grams)
    return inter / max(1, union)

def graded_gain(query: str, candidate_text: str, exact: bool, j_thr=0.2) -> float:
    if exact:
        return 1.0
    j = token_jaccard(query, candidate_text)
    c = char_overlap(query, candidate_text)
    g = 0.6 * j + 0.4 * c
    return g if g >= j_thr else 0.0

def graded_average_precision_at_k(retrieved: List[str],
                                  gold: Set[str],
                                  k: int,
                                  query: str,
                                  id2text: Dict[str, str]) -> float:
    """AP with gains: each hit contributes gain * precision@i"""
    gains = []
    for i, pid in enumerate(retrieved[:k], start=1):
        exact = pid in gold
        cand = id2text.get(pid, "")
        g = graded_gain(query, cand, exact)
        if g > 0:
            gains.append((g, i))
    if not gains:
        return 0.0
    weighted_precisions = []
    retrieved_prefix = retrieved[:k]
    for g, i in gains:
        # count how many items up to i have gain>0
        rel_so_far = 0
        for pid2 in retrieved_prefix[:i]:
            cand2 = id2text.get(pid2, "")
            rel2 = graded_gain(query, cand2, pid2 in gold)
            if rel2 > 0:
                rel_so_far += 1
        precision_i = rel_so_far / i
        weighted_precisions.append(g * precision_i)
    return float(np.mean(weighted_precisions))

def graded_map_at_k(all_retrieved: List[List[str]],
                    all_gold: List[Iterable[str]],
                    queries: List[str],
                    id2text: Dict[str, str],
                    k: int=10) -> float:
    ap = []
    for preds, gold_ids, q in zip(all_retrieved, all_gold, queries):
        ap.append(
            graded_average_precision_at_k(preds, set(map(str, gold_ids)), k, q, id2text)
        )
    return float(np.mean(ap)) if ap else 0.0
