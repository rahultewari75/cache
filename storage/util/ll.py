from typing import Optional, Iterator, List, Tuple
from storage.data_types.entry import Entry

class Node:
    """
    Node class for doubly linked list.
    """
    def __init__(self, key: str = None, value: Entry = None):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None
    
    def __str__(self) -> str:
        return f"Node(key={self.key}, value={str(self.value)})"
    
    def __repr__(self) -> str:
        return self.__str__()

class DoublyLinkedList:
    """
    Doubly Linked List implementation optimized for cache operations.
    """
    
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self._size = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __bool__(self) -> bool:
        return self._size > 0
    
    def __iter__(self) -> Iterator[Node]:
        current = self.head.next
        while current != self.tail:
            yield current
            current = current.next
    
    def __reversed__(self) -> Iterator[Node]:
        current = self.tail.prev
        while current != self.head:
            yield current
            current = current.prev
    
    def is_empty(self) -> bool:
        """Check if the list is empty"""
        return self._size == 0
    
    def size(self) -> int:
        """Get the current size of the list"""
        return self._size
    
    def _add_node(self, node: Node, prev_node: Node, next_node: Node):
        """Internal method to add a node between two nodes"""
        node.prev = prev_node
        node.next = next_node
        prev_node.next = node
        next_node.prev = node
        self._size += 1
    
    def _remove_node(self, node: Node):
        """Internal method to remove a node from the list"""
        if node == self.head or node == self.tail:
            raise ValueError("Cannot remove dummy head or tail nodes")
        
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        self._size -= 1
    
    def add_to_head(self, key: str = None, value: Entry = None) -> Node:
        """Add a new node right after the head"""
        node = Node(key, value)
        self._add_node(node, self.head, self.head.next)
        return node
    
    def add_to_tail(self, key: str = None, value: Entry = None) -> Node:
        """Add a new node right before the tail"""
        node = Node(key, value)
        self._add_node(node, self.tail.prev, self.tail)
        return node
    
    def remove_from_head(self) -> Optional[Node]:
        """Remove and return the node right after head"""
        if self.is_empty():
            return None
        
        node = self.head.next
        self._remove_node(node)
        return node
    
    def remove_from_tail(self) -> Optional[Node]:
        """Remove and return the node right before tail"""
        if self.is_empty():
            return None
        
        node = self.tail.prev
        self._remove_node(node)
        return node
    
    def remove_node(self, node: Node):
        """Remove a specific node from the list"""
        self._remove_node(node)
    
    def move_to_head(self, node: Node):
        """Move an existing node to the head position"""
        self._remove_node(node)
        self._add_node(node, self.head, self.head.next)
    
    def move_to_tail(self, node: Node):
        """Move an existing node to the tail position"""
        self._remove_node(node)
        self._add_node(node, self.tail.prev, self.tail)
    
    def peek_head(self) -> Optional[Node]:
        """Return the head node without removing it"""
        if self.is_empty():
            return None
        return self.head.next
    
    def peek_tail(self) -> Optional[Node]:
        """Return the tail node without removing it"""
        if self.is_empty():
            return None
        return self.tail.prev
    
    def find(self, key: str) -> Optional[Node]:
        """Find a node by key"""
        for node in self:
            if node.key == key:
                return node
        return None
    
    def clear(self):
        """Remove all nodes from the list"""
        self.head.next = self.tail
        self.tail.prev = self.head
        self._size = 0
    
    def to_list(self) -> List[Tuple[str, Entry]]:
        """Convert to a regular Python list of (key, value) tuples"""
        return [(node.key, node.value) for node in self]
    
    def keys(self) -> list:
        """Get all keys in order from head to tail"""
        return [node.key for node in self]
    
    def values(self) -> list:
        """Get all values in order from head to tail"""
        return [node.value for node in self]
    
    def __str__(self) -> str:
        """String representation of the list"""
        if self.is_empty():
            return "DoublyLinkedList([])"
        
        items = [f"({node.key}, {node.value})" for node in self]
        return f"DoublyLinkedList([{' <-> '.join(items)}])"
    
    def __repr__(self) -> str:
        """Developer representation of the list"""
        return self.__str__()
    