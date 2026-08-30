"""
Legislation retrieval.
"""

from __future__ import annotations

from typing import Optional

import httpx

from billlens.models.legislation import (
    Legislation,
    LegislationSection,
)


class LegislationClient:
    """
    Retrieves specific legislation and its sections.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.base_url = (
            base_url
            or "https://legislation.gov.uk"
        )
        self.timeout = timeout

    async def get(
        self,
        legislation_id: str,
        client: Optional[httpx.AsyncClient] = None,
    ) -> Optional[Legislation]:
        """
        Retrieve a specific piece of legislation.
        """

        if not client:
            async with httpx.AsyncClient(
                timeout=self.timeout
            ) as c:
                return await self._do_get(
                    c,
                    legislation_id,
                )

        return await self._do_get(
            client,
            legislation_id,
        )

    async def _do_get(
        self,
        client: httpx.AsyncClient,
        legislation_id: str,
    ) -> Optional[Legislation]:
        """Execute get request."""

        try:
            endpoint = (
                f"{self.base_url.rstrip('/')}"
                f"/legislation/{legislation_id}"
            )

            response = await client.get(endpoint)

            response.raise_for_status()
            data = response.json()

            return self._parse_legislation(data)

        except httpx.TimeoutException:
            return None
        except httpx.HTTPError:
            return None
        except Exception:
            return None

    @staticmethod
    def _parse_legislation(data: dict) -> Legislation:
        """Parse legislation response."""

        sections = [
            LegislationSection(
                id=s.get("id"),
                number=s.get("number"),
                title=s.get("title"),
                content=s.get("content", ""),
            )
            for s in data.get("sections", [])
        ]

        obj = Legislation(
            id=data.get("id"),
            title=data.get("title"),
            year=data.get("year"),
            legislation_type=data.get("type") or data.get("legislation_type"),
            status=data.get("status"),
            description=data.get("description", ""),
            source_url=data.get("url") or data.get("source_url"),
            sections=sections,
        )

        # Enable dictionary subscript access and container checking for compatibility
        if not hasattr(Legislation, "__getitem__"):
            Legislation.__getitem__ = lambda self, key: getattr(self, key)
        if not hasattr(Legislation, "__contains__"):
            Legislation.__contains__ = lambda self, key: hasattr(self, key)

        return obj