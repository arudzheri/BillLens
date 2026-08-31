"""
Question endpoints.
"""

from __future__ import annotations

import traceback
import logging
from fastapi import APIRouter, Depends, HTTPException
from billlens.models.question import QuestionRequest
from billlens.models.answer import AnswerResponse, AnswerClaim, AnswerSource
from billlens.agent.orchestrator import BillLensOrchestrator
from ..dependencies import get_orchestrator

# Set up logging
logger = logging.getLogger(__name__)

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
        logger.info(f"Processing question: {request.question}")
        answer = await orchestrator.answer(request)
        logger.info(f"Successfully generated answer for: {request.question}")
        return answer
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error handling question: {e}", exc_info=True)
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}",
        )


@router.post("/api/v1/questions/test", response_model=AnswerResponse)
async def test_question(request: QuestionRequest) -> AnswerResponse:
    """
    Test endpoint that returns sample parliamentary data without requiring full orchestration.
    Useful for debugging and testing the frontend.
    """
    return AnswerResponse(
        question=request.question,
        summary="Based on parliamentary records: Housing legislation has been a key focus of recent parliamentary sessions. Multiple bills and debates have addressed housing affordability, planning reforms, and tenant protections.",
        what_happened=[
            "Parliament debated housing affordability crisis",
            "Planning reform proposals introduced to speed up housebuilding",
            "Tenant protection measures discussed in recent sessions",
        ],
        legislation=[
            "Housing Act 2004 - Requires landlords to meet minimum rental standards",
            "Planning and Infrastructure Act 2024 - Speeds up housebuilding and reforms planning permissions",
            "Renters Reform Bill 2024 - Proposes abolishing no-fault evictions",
            "Levelling Up Act 2023 - Includes housing regeneration and local authority housing provisions",
        ],
        parliamentary_activity=[
            "Commons debate on housing crisis (June 2024)",
            "Select Committee review of housing policy effectiveness",
            "Hansard records of parliamentary discussions on affordability",
        ],
        votes=[
            "Parliamentary vote on Housing Act amendments (passed 324-156)",
            "Planning reform bill second reading (approved)",
        ],
        what_did_not_happen=[],
        claims=[
            AnswerClaim(
                text="The Housing Act 2004 reformed housing standards and introduced selective licensing",
                supported=True,
                confidence=0.95,
                sources=[
                    AnswerSource(
                        title="Housing Act 2004",
                        source_type="legislation",
                        url="https://legislation.gov.uk/ukpga/2004/34",
                        date="2004-07-18",
                    )
                ],
            ),
            AnswerClaim(
                text="Recent planning reforms aim to increase housing supply",
                supported=True,
                confidence=0.9,
                sources=[
                    AnswerSource(
                        title="Planning and Infrastructure Act 2024",
                        source_type="bill",
                        url="https://bills.parliament.uk/planning",
                        date="2024-01-15",
                    )
                ],
            ),
        ],
        sources=[
            AnswerSource(
                title="Housing Act 2004",
                source_type="legislation",
                url="https://legislation.gov.uk/ukpga/2004/34",
                date="2004-07-18",
            ),
            AnswerSource(
                title="Planning and Infrastructure Act 2024",
                source_type="bill",
                url="https://bills.parliament.uk/planning",
                date="2024-01-15",
            ),
            AnswerSource(
                title="Renters Reform Bill 2024",
                source_type="bill",
                url="https://bills.parliament.uk/renters-reform",
                date="2024-05-10",
            ),
            AnswerSource(
                title="Levelling Up Act 2023",
                source_type="legislation",
                url="https://legislation.gov.uk/ukpga/2023/55",
                date="2023-04-26",
            ),
        ],
        confidence=0.92,
        warnings=[],
    )
