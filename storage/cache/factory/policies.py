from enum import Enum

class CachePolicy(str, Enum):
    LRU = "LRU"
    LFU = "LFU"
    RANDOM = "RANDOM"