"""
Repository pattern for data access.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from billlens.models.question import QuestionRequest
from billlens.models.answer import AnswerResponse
from billlens.models.evidence import Evidence as EvidenceModel

from .models import (
    Question,
    ResearchRun,
    Evidence,
    Answer,
)


class QuestionRepository:
    """Repository for questions."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(
        self,
        request: QuestionRequest,
    ) -> str:
        """Create and store a question."""
        
        question_id = str(uuid.uuid4())
        
        question = Question(
            id=question_id,
            question_text=request.question,
        )
        
        self.session.add(question)
        await self.session.commit()
        
        return question_id
    
    async def get_by_id(
        self,
        question_id: str,
    ) -> Question | None:
        """Retrieve a question by ID."""
        
        result = await self.session.execute(
            select(Question).where(
                Question.id == question_id
            )
        )
        
        return result.scalar_one_or_none()


class ResearchRunRepository:
    """Repository for research runs."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(
        self,
        question_id: str,
        topic: str,
    ) -> str:
        """Create a research run record."""
        
        run_id = str(uuid.uuid4())
        
        run = ResearchRun(
            id=run_id,
            question_id=question_id,
            topic=topic,
        )
        
        self.session.add(run)
        await self.session.commit()
        
        return run_id
    
    async def update_steps(
        self,
        run_id: str,
        completed: list[str],
        failed: list[str],
    ) -> None:
        """Update completed and failed steps."""
        
        result = await self.session.execute(
            select(ResearchRun).where(
                ResearchRun.id == run_id
            )
        )
        
        run = result.scalar_one_or_none()
        
        if run:
            run.completed_steps = completed
            run.failed_steps = failed
            await self.session.commit()


class EvidenceRepository:
    """Repository for evidence."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_batch(
        self,
        run_id: str,
        evidence_list: list[EvidenceModel],
    ) -> None:
        """Store multiple evidence items."""
        
        for item in evidence_list:
            evidence = Evidence(
                id=str(uuid.uuid4()),
                research_run_id=run_id,
                title=item.title,
                source_type=item.source_type,
                url=item.url,
                content=item.content,
                date=item.date,
                relevance_score=item.relevance_score,
                meta=item.metadata,
            )
            
            self.session.add(evidence)
        
        await self.session.commit()


class AnswerRepository:
    """Repository for answers."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(
        self,
        question_id: str,
        answer: AnswerResponse,
    ) -> str:
        """Store an answer response."""
        
        answer_id = str(uuid.uuid4())
        
        stored_answer = Answer(
            id=answer_id,
            question_id=question_id,
            summary=answer.summary,
            what_happened=answer.what_happened,
            legislation=answer.legislation,
            parliamentary_activity=answer.parliamentary_activity,
            votes=answer.votes,
            what_did_not_happen=answer.what_did_not_happen,
            claims=[
                c.model_dump()
                for c in answer.claims
            ],
            sources=[
                s.model_dump()
                for s in answer.sources
            ],
            confidence=answer.confidence,
            warnings=answer.warnings,
        )
        
        self.session.add(stored_answer)
        await self.session.commit()
        
        return answer_id
    
    async def get_by_id(
        self,
        answer_id: str,
    ) -> Answer | None:
        """Retrieve an answer by ID."""
        
        result = await self.session.execute(
            select(Answer).where(
                Answer.id == answer_id
            )
        )
        
        return result.scalar_one_or_none()