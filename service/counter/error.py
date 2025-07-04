class CounterError(Exception):
    """Base exception class for counter-related errors."""
    pass

class CounterNotFoundError(CounterError):
    """Raised when attempting to access a non-existent counter."""
    def __init__(self, counter_key: str):
        self.counter_key = counter_key
        super().__init__(f"Counter '{counter_key}' not found")

class CounterCapacityError(CounterError):
    """Raised when counter capacity is exceeded."""
    def __init__(self, message: str):
        super().__init__(message)

class CounterOverflowError(CounterError):
    """Raised when counter value exceeds maximum value."""
    def __init__(self, counter_key: str, value: int):
        self.counter_key = counter_key
        self.value = value
        super().__init__(f"Counter '{counter_key}' overflow: {value}")

class CounterUnderflowError(CounterError):
    """Raised when counter value goes below zero."""
    def __init__(self, counter_key: str):
        self.counter_key = counter_key
        super().__init__(f"Counter '{counter_key}' cannot go below zero")
