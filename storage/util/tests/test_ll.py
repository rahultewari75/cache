import unittest
from storage.util.ll import Node, DoublyLinkedList
from storage.data_types.entry import Entry

class TestNode(unittest.TestCase):
    def test_node_creation(self):
        """Test node creation and string representation"""
        entry = Entry("test_value")
        node = Node("test_key", entry)
        
        self.assertEqual(node.key, "test_key")
        self.assertEqual(node.value, entry)
        self.assertIsNone(node.prev)
        self.assertIsNone(node.next)
        self.assertIn("test_key", str(node))

class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoublyLinkedList()
        self.entry1 = Entry("value1")
        self.entry2 = Entry("value2")
        self.entry3 = Entry("value3")
    
    def test_empty_list(self):
        """Test empty list properties"""
        self.assertTrue(self.dll.is_empty())
        self.assertEqual(len(self.dll), 0)
        self.assertEqual(self.dll.size(), 0)
        self.assertIsNone(self.dll.peek_head())
        self.assertIsNone(self.dll.peek_tail())
    
    def test_add_to_head(self):
        """Test adding nodes to head"""
        node1 = self.dll.add_to_head("key1", self.entry1)
        self.assertEqual(len(self.dll), 1)
        self.assertEqual(self.dll.peek_head(), node1)
        self.assertEqual(self.dll.peek_tail(), node1)
        
        node2 = self.dll.add_to_head("key2", self.entry2)
        self.assertEqual(len(self.dll), 2)
        self.assertEqual(self.dll.peek_head(), node2)
        self.assertEqual(self.dll.peek_tail(), node1)
    
    def test_add_to_tail(self):
        """Test adding nodes to tail"""
        node1 = self.dll.add_to_tail("key1", self.entry1)
        self.assertEqual(len(self.dll), 1)
        self.assertEqual(self.dll.peek_head(), node1)
        self.assertEqual(self.dll.peek_tail(), node1)
        
        node2 = self.dll.add_to_tail("key2", self.entry2)
        self.assertEqual(len(self.dll), 2)
        self.assertEqual(self.dll.peek_head(), node1)
        self.assertEqual(self.dll.peek_tail(), node2)
    
    def test_remove_operations(self):
        """Test node removal operations"""
        node1 = self.dll.add_to_tail("key1", self.entry1)
        node2 = self.dll.add_to_tail("key2", self.entry2)
        node3 = self.dll.add_to_tail("key3", self.entry3)
        
        # Remove from head
        removed = self.dll.remove_from_head()
        self.assertEqual(removed, node1)
        self.assertEqual(len(self.dll), 2)
        self.assertEqual(self.dll.peek_head(), node2)
        
        # Remove from tail
        removed = self.dll.remove_from_tail()
        self.assertEqual(removed, node3)
        self.assertEqual(len(self.dll), 1)
        self.assertEqual(self.dll.peek_tail(), node2)
        
        # Remove specific node
        self.dll.remove_node(node2)
        self.assertTrue(self.dll.is_empty())
    
    def test_move_operations(self):
        """Test moving nodes within the list"""
        node1 = self.dll.add_to_tail("key1", self.entry1)
        node2 = self.dll.add_to_tail("key2", self.entry2)
        node3 = self.dll.add_to_tail("key3", self.entry3)
        
        # Move middle node to head
        self.dll.move_to_head(node2)
        self.assertEqual(self.dll.peek_head(), node2)
        self.assertEqual(self.dll.peek_head().next, node1)
        self.assertEqual(self.dll.peek_tail(), node3)
        
        # Move first node to tail
        self.dll.move_to_tail(node2)
        self.assertEqual(self.dll.peek_head(), node1)
        self.assertEqual(self.dll.peek_tail(), node2)
    
    def test_iteration(self):
        """Test list iteration"""
        nodes = [
            self.dll.add_to_tail("key1", self.entry1),
            self.dll.add_to_tail("key2", self.entry2),
            self.dll.add_to_tail("key3", self.entry3)
        ]
        
        # Forward iteration
        for i, node in enumerate(self.dll):
            self.assertEqual(node, nodes[i])
        
        # Reverse iteration
        for i, node in enumerate(reversed(self.dll)):
            self.assertEqual(node, nodes[2-i])
    
    def test_find_operation(self):
        """Test finding nodes by key"""
        node1 = self.dll.add_to_tail("key1", self.entry1)
        node2 = self.dll.add_to_tail("key2", self.entry2)
        
        self.assertEqual(self.dll.find("key1"), node1)
        self.assertEqual(self.dll.find("key2"), node2)
        self.assertIsNone(self.dll.find("nonexistent"))
    
    def test_clear_operation(self):
        """Test clearing the list"""
        self.dll.add_to_tail("key1", self.entry1)
        self.dll.add_to_tail("key2", self.entry2)
        
        self.dll.clear()
        self.assertTrue(self.dll.is_empty())
        self.assertEqual(len(self.dll), 0)
    
    def test_list_conversions(self):
        """Test converting list to Python lists"""
        self.dll.add_to_tail("key1", self.entry1)
        self.dll.add_to_tail("key2", self.entry2)
        
        self.assertEqual(self.dll.keys(), ["key1", "key2"])
        self.assertEqual(self.dll.values(), [self.entry1, self.entry2])
        self.assertEqual(self.dll.to_list(), [("key1", self.entry1), ("key2", self.entry2)])

if __name__ == '__main__':
    unittest.main() 