import pytest

from cache import LRUCache


def test_basic():
    cache = LRUCache(2)
    cache.put("a", 1)
    assert cache.get("a") == 1
    assert cache.get("missing", 0) == 0


def test_evicts_least_recently_used():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # "a" becomes the most recently used
    cache.put("c", 3)
    assert cache.get("b") is None
    assert cache.get("a") == 1 and cache.get("c") == 3


def test_update_existing_key_does_not_evict():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    assert len(cache) == 2
    assert cache.get("a") == 10 and cache.get("b") == 2


def test_update_refreshes_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    cache.put("c", 3)
    assert cache.get("b") is None


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)


def test_stats():
    cache = LRUCache(2)
    assert cache.stats() == {"hits": 0, "misses": 0, "hit_rate": 0.0}
    cache.put("a", 1)
    cache.get("a")
    cache.get("a")
    cache.get("b")
    cache.get("c")
    assert cache.stats() == {"hits": 2, "misses": 2, "hit_rate": 0.5}
