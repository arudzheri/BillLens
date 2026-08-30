import pytest

from billlens.agent.planner import (
    BillLensPlanner,
)

from billlens.agent.orchestrator import BillLensOrchestrator
from billlens.agent.researcher import (
    BillLensResearcher,
    ResearchResult,
)
from billlens.models.evidence import Evidence
from billlens.models.question import QuestionRequest


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


class FakeAsyncClient:
    async def get(self, *args, **kwargs):
        return FakeResponse(
            {
                "results": [
                    {
                        "title": "Housing Bill",
                        "description": (
                            "A bill concerning housing."
                        ),
                        "url": "https://example.com/bill",
                        "date": "2026-01-01",
                        "score": 0.9,
                    }
                ]
            }
        )

    async def post(self, *args, **kwargs):
        return FakeResponse(
            {
                "results": [
                    {
                        "title": "Housing Act",
                        "text": (
                            "Legislation concerning housing."
                        ),
                        "url": "https://example.com/act",
                        "date": "2026-01-01",
                        "score": 0.95,
                    }
                ]
            }
        )

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
async def test_researcher_returns_evidence(monkeypatch):

    planner = BillLensPlanner()

    plan = planner.create_plan(
        "What laws have changed about housing?"
    )

    researcher = BillLensResearcher(
        lex_base_url="https://lex.example",
        parliament_base_url="https://parliament.example",
    )

    monkeypatch.setattr(
        "httpx.AsyncClient",
        lambda *args, **kwargs: FakeAsyncClient(),
    )

    result = await researcher.research(plan)

    assert result.topic == "housing"

    assert len(result.evidence) > 0


@pytest.mark.asyncio
async def test_researcher_deduplicates_evidence(
    monkeypatch,
):

    planner = BillLensPlanner()

    plan = planner.create_plan(
        "What has Parliament done about housing?"
    )

    researcher = BillLensResearcher(
        lex_base_url="https://lex.example",
        parliament_base_url="https://parliament.example",
    )

    class DuplicateClient(FakeAsyncClient):

        async def get(self, *args, **kwargs):
            return FakeResponse(
                {
                    "results": [
                        {
                            "title": "Housing",
                            "text": "Housing evidence",
                            "url": "https://example.com/same",
                            "score": 0.9,
                        },
                        {
                            "title": "Housing",
                            "text": "Housing evidence",
                            "url": "https://example.com/same",
                            "score": 0.8,
                        },
                    ]
                }
            )

    monkeypatch.setattr(
        "httpx.AsyncClient",
        lambda *args, **kwargs: DuplicateClient(),
    )

    result = await researcher.research(plan)

    urls = [
        item.url
        for item in result.evidence
    ]

    assert len(urls) == len(set(urls))


@pytest.mark.asyncio
async def test_orchestrator_answer_uses_research_result(monkeypatch):
    orchestrator = BillLensOrchestrator()

    async def fake_research(self, plan):
        return ResearchResult(
            topic="housing",
            evidence=[
                Evidence(
                    title="Housing Act",
                    content="The Housing Act introduced new protections for renters.",
                    source_type="legislation",
                    url="https://example.com/housing",
                    relevance_score=0.95,
                )
            ],
        )

    monkeypatch.setattr(BillLensResearcher, "research", fake_research)

    answer = await orchestrator.answer(
        QuestionRequest(question="What has Parliament done about housing?")
    )

    assert answer.question == "What has Parliament done about housing?"
    assert answer.summary
    assert answer.confidence >= 0
