from server.base import _cache_factory, _counter_factory, _queue_factory, with_instance
from server.error import CacheAlreadyConfiguredError, InvalidInputError, KeyNotFoundError, KeyExpiredError
from storage.error import InvalidInputError as StorageInvalidInputError
from storage.cache.error import KeyNotFoundError as StorageKeyNotFoundError, KeyExpiredError as StorageKeyExpiredError
from storage.cache.factory.error import InvalidCachePolicyError
from storage.counter.error import CounterNotFoundError
from storage.queue.error import QueueNotFoundError
from typing import Optional, List, Any
from storage.cache.cache import Cache
from storage.counter.counter import Counter
from storage.queue.queue import Queue

def ping():
    return "hello world"

# Cache operations
def configure_cache(policy: str, capacity: int):
    """Configure cache policy and capacity"""
    if _cache_factory.instance_exists():
        raise CacheAlreadyConfiguredError()
    
    try:
        _cache_factory.create_instance(policy, capacity)
    except InvalidCachePolicyError as e:
        raise InvalidInputError(str(e))

def reset_cache():
    """Reset cache"""
    _cache_factory.reset_instance()

@with_instance(_cache_factory)
def set_cache(cache: Cache, key: str, value: Any, ttl: Optional[int] = None):
    """Set a key-value pair in cache with optional TTL"""
    try:
        cache.set(key, value, ttl)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))

@with_instance(_cache_factory)
def get_cache(cache: Cache, key: str) -> Any:
    """Get value from cache by key"""
    try:
        return cache.get(key)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))
    except StorageKeyNotFoundError as e:
        raise KeyNotFoundError(e.key)
    except StorageKeyExpiredError as e:
        raise KeyExpiredError(e.key)

@with_instance(_cache_factory)
def get_cache_ttl(cache: Cache, key: str) -> Optional[int]:
    """Get TTL for a cache key"""
    try:
        return cache.ttl(key)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))
    except StorageKeyNotFoundError as e:
        raise KeyNotFoundError(e.key)
    except StorageKeyExpiredError as e:
        raise KeyExpiredError(e.key)

@with_instance(_cache_factory)
def set_cache_expiration(cache: Cache, key: str, timestamp: float):
    """Set expiration timestamp for a cache key"""
    try:
        cache.expire(key, timestamp)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))
    except StorageKeyNotFoundError as e:
        raise KeyNotFoundError(e.key)

@with_instance(_cache_factory)
def scan_cache(cache: Cache) -> List[str]:
    """Get all non-expired cache keys"""
    try:
        return cache.scan()
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))

# Counter operations
def configure_counter():
    """Configure counter"""
    if _counter_factory.instance_exists():
        raise InvalidInputError("Counter already configured")
    _counter_factory.create_instance()

@with_instance(_counter_factory)
def set_counter(counter: Counter, key: str, ttl: Optional[int] = None):
    """Create/reset a counter to 0 with optional TTL"""
    try:
        counter.set(key, ttl)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))

@with_instance(_counter_factory)
def get_counter(counter: Counter, key: str) -> int:
    """Get counter value"""
    try:
        return counter.get(key)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))
    except CounterNotFoundError as e:
        raise KeyNotFoundError(e.counter_key)

@with_instance(_counter_factory)
def increment_counter(counter: Counter, key: str) -> int:
    """Increment counter by 1, returns new value"""
    try:
        return counter.increment(key)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))
    except CounterNotFoundError as e:
        raise KeyNotFoundError(e.counter_key)

@with_instance(_counter_factory)
def decrement_counter(counter: Counter, key: str) -> int:
    """Decrement counter by 1, returns new value"""
    try:
        return counter.decrement(key)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))
    except CounterNotFoundError as e:
        raise KeyNotFoundError(e.counter_key)

# Queue operations
def configure_queue():
    """Configure queue"""
    if _queue_factory.instance_exists():
        raise InvalidInputError("Queue already configured")
    _queue_factory.create_instance()

@with_instance(_queue_factory)
def set_queue(queue: Queue, key: str, ttl: Optional[int] = None):
    """Create/reset a queue with optional TTL"""
    try:
        queue.set(key, ttl)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))

@with_instance(_queue_factory)
def get_queue(queue: Queue, key: str) -> List[str]:
    """Get queue contents"""
    try:
        return queue.get(key)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))
    except QueueNotFoundError as e:
        raise KeyNotFoundError(e.queue_key)

@with_instance(_queue_factory)
def enqueue(queue: Queue, key: str, value: str) -> int:
    """Add value to queue, returns new size"""
    try:
        return queue.enqueue(key, value)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))
    except QueueNotFoundError as e:
        raise KeyNotFoundError(e.queue_key)

@with_instance(_queue_factory)
def dequeue(queue: Queue, key: str) -> str:
    """Remove and return first value from queue"""
    try:
        return queue.dequeue(key)
    except StorageInvalidInputError as e:
        raise InvalidInputError(str(e))
    except QueueNotFoundError as e:
        raise KeyNotFoundError(e.queue_key)