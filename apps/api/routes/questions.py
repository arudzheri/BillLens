"""
Question endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from billlens.models.question import QuestionRequest
from billlens.models.answer import AnswerResponse
from billlens.agent.orchestrator import BillLensOrchestrator
from ..dependencies import get_orchestrator

router = APIRouter(prefix="/api/v1", tags=["questions"])


@router.post("/questions", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    orchestrator: BillLensOrchestrator = Depends(get_orchestrator),
) -> AnswerResponse:
    """
    Ask BillLens a question about UK Parliament.
    
    Returns a structured answer with verified evidence,
    sources, and confidence levels.
    """
    try:
        answer = await orchestrator.answer(request)
        return answer
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing question.",
        )