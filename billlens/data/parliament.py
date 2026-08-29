from typing import Any, Dict, List
import httpx


class ParliamentAPIClient:
    BASE_URL = "https://members-api.parliament.uk/api"

    def __init__(self) -> None:
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
                " Safari/537.36"
            ),
            "Accept": "application/json",
        }

    async def search_members(
        self, name: str = "", house: int = None
    ) -> List[Dict[str, Any]]:
        """Fetch parliamentary members matching search criteria."""
        params: Dict[str, Any] = {"take": 20}
        if name:
            params["Name"] = name
        if house:
            params["House"] = house

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/Members/Search",
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

    def __init__(self) -> None:
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
                " Safari/537.36"
            ),
            "Accept": "application/json",
        }

    async def search_bills(self, search_term: str = "") -> List[Dict[str, Any]]:
        """Fetch bills matching a specific search keyword."""
        params: Dict[str, Any] = {"take": 20}
        if search_term:
            params["SearchTerm"] = search_term

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/Bills", headers=self.headers, params=params
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


# Backward compatibility aliases for existing codebase imports
ParliamentClient = ParliamentAPIClient