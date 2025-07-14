import pytest
import time

from policy_injection_cache.cache.cache import Cache
from policy_injection_cache.policies.lru import LRUPolicy
from policy_injection_cache.policies.lfu import LFUPolicy
from policy_injection_cache.policies.random import RandomPolicy
from policy_injection_cache.errors.cache import KeyNotFoundError, KeyExpiredError
from policy_injection_cache.errors.base import InvalidInputError
from policy_injection_cache.policies.policy import ReplacementPolicy
from typing import List, Optional, Any

# Test parameters for different policies
POLICIES = [
    LRUPolicy,
    LFUPolicy,
    RandomPolicy
]

@pytest.fixture(params=POLICIES)
def cache(request) -> Cache:
    """Fixture that provides a cache instance with each policy type."""
    policy_class = request.param
    return Cache(policy=policy_class(), capacity=3)

# Basic Operations Tests
class TestBasicOperations:
    def test_get_set(self, cache: Cache):
        """Test basic get/set operations."""
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_get_nonexistent(self, cache: Cache):
        """Test getting a nonexistent key raises KeyNotFoundError."""
        with pytest.raises(KeyNotFoundError):
            cache.get("nonexistent")

    def test_invalid_key_type(self, cache: Cache):
        """Test that non-string keys raise InvalidInputError."""
        with pytest.raises(InvalidInputError):
            cache.set(123, "value")
        with pytest.raises(InvalidInputError):
            cache.get(123)

    def test_invalid_ttl(self, cache: Cache):
        """Test that invalid TTL values raise InvalidInputError."""
        with pytest.raises(InvalidInputError):
            cache.set("key1", "value1", ttl=-1)

    def test_clear(self, cache: Cache):
        """Test clearing the cache."""
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        with pytest.raises(KeyNotFoundError):
            cache.get("key1")
        with pytest.raises(KeyNotFoundError):
            cache.get("key2")

    def test_delete(self, cache: Cache):
        """Test deleting a specific key from the cache."""
        # Set up test data
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        # Delete one key
        cache.delete("key1")
        
        # Verify key1 is gone
        with pytest.raises(KeyNotFoundError):
            cache.get("key1")
        
        # Verify key2 is still there
        assert cache.get("key2") == "value2"
        
        # Test deleting non-existent key
        with pytest.raises(KeyNotFoundError):
            cache.delete("nonexistent")
        
        # Test deleting with invalid key type
        with pytest.raises(InvalidInputError):
            cache.delete(123)

# Eviction Tests
class TestEviction:
    def test_eviction_on_full(self, cache: Cache):
        """Test that items are evicted when cache is full."""
        # Fill the cache (capacity=3)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        
        # Add one more item
        cache.set("key4", "value4")
        
        # Verify key4 was added
        assert cache.get("key4") == "value4"
        
        # Verify only 3 items remain (capacity=3)
        keys_present = 0
        for key in ["key1", "key2", "key3", "key4"]:
            try:
                cache.get(key)
                keys_present += 1
            except KeyNotFoundError:
                continue
        assert keys_present == 3

    def test_no_eviction_when_not_full(self, cache: Cache):
        """Test that items are not evicted when cache is not full."""
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        assert cache.get("key1") == "value1"
        assert cache.get("key2") == "value2"

# TTL Tests
class TestTTL:
    def test_ttl_expiration(self, cache: Cache):
        """Test that items expire after their TTL."""
        cache.set("key1", "value1", ttl=1)  # 1 second TTL
        assert cache.get("key1") == "value1"
        time.sleep(1.1)  # Wait for TTL to expire
        with pytest.raises(KeyExpiredError):
            cache.get("key1")

    def test_ttl_update(self, cache: Cache):
        """Test that TTL is updated when setting an existing key."""
        cache.set("key1", "value1", ttl=10)
        cache.set("key1", "value2", ttl=1)  # Update with shorter TTL
        time.sleep(1.1)
        with pytest.raises(KeyExpiredError):
            cache.get("key1")

    def test_expired_key_removed(self, cache: Cache):
        """Test that expired keys are removed from policy tracking."""
        cache.set("key1", "value1", ttl=1)
        cache.set("key2", "value2")
        time.sleep(1.1)
        
        # Trigger cleanup by accessing key2
        assert cache.get("key2") == "value2"
        
        # key1 should be expired
        with pytest.raises(KeyExpiredError):
            cache.get("key1")

# Policy-Specific Tests
class TestLRUPolicy:
    def test_lru_specific_eviction(self):
        """Test LRU-specific eviction behavior."""
        cache = Cache(policy=LRUPolicy(), capacity=2)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        # Access key1 to make it most recently used
        cache.get("key1")
        
        # Add new item - should evict key2
        cache.set("key3", "value3")
        
        # Verify key1 (most recently used) and key3 (just added) remain
        assert cache.get("key1") == "value1"
        assert cache.get("key3") == "value3"
        
        # Verify key2 was evicted
        with pytest.raises(KeyNotFoundError):
            cache.get("key2")

class TestLFUPolicy:
    def test_lfu_specific_eviction(self):
        """Test LFU-specific eviction behavior."""
        cache = Cache(policy=LFUPolicy(), capacity=2)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        # Access key1 multiple times to increase its frequency
        cache.get("key1")
        cache.get("key1")
        
        # Add new item - should evict key2 (least frequently used)
        cache.set("key3", "value3")
        
        # Verify key1 (most frequently used) and key3 (just added) remain
        assert cache.get("key1") == "value1"
        assert cache.get("key3") == "value3"
        
        # Verify key2 was evicted
        with pytest.raises(KeyNotFoundError):
            cache.get("key2")

class TestRandomPolicy:
    def test_random_eviction(self):
        """Test that random eviction removes exactly one item."""
        cache = Cache(policy=RandomPolicy(), capacity=2)
        
        # Add two items
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        # Add third item to force eviction
        cache.set("key3", "value3")
        
        # Verify exactly one item was evicted (2 remain)
        items_remaining = 0
        for key in ["key1", "key2", "key3"]:
            try:
                cache.get(key)
                items_remaining += 1
            except KeyNotFoundError:
                continue
        
        assert items_remaining == 2 

class TestEvictKeyBug:
    def test_evict_triggers_remove_key(self):
        """Ensure that eviction calls policy.remove_key(evicted_key)."""
        # Spy policy to capture calls
        class SpyPolicy(ReplacementPolicy[str, Any]):
            def __init__(self):
                self.accesses: List[str] = []
                self.evicted: Optional[str] = None
                self.removed: List[str] = []
            def record_access(self, key: str) -> None:
                self.accesses.append(key)
            def evict(self) -> str:
                # evict the first accessed key
                self.evicted = self.accesses[0]
                return self.evicted
            def remove_key(self, key: str) -> None:
                self.removed.append(key)
            def clear(self) -> None:
                pass

        spy = SpyPolicy()
        cache = Cache(policy=spy, capacity=1)

        cache.set("a", 1)
        # No removal yet
        assert spy.removed == []

        # This should evict "a" and call remove_key("a")
        cache.set("b", 2)

        assert spy.evicted == "a"
        assert spy.removed == ["a"], "policy.remove_key was not called on eviction"

class TestExpiredKeyRemoval:
    def test_expired_key_raises_expired_error(self):
        """Test that expired keys raise KeyExpiredError."""
        # Mock Entry that can be manually set as expired
        class MockEntry:
            def __init__(self, value: Any, expired: bool = False):
                self.value = value
                self._expired = expired
                self.created_at = time.time()
                self.expiration_time = time.time() - 1 if expired else None
                
            def is_expired(self) -> bool:
                return self._expired
                
            def get_value(self) -> Any:
                return self.value
                
            def set_expired(self, expired: bool) -> None:
                self._expired = expired
                if expired:
                    self.expiration_time = time.time() - 1
                else:
                    self.expiration_time = None

        # Spy policy to track removals
        class SpyPolicy(ReplacementPolicy[str, Any]):
            def __init__(self):
                self.removed: List[str] = []
            def record_access(self, key: str) -> None:
                pass
            def evict(self) -> str:
                return "dummy"
            def remove_key(self, key: str) -> None:
                self.removed.append(key)
            def clear(self) -> None:
                pass

        spy = SpyPolicy()
        cache = Cache(policy=spy, capacity=2)
        
        # Inject our mock entries directly into storage
        mock_entry1 = MockEntry("value1", expired=True)
        mock_entry2 = MockEntry("value2", expired=False)
        cache._storage["key1"] = mock_entry1
        cache._storage["key2"] = mock_entry2
        
        # Access key2 (not expired) - should work
        assert cache.get("key2") == "value2"
        
        # Try to access key1 (expired) - should raise KeyExpiredError
        with pytest.raises(KeyExpiredError):
            cache.get("key1")
            
        # Verify key1 was removed from both storage and policy
        assert "key1" not in cache._storage
        assert "key1" in spy.removed
