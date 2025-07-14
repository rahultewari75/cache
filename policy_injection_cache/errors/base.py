class CacheError(Exception):
    """Base exception class for all cache-related errors."""
    pass

class InvalidInputError(CacheError):
    """Raised when an invalid input is provided."""
    def __init__(self, message: str):
        super().__init__(message) 