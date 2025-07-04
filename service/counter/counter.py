from typing import Dict, Optional
from data_types.entry import CounterEntry

class Counter:
    """
    In-memory counter implementation that maps keys to integer values.
    """
    
    def __init__(self):
        self._counters: Dict[str, CounterEntry] = {}
    
    def set(self, key: str, ttl: Optional[int] = None):
        """Set/reset a counter to 0 with optional TTL"""
        self._counters[key] = CounterEntry(ttl)
    
    def get(self, key: str) -> Optional[int]:
        """Get counter value, returns None if counter doesn't exist or expired"""
        if key not in self._counters:
            return None
        return self._counters[key].get_value()
    
    def increment(self, key: str) -> Optional[int]:
        """Increment counter by 1, returns new value or None if counter doesn't exist or expired"""
        if key not in self._counters:
            return None
        return self._counters[key].increment() 
    
    def decrement(self, key: str) -> Optional[int]:
        """Decrement counter by 1, returns new value or None if counter doesn't exist or expired"""
        if key not in self._counters:
            return None
        return self._counters[key].decrement()
    
    def ttl(self, key: str) -> Optional[int]:
        """Get TTL for a counter in seconds, returns None if counter doesn't exist or no expiration"""
        if key not in self._counters:
            return None
        return self._counters[key].get_ttl()
    
    def expire(self, key: str, timestamp: float):
        """Set expiration timestamp for a counter"""
        if key in self._counters:
            self._counters[key].set_expiration(timestamp)
    
    def scan(self) -> list[str]:
        """Get all non-expired counter keys"""
        active_counters = [(k, v) for k, v in self._counters.items() if not v.is_expired()]
        return [k for k, _ in active_counters] 