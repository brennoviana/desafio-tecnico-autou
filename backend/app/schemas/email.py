"""Schemas para validação de dados de email."""
from datetime import datetime
from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class TextEmailRequest(BaseModel):
    """Schema para submissão de email via texto direto."""
    
    email_title: str = Field(..., min_length=2, max_length=255, description="Título do email")
    content: str = Field(..., min_length=10, max_length=10000, description="Conteúdo da mensagem")


class FileEmailRequest(BaseModel):
    """Schema para submissão de email via arquivo."""
    
    email_title: str = Field(..., min_length=2, max_length=255, description="Título do email")

class EmailSubmissionCreate(BaseModel):
    """Schema para criação de uma nova submissão de email."""

    email_title: str = Field(..., min_length=2, max_length=255, description="Título do email")
    content: str = Field(..., min_length=10, max_length=10000, description="Conteúdo da mensagem")
    type: Literal["Texto puro", "TXT", "PDF"] = Field(..., description="Tipo de entrada do conteúdo")


class EmailSubmissionResponse(BaseModel):
    """Schema para resposta de uma submissão de email."""

    id: int
    email_title: str
    message: str
    type: str
    ai_classification: Optional[str] = None
    ai_suggested_reply: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class EmailSubmissionList(BaseModel):
    """Schema para lista de submissões de email."""

    submissions: list[EmailSubmissionResponse]
    total: int

class DeleteEmailsRequest(BaseModel):
    """Schema para requisição de exclusão de emails por IDs."""
    
    ids: List[int] = Field(..., min_length=1, max_length=100, description="Lista de IDs dos emails para deletar")

class DeleteEmailsResponse(BaseModel):
    """Schema para resposta de exclusão de emails."""
    
    deleted_count: int = Field(..., description="Quantidade de emails deletados")
    deleted_ids: List[int] = Field(..., description="Lista de IDs que foram deletados")
    not_found_ids: Optional[List[int]] = Field(default=None, description="Lista de IDs que não foram encontrados")

class EmailStatsResponse(BaseModel):
    """Schema para estatísticas de emails."""
    
    total: int = Field(..., description="Total de emails")
    produtivos: int = Field(..., description="Emails classificados como produtivos")
    improdutivos: int = Field(..., description="Emails classificados como improdutivos")
    nao_classificados: int = Field(..., description="Emails não classificados pela IA")
    pdf: int = Field(..., description="Emails do tipo PDF")
    txt: int = Field(..., description="Emails do tipo TXT")
    texto_puro: int = Field(..., description="Emails do tipo texto puro")