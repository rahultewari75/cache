from typing import Dict, Optional
from data_types.entry import QueueEntry

class Queue:
    """
    In-memory queue implementation that maps keys to queues with optional TTL.
    """
    
    def __init__(self):
        self._queues: Dict[str, QueueEntry] = {}
    
    def set(self, key: str, ttl: Optional[int] = None):
        """Create/reset a queue with optional TTL"""
        self._queues[key] = QueueEntry(ttl)
    
    def get(self, key: str) -> Optional[list[str]]:
        """Get queue contents, returns None if queue doesn't exist or expired"""
        if key not in self._queues:
            return None
        return self._queues[key].get_value()
    
    def enqueue(self, key: str, value: str) -> Optional[int]:
        """Add value to queue, returns new size or None if queue doesn't exist or expired"""
        if key not in self._queues:
            return None
        return self._queues[key].enqueue(value)
    
    def dequeue(self, key: str) -> Optional[str]:
        """Remove and return first value from queue, returns None if queue doesn't exist, is empty, or expired"""
        if key not in self._queues:
            return None
        return self._queues[key].dequeue()
    
    def size(self, key: str) -> Optional[int]:
        """Get queue size, returns None if queue doesn't exist or expired"""
        if key not in self._queues:
            return None
        return self._queues[key].size()
    
    def ttl(self, key: str) -> Optional[int]:
        """Get TTL for a queue in seconds, returns None if queue doesn't exist or no expiration"""
        if key not in self._queues:
            return None
        return self._queues[key].get_ttl()
    
    def expire(self, key: str, timestamp: float):
        """Set expiration timestamp for a queue"""
        if key in self._queues:
            self._queues[key].set_expiration(timestamp)
    
    def scan(self) -> list[str]:
        """Get all non-expired queue keys"""
        active_queues = [(k, v) for k, v in self._queues.items() if not v.is_expired()]
        return [k for k, _ in active_queues] 