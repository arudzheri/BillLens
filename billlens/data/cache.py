"""
Redis cache client for BillLens.
"""

from __future__ import annotations

import json
from typing import Any, Optional

import redis.asyncio as redis


class Cache:
    """
    Redis cache with JSON serialization and namespacing.
    """
    
    def __init__(
        self,
        url: str,
        namespace: str = "billlens",
        version: str = "v1",
        ttl: int = 3600,
    ):
        self.url = url
        self.namespace = namespace
        self.version = version
        self.ttl = ttl
        self.client: Optional[redis.Redis] = None
    
    async def connect(self) -> None:
        """Connect to Redis."""
        try:
            self.client = redis.from_url(
                self.url,
                decode_responses=True,
            )
            # Test connection
            await self.client.ping()
        except Exception:
            self.client = None
    
    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.client:
            await self.client.close()
    
    def _make_key(self, key: str) -> str:
        """Create namespaced key."""
        return f"{self.namespace}:{self.version}:{key}"
    
    async def get(
        self,
        key: str,
    ) -> Any:
        """Get value from cache."""
        if not self.client:
            return None
        
        try:
            full_key = self._make_key(key)
            value = await self.client.get(full_key)
            
            if value is None:
                return None
            
            return json.loads(value)
        
        except Exception:
            return None
    
    async def get_json(
        self,
        key: str,
    ) -> Any:
        """Get JSON value from cache."""
        return await self.get(key)
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set value in cache."""
        if not self.client:
            return False
        
        try:
            full_key = self._make_key(key)
            ttl = ttl or self.ttl
            
            await self.client.set(
                full_key,
                json.dumps(value),
                ex=ttl,
            )
            
            return True
        
        except Exception:
            return False
    
    async def set_json(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set JSON value in cache."""
        return await self.set(key, value, ttl)
    
    async def delete(
        self,
        key: str,
    ) -> bool:
        """Delete value from cache."""
        if not self.client:
            return False
        
        try:
            full_key = self._make_key(key)
            await self.client.delete(full_key)
            return True
        
        except Exception:
            return False
    
    async def healthcheck(self) -> bool:
        """Check Redis connection health."""
        if not self.client:
            return False
        
        try:
            await self.client.ping()
            return True
        
        except Exception:
            return False