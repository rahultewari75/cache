from typing import Optional, Any, Iterator, Dict
from .ll import DoublyLinkedList, Node
from data_types.entry import Entry

class OrderedDict:
    """
    An ordered dictionary implementation using a doubly linked list.
    """
    
    def __init__(self):
        self._dict: Dict[str, Node] = {}
        self._list = DoublyLinkedList()
    
    def __len__(self) -> int:
        return len(self._dict)
    
    def __bool__(self) -> bool:
        return bool(self._dict)
    
    def __contains__(self, key: str) -> bool:
        return key in self._dict
    
    def __iter__(self) -> Iterator[str]:
        """Iterate over keys in insertion order"""
        for node in self._list:
            yield node.key
    
    def __getitem__(self, key: str) -> Entry:
        """Get value by key, raises KeyError if not found"""
        if key not in self._dict:
            raise KeyError(key)
        return self._dict[key].value
    
    def __setitem__(self, key: str, value: Entry):
        """Set value for key, maintaining order"""
        if key in self._dict:
            node = self._dict[key]
            node.value = value
            self._list.move_to_tail(node)
        else:
            node = self._list.add_to_tail(key, value)
            self._dict[key] = node
    
    def __delitem__(self, key: str):
        """Delete item by key, raises KeyError if not found"""
        if key not in self._dict:
            raise KeyError(key)
        node = self._dict[key]
        self._list.remove_node(node)
        del self._dict[key]
    
    def get(self, key: str, default: Any = None) -> Optional[Entry]:
        """Get value by key, returns default if not found"""
        return self._dict[key].value if key in self._dict else default
    
    def pop(self, key: str, default: Any = None) -> Optional[Entry]:
        """Remove and return value by key, returns default if not found"""
        if key not in self._dict:
            if default is None:
                raise KeyError(key)
            return default
        
        node = self._dict[key]
        self._list.remove_node(node)
        del self._dict[key]
        return node.value
    
    def popitem(self, last: bool = True) -> tuple[str, Entry]:
        """Remove and return (key, value) pair. LIFO order if last=True, FIFO if False"""
        if not self._dict:
            raise KeyError('Dictionary is empty')
        
        node = self._list.remove_from_tail() if last else self._list.remove_from_head()
        del self._dict[node.key]
        return node.key, node.value
    
    def clear(self):
        """Remove all items"""
        self._dict.clear()
        self._list.clear()
    
    def keys(self) -> list[str]:
        """Return list of keys in order"""
        return self._list.keys()
    
    def values(self) -> list[Entry]:
        """Return list of values in order"""
        return self._list.values()
    
    def items(self) -> list[tuple[str, Entry]]:
        """Return list of (key, value) pairs in order"""
        return self._list.to_list()
    
    def move_to_end(self, key: str, last: bool = True):
        """Move an existing key to the beginning (last=False) or end (last=True)"""
        if key not in self._dict:
            raise KeyError(key)
        
        node = self._dict[key]
        if last:
            self._list.move_to_tail(node)
        else:
            self._list.move_to_head(node)
    
    def __str__(self) -> str:
        """String representation"""
        items = [f"{node.key}: {node.value}" for node in self._list]
        return "{" + ", ".join(items) + "}"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return self.__str__()
