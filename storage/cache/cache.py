from typing import Any, Optional, List

class Cache:
    def __init__(self, capacity: int = 1000):
        pass

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        pass

    def get(self, key: str) -> Any:
        pass   

    def ttl(self, key: str) -> Optional[int]:
        pass

    def expire(self, key: str, timestamp: float):
        pass

    def scan(self) -> List[str]:
        pass