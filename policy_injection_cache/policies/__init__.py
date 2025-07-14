"""Policy implementations for the cache."""
from .policy import ReplacementPolicy
from .lru import LRUPolicy
from .lfu import LFUPolicy
from .random import RandomPolicy

__all__ = [
    'ReplacementPolicy',
    'LRUPolicy',
    'LFUPolicy',
    'RandomPolicy'
]
