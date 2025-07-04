from typing import Optional, List, Union, Dict
from .entry import KVEntry
from storage.util.ll import DoublyLinkedList, Node
from storage.cache.error import KeyNotFoundError, KeyExpiredError
from storage.error import InvalidInputError
from storage.cache.cache import Cache

class LRUCache(Cache):
    """
    Least Recently Used (LRU) cache implementation
    """
    
    def __init__(self, capacity: int = 1000):
        if capacity <= 0:
            raise InvalidInputError("Cache capacity must be greater than 0")
        self.capacity = capacity
        
        self._cache: Dict[str, Node] = {}
        
        self._dll = DoublyLinkedList()
    
    def configure(self, capacity: int):
        """Configure cache capacity"""
        if capacity <= 0:
            raise InvalidInputError("Cache capacity must be greater than 0")
        self.capacity = capacity
        
        while len(self._cache) > self.capacity:
            self._evict_lru()
    
    def set(self, key: str, value: Union[str, int, float, bool, dict, list, bytes], ttl: Optional[int] = None):
        """Set a key-value pair with optional TTL"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if ttl is not None and ttl <= 0:
            raise InvalidInputError("TTL must be a positive integer")
            
        if key in self._cache:
            node = self._cache[key]
            entry = node.value
            entry.update_value(value, ttl)
            self._dll.move_to_head(node)
        else:
            if len(self._cache) >= self.capacity:
                self._evict_lru()
            
            entry = KVEntry(value, ttl)
            node = self._dll.add_to_head(key, entry)
            self._cache[key] = node
    
    def get(self, key: str) -> Union[str, int, float, bool, dict, list, bytes]:
        """Get value by key"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._cache:
            raise KeyNotFoundError(key)
            
        node = self._cache[key]
        entry = node.value
        
        if entry.is_expired():
            expiration_time = entry.expiration_time
            self._remove_expired_key(key)
            raise KeyExpiredError(key, expiration_time)
        
        self._dll.move_to_head(node)
        return entry.get_value()
    
    def ttl(self, key: str) -> Optional[int]:
        """Get TTL for a key in seconds, returns None if key doesn't exist or no expiration"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._cache:
            raise KeyNotFoundError(key)
            
        node = self._cache[key]
        entry = node.value
        
        if entry.is_expired():
            expiration_time = entry.expiration_time
            self._remove_expired_key(key)
            raise KeyExpiredError(key, expiration_time)
        
        return entry.get_ttl()
    
    def expire(self, key: str, timestamp: float):
        """Set expiration timestamp for a key"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if not isinstance(timestamp, (int, float)) or timestamp < 0:
            raise InvalidInputError("Timestamp must be a non-negative number")
            
        if key not in self._cache:
            raise KeyNotFoundError(key)
            
        node = self._cache[key]
        entry = node.value
        entry.set_expiration(timestamp)
    
    def scan(self) -> List[str]:
        """Get all non-expired keys"""
        self._cleanup_expired_keys()
        return list(self._cache.keys())
    
    def _is_expired(self, key: str) -> bool:
        """Check if a key has expired"""
        if key not in self._cache:
            return True
        
        node = self._cache[key]
        entry = node.value
        if entry.is_expired():
            self._remove_expired_key(key)
            return True
        return False
    
    def _remove_expired_key(self, key: str):
        """Remove an expired key from cache"""
        if key in self._cache:
            node = self._cache[key]
            self._dll.remove_node(node)
            del self._cache[key]
    
    def _cleanup_expired_keys(self):
        """Clean up all expired keys"""
        expired_keys = []
        
        for key, node in self._cache.items():
            entry = node.value
            if entry.is_expired():
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove_expired_key(key)
    
    def _evict_lru(self):
        """Evict the least recently used key"""
        if not self._dll.is_empty():
            lru_node = self._dll.remove_from_tail()
            if lru_node and lru_node.key in self._cache:
                del self._cache[lru_node.key]
    