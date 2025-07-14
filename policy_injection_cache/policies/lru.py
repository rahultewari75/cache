from collections import OrderedDict
from .policy import ReplacementPolicy
from ..errors import InvalidPolicyError

class LRUPolicy(ReplacementPolicy):
    """Least Recently Used (LRU) replacement policy.
    
    Uses an OrderedDict to track access order, where the least recently used item
    is at the beginning and most recently used is at the end.
    """
    
    def __init__(self):
        self._access_order = OrderedDict()
    
    def record_access(self, key: str) -> None:
        """Record access to a key by moving it to the end of the order.
        
        Args:
            key: The key being accessed
        """
        # Remove and re-add to move to end
        self._access_order.pop(key, None)
        self._access_order[key] = None
    
    def evict(self) -> str:
        """Choose the least recently used key to evict.
        
        Returns:
            The key that was least recently accessed
            
        Raises:
            InvalidPolicyError: If no keys are available to evict
        """
        try:
            # Get and remove the first item (least recently used)
            return next(iter(self._access_order))
        except StopIteration:
            raise InvalidPolicyError("No keys available to evict")
    
    def remove_key(self, key: str) -> None:
        """Remove a key from tracking.
        
        Args:
            key: The key to remove
        """
        self._access_order.pop(key, None)
    
    def clear(self) -> None:
        """Clear all tracking state."""
        self._access_order.clear() 