import unittest
from util.ordered_dict import OrderedDict
from data_types.entry import Entry

class TestOrderedDict(unittest.TestCase):
    def setUp(self):
        self.od = OrderedDict()
        self.entry1 = Entry("value1")
        self.entry2 = Entry("value2")
        self.entry3 = Entry("value3")
    
    def test_empty_dict(self):
        """Test empty dictionary properties"""
        self.assertEqual(len(self.od), 0)
        self.assertFalse(bool(self.od))
        self.assertFalse("key1" in self.od)
        with self.assertRaises(KeyError):
            _ = self.od["nonexistent"]
    
    def test_basic_operations(self):
        """Test basic dictionary operations"""
        # Set items
        self.od["key1"] = self.entry1
        self.od["key2"] = self.entry2
        
        # Length and contains
        self.assertEqual(len(self.od), 2)
        self.assertTrue(bool(self.od))
        self.assertTrue("key1" in self.od)
        self.assertTrue("key2" in self.od)
        
        # Get items
        self.assertEqual(self.od["key1"], self.entry1)
        self.assertEqual(self.od["key2"], self.entry2)
        
        # Get with default
        self.assertEqual(self.od.get("key1"), self.entry1)
        self.assertIsNone(self.od.get("nonexistent"))
        self.assertEqual(self.od.get("nonexistent", "default"), "default")
    
    def test_order_preservation(self):
        """Test that insertion order is preserved"""
        self.od["key1"] = self.entry1
        self.od["key2"] = self.entry2
        self.od["key3"] = self.entry3
        
        expected = ["key1", "key2", "key3"]
        self.assertEqual(list(self.od), expected)
        self.assertEqual(self.od.keys(), expected)
        self.assertEqual(self.od.values(), [self.entry1, self.entry2, self.entry3])
        self.assertEqual(self.od.items(), [("key1", self.entry1), ("key2", self.entry2), ("key3", self.entry3)])
    
    def test_update_existing(self):
        """Test updating existing keys"""
        self.od["key1"] = self.entry1
        self.od["key2"] = self.entry2
        
        # Update existing key
        new_entry = Entry("new_value")
        self.od["key1"] = new_entry
        
        self.assertEqual(self.od["key1"], new_entry)
        self.assertEqual(len(self.od), 2)
        self.assertEqual(list(self.od), ["key2", "key1"])  # key1 moved to end
    
    def test_deletion(self):
        """Test item deletion"""
        self.od["key1"] = self.entry1
        self.od["key2"] = self.entry2
        
        # Delete item
        del self.od["key1"]
        self.assertEqual(len(self.od), 1)
        self.assertFalse("key1" in self.od)
        self.assertEqual(list(self.od), ["key2"])
        
        # Delete nonexistent
        with self.assertRaises(KeyError):
            del self.od["nonexistent"]
    
    def test_pop_operations(self):
        """Test pop operations"""
        self.od["key1"] = self.entry1
        self.od["key2"] = self.entry2
        self.od["key3"] = self.entry3
        
        # Pop existing
        self.assertEqual(self.od.pop("key2"), self.entry2)
        self.assertEqual(len(self.od), 2)
        self.assertFalse("key2" in self.od)
        
        # Pop with default
        self.assertEqual(self.od.pop("nonexistent", "default"), "default")
        
        # Pop without default
        with self.assertRaises(KeyError):
            self.od.pop("nonexistent")
        
        # Popitem LIFO
        self.assertEqual(self.od.popitem(), ("key3", self.entry3))
        self.assertEqual(self.od.popitem(last=False), ("key1", self.entry1))
        
        # Popitem empty
        with self.assertRaises(KeyError):
            self.od.popitem()
    
    def test_move_to_end(self):
        """Test moving items to end/beginning"""
        self.od["key1"] = self.entry1
        self.od["key2"] = self.entry2
        self.od["key3"] = self.entry3
        
        # Move to end
        self.od.move_to_end("key1")
        self.assertEqual(list(self.od), ["key2", "key3", "key1"])
        
        # Move to beginning
        self.od.move_to_end("key3", last=False)
        self.assertEqual(list(self.od), ["key3", "key2", "key1"])
        
        # Move nonexistent
        with self.assertRaises(KeyError):
            self.od.move_to_end("nonexistent")
    
    def test_clear(self):
        """Test clearing the dictionary"""
        self.od["key1"] = self.entry1
        self.od["key2"] = self.entry2
        
        self.od.clear()
        self.assertEqual(len(self.od), 0)
        self.assertFalse(bool(self.od))
        self.assertEqual(list(self.od), [])
    
    def test_string_representation(self):
        """Test string representations"""
        self.od["key1"] = self.entry1
        self.od["key2"] = self.entry2
        
        str_rep = str(self.od)
        self.assertIn("key1", str_rep)
        self.assertIn("key2", str_rep)
        self.assertEqual(str_rep, repr(self.od))

if __name__ == '__main__':
    unittest.main() 