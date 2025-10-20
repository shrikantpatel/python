class BucketNode :
    def __init__(self, count: int):
        self.count = count
        self.keys = set()
        self.prev = None
        self.next = None

class AllOne:

    def __init__(self):
        
        self.key_to_frequency = {}         # Maps key → frequency
        self.frequency_to_node = {}        # Maps frequency → FrequencyNode
        
        self.head = BucketNode(float('-inf'))  # Dummy head for min lookup
        self.tail = BucketNode(float('inf'))   # Dummy tail for max lookup

        self.head.next = self.tail
        self.tail.prev = self.head
        

    def inc(self, key: str) -> None:
        
        current_count = self.key_to_frequency.get(key, 0)
        new_count = current_count + 1
        self.key_to_frequency[key] = new_count

        current_bucket = self.frequency_to_node.get(current_count)

        # Create next bucket and insert in right position in the doubly linked list
        if new_count not in self.frequency_to_node:
            new_bucket = BucketNode(new_count)
            self.frequency_to_node[new_count] = new_bucket 
            if current_bucket:
                self._insert_bucket_after(new_bucket, current_bucket)
            else:
                self._insert_bucket_after(new_bucket, self.head)

        # Add this key to the frequency_to_node
        self.frequency_to_node[new_count].keys.add(key)  


        # Remove key from current bucket
        if current_bucket:
            current_bucket.keys.remove(key)
            if not current_bucket.keys:
                self._remove_bucket(current_bucket)


    def dec(self, key: str) -> None:

        if key not in self.key_to_frequency:
            return
        
        current_count = self.key_to_frequency.get(key)
        current_bucket = self.frequency_to_node.get(current_count)

        if current_count == 1:
            del self.key_to_frequency[key]
        else:
            new_count = current_count-1
            self.key_to_frequency[key] = new_count

            if new_count not in self.frequency_to_node:
                new_bucket = BucketNode(new_count)
                self.frequency_to_node[new_count] = new_bucket
                self._insert_bucket_after(new_bucket, current_bucket.prev)

            self.frequency_to_node[new_count].keys.add(key)

        # Remove key from current bucket
        current_bucket.keys.remove(key)
        if not current_bucket.keys:
            self._remove_bucket(current_bucket)


    def _remove_bucket(self, current_bucket: BucketNode) -> None:
        current_bucket.prev.next = current_bucket.next
        current_bucket.next.prev = current_bucket.prev
        del self.frequency_to_node[current_bucket.count]


    def _insert_bucket_after(self, new_bucket: BucketNode, current_bucket: BucketNode) -> None:
        new_bucket.next = current_bucket.next
        new_bucket.prev = current_bucket
        current_bucket.next.prev = new_bucket        
        current_bucket.next = new_bucket
        
    def getMaxKey(self) -> str:
        if self.tail.prev == self.head:
            return ""
        return next(iter(self.tail.prev.keys))    

    def getMinKey(self) -> str:
        if self.head.next == self.tail:
            return ""
        return next(iter(self.head.next.keys))


def main():
    tracker = AllOne()

    # Initial incs
    tracker.inc("a")  # a: 1
    tracker.inc("b")  # b: 1
    tracker.inc("c")  # c: 1

    tracker.inc("a")  # a: 2
    tracker.inc("a")  # a: 3
    tracker.inc("b")  # b: 2

    # Validate max and min
    assert tracker.getMaxKey() == "a", "Expected max key to be 'a'"
    assert tracker.getMinKey() == "c", "Expected min key to be 'c'"

    # Decrement 'a' from 3 → 2
    tracker.dec("a")
    assert tracker.getMaxKey() in {"a", "b"}, "Expected max key to be 'a' or 'b'"
    assert tracker.getMinKey() == "c", "Expected min key to still be 'c'"

    # Remove 'c' completely
    tracker.dec("c")
    assert tracker.getMinKey() in {"a", "b"}, "Expected min key to be 'a' or 'b' after removing 'c'"

    # Decrement both 'a' and 'b' to 1
    tracker.dec("a")
    tracker.dec("b")
    assert tracker.getMaxKey() in {"a", "b"}, "Expected max key to be 'a' or 'b' at count 1"
    assert tracker.getMinKey() in {"a", "b"}, "Expected min key to be 'a' or 'b' at count 1"

    print("✅ All assertions passed!")

if __name__ == "__main__":
    main()