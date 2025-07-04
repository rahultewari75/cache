from storage.error import StorageError

class CounterError(StorageError):
    """Base exception class for counter-related errors."""
    pass

class CounterNotFoundError(CounterError):
    """Raised when attempting to access a non-existent counter."""
    def __init__(self, counter_key: str):
        self.counter_key = counter_key
        super().__init__(f"Counter '{counter_key}' not found")
