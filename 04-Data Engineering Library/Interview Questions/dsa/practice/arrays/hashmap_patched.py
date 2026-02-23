class ListNode:
    def __init__(self, key=None, value=None, next=None):
        self.key = key
        self.value = value
        self.next = next


class MyHashMap:
    def __init__(self, initial_capacity=1000):
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be positive")
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [ListNode() for _ in range(self.capacity)]

    def _hash(self, key: int) -> int:
        return key % self.capacity

    def _find_prev(self, key: int):
        idx = self._hash(key)
        prev = self.buckets[idx]
        while prev.next and prev.next.key != key:
            prev = prev.next
        return prev

    def put(self, key: int, value: int) -> None:
        prev = self._find_prev(key)
        if prev.next:
            prev.next.value = value
            return

        prev.next = ListNode(key, value)
        self.size += 1

        # Rehash when load factor exceeds 0.75.
        if self.size / self.capacity > 0.75:
            self._rehash(self.capacity * 2)

    def get(self, key: int) -> int:
        prev = self._find_prev(key)
        if not prev.next:
            raise KeyError("Key not found")
        return prev.next.value

    def remove(self, key: int) -> None:
        prev = self._find_prev(key)
        if not prev.next:
            raise KeyError("Key not found")
        prev.next = prev.next.next
        self.size -= 1

    def _rehash(self, new_capacity: int) -> None:
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [ListNode() for _ in range(self.capacity)]
        old_size = self.size
        self.size = 0

        for head in old_buckets:
            curr = head.next
            while curr:
                self.put(curr.key, curr.value)
                curr = curr.next

        self.size = old_size

    def __len__(self) -> int:
        return self.size
