import pytest

from billlens.data.legislation import (
    LegislationClient,
)


class FakeResponse:

    def raise_for_status(self):
        pass

    def json(self):
        return {
            "title": "Housing Act",
            "id": "housing-act-2026",
            "status": "in_force",
            "url": (
                "https://example.com/housing-act"
            ),
        }


class FakeClient:

    async def get(self, *args, **kwargs):
        return FakeResponse()

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        traceback,
    ):
        pass


@pytest.mark.asyncio
async def test_get_legislation(monkeypatch):

    monkeypatch.setattr(
        "httpx.AsyncClient",
        lambda *args, **kwargs: FakeClient(),
    )

    client = LegislationClient(
        base_url="https://example.com"
    )

    legislation = await client.get(
        "housing-act-2026"
    )

    assert legislation["title"] == "Housing Act"

    assert legislation["id"] == (
        "housing-act-2026"
    )


@pytest.mark.asyncio
async def test_legislation_contains_status(
    monkeypatch,
):

    monkeypatch.setattr(
        "httpx.AsyncClient",
        lambda *args, **kwargs: FakeClient(),
    )

    client = LegislationClient(
        base_url="https://example.com"
    )

    result = await client.get(
        "housing-act-2026"
    )

    assert "status" in result

    assert result["status"] == "in_force"
