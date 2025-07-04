class ServiceError(Exception):
    """Base exception class for service-related errors."""
    pass

class ClientError(ServiceError):
    """Raised when a client error occurs."""
    pass

class InvalidInputError(ClientError):
    """Raised when an invalid input is provided."""
    def __init__(self, message: str):
        super().__init__(message)

class KeyNotFoundError(ClientError):
    """Raised when a key is not found."""
    def __init__(self, key: str):
        self.key = key
        super().__init__(f"Key '{key}' not found")

class KeyExpiredError(ClientError):
    """Raised when a key is expired."""
    def __init__(self, key: str):
        self.key = key
        super().__init__(f"Key '{key}' expired")

class CacheAlreadyConfiguredError(ClientError):
    """Raised when cache is already configured."""
    def __init__(self):
        super().__init__("Cache already configured")
