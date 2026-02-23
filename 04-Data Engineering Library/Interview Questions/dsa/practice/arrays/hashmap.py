class ListNode:
    def __init__(self, key=-1, value=-1, next=None):
        self.key = key
        self.value = value
        self.next = next

class MyHashMap:

    def __init__(self):
        self.map = [ListNode() for i in range(1000)]

    def hash(self, key) -> int:
        return key%1000

    def put(self, key: int, value: int) -> None:
        hash_value = self.hash(key)
        curr = self.map[hash_value]
        while curr.next:
            if curr.next.key == key:
                curr.next.value = value
                return
            curr = curr.next
            
        curr.next = ListNode(key, value)

    def get(self, key: int) -> int:
        hash_value = self.hash(key)
        curr = self.map[hash_value]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        raise KeyError("Key Not Found")

        

    def remove(self, key: int) -> None:
        hash_value = self.hash(key)
        curr = self.map[hash_value]
        while curr.next:
            if curr.next.key == key:
                curr.next = curr.next.next
                return
            curr = curr.next
        raise KeyError("Key Not Found")