"""Schemas para validação de dados de email."""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class EmailSubmissionCreate(BaseModel):
    
    name: str = Field(..., min_length=2, max_length=100, description="Nome do usuário")
    email: EmailStr = Field(..., description="Email válido")
    message: str = Field(..., min_length=10, max_length=1000, description="Mensagem")


class EmailSubmissionResponse(BaseModel):
    
    id: int
    name: str
    email: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class EmailSubmissionList(BaseModel):
    
    submissions: list[EmailSubmissionResponse]
    total: int
