from billlens.agent.answer import (
    BillLensAnswerGenerator,
)

from billlens.agent.researcher import Evidence

from billlens.agent.verifier import (
    BillLensVerifier,
    Claim,
)


def test_answer_generator_creates_answer():

    verifier = BillLensVerifier()

    evidence = [
        Evidence(
            title="Housing Act",
            source_type="legislation",
            url="https://example.com/housing",
            content=(
                "The Housing Act introduced "
                "new protections for renters."
            ),
            relevance_score=0.95,
        )
    ]

    claims = [
        Claim(
            text=(
                "The Housing Act introduced "
                "new protections for renters."
            )
        )
    ]

    verification = verifier.verify(
        claims,
        evidence,
    )

    generator = BillLensAnswerGenerator()

    answer = generator.generate(
        question=(
            "What has Parliament done about housing?"
        ),
        verification=verification,
        evidence=evidence,
    )

    assert answer.question == (
        "What has Parliament done about housing?"
    )

    assert answer.summary != ""

    assert answer.confidence > 0


def test_answer_contains_sources():

    verifier = BillLensVerifier()

    evidence = [
        Evidence(
            title="Housing Act",
            source_type="legislation",
            url="https://example.com/housing",
            content=(
                "Housing legislation introduced "
                "new protections."
            ),
            relevance_score=0.9,
        )
    ]

    claims = [
        Claim(
            text=(
                "Housing legislation introduced "
                "new protections."
            )
        )
    ]

    verification = verifier.verify(
        claims,
        evidence,
    )

    generator = BillLensAnswerGenerator()

    answer = generator.generate(
        question="What changed?",
        verification=verification,
        evidence=evidence,
    )

    assert len(answer.sources) > 0

    assert (
        answer.sources[0].url
        == "https://example.com/housing"
    )


def test_answer_warns_about_unverified_claims():

    verifier = BillLensVerifier()

    claims = [
        Claim(
            text=(
                "Parliament completely solved "
                "the housing crisis."
            )
        )
    ]

    verification = verifier.verify(
        claims,
        [],
    )

    generator = BillLensAnswerGenerator()

    answer = generator.generate(
        question="What happened with housing?",
        verification=verification,
        evidence=[],
    )

    assert len(answer.warnings) > 0
