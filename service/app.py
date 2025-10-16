from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .schemas import IndexRequest, SearchRequest, SearchResponse
from retrieval.pipeline import RetrievalPipeline
import pandas as pd
import logging

logger = logging.getLogger("indra.service")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Indra Retrieval Service", version="0.1.0")

PIPELINE = None
PRODUCTS_DF = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/index")
def index(req: IndexRequest):
    global PIPELINE, PRODUCTS_DF
    try:
        PRODUCTS_DF = pd.DataFrame(req.products)
        if not {"product_id","title","description"}.issubset(PRODUCTS_DF.columns):
            raise HTTPException(status_code=400, detail="products must include product_id, title, description")
        PIPELINE = RetrievalPipeline(model=req.model or "tfidf_char_word").fit(PRODUCTS_DF)
        return {"indexed": len(PRODUCTS_DF)}
    except Exception as e:
        logger.exception("Indexing failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    global PIPELINE, PRODUCTS_DF
    if PIPELINE is None:
        raise HTTPException(status_code=400, detail="Index not built. Call /index first.")
    try:
        results = PIPELINE.search(req.queries, k=req.k or 10)
        return SearchResponse(results=results)
    except Exception as e:
        logger.exception("Search failed")
        raise HTTPException(status_code=500, detail=str(e))
