from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException

from apps.api.dependencies import get_orchestrator
from billlens.agent.orchestrator import BillLensOrchestrator
from billlens.models.answer import AnswerResponse
from billlens.models.question import QuestionRequest

logger = logging.getLogger(__name__)

router = APIRouter(tags=["questions"])


@router.post("/api/v1/questions", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    orchestrator: BillLensOrchestrator = Depends(get_orchestrator),
) -> AnswerResponse:
    """Answer a parliamentary question using live research."""
    question = request.question.strip()

    if len(question) < 3:
        raise HTTPException(
            status_code=400,
            detail="Question must be at least 3 characters long",
        )

    try:
        logger.info("Processing question: %s", question)
        return await orchestrator.answer(
            QuestionRequest(question=question)
        )
    except Exception as error:
        logger.exception("Error processing question")
        raise HTTPException(
            status_code=500,
            detail="Unable to research this question.",
        ) from error