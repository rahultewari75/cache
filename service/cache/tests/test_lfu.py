import unittest
import time
from service.cache.lfu import LFUCache

class TestLFUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LFUCache(capacity=3)
    
    def test_basic_operations(self):
        """Test basic cache operations"""
        # Set and get
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertIsNone(self.cache.get("nonexistent"))
        
        # Update existing
        self.cache.set("key1", "new_value1")
        self.assertEqual(self.cache.get("key1"), "new_value1")
    
    def test_capacity_limit(self):
        """Test cache capacity enforcement"""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        self.cache.set("key4", "value4")  # Should evict least frequently used
        
        # Since all keys were accessed once, key1 should be evicted (LRU among equal frequencies)
        self.assertIsNone(self.cache.get("key1"))
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")
    
    def test_lfu_eviction(self):
        """Test LFU eviction policy"""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # Increase frequency of key1 and key2
        self.cache.get("key1")  # frequency 2
        self.cache.get("key1")  # frequency 3
        self.cache.get("key2")  # frequency 2
        
        # Add new key, should evict key3 (lowest frequency)
        self.cache.set("key4", "value4")
        
        self.assertIsNone(self.cache.get("key3"))  # Evicted (frequency was 1)
        self.assertEqual(self.cache.get("key1"), "value1")  # Frequency 3
        self.assertEqual(self.cache.get("key2"), "value2")  # Frequency 2
        self.assertEqual(self.cache.get("key4"), "value4")  # Frequency 1
    
    def test_ttl_operations(self):
        """Test TTL functionality"""
        # Set with TTL
        self.cache.set("key1", "value1", ttl=1)  # 1 second TTL
        self.cache.set("key2", "value2")  # No TTL
        
        # Immediate access
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        
        # Wait for TTL to expire
        time.sleep(1.1)
        
        self.assertIsNone(self.cache.get("key1"))  # Expired
        self.assertEqual(self.cache.get("key2"), "value2")  # Still valid
    
    def test_ttl_query(self):
        """Test TTL query functionality"""
        # Set with different TTLs
        self.cache.set("key1", "value1", ttl=2)
        self.cache.set("key2", "value2")  # No TTL
        
        # Check TTLs
        self.assertIsNotNone(self.cache.ttl("key1"))
        self.assertIsNone(self.cache.ttl("key2"))  # No TTL
        self.assertIsNone(self.cache.ttl("nonexistent"))
        
        # Wait and check again
        time.sleep(2.1)
        self.assertIsNone(self.cache.ttl("key1"))  # Expired
    
    def test_expire_command(self):
        """Test explicit expire command"""
        self.cache.set("key1", "value1")
        current_time = time.time()
        
        # Set expiration
        self.cache.expire("key1", current_time + 1)
        self.assertEqual(self.cache.get("key1"), "value1")
        
        # Wait for expiration
        time.sleep(1.1)
        self.assertIsNone(self.cache.get("key1"))
    
    def test_scan_operation(self):
        """Test scan operation"""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2", ttl=1)
        self.cache.set("key3", "value3")
        
        # Initial scan
        keys = self.cache.scan()
        self.assertEqual(len(keys), 3)
        self.assertIn("key1", keys)
        self.assertIn("key2", keys)
        self.assertIn("key3", keys)
        
        # Wait for key2 to expire
        time.sleep(1.1)
        
        # Scan after expiration
        keys = self.cache.scan()
        self.assertEqual(len(keys), 2)
        self.assertIn("key1", keys)
        self.assertIn("key3", keys)
        self.assertNotIn("key2", keys)
    
    def test_frequency_tracking(self):
        """Test frequency tracking and eviction based on frequency"""
        # Add items
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # Access key1 multiple times
        for _ in range(3):
            self.cache.get("key1")
        
        # Access key2 twice
        for _ in range(2):
            self.cache.get("key2")
        
        # Add new item, should evict key3 (lowest frequency)
        self.cache.set("key4", "value4")
        
        self.assertEqual(self.cache.get("key1"), "value1")  # Frequency 4
        self.assertEqual(self.cache.get("key2"), "value2")  # Frequency 3
        self.assertEqual(self.cache.get("key4"), "value4")  # Frequency 1
        self.assertIsNone(self.cache.get("key3"))  # Evicted (had frequency 1)
    
    def test_reconfigure_capacity(self):
        """Test capacity reconfiguration"""
        self.cache.set("key1", "value1")
        self.cache.get("key1")  # Frequency 2
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # Reduce capacity
        self.cache.configure(2)
        
        # Should keep key1 (higher frequency) and most recently used among frequency 1
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertIsNone(self.cache.get("key2"))  # Evicted
        
        # Increase capacity
        self.cache.configure(4)
        self.cache.set("key4", "value4")
        keys = self.cache.scan()
        self.assertEqual(len(keys), 3)
    
    def test_different_value_types(self):
        """Test handling of different value types"""
        test_values = {
            "string": "test",
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "list": [1, 2, 3],
            "dict": {"key": "value"},
            "bytes": b"binary data"
        }
        
        for key, value in test_values.items():
            self.cache.set(key, value)
            self.assertEqual(self.cache.get(key), value)

if __name__ == '__main__':
    unittest.main() 