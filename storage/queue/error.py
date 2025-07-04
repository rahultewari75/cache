from storage.error import StorageError

class QueueError(StorageError):
    """Base exception class for queue-related errors."""
    pass

class QueueNotFoundError(QueueError):
    """Raised when attempting to access a non-existent queue."""
    def __init__(self, queue_key: str):
        self.queue_key = queue_key
        super().__init__(f"Queue '{queue_key}' not found")

