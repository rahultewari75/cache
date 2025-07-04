from typing import Dict, Optional
from .entry import CounterEntry
from storage.counter.error import CounterNotFoundError
from storage.error import InvalidInputError

class Counter:
    """
    In-memory counter implementation that maps keys to integer values.
    """
    
    def __init__(self):
        self._counters: Dict[str, CounterEntry] = {}
    
    def set(self, key: str, ttl: Optional[int] = None):
        """Set/reset a counter to 0 with optional TTL"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if ttl is not None and ttl <= 0:
            raise InvalidInputError("TTL must be a positive integer")
            
        self._counters[key] = CounterEntry(ttl)
    
    def get(self, key: str) -> int:
        """Get counter value"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._counters:
            raise CounterNotFoundError(key)
            
        if self._counters[key].is_expired():
            del self._counters[key]
            raise CounterNotFoundError(key)
            
        return self._counters[key].get_value()
    
    def increment(self, key: str) -> int:
        """Increment counter by 1, returns new value"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._counters:
            raise CounterNotFoundError(key)
            
        if self._counters[key].is_expired():
            del self._counters[key]
            raise CounterNotFoundError(key)
            
        return self._counters[key].increment()
    
    def decrement(self, key: str) -> int:
        """Decrement counter by 1, returns new value"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._counters:
            raise CounterNotFoundError(key)
            
        if self._counters[key].is_expired():
            del self._counters[key]
            raise CounterNotFoundError(key)
            
        return self._counters[key].decrement()
    
    def ttl(self, key: str) -> Optional[int]:
        """Get TTL for a counter in seconds, returns None if counter doesn't exist or no expiration"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._counters:
            raise CounterNotFoundError(key)
            
        if self._counters[key].is_expired():
            del self._counters[key]
            raise CounterNotFoundError(key)
            
        return self._counters[key].get_ttl()
    
    def expire(self, key: str, timestamp: float):
        """Set expiration timestamp for a counter"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if not isinstance(timestamp, (int, float)) or timestamp < 0:
            raise InvalidInputError("Timestamp must be a non-negative number")
            
        if key not in self._counters:
            raise CounterNotFoundError(key)
            
        self._counters[key].set_expiration(timestamp)
    
    def scan(self) -> list[str]:
        """Get all non-expired counter keys"""
        expired_keys = [k for k, v in self._counters.items() if v.is_expired()]
        for key in expired_keys:
            del self._counters[key]
            
        return list(self._counters.keys()) 