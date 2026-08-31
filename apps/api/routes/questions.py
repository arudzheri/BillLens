"""
Question endpoints.
"""

from __future__ import annotations

import traceback
from fastapi import APIRouter, Depends, HTTPException
from billlens.models.question import QuestionRequest
from billlens.models.answer import AnswerResponse
from billlens.agent.orchestrator import BillLensOrchestrator
from ..dependencies import get_orchestrator

router = APIRouter(tags=["questions"])


@router.post("/api/v1/questions", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    orchestrator: BillLensOrchestrator = Depends(get_orchestrator),
) -> AnswerResponse:
    """
    Ask a question about UK Parliament.
    
    Accepts a question and returns a structured answer with:
    - Summary of findings
    - Evidence from bills, debates, votes, legislation
    - Verification results with confidence scores
    - Sources with links
    """
    try:
        return await orchestrator.answer(request)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        print(f"Error handling question: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}",
        )
