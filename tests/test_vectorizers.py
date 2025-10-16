from ..retrieval.retriever import TfidfRetriever, Product

def test_tfidf_fit_search():
    prods = [
        Product("1","Blue Chair","Velvet accent"),
        Product("2","Red Sofa","Leather"),
        Product("3","Wood Table","Dining")
    ]
    r = TfidfRetriever().fit(prods)
    idx = r.search(["blue velvet"], k=2)
    assert idx.shape == (1,2)
