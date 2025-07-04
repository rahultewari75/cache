from typing import Dict, Optional
from storage.queue.entry import QueueEntry
from storage.error import InvalidInputError
from storage.queue.error import QueueNotFoundError

class Queue:
    """
    In-memory queue implementation that maps keys to queues with optional TTL.
    """
    
    def __init__(self):
        self._queues: Dict[str, QueueEntry] = {}
    
    def set(self, key: str, ttl: Optional[int] = None):
        """Create/reset a queue with optional TTL"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if ttl is not None and ttl <= 0:
            raise InvalidInputError("TTL must be a positive integer")
            
        self._queues[key] = QueueEntry(ttl)
    
    def get(self, key: str) -> list[str]:
        """Get queue contents"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._queues:
            raise QueueNotFoundError(key)
            
        if self._queues[key].is_expired():
            del self._queues[key]
            raise QueueNotFoundError(key)
            
        queue_ll = self._queues[key].get_value()
        return [item[1] for item in queue_ll] if queue_ll else []
    
    def enqueue(self, key: str, value: str) -> int:
        """Add value to queue, returns new size"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if not isinstance(value, str):
            raise InvalidInputError("Value must be a string")
            
        if key not in self._queues:
            raise QueueNotFoundError(key)
            
        if self._queues[key].is_expired():
            del self._queues[key]
            raise QueueNotFoundError(key)
            
        return self._queues[key].enqueue(value)
    
    def dequeue(self, key: str) -> str:
        """Remove and return first value from queue"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._queues:
            raise QueueNotFoundError(key)
            
        if self._queues[key].is_expired():
            del self._queues[key]
            raise QueueNotFoundError(key)
            
        value = self._queues[key].dequeue()
        if value is None:
            raise InvalidInputError("Queue is empty")
        return value
    
    def size(self, key: str) -> int:
        """Get queue size"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._queues:
            raise QueueNotFoundError(key)
            
        if self._queues[key].is_expired():
            del self._queues[key]
            raise QueueNotFoundError(key)
            
        return self._queues[key].size()
    
    def ttl(self, key: str) -> Optional[int]:
        """Get TTL for a queue in seconds, returns None if no expiration"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
            
        if key not in self._queues:
            raise QueueNotFoundError(key)
            
        if self._queues[key].is_expired():
            del self._queues[key]
            raise QueueNotFoundError(key)
            
        return self._queues[key].get_ttl()
    
    def expire(self, key: str, timestamp: float):
        """Set expiration timestamp for a queue"""
        if not isinstance(key, str):
            raise InvalidInputError("Key must be a string")
        if not isinstance(timestamp, (int, float)) or timestamp < 0:
            raise InvalidInputError("Timestamp must be a non-negative number")
            
        if key not in self._queues:
            raise QueueNotFoundError(key)
            
        self._queues[key].set_expiration(timestamp)
    
    def scan(self) -> list[str]:
        """Get all non-expired queue keys"""
        expired_keys = [k for k, v in self._queues.items() if v.is_expired()]
        for key in expired_keys:
            del self._queues[key]
            
        return list(self._queues.keys()) 