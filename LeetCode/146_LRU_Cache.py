#https://leetcode.com/problems/lru-cache/description/

class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # map key to node

        # Dummy head and tail
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_to_head(node)
        return node.value
        
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        if len(self.cache) == self.capacity:
            lru = self.tail.prev
            self._remove(lru)

        new_node = Node(key, value)
        self._insert_to_head(new_node)

    def _insert_to_head(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.cache[node.key] = node

    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev
        del self.cache[node.key]

cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))  # returns 1
cache.put(3, 3)      # evicts key 2
print(cache.get(2))  # returns -1
cache.put(4, 4)      # evicts key 1
print(cache.get(1))  # returns -1
print(cache.get(3))  # returns 3
print(cache.get(4))  # returns 4
