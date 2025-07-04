from storage.cache import LRUCache, LFUCache
from storage.cache.factory.policies import CachePolicy
from typing import Union
from storage.cache.factory.error import InvalidCachePolicyError
from storage.factory_base.factory_base import FactoryBase

class CacheFactory(FactoryBase):
    def __init__(self):
        super().__init__()

    def create_instance(self, policy: CachePolicy, capacity: int) -> Union[LRUCache, LFUCache]:
        if policy == CachePolicy.LRU:
            self.instance = LRUCache(capacity)
        elif policy == CachePolicy.LFU:
            self.instance = LFUCache(capacity)
        else:
            raise InvalidCachePolicyError(policy)
