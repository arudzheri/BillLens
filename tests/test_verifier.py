from billlens.agent.researcher import Evidence

from billlens.agent.verifier import (
    BillLensVerifier,
    Claim,
)


def make_evidence(
    title: str,
    content: str,
    score: float = 0.9,
):
    return Evidence(
        title=title,
        source_type="legislation",
        url="https://example.com/source",
        content=content,
        relevance_score=score,
    )


def test_verifier_supports_matching_claim():

    verifier = BillLensVerifier()

    evidence = [
        make_evidence(
            title="Housing Act",
            content=(
                "The Housing Act introduced "
                "new protections for renters."
            ),
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

    result = verifier.verify(
        claims,
        evidence,
    )

    assert len(result.verified_claims) == 1

    assert result.verified_claims[0].supported is True

    assert (
        result.verified_claims[0].confidence > 0
    )


def test_verifier_rejects_unsupported_claim():

    verifier = BillLensVerifier()

    evidence = [
        make_evidence(
            title="Housing Act",
            content=(
                "The Act concerns housing standards."
            ),
        )
    ]

    claims = [
        Claim(
            text=(
                "Parliament abolished all "
                "housing taxes."
            )
        )
    ]

    result = verifier.verify(
        claims,
        evidence,
    )

    assert (
        result.verified_claims[0].supported
        is False
    )


def test_verifier_handles_no_evidence():

    verifier = BillLensVerifier()

    claims = [
        Claim(
            text="Parliament changed housing law."
        )
    ]

    result = verifier.verify(
        claims,
        [],
    )

    assert (
        result.verified_claims[0].supported
        is False
    )

    assert result.overall_confidence == 0


def test_verifier_generates_warning():

    verifier = BillLensVerifier()

    claims = [
        Claim(
            text="Something completely unsupported happened."
        )
    ]

    result = verifier.verify(
        claims,
        [],
    )

    assert len(result.warnings) > 0
