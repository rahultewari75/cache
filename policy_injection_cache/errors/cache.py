from .base import CacheError

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

class InvalidPolicyError(CacheError):
    """Raised when an invalid or incompatible policy is provided."""
    def __init__(self, message: str):
        super().__init__(f"Invalid policy: {message}") 