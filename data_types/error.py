class CacheError(Exception):
    """Base exception class for cache-related errors."""
    pass

class KeyNotFoundError(CacheError):
    """Raised when attempting to access a non-existent key in the cache."""
    def __init__(self, key: str):
        self.key = key
        super().__init__(f"Key '{key}' not found in cache")

class KeyExpiredError(CacheError):
    """Raised when attempting to access a key that has expired."""
    def __init__(self, key: str, expiry_time: float):
        self.key = key
        self.expiry_time = expiry_time
        super().__init__(f"Key '{key}' has expired at timestamp {expiry_time}")

class CacheCapacityError(CacheError):
    """Raised when cache capacity is exceeded or invalid capacity is provided."""
    def __init__(self, message: str):
        super().__init__(message)

class InvalidKeyError(CacheError):
    """Raised when an invalid key type is provided."""
    def __init__(self, key):
        self.key = key
        super().__init__(f"Invalid key type: {type(key)}. Keys must be strings.")

class InvalidValueError(CacheError):
    """Raised when an invalid value type is provided."""
    def __init__(self, value):
        self.value = value
        super().__init__(f"Invalid value type: {type(value)}. Values must be JSON serializable.")

class InvalidCachePolicyError(CacheError):
    """Raised when an invalid cache policy is specified."""
    def __init__(self, policy: str):
        self.policy = policy
        super().__init__(f"Invalid cache policy: {policy}. Supported policies are 'LRU' and 'LFU'.")

class InvalidTTLError(CacheError):
    """Raised when an invalid TTL value is provided."""
    def __init__(self, ttl):
        self.ttl = ttl
        super().__init__(f"Invalid TTL value: {ttl}. TTL must be a positive integer or timestamp in the future.")
