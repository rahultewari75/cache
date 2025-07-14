from typing import Any, Optional, List, Dict
import time
from ..policies.policy import ReplacementPolicy
from ..data_types.entry import Entry
from ..errors import InvalidInputError, KeyNotFoundError, KeyExpiredError

class Cache:
    """A generic cache implementation that uses a pluggable replacement policy.
    
    This cache stores key-value pairs with optional TTL and uses a provided
    replacement policy to determine which items to evict when capacity is reached.
    """
    
    def __init__(self, capacity: int, policy: ReplacementPolicy):
        """Initialize the cache with a given capacity and replacement policy.
        
        Args:
            capacity: Maximum number of items the cache can hold
            policy: The replacement policy to use for eviction decisions
            
        Raises:
            InvalidInputError: If capacity is not a positive integer
        """
        if not isinstance(capacity, int) or capacity <= 0:
            raise InvalidInputError("Cache capacity must be greater than 0")
            
        self.capacity = capacity
        self.policy = policy
        self._storage: Dict[str, Entry[Any]] = {}
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a key-value pair in the cache with optional TTL.
        
        Args:
            key: The key to store the value under
            value: The value to store
            ttl: Optional TTL in seconds
            
        Raises:
            InvalidInputError: If key is not a string or TTL is not a positive integer
        """
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if ttl is not None and ttl <= 0:
            raise InvalidInputError("TTL must be a positive integer")
            
        # Clean up expired entries first
        self._cleanup_expired()
        
        if key in self._storage:
            # Update existing key
            self._storage[key].update_value(value, ttl)
            self.policy.record_access(key)
        else:
            # Add new key
            if len(self._storage) >= self.capacity:
                evict_key = self.policy.evict()
                del self._storage[evict_key]
            
            self._storage[key] = Entry(value, ttl)
            self.policy.record_access(key)
    
    def get(self, key: str) -> Any:
        """Get a value from the cache.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The stored value
            
        Raises:
            InvalidInputError: If key is not a string
            KeyNotFoundError: If key does not exist
            KeyExpiredError: If key exists but has expired
        """
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._storage:
            raise KeyNotFoundError(key)
            
        entry = self._storage[key]
        if entry.is_expired():
            expiration_time = entry.expiration_time
            self._remove_key(key)
            raise KeyExpiredError(key, expiration_time)
            
        self.policy.record_access(key)
        return entry.get_value()
    
    def ttl(self, key: str) -> Optional[int]:
        """Get the remaining TTL for a key in seconds.
        
        Args:
            key: The key to check
            
        Returns:
            Remaining TTL in seconds, or None if no TTL
            
        Raises:
            InvalidInputError: If key is not a string
            KeyNotFoundError: If key does not exist
            KeyExpiredError: If key exists but has expired
        """
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._storage:
            raise KeyNotFoundError(key)
            
        entry = self._storage[key]
        if entry.is_expired():
            expiration_time = entry.expiration_time
            self._remove_key(key)
            raise KeyExpiredError(key, expiration_time)
            
        return entry.get_ttl()
    
    def expire(self, key: str, timestamp: float) -> None:
        """Set an expiration timestamp for a key.
        
        Args:
            key: The key to set expiration for
            timestamp: Unix timestamp when the key should expire
            
        Raises:
            InvalidInputError: If key is not a string or timestamp is negative
            KeyNotFoundError: If key does not exist
        """
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if not isinstance(timestamp, (int, float)) or timestamp < 0:
            raise InvalidInputError("Timestamp must be a non-negative number")
            
        if key not in self._storage:
            raise KeyNotFoundError(key)
            
        self._storage[key].set_expiration(timestamp)
    
    def scan(self) -> List[str]:
        """Get all non-expired keys in the cache.
        
        Returns:
            List of non-expired keys
        """
        self._cleanup_expired()
        return list(self._storage.keys())
    
    def _remove_key(self, key: str) -> None:
        """Remove a key from the cache and policy."""
        if key in self._storage:
            del self._storage[key]
            self.policy.remove_key(key)
    
    def _cleanup_expired(self) -> None:
        """Remove all expired entries from the cache."""
        expired = [k for k, v in self._storage.items() if v.is_expired()]
        for key in expired:
            self._remove_key(key)
    
    def clear(self) -> None:
        """Remove all entries from the cache."""
        self._storage.clear()
        self.policy.clear()

    def delete(self, key: str) -> None:
        """Delete a key-value pair from the cache.
        
        Args:
            key: The key to delete
            
        Raises:
            InvalidInputError: If key is not a string
            KeyNotFoundError: If key does not exist
        """
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._storage:
            raise KeyNotFoundError(key)
            
        self._remove_key(key) 