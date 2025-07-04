from typing import Optional
from data_types.entry import Entry
from util.ll import DoublyLinkedList

class QueueEntry(Entry[DoublyLinkedList]):
    """
    Entry class specifically for queue values that store values in a linked list.
    Provides enqueue/dequeue operations with O(1) complexity.
    """
    
    def __init__(self, ttl: Optional[int] = None):
        """Initialize empty queue with a doubly linked list"""
        super().__init__(DoublyLinkedList(), ttl)
    
    def enqueue(self, value: str) -> Optional[int]:
        """Add value to queue, returns new length or None if expired"""
        if self.is_expired():
            return None
        self.value.add_to_tail(value=value)
        return self.value.size()
    
    def dequeue(self) -> Optional[str]:
        """Remove and return first value from queue, or None if empty/expired"""
        if self.is_expired():
            return None
        node = self.value.remove_from_head()
        return node.value if node else None
    
    def size(self) -> Optional[int]:
        """Get current queue size or None if expired"""
        if self.is_expired():
            return None
        return self.value.size()

    def get_value(self) -> Optional[DoublyLinkedList]:
        """Get the queue contents as a linked list if not expired, None otherwise"""
        if self.is_expired():
            return None
        return self.value 