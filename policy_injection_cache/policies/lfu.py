from collections import defaultdict, OrderedDict
from .policy import ReplacementPolicy
from ..errors import InvalidPolicyError

class LFUPolicy(ReplacementPolicy):
    """Least Frequently Used (LFU) replacement policy.
    
    Uses a combination of frequency counting and recency ordering to track usage.
    When multiple items have the same frequency, the least recently used among
    them is chosen for eviction.
    """
    
    def __init__(self):
        # Maps key to access frequency
        self._frequencies = defaultdict(int)
        # Maps frequency to OrderedDict of keys with that frequency
        self._freq_groups = defaultdict(OrderedDict)
        # Track minimum frequency for O(1) eviction
        self._min_freq = 0
    
    def record_access(self, key: str) -> None:
        """Record access to a key by incrementing its frequency.
        
        Args:
            key: The key being accessed
        """
        if key in self._frequencies:
            # Get current frequency and increment
            old_freq = self._frequencies[key]
            new_freq = old_freq + 1
            
            # Move key to next frequency group
            del self._freq_groups[old_freq][key]
            self._freq_groups[new_freq][key] = None
            self._frequencies[key] = new_freq
            
            # Update min frequency if needed
            if old_freq == self._min_freq and not self._freq_groups[old_freq]:
                self._min_freq = new_freq
        else:
            # First access to this key
            self._frequencies[key] = 1
            self._freq_groups[1][key] = None
            self._min_freq = 1
    
    def evict(self) -> str:
        """Choose the least frequently used key to evict.
        
        Returns:
            The key with lowest frequency (and oldest among those)
            
        Raises:
            InvalidPolicyError: If no keys are available to evict
        """
        try:
            # Get the first key from the minimum frequency group
            return next(iter(self._freq_groups[self._min_freq]))
        except (KeyError, StopIteration):
            raise InvalidPolicyError("No keys available to evict")
    
    def remove_key(self, key: str) -> None:
        """Remove a key from tracking.
        
        Args:
            key: The key to remove
        """
        if key in self._frequencies:
            freq = self._frequencies[key]
            del self._freq_groups[freq][key]
            del self._frequencies[key]
            
            # Update min frequency if needed
            if freq == self._min_freq and not self._freq_groups[freq]:
                # Find next non-empty frequency if any
                self._min_freq = min(self._freq_groups.keys(), default=0)
    
    def clear(self) -> None:
        """Clear all tracking state."""
        self._frequencies.clear()
        self._freq_groups.clear()
        self._min_freq = 0 