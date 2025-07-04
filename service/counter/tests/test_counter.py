import unittest
import time
from service.counter.counter import Counter

class TestCounter(unittest.TestCase):
    def setUp(self):
        self.counter = Counter()
    
    def test_basic_operations(self):
        """Test basic counter operations"""
        # Set and get
        self.counter.set("counter1")
        self.counter.set("counter2")
        
        self.assertEqual(self.counter.get("counter1"), 0)
        self.assertEqual(self.counter.get("counter2"), 0)
        self.assertIsNone(self.counter.get("nonexistent"))
        
        # Increment and decrement
        self.assertEqual(self.counter.increment("counter1"), 1)
        self.assertEqual(self.counter.increment("counter1"), 2)
        self.assertEqual(self.counter.decrement("counter1"), 1)
        self.assertEqual(self.counter.get("counter1"), 1)
    
    def test_ttl_operations(self):
        """Test TTL functionality"""
        # Set with TTL
        self.counter.set("counter1", ttl=1)  # 1 second TTL
        self.counter.set("counter2")  # No TTL
        
        # Immediate access
        self.assertEqual(self.counter.get("counter1"), 0)
        self.assertEqual(self.counter.get("counter2"), 0)
        
        # Wait for TTL to expire
        time.sleep(1.1)
        
        self.assertIsNone(self.counter.get("counter1"))  # Expired
        self.assertEqual(self.counter.get("counter2"), 0)  # Still valid
    
    def test_ttl_query(self):
        """Test TTL query functionality"""
        # Set with different TTLs
        self.counter.set("counter1", ttl=2)
        self.counter.set("counter2")  # No TTL
        
        # Check TTLs
        self.assertIsNotNone(self.counter.ttl("counter1"))
        self.assertIsNone(self.counter.ttl("counter2"))  # No TTL
        self.assertIsNone(self.counter.ttl("nonexistent"))
        
        # Wait and check again
        time.sleep(2.1)
        self.assertIsNone(self.counter.ttl("counter1"))  # Expired
    
    def test_expire_command(self):
        """Test explicit expire command"""
        self.counter.set("counter1")
        current_time = time.time()
        
        # Set expiration
        self.counter.expire("counter1", current_time + 1)
        self.assertEqual(self.counter.get("counter1"), 0)
        
        # Wait for expiration
        time.sleep(1.1)
        self.assertIsNone(self.counter.get("counter1"))
    
    def test_scan_operation(self):
        """Test scan operation"""
        self.counter.set("counter1")
        self.counter.set("counter2", ttl=1)
        self.counter.set("counter3")
        
        # Initial scan
        keys = self.counter.scan()
        self.assertEqual(len(keys), 3)
        self.assertIn("counter1", keys)
        self.assertIn("counter2", keys)
        self.assertIn("counter3", keys)
        
        # Wait for counter2 to expire
        time.sleep(1.1)
        
        # Scan after expiration
        keys = self.counter.scan()
        self.assertEqual(len(keys), 2)
        self.assertIn("counter1", keys)
        self.assertIn("counter3", keys)
        self.assertNotIn("counter2", keys)
    
    def test_counter_operations(self):
        """Test counter increment/decrement operations"""
        self.counter.set("counter1")
        
        # Test increment
        self.assertEqual(self.counter.increment("counter1"), 1)
        self.assertEqual(self.counter.increment("counter1"), 2)
        self.assertEqual(self.counter.get("counter1"), 2)
        
        # Test decrement
        self.assertEqual(self.counter.decrement("counter1"), 1)
        self.assertEqual(self.counter.decrement("counter1"), 0)
        self.assertEqual(self.counter.get("counter1"), 0)
        
        # Test operations on nonexistent counter
        self.assertIsNone(self.counter.increment("nonexistent"))
        self.assertIsNone(self.counter.decrement("nonexistent"))
    
    def test_ttl_with_operations(self):
        """Test TTL behavior with counter operations"""
        self.counter.set("counter1", ttl=2)
        
        # Operations before expiry
        self.assertEqual(self.counter.increment("counter1"), 1)
        self.assertEqual(self.counter.increment("counter1"), 2)
        self.assertEqual(self.counter.get("counter1"), 2)
        
        # Wait for expiration
        time.sleep(2.1)
        
        # Operations after expiry
        self.assertIsNone(self.counter.increment("counter1"))
        self.assertIsNone(self.counter.decrement("counter1"))
        self.assertIsNone(self.counter.get("counter1"))
    
    def test_multiple_counters(self):
        """Test operations with multiple counters"""
        self.counter.set("counter1")
        self.counter.set("counter2")
        self.counter.set("counter3", ttl=1)
        
        # Different operations on different counters
        self.assertEqual(self.counter.increment("counter1"), 1)
        self.assertEqual(self.counter.increment("counter1"), 2)
        self.assertEqual(self.counter.increment("counter2"), 1)
        self.assertEqual(self.counter.decrement("counter1"), 1)
        
        # Wait for counter3 to expire
        time.sleep(1.1)
        
        self.assertEqual(self.counter.get("counter1"), 1)
        self.assertEqual(self.counter.get("counter2"), 1)
        self.assertIsNone(self.counter.get("counter3"))

if __name__ == '__main__':
    unittest.main()
