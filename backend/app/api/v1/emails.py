"""Endpoints da API para submissão e listagem de emails."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.email import EmailSubmissionCreate, EmailSubmissionResponse, EmailSubmissionList
from app.services.email_service import EmailService
from app.integration.ai import OpenAIIntegration


router = APIRouter()

@router.post("/", response_model=EmailSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_email(
    email_data: EmailSubmissionCreate,
    db: Session = Depends(get_db)
):
    """Cria uma nova submissão de email."""
    try:
        service = EmailService(db, OpenAIIntegration())
        result = await service.submit_email(email_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar email: {str(e)}"
        ) from e


@router.get("/", response_model=EmailSubmissionList)
async def list_submissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista submissões com paginação (máx. 100)."""
    try:
        if limit > 100:
            limit = 100

        service = EmailService(db)

        result = await service.get_submissions(skip=skip, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar submissões: {str(e)}"
        ) from e
