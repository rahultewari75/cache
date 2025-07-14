import unittest
import time
from server.server import (
    configure_cache, set_cache, get_cache, get_cache_ttl, set_cache_expiration, scan_cache,
    configure_counter, set_counter, get_counter, increment_counter, decrement_counter,
    configure_queue, set_queue, get_queue, enqueue, dequeue
)
from server.base import reset_all
from storage.cache.factory.policies import CachePolicy
from server.error import KeyNotFoundError, KeyExpiredError

class TestServer(unittest.TestCase):
    def setUp(self):
        """Reset all singletons before each test"""
        reset_all()

    def test_lru_cache_happy_path(self):
        """Test LRU cache end-to-end happy path"""
        configure_cache(CachePolicy.LRU, capacity=3)
        
        set_cache("key1", "value1", ttl=2)
        set_cache("key2", "value2")
        
        self.assertEqual(get_cache("key1"), "value1")
        self.assertEqual(get_cache("key2"), "value2")
        
        self.assertIsNotNone(get_cache_ttl("key1"))
        self.assertIsNone(get_cache_ttl("key2"))
        
        time.sleep(2.1)
        
        with self.assertRaises(KeyExpiredError):
            get_cache("key1")
        self.assertEqual(get_cache("key2"), "value2")
        
        set_cache("key3", "value3")
        set_cache_expiration("key3", time.time() + 1)
        self.assertEqual(get_cache("key3"), "value3")
        
        time.sleep(1.1)
        with self.assertRaises(KeyExpiredError):
            get_cache("key3")
    
    def test_lfu_cache_happy_path(self):
        """Test LFU cache end-to-end happy path"""
        configure_cache(CachePolicy.LFU, capacity=3)
        
        set_cache("key1", "value1")
        set_cache("key2", "value2")
        set_cache("key3", "value3")
        
        get_cache("key1")
        get_cache("key1")
        get_cache("key1")
        
        get_cache("key2")
        get_cache("key2")
        
        set_cache("key4", "value4")
        
        with self.assertRaises(KeyNotFoundError):
            get_cache("key3")
        
        self.assertEqual(get_cache("key1"), "value1")
        self.assertEqual(get_cache("key2"), "value2")
        self.assertEqual(get_cache("key4"), "value4")
    
    def test_random_cache_happy_path(self):
        """Test random cache end-to-end happy path"""
        configure_cache(CachePolicy.RANDOM, capacity=3)
        
        # Set initial values
        set_cache("key1", "value1")
        set_cache("key2", "value2")
        set_cache("key3", "value3")
        
        # Verify initial values
        self.assertEqual(get_cache("key1"), "value1")
        self.assertEqual(get_cache("key2"), "value2")
        self.assertEqual(get_cache("key3"), "value3")
        
        # Add new value to trigger eviction
        set_cache("key4", "value4")
        
        # Verify we still have exactly 3 items
        keys = scan_cache()
        self.assertEqual(len(keys), 3)
        
        # Verify the values we can still access are correct
        for key in keys:
            if key == "key1":
                self.assertEqual(get_cache(key), "value1")
            elif key == "key2":
                self.assertEqual(get_cache(key), "value2")
            elif key == "key3":
                self.assertEqual(get_cache(key), "value3")
            elif key == "key4":
                self.assertEqual(get_cache(key), "value4")
        
        # Test TTL functionality
        set_cache("key5", "value5", ttl=1)
        self.assertEqual(get_cache("key5"), "value5")
        
        time.sleep(1.1)
        with self.assertRaises(KeyExpiredError):
            get_cache("key5")
    
    def test_counter_happy_path(self):
        """Test counter end-to-end happy path"""
        configure_counter()
        
        set_counter("counter1", ttl=2)
        set_counter("counter2")
        
        self.assertEqual(get_counter("counter1"), 0)
        self.assertEqual(get_counter("counter2"), 0)
        
        self.assertEqual(increment_counter("counter1"), 1)
        self.assertEqual(increment_counter("counter1"), 2)
        self.assertEqual(increment_counter("counter2"), 1)
        
        self.assertEqual(decrement_counter("counter1"), 1)
        
        time.sleep(2.1)
        
        with self.assertRaises(KeyNotFoundError):
            get_counter("counter1")
        
        self.assertEqual(get_counter("counter2"), 1)
    
    def test_queue_happy_path(self):
        """Test queue end-to-end happy path"""
        configure_queue()
        
        set_queue("queue1", ttl=2)
        set_queue("queue2")
        
        self.assertEqual(get_queue("queue1"), [])
        self.assertEqual(get_queue("queue2"), [])
        
        self.assertEqual(enqueue("queue1", "item1"), 1)
        self.assertEqual(enqueue("queue1", "item2"), 2)
        self.assertEqual(enqueue("queue2", "item3"), 1)
        
        self.assertEqual(get_queue("queue1"), ["item1", "item2"])
        self.assertEqual(get_queue("queue2"), ["item3"])
        
        self.assertEqual(dequeue("queue1"), "item1")
        self.assertEqual(dequeue("queue1"), "item2")
        
        time.sleep(2.1)
        
        with self.assertRaises(KeyNotFoundError):
            get_queue("queue1")
        
        self.assertEqual(get_queue("queue2"), ["item3"])

if __name__ == '__main__':
    unittest.main() 