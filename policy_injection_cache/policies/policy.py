from typing import Protocol, TypeVar

K = TypeVar('K')
V = TypeVar('V')

class ReplacementPolicy(Protocol[K, V]):
    """Protocol defining the interface for cache replacement policies.
    
    This protocol defines the methods that any cache replacement policy must implement
    to be used with the policy-based cache implementation.
    """

    def record_access(self, key: str) -> None:
        """Record an access to the given key.
        
        This is called whenever a key is accessed via get() or set().
        The policy should update its internal state accordingly.

        Args:
            key: The key being accessed
        """
        ...

    def evict(self) -> str:
        """Choose a key to evict from the cache.
        
        Called when the cache is at capacity and needs to remove an item.
        The policy should choose a key based on its replacement strategy.

        Returns:
            The key to evict from the cache
        """
        ...

    def remove_key(self, key: str) -> None:
        """Remove a key from the policy's tracking.
        
        Called when a key is explicitly deleted or expires.
        The policy should update its internal state accordingly.

        Args:
            key: The key being removed
        """
        ...

    def clear(self) -> None:
        """Clear all policy state.
        
        Called when the cache is cleared or reset.
        """
        ... 