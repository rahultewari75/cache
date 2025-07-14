import random
from .policy import ReplacementPolicy
from ..errors import InvalidPolicyError

class RandomPolicy(ReplacementPolicy):
    """Random replacement policy.
    
    Maintains a set of active keys and randomly selects one for eviction
    when needed. This provides O(1) operations and good distribution of
    evictions across the keyspace.
    """
    
    def __init__(self):
        self._keys = set()
    
    def record_access(self, key: str) -> None:
        """Record access to a key by adding it to the tracked set.
        
        Args:
            key: The key being accessed
        """
        self._keys.add(key)
    
    def evict(self) -> str:
        """Choose a random key to evict.
        
        Returns:
            A randomly selected key
            
        Raises:
            InvalidPolicyError: If no keys are available to evict
        """
        try:
            return random.choice(tuple(self._keys))
        except IndexError:
            raise InvalidPolicyError("No keys available to evict")
    
    def remove_key(self, key: str) -> None:
        """Remove a key from tracking.
        
        Args:
            key: The key to remove
        """
        self._keys.discard(key)
    
    def clear(self) -> None:
        """Clear all tracking state."""
        self._keys.clear() 