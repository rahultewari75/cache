class StorageError(Exception):
    """Base exception class for storage-related errors."""
    pass

class InvalidInputError(StorageError):
    """Raised when an invalid input is provided."""
    def __init__(self, message: str):
        super().__init__(message)