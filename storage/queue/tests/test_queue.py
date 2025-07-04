import unittest
import time
from storage.queue.queue import Queue
from storage.queue.error import QueueNotFoundError
from storage.error import InvalidInputError

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()
    
    def test_basic_operations(self):
        """Test basic queue operations"""
        # Set and get
        self.queue.set("test_queue")
        self.assertEqual(self.queue.get("test_queue"), [])
        
        # Test invalid inputs
        with self.assertRaises(InvalidInputError):
            self.queue.set(123)
        with self.assertRaises(InvalidInputError):
            self.queue.set("test", ttl=-1)

    def test_enqueue_dequeue(self):
        """Test enqueue and dequeue operations"""
        self.queue.set("test_queue")
        
        # Test enqueue
        self.assertEqual(self.queue.enqueue("test_queue", "item1"), 1)
        self.assertEqual(self.queue.enqueue("test_queue", "item2"), 2)
        self.assertEqual(self.queue.get("test_queue"), ["item1", "item2"])
        
        # Test dequeue
        self.assertEqual(self.queue.dequeue("test_queue"), "item1")
        self.assertEqual(self.queue.dequeue("test_queue"), "item2")
        with self.assertRaises(InvalidInputError):
            self.queue.dequeue("test_queue")
            
        # Test invalid inputs
        with self.assertRaises(InvalidInputError):
            self.queue.enqueue(123, "item")
        with self.assertRaises(InvalidInputError):
            self.queue.enqueue("test_queue", 123)
        with self.assertRaises(QueueNotFoundError):
            self.queue.enqueue("nonexistent", "item")

    def test_queue_size(self):
        """Test queue size operations"""
        self.queue.set("test_queue")
        self.assertEqual(self.queue.size("test_queue"), 0)
        
        self.queue.enqueue("test_queue", "item1")
        self.assertEqual(self.queue.size("test_queue"), 1)
        
        self.queue.enqueue("test_queue", "item2")
        self.assertEqual(self.queue.size("test_queue"), 2)
        
        self.queue.dequeue("test_queue")
        self.assertEqual(self.queue.size("test_queue"), 1)
        
        # Test invalid inputs
        with self.assertRaises(InvalidInputError):
            self.queue.size(123)
        with self.assertRaises(QueueNotFoundError):
            self.queue.size("nonexistent")

    def test_queue_ttl(self):
        """Test TTL functionality"""
        # Set queue with 1 second TTL
        self.queue.set("test_queue", ttl=1)
        self.queue.enqueue("test_queue", "item1")
        
        # Should be accessible immediately
        self.assertEqual(self.queue.get("test_queue"), ["item1"])
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Should raise QueueNotFoundError after expiration
        with self.assertRaises(QueueNotFoundError):
            self.queue.get("test_queue")
        with self.assertRaises(QueueNotFoundError):
            self.queue.size("test_queue")
        with self.assertRaises(QueueNotFoundError):
            self.queue.dequeue("test_queue")

    def test_queue_expire(self):
        """Test explicit expire command"""
        self.queue.set("test_queue")
        self.queue.enqueue("test_queue", "item1")
        
        # Test invalid inputs
        with self.assertRaises(InvalidInputError):
            self.queue.expire(123, time.time() + 1)
        with self.assertRaises(InvalidInputError):
            self.queue.expire("test_queue", -1)
        with self.assertRaises(QueueNotFoundError):
            self.queue.expire("nonexistent", time.time() + 1)
        
        # Set expiration to 1 second from now
        future = time.time() + 1
        self.queue.expire("test_queue", future)
        
        # Should be accessible before expiration
        self.assertEqual(self.queue.get("test_queue"), ["item1"])
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Should raise QueueNotFoundError after expiration
        with self.assertRaises(QueueNotFoundError):
            self.queue.get("test_queue")

    def test_queue_scan(self):
        """Test scan operation"""
        # Create multiple queues
        self.queue.set("queue1")
        self.queue.set("queue2", ttl=1)
        self.queue.set("queue3")
        
        # Initial scan should show all queues
        self.assertEqual(sorted(self.queue.scan()), ["queue1", "queue2", "queue3"])
        
        # Wait for queue2 to expire
        time.sleep(1.1)
        
        # Scan should only show non-expired queues
        self.assertEqual(sorted(self.queue.scan()), ["queue1", "queue3"])

    def test_nonexistent_queue(self):
        """Test operations on nonexistent queues"""
        with self.assertRaises(QueueNotFoundError):
            self.queue.get("nonexistent")
        with self.assertRaises(QueueNotFoundError):
            self.queue.size("nonexistent")
        with self.assertRaises(QueueNotFoundError):
            self.queue.dequeue("nonexistent")
        with self.assertRaises(QueueNotFoundError):
            self.queue.enqueue("nonexistent", "item")
        with self.assertRaises(QueueNotFoundError):
            self.queue.ttl("nonexistent")

if __name__ == '__main__':
    unittest.main() 