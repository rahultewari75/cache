from typing import Optional
from data_types.entry import Entry

class CounterEntry(Entry[int]):
    """
    Entry class specifically for counter values that only store integers.
    Provides atomic increment/decrement operations.
    """
    
    def __init__(self, ttl: Optional[int] = None):
        """Initialize counter to 0"""
        super().__init__(0, ttl)
    
    def increment(self) -> Optional[int]:
        """Increment counter by 1, returns new value or None if expired"""
        if self.is_expired():
            return None
        self.value += 1
        return self.value
    
    def decrement(self) -> Optional[int]:
        """Decrement counter by 1, returns new value or None if expired"""
        if self.is_expired():
            return None
        self.value -= 1
        return self.value 