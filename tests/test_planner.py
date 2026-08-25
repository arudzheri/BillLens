from billlens.agent.planner import (
    BillLensPlanner,
    ResearchType,
)


def test_planner_creates_housing_plan():
    planner = BillLensPlanner()

    plan = planner.create_plan(
        "What has Parliament done about housing?"
    )

    assert plan.original_question == (
        "What has Parliament done about housing?"
    )

    assert plan.topic == "housing"

    assert len(plan.steps) > 0


def test_planner_detects_legislation():
    planner = BillLensPlanner()

    plan = planner.create_plan(
        "What laws have changed about housing?"
    )

    step_types = {
        step.type
        for step in plan.steps
    }

    assert ResearchType.LEGISLATION in step_types


def test_planner_detects_bills():
    planner = BillLensPlanner()

    plan = planner.create_plan(
        "What bills about housing have Parliament discussed?"
    )

    step_types = {
        step.type
        for step in plan.steps
    }

    assert ResearchType.BILLS in step_types


def test_planner_detects_votes():
    planner = BillLensPlanner()

    plan = planner.create_plan(
        "What did MPs vote on regarding housing?"
    )

    assert plan.requires_vote_lookup is True

    step_types = {
        step.type
        for step in plan.steps
    }

    assert ResearchType.VOTES in step_types


def test_planner_detects_mps():
    planner = BillLensPlanner()

    plan = planner.create_plan(
        "Which MPs have raised housing issues?"
    )

    assert plan.requires_mp_lookup is True

    step_types = {
        step.type
        for step in plan.steps
    }

    assert ResearchType.MPS in step_types


def test_planner_detects_timeline():
    planner = BillLensPlanner()

    plan = planner.create_plan(
        "What actually happened with housing over time?"
    )

    assert plan.requires_timeline is True

    step_types = {
        step.type
        for step in plan.steps
    }

    assert ResearchType.TIMELINE in step_types


def test_empty_question_is_rejected():
    planner = BillLensPlanner()

    try:
        planner.create_plan("")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_whitespace_question_is_rejected():
    planner = BillLensPlanner()

    try:
        planner.create_plan("   ")
        assert False, "Expected ValueError"
    except ValueError:
        pass
