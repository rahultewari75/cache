from collections import defaultdict
from typing import Optional, List, Dict, Union
from data_types.entry import Entry
from util.ordered_dict import OrderedDict

class LFUCache:
    """
    Least Frequently Used (LFU) cache implementation
    """
    
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self._size = 0
        self._values: Dict[str, Entry] = {}
        self._frequencies: Dict[str, int] = defaultdict(int)
        self._freq_groups: Dict[int, OrderedDict] = defaultdict(OrderedDict)
        self._min_freq = 0
    
    def configure(self, capacity: int):
        """Configure cache capacity"""
        self.capacity = capacity
        while self._size > self.capacity:
            self._evict_lfu()
    
    def set(self, key: str, value: Union[str, int, float, bool, dict, list, bytes], ttl: Optional[int] = None):
        """Set a key-value pair with optional TTL"""
            
        if key in self._values:
            self._values[key].update_value(value, ttl)
            self._increment_freq(key)
        else:
            if self._size >= self.capacity:
                self._evict_lfu()
            
            entry = Entry(value, ttl)
            self._values[key] = entry
            self._frequencies[key] = 1
            self._freq_groups[1][key] = entry
            self._size += 1
            
            if self._min_freq == 0 or self._min_freq > 1:
                self._min_freq = 1
    
    def get(self, key: str) -> Optional[Union[str, int, float, bool, dict, list, bytes]]:
        """Get value by key, returns None if not found or expired"""
        if self._is_expired(key):
            return None
        
        if key not in self._values:
            return None
        
        self._increment_freq(key)
        return self._values[key].get_value()
    
    def ttl(self, key: str) -> Optional[int]:
        """Get TTL for a key in seconds, returns None if key doesn't exist or no expiration"""
        if self._is_expired(key):
            return None
        
        if key not in self._values:
            return None
        
        return self._values[key].get_ttl()
    
    def expire(self, key: str, timestamp: float):
        """Set expiration timestamp for a key"""
        if key in self._values:
            self._values[key].set_expiration(timestamp)
    
    def scan(self) -> List[str]:
        """Get all non-expired keys"""
        self._cleanup_expired()
        return list(self._values.keys())
    
    def _increment_freq(self, key: str):
        old_freq = self._frequencies[key]
        new_freq = old_freq + 1
        
        entry = self._values[key]
        del self._freq_groups[old_freq][key]
        if old_freq == self._min_freq and not self._freq_groups[old_freq]:
            self._min_freq += 1
        
        self._freq_groups[new_freq][key] = entry
        self._frequencies[key] = new_freq
    
    def _evict_lfu(self):
        if not self._freq_groups[self._min_freq]:
            return
        
        lfu_key = next(iter(self._freq_groups[self._min_freq]))
        del self._freq_groups[self._min_freq][lfu_key]
        del self._values[lfu_key]
        del self._frequencies[lfu_key]
        self._size -= 1
    
    def _is_expired(self, key: str) -> bool:
        if key not in self._values:
            return True
        
        if self._values[key].is_expired():
            self._remove_expired(key)
            return True
        return False
    
    def _remove_expired(self, key: str):
        if key in self._values:
            freq = self._frequencies[key]
            del self._freq_groups[freq][key]
            del self._values[key]
            del self._frequencies[key]
            self._size -= 1
    
    def _cleanup_expired(self):
        expired_keys = [k for k, v in self._values.items() if v.is_expired()]
        for key in expired_keys:
            self._remove_expired(key) 