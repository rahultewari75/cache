class QueueError(Exception):
    """Base exception class for queue-related errors."""
    pass

class QueueNotFoundError(QueueError):
    """Raised when attempting to access a non-existent queue."""
    def __init__(self, queue_key: str):
        self.queue_key = queue_key
        super().__init__(f"Queue '{queue_key}' not found")

class QueueCapacityError(QueueError):
    """Raised when queue capacity is exceeded."""
    def __init__(self, message: str):
        super().__init__(message)

class QueueEmptyError(QueueError):
    """Raised when attempting to dequeue from an empty queue."""
    def __init__(self, queue_key: str):
        self.queue_key = queue_key
        super().__init__(f"Queue '{queue_key}' is empty")
