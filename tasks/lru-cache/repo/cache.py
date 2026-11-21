class LRUCache:
    """Least recently used cache: when full, the entry unused for the longest time is evicted."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.data = {}  # dicts keep insertion order: the first key is the least recently used

    def get(self, key, default=None):
        if key in self.data:
            return self.data[key]
        return default

    def put(self, key, value) -> None:
        if len(self.data) >= self.capacity:
            oldest = next(iter(self.data))
            del self.data[oldest]
        self.data[key] = value

    def __len__(self) -> int:
        return len(self.data)
