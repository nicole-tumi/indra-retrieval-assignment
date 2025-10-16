from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IndexRequest(BaseModel):
    model: Optional[str] = Field(default="tfidf_char_word", description="tfidf_char_word | bm25")
    products: List[Dict[str, Any]]

class SearchRequest(BaseModel):
    queries: List[str]
    k: Optional[int] = 10

class SearchResponse(BaseModel):
    results: List[List[str]]
