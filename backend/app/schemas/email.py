"""Schemas para validação de dados de email."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class EmailSubmissionCreate(BaseModel):
    """Schema para criação de uma nova submissão de email."""

    email_title: str = Field(..., min_length=2, max_length=255, description="Título do email")
    message: str = Field(..., min_length=10, max_length=1000, description="Mensagem")


class EmailSubmissionResponse(BaseModel):
    """Schema para resposta de uma submissão de email."""

    id: int
    email_title: str
    message: str
    ai_classification: Optional[str] = None
    ai_suggested_reply: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class EmailSubmissionList(BaseModel):
    """Schema para lista de submissões de email."""

    submissions: list[EmailSubmissionResponse]
    total: int
