import unittest
import time
import pytest
from storage.cache.random import RandomCache
from storage.cache.error import KeyNotFoundError, KeyExpiredError
from storage.error import InvalidInputError

class TestRandomCache(unittest.TestCase):
    def setUp(self):
        self.cache = RandomCache(capacity=3)
    
    def test_basic_operations(self):
        """Test basic cache operations"""
        # Set and get
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        
        # Test invalid key type
        with self.assertRaises(InvalidInputError):
            self.cache.get(123)
            
        # Test nonexistent key
        with self.assertRaises(KeyNotFoundError):
            self.cache.get("nonexistent")
        
        # Update existing
        self.cache.set("key1", "new_value1")
        self.assertEqual(self.cache.get("key1"), "new_value1")
    
    def test_capacity_limit(self):
        """Test cache capacity enforcement"""
        # Test invalid capacity
        with self.assertRaises(InvalidInputError):
            RandomCache(capacity=0)
        with self.assertRaises(InvalidInputError):
            RandomCache(capacity=-1)
            
        # Fill cache
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # Adding one more should evict one random key
        self.cache.set("key4", "value4")
        
        # Verify we still have exactly 3 items
        self.assertEqual(len(self.cache.scan()), 3)
        
        # Verify the values we can still access are correct
        remaining_keys = self.cache.scan()
        for key in remaining_keys:
            if key == "key1":
                self.assertEqual(self.cache.get(key), "value1")
            elif key == "key2":
                self.assertEqual(self.cache.get(key), "value2")
            elif key == "key3":
                self.assertEqual(self.cache.get(key), "value3")
            elif key == "key4":
                self.assertEqual(self.cache.get(key), "value4")
    
    def test_random_eviction_distribution(self):
        """Test that eviction appears random"""
        eviction_counts = {"key1": 0, "key2": 0, "key3": 0}
        trials = 1000
        
        for _ in range(trials):
            cache = RandomCache(capacity=3)
            cache.set("key1", "value1")
            cache.set("key2", "value2")
            cache.set("key3", "value3")
            cache.set("key4", "value4")  # This will trigger eviction
            
            # Count which key was evicted
            for key in ["key1", "key2", "key3"]:
                try:
                    cache.get(key)
                except KeyNotFoundError:
                    eviction_counts[key] += 1
        
        # Check that each key was evicted at least once
        for count in eviction_counts.values():
            self.assertGreater(count, 0)
        
        # Check that no key was evicted more than 50% of the time
        # (allowing for some random variation)
        for count in eviction_counts.values():
            self.assertLess(count, trials * 0.5)
            
        # Check individual proportions (each key should be evicted ~33% of the time)
        for key, count in eviction_counts.items():
            proportion = count / trials
            self.assertGreater(proportion, 0.28,  # Allow 5% deviation from expected 33%
                f"{key} was evicted too rarely: {proportion:.2%}")
            self.assertLess(proportion, 0.38,
                f"{key} was evicted too often: {proportion:.2%}")
        
        # Test for sequential bias
        sequential_evictions = []
        for _ in range(200):  # Increased to 200 trials for better sampling
            cache = RandomCache(capacity=3)
            cache.set("key1", "value1")
            cache.set("key2", "value2")
            cache.set("key3", "value3")
            
            # Record which key was evicted
            pre_eviction = set(["key1", "key2", "key3"])
            cache.set("key4", "value4")
            post_eviction = set(cache.scan())
            evicted = (pre_eviction - post_eviction).pop()
            sequential_evictions.append(evicted)
        
        # Test for sequential patterns - no key should be evicted more than 4 times in a row
        max_run_length = 1
        current_run = 1
        for i in range(1, len(sequential_evictions)):
            if sequential_evictions[i] == sequential_evictions[i-1]:
                current_run += 1
                max_run_length = max(max_run_length, current_run)
            else:
                current_run = 1
        
        self.assertLess(max_run_length, 6,
            f"Found suspicious run of {max_run_length} sequential evictions")
    
    def test_ttl_operations(self):
        """Test TTL functionality"""
        # Test invalid TTL
        with self.assertRaises(InvalidInputError):
            self.cache.set("key1", "value1", ttl=-1)
            
        # Set with TTL
        self.cache.set("key1", "value1", ttl=1)  # 1 second TTL
        self.cache.set("key2", "value2")  # No TTL
        
        # Immediate access
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        
        # Wait for TTL to expire
        time.sleep(1.1)
        
        # Should raise KeyExpiredError after expiration
        with self.assertRaises(KeyExpiredError):
            self.cache.get("key1")
        self.assertEqual(self.cache.get("key2"), "value2")  # Still valid
    
    def test_ttl_query(self):
        """Test TTL query functionality"""
        # Set with different TTLs
        self.cache.set("key1", "value1", ttl=2)
        self.cache.set("key2", "value2")  # No TTL
        
        # Check TTLs
        self.assertIsNotNone(self.cache.ttl("key1"))
        self.assertIsNone(self.cache.ttl("key2"))  # No TTL
        
        # Test invalid key type
        with self.assertRaises(InvalidInputError):
            self.cache.ttl(123)
            
        # Test nonexistent key
        with self.assertRaises(KeyNotFoundError):
            self.cache.ttl("nonexistent")
        
        # Wait and check again
        time.sleep(2.1)
        with self.assertRaises(KeyExpiredError):
            self.cache.ttl("key1")  # Expired
    
    def test_expire_command(self):
        """Test explicit expire command"""
        self.cache.set("key1", "value1")
        current_time = time.time()
        
        # Test invalid inputs
        with self.assertRaises(InvalidInputError):
            self.cache.expire(123, current_time + 1)
        with self.assertRaises(InvalidInputError):
            self.cache.expire("key1", -1)
        with self.assertRaises(KeyNotFoundError):
            self.cache.expire("nonexistent", current_time + 1)
        
        # Set expiration
        self.cache.expire("key1", current_time + 1)
        self.assertEqual(self.cache.get("key1"), "value1")
        
        # Wait for expiration
        time.sleep(1.1)
        with self.assertRaises(KeyExpiredError):
            self.cache.get("key1")
    
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
    
    def test_reconfigure_capacity(self):
        """Test capacity reconfiguration"""
        # Test invalid capacity
        with self.assertRaises(InvalidInputError):
            self.cache.configure(0)
        with self.assertRaises(InvalidInputError):
            self.cache.configure(-1)
            
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        # Reduce capacity to 2
        self.cache.configure(2)
        
        # Should have exactly 2 items now
        self.assertEqual(len(self.cache.scan()), 2)
        
        # Increase capacity
        self.cache.configure(4)
        self.cache.set("key4", "value4")
        self.assertEqual(len(self.cache.scan()), 3)  # Can store more items now
    
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