import re
from typing import List

def normalize_text(s) -> str:
    if s is None:
        return ""
    # tolerante a NaN/numéricos/objetos raros
    try:
        s = "" if (s != s) else s  # NaN check for NaN
        s = str(s)
    except Exception:
        return ""
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def tokenize(s: str) -> List[str]:
    return normalize_text(s).split()

def char_ngrams(s: str, n: int) -> List[str]:
    s = normalize_text(s).replace(" ", "_")
    return [s[i:i+n] for i in range(max(0, len(s)-n+1))]
