"""
UK Legislation (Lex) API client.
"""

from __future__ import annotations

from typing import Optional

import httpx

from billlens.models.evidence import Evidence


class LexClient:
    """
    Client for UK Legislation (Lex) API.
    
    Searches legislation and legislation sections.
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
    
    async def search(
        self,
        query: str,
        limit: int = 10,
        client: Optional[httpx.AsyncClient] = None,
    ) -> list[Evidence]:
        """
        Search legislation.
        """
        
        if not client:
            async with httpx.AsyncClient(
                timeout=self.timeout
            ) as c:
                return await self._do_search(
                    c,
                    query,
                    limit,
                )
        
        return await self._do_search(
            client,
            query,
            limit,
        )
    
    async def _do_search(
        self,
        client: httpx.AsyncClient,
        query: str,
        limit: int,
    ) -> list[Evidence]:
        """Execute search request."""
        
        try:
            endpoint = (
                f"{self.base_url.rstrip('/')}"
                "/legislation/section/search"
            )
            
            response = await client.post(
                endpoint,
                json={
                    "query": query,
                    "limit": limit,
                },
            )
            
            response.raise_for_status()
            data = response.json()
            
            return self._parse_results(data)
        
        except httpx.TimeoutException:
            return []
        except httpx.HTTPError:
            return []
        except Exception:
            return []
    
    @staticmethod
    def _parse_results(data: dict) -> list[Evidence]:
        """Parse API response into Evidence."""
        
        results = data.get("results", [])
        evidence = []
        
        for item in results:
            evidence.append(
                Evidence(
                    title=item.get(
                        "title",
                        "UK legislation",
                    ),
                    source_type="legislation",
                    url=item.get("url"),
                    content=item.get(
                        "text",
                        item.get("description", ""),
                    ),
                    date=item.get("date"),
                    relevance_score=float(
                        item.get("score", 0.0)
                    ),
                    metadata=item,
                )
            )
        
        return evidence