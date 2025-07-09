from storage.cache import LRUCache, LFUCache, RandomCache
from storage.cache.factory.policies import CachePolicy
from typing import Union
from storage.cache.factory.error import InvalidCachePolicyError
from storage.factory_base.factory_base import FactoryBase

class CacheFactory(FactoryBase):
    def __init__(self):
        super().__init__()

    def create_instance(self, policy: CachePolicy, capacity: int) -> Union[LRUCache, LFUCache, RandomCache]:
        if policy == CachePolicy.LRU:
            self.instance = LRUCache(capacity)
        elif policy == CachePolicy.LFU:
            self.instance = LFUCache(capacity)
        elif policy == CachePolicy.RANDOM:
            self.instance = RandomCache(capacity)
        else:
            raise InvalidCachePolicyError(policy)
        return self.instance
