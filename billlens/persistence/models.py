"""
SQLAlchemy models for persistence.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Text,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class Question(Base):
    """Stored user question."""
    
    __tablename__ = "questions"
    
    id = Column(String(36), primary_key=True)
    question_text = Column(String(2000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class ResearchRun(Base):
    """Research execution record."""
    
    __tablename__ = "research_runs"
    
    id = Column(String(36), primary_key=True)
    question_id = Column(
        String(36),
        ForeignKey("questions.id"),
        nullable=False,
    )
    topic = Column(String(500), nullable=False)
    completed_steps = Column(JSON, default=list)
    failed_steps = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class Evidence(Base):
    """Retrieved evidence."""
    
    __tablename__ = "evidence"
    
    id = Column(String(36), primary_key=True)
    research_run_id = Column(
        String(36),
        ForeignKey("research_runs.id"),
        nullable=False,
    )
    title = Column(String(500), nullable=False)
    source_type = Column(String(50), nullable=False)
    url = Column(String(2000))
    content = Column(Text)
    date = Column(String(50))
    relevance_score = Column(Float, default=0.0)
    meta = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class Answer(Base):
    """Stored answer response."""
    
    __tablename__ = "answers"
    
    id = Column(String(36), primary_key=True)
    question_id = Column(
        String(36),
        ForeignKey("questions.id"),
        nullable=False,
    )
    summary = Column(Text)
    what_happened = Column(JSON, default=list)
    legislation = Column(JSON, default=list)
    parliamentary_activity = Column(JSON, default=list)
    votes = Column(JSON, default=list)
    what_did_not_happen = Column(JSON, default=list)
    claims = Column(JSON, default=list)
    sources = Column(JSON, default=list)
    confidence = Column(Float, default=0.0)
    warnings = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)