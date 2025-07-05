from storage.cache.factory.cache_factory import CacheFactory
from storage.counter.factory.counter_factory import CounterFactory
from storage.queue.factory.queue_factory import QueueFactory
from storage.factory_base.factory_base import FactoryBase
from functools import wraps
from typing import Callable, TypeVar, Any
from server.error import InvalidInputError

T = TypeVar('T')

# Storage singletons
_cache_factory: CacheFactory = CacheFactory()
_counter_factory: CounterFactory = CounterFactory()
_queue_factory: QueueFactory = QueueFactory()

def with_instance(factory: FactoryBase):
    """Decorator factory that creates a decorator to pass instance from factory to function"""
    def decorator(f: Callable[..., T]) -> Callable[..., T]:
        @wraps(f)
        def wrapper(*args, **kwargs) -> T:
            if not factory.instance_exists():
                raise InvalidInputError("Service not configured. Call configure_service first.")
            instance = factory.get_instance()
            return f(instance, *args, **kwargs)
        return wrapper
    return decorator

def reset_all():
    """Reset all storage singletons to initial state"""
    global _cache_factory, _counter_factory, _queue_factory
    _cache_factory.reset_instance()
    _counter_factory.reset_instance()
    _queue_factory.reset_instance()
