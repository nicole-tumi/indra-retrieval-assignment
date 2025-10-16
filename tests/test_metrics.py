from ..metrics.ranking import map_at_k, graded_map_at_k

def test_map_simple():
    preds = [["a","b","c"], ["x","y","z"]]
    gold  = [["b"], ["y","q"]]
    m = map_at_k(preds, gold, k=3)
    assert 0.3 <= m <= 0.7

def test_graded_runs():
    preds = [["a","b","c"]]
    gold  = [["q"]]
    id2text = {"a":"alpha chair", "b":"blue chair", "c":"red table", "q":"blue velvet chair"}
    q = ["blue chair"]
    g = graded_map_at_k(preds, gold, queries=q, id2text=id2text, k=3)
    assert 0.0 <= g <= 1.0
