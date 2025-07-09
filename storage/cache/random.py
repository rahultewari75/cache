from typing import Optional, List, Dict, Union
from storage.cache.error import KeyNotFoundError, KeyExpiredError
from storage.error import InvalidInputError
from storage.cache.cache import Cache
from storage.cache.entry import KVEntry

import random

class RandomCache(Cache):
    """
    Random Eviction Cache implementation - evicts a random element when capacity is reached
    Uses array + index mapping for O(1) operations with optimal memory layout
    """
    
    def __init__(self, capacity: int = 1000):
        if capacity <= 0:
            raise InvalidInputError("Cache capacity must be greater than 0")
        self.capacity = capacity
        
        # Array of (key, entry) tuples for O(1) random access and value storage
        self._entries: List[tuple[str, KVEntry]] = []
        # Map of key to index in entries array for O(1) lookup
        self._key_to_idx: Dict[str, int] = {}
    
    def configure(self, capacity: int):
        """Configure cache capacity"""
        if capacity <= 0:
            raise InvalidInputError("Cache capacity must be greater than 0")
        self.capacity = capacity
        
        while len(self._entries) > self.capacity:
            self._evict_random()
    
    def set(self, key: str, value: Union[str, int, float, bool, dict, list, bytes], ttl: Optional[int] = None):
        """Set a key-value pair with optional TTL"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if ttl is not None and ttl <= 0:
            raise InvalidInputError("TTL must be a positive integer")
            
        if key in self._key_to_idx:
            # Update existing entry
            idx = self._key_to_idx[key]
            self._entries[idx][1].update_value(value, ttl)
        else:
            if len(self._entries) >= self.capacity:
                self._evict_random()
            
            entry = KVEntry(value, ttl)
            self._entries.append((key, entry))
            self._key_to_idx[key] = len(self._entries) - 1
    
    def get(self, key: str) -> Union[str, int, float, bool, dict, list, bytes]:
        """Get value by key"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._key_to_idx:
            raise KeyNotFoundError(key)
            
        idx = self._key_to_idx[key]
        entry = self._entries[idx][1]
        
        if entry.is_expired():
            expiration_time = entry.expiration_time
            self._remove_expired_key(key)
            raise KeyExpiredError(key, expiration_time)
        
        return entry.get_value()
    
    def ttl(self, key: str) -> Optional[int]:
        """Get TTL for a key in seconds, returns None if key doesn't exist or no expiration"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._key_to_idx:
            raise KeyNotFoundError(key)
            
        idx = self._key_to_idx[key]
        entry = self._entries[idx][1]
        
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
            
        if key not in self._key_to_idx:
            raise KeyNotFoundError(key)
            
        idx = self._key_to_idx[key]
        self._entries[idx][1].set_expiration(timestamp)
    
    def scan(self) -> List[str]:
        """Get all non-expired keys"""
        self._cleanup_expired_keys()
        return [key for key, _ in self._entries]
    
    def _is_expired(self, key: str) -> bool:
        """Check if a key has expired"""
        if key not in self._key_to_idx:
            return True
        
        idx = self._key_to_idx[key]
        if self._entries[idx][1].is_expired():
            self._remove_expired_key(key)
            return True
        return False
    
    def _remove_expired_key(self, key: str):
        """Remove an expired key from cache using O(1) swap and pop"""
        if key in self._key_to_idx:
            idx = self._key_to_idx[key]
            self._remove_at_index(idx)
    
    def _cleanup_expired_keys(self):
        """Clean up all expired keys"""
        # Iterate backwards to handle removals
        i = len(self._entries) - 1
        while i >= 0:
            key, entry = self._entries[i]
            if entry.is_expired():
                self._remove_at_index(i)
            i -= 1
    
    def _evict_random(self):
        """Evict a random key from cache using O(1) operations"""
        if self._entries:
            idx = random.randrange(len(self._entries))
            self._remove_at_index(idx)
    
    def _remove_at_index(self, idx: int):
        """Helper to remove entry at given index using O(1) swap and pop"""
        if idx >= len(self._entries):
            return
            
        # Remove the mapping for the key being deleted
        key_to_remove = self._entries[idx][0]
        del self._key_to_idx[key_to_remove]
        
        if idx < len(self._entries) - 1:
            # Swap with last element if not already last
            self._entries[idx] = self._entries[-1]
            # Update index mapping for swapped key
            self._key_to_idx[self._entries[idx][0]] = idx
            
        # Pop last element
        self._entries.pop() 