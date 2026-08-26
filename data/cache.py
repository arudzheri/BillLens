from __future__ import annotations

import json

import redis.asyncio as redis


class Cache:

    def __init__(
        self,
        url: str,
    ):
        self.client = redis.from_url(
            url,
            decode_responses=True,
        )

    async def get(
        self,
        key: str,
    ):
        value = await self.client.get(key)

        if value is None:
            return None

        return json.loads(value)

    async def set(
        self,
        key: str,
        value,
        ttl: int = 3600,
    ):
        await self.client.set(
            key,
            json.dumps(value),
            ex=ttl,
        )

    async def delete(
        self,
        key: str,
    ):
        await self.client.delete(key)
