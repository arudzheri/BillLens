from billlens.agent.researcher import Evidence


def test_evidence_can_be_ranked():

    evidence = [
        Evidence(
            title="Unrelated document",
            source_type="debate",
            content="Something unrelated.",
            relevance_score=0.2,
        ),
        Evidence(
            title="Housing debate",
            source_type="debate",
            content="Parliament discussed housing.",
            relevance_score=0.9,
        ),
    ]

    ranked = sorted(
        evidence,
        key=lambda item: item.relevance_score,
        reverse=True,
    )

    assert ranked[0].title == "Housing debate"


def test_retrieval_scores_are_valid():

    evidence = [
        Evidence(
            title="Housing",
            source_type="legislation",
            content="Housing law.",
            relevance_score=0.8,
        )
    ]

    for item in evidence:
        assert 0 <= item.relevance_score <= 1


def test_duplicate_documents_can_be_removed():

    evidence = [
        Evidence(
            title="Housing Act",
            source_type="legislation",
            url="https://example.com/housing",
            content="Housing Act.",
        ),
        Evidence(
            title="Housing Act",
            source_type="legislation",
            url="https://example.com/housing",
            content="Housing Act.",
        ),
    ]

    unique = {}

    for item in evidence:
        unique[item.url] = item

    assert len(unique) == 1
