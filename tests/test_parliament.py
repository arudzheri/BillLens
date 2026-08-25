import pytest

from billlens.data.parliament import (
    ParliamentClient,
)


class FakeResponse:

    def raise_for_status(self):
        pass

    def json(self):
        return {
            "results": [
                {
                    "id": "123",
                    "title": "Housing debate",
                    "description": (
                        "A debate about housing."
                    ),
                    "url": (
                        "https://example.com/debate/123"
                    ),
                }
            ]
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
async def test_parliament_search(monkeypatch):

    monkeypatch.setattr(
        "httpx.AsyncClient",
        lambda *args, **kwargs: FakeClient(),
    )

    client = ParliamentClient(
        base_url="https://example.com"
    )

    results = await client.search(
        "housing"
    )

    assert len(results) == 1

    assert results[0]["title"] == (
        "Housing debate"
    )


@pytest.mark.asyncio
async def test_parliament_result_has_url(
    monkeypatch,
):

    monkeypatch.setattr(
        "httpx.AsyncClient",
        lambda *args, **kwargs: FakeClient(),
    )

    client = ParliamentClient(
        base_url="https://example.com"
    )

    results = await client.search(
        "housing"
    )

    assert results[0]["url"].startswith(
        "https://"
    )
