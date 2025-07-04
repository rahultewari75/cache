class CacheFactoryError(Exception):
    """Base exception class for cache factory-related errors."""
    pass

class InvalidCachePolicyError(CacheFactoryError):
    """Raised when an invalid cache policy is provided."""
    def __init__(self, policy: str):
        self.policy = policy
        super().__init__(f"Invalid cache policy: {policy}")