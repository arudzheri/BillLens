from typing import Any, Dict, List, Optional
import httpx

from billlens.data.keywords import extract_keywords


class ParliamentAPIClient:
    BASE_URL = "https://members-api.parliament.uk/api"

    def __init__(self, base_url: Optional[str] = None, **kwargs) -> None:
        self.base_url = base_url or self.BASE_URL
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
                " Safari/537.36"
            ),
            "Accept": "application/json",
        }

    async def search(self, query: str = "") -> List[Dict[str, Any]]:
        """Search parliamentary data for a given query string."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url.rstrip('/')}/search",
                headers=self.headers,
                params={"q": query},
            )
            response.raise_for_status()
            data = response.json()

        if "results" in data:
            return data["results"]

        results = []
        for item in data.get("items", []):
            val = item.get("value", {})
            results.append({
                "id": str(val.get("id", "")),
                "title": val.get("nameDisplayAs", val.get("title", "")),
                "description": val.get("nameFullTitle", val.get("description", "")),
                "url": val.get("url", f"https://parliament.uk/item/{val.get('id', '')}"),
            })
        return results

    async def search_members(
        self, name: str = "", house: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Fetch parliamentary members matching search criteria."""
        params: Dict[str, Any] = {"take": 20}
        if name:
            params["Name"] = name
        if house:
            params["House"] = house

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url.rstrip('/')}/Members/Search",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            data = response.json()

        members = []
        for item in data.get("items", []):
            val = item.get("value", {})
            house_info = val.get("latestHouseMembership", {}) or {}
            party_info = val.get("latestParty", {}) or {}

            members.append({
                "id": val.get("id"),
                "name": val.get("nameDisplayAs"),
                "full_title": val.get("nameFullTitle"),
                "party": party_info.get("name"),
                "constituency_or_house": house_info.get("membershipFrom"),
                "is_active": house_info.get("membershipStatus", {}).get(
                    "statusIsActive", False
                )
                if house_info.get("membershipStatus")
                else False,
                "source": "UK Parliament API",
            })
        return members


class BillsAPIClient:
    BASE_URL = "https://bills-api.parliament.uk/api/v1"

    def __init__(self, base_url: Optional[str] = None, **kwargs) -> None:
        self.base_url = base_url or self.BASE_URL
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
                " Safari/537.36"
            ),
            "Accept": "application/json",
        }

    async def search_bills(self, search_term: str = "") -> List[Dict[str, Any]]:
        """Fetch bills matching a keyword from the live UK Parliament API."""
        # Extract primary keyword if full sentence is passed
        clean_keyword = self._extract_keyword(search_term)
        params: Dict[str, Any] = {"take": 20}
        if clean_keyword:
            params["SearchTerm"] = clean_keyword

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url.rstrip('/')}/Bills", headers=self.headers, params=params
            )
            response.raise_for_status()
            data = response.json()

        bills = []
        for item in data.get("items", []):
            stage_info = item.get("currentStage", {}) or {}

            bills.append({
                "id": item.get("billId"),
                "title": item.get("shortTitle"),
                "is_act": item.get("isAct", False),
                "is_defeated": item.get("isDefeated", False),
                "stage": stage_info.get("description", "Unknown stage"),
                "house": stage_info.get("house", "Unknown house"),
                "last_updated": item.get("lastUpdate"),
                "source": "UK Parliament Bills API",
            })
        return bills

    @staticmethod
    def _extract_keyword(text: str) -> str:
        """Extract the main search topic from a conversational query."""
        return extract_keywords(text)


# Backward compatibility aliases
ParliamentClient = ParliamentAPIClient