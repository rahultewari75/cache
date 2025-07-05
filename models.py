from pydantic import BaseModel, Field
from typing import Optional, Any
from storage.cache.factory.policies import CachePolicy
from datetime import datetime

class CacheConfigureRequest(BaseModel):
    policy: CachePolicy = Field(default=CachePolicy.LRU)
    capacity: int = Field(
        default=10,
        ge=1,
        description="Maximum number of items the cache can hold"
    )

class KeyValueRequest(BaseModel):
    key: str = Field(
        description="Key to store value under",
        min_length=1,
        example="user"
    )
    value: Any = Field(
        description="Value to store",
        example="John Doe"
    )
    ttl: Optional[int] = Field(
        default=None,
        ge=0,
        description="Time-to-live in seconds. If set, key will automatically expire after this duration",
        example=3600
    )

class KeyRequest(BaseModel):
    key: str = Field(
        description="Key to lookup",
        min_length=1,
        example="user"
    )

class ExpirationRequest(BaseModel):
    key: str = Field(
        description="Key to set expiration for",
        min_length=1,
        example="user"
    )
    expiry: datetime = Field(
        description="When the key should expire",
        example="2025-01-01T00:00:00Z"
    )

class QueueKeyRequest(KeyRequest):
    key: str = Field(
        description="Queue identifier",
        min_length=1,
        example="notifications"
    )

class QueueEnqueueRequest(BaseModel):
    key: str = Field(
        description="Queue identifier",
        min_length=1,
        example="notifications"
    )
    value: str = Field(
        description="Value to add to the queue",
        min_length=1,
        example="New message from user"
    ) 