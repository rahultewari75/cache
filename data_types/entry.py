import time
from typing import Optional, TypeVar, Generic

T = TypeVar('T')

class Entry(Generic[T]):
    """
    Base entry class to wrap values with TTL metadata.
    """
    
    def __init__(self, value: T, ttl: Optional[int] = None):
        self.value = value
        self.created_at = time.time()
        self.expiration_time = self.created_at + ttl if ttl is not None else None
    
    def is_expired(self) -> bool:
        """Check if the entry has expired"""
        if self.expiration_time is None:
            return False
        return time.time() > self.expiration_time
    
    def get_value(self) -> Optional[T]:
        """Get the value if not expired, None otherwise"""
        if self.is_expired():
            return None
        return self.value
    
    def get_ttl(self) -> Optional[int]:
        """Get remaining TTL in seconds, None if no expiration or expired"""
        if self.expiration_time is None:
            return None
        
        if self.is_expired():
            return None
        
        remaining = self.expiration_time - time.time()
        return max(0, int(remaining))
    
    def set_expiration(self, timestamp: float):
        """Set expiration timestamp"""
        self.expiration_time = timestamp
    
    def update_value(self, new_value: T, ttl: Optional[int] = None):
        """Update the entry's value and optionally its TTL"""
        self.value = new_value
        self.created_at = time.time()
        self.expiration_time = self.created_at + ttl if ttl is not None else None
    
    def __str__(self) -> str:
        """String representation of the entry"""
        value_display = f"<bytes: {len(self.value)} bytes>" if isinstance(self.value, bytes) else self.value
        return f"{self.__class__.__name__}(value={value_display}, created_at={self.created_at}, expiration_time={self.expiration_time})"
    
    def __repr__(self) -> str:
        """Developer representation of the entry"""
        return self.__str__()