import time
import pytest
from service.queue.queue import Queue
from service.queue.error import QueueNotFoundError, QueueEmptyError

@pytest.fixture
def queue():
    return Queue()

def test_set_queue(queue):
    queue.set("test_queue")
    assert queue.get("test_queue") == []

def test_enqueue_dequeue(queue):
    queue.set("test_queue")
    
    # Test enqueue
    assert queue.enqueue("test_queue", "item1") == 1
    assert queue.enqueue("test_queue", "item2") == 2
    assert queue.get("test_queue") == ["item1", "item2"]
    
    # Test dequeue
    assert queue.dequeue("test_queue") == "item1"
    assert queue.dequeue("test_queue") == "item2"
    assert queue.dequeue("test_queue") is None

def test_queue_size(queue):
    queue.set("test_queue")
    assert queue.size("test_queue") == 0
    
    queue.enqueue("test_queue", "item1")
    assert queue.size("test_queue") == 1
    
    queue.enqueue("test_queue", "item2")
    assert queue.size("test_queue") == 2
    
    queue.dequeue("test_queue")
    assert queue.size("test_queue") == 1

def test_queue_ttl(queue):
    # Set queue with 1 second TTL
    queue.set("test_queue", ttl=1)
    queue.enqueue("test_queue", "item1")
    
    # Should be accessible immediately
    assert queue.get("test_queue") == ["item1"]
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Should return None after expiration
    assert queue.get("test_queue") is None
    assert queue.size("test_queue") is None
    assert queue.dequeue("test_queue") is None

def test_queue_expire(queue):
    queue.set("test_queue")
    queue.enqueue("test_queue", "item1")
    
    # Set expiration to 1 second from now
    future = time.time() + 1
    queue.expire("test_queue", future)
    
    # Should be accessible before expiration
    assert queue.get("test_queue") == ["item1"]
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Should return None after expiration
    assert queue.get("test_queue") is None

def test_queue_scan(queue):
    # Create multiple queues
    queue.set("queue1")
    queue.set("queue2", ttl=1)
    queue.set("queue3")
    
    # Initial scan should show all queues
    assert sorted(queue.scan()) == ["queue1", "queue2", "queue3"]
    
    # Wait for queue2 to expire
    time.sleep(1.1)
    
    # Scan should only show non-expired queues
    assert sorted(queue.scan()) == ["queue1", "queue3"]

def test_nonexistent_queue(queue):
    assert queue.get("nonexistent") is None
    assert queue.size("nonexistent") is None
    assert queue.dequeue("nonexistent") is None
    assert queue.enqueue("nonexistent", "item") is None
    assert queue.ttl("nonexistent") is None 