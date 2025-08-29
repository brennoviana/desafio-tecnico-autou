"""Endpoints da API para submissão e listagem de emails."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.schemas.email import EmailSubmissionCreate, EmailSubmissionResponse, EmailSubmissionList
from app.services.email_service import EmailService
from app.integrations.ai import OpenAIIntegration
from app.repositories.email_repository import EmailRepository


router = APIRouter()

@router.post("/", response_model=EmailSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_email(
    email_data: EmailSubmissionCreate,
    db: Session = Depends(get_db_session)
):
    """Cria uma nova submissão de email."""
    try:
        if not email_data.message:
            raise ValueError("Mensagem do email não pode estar vazia")
        if not email_data.email_title:
            raise ValueError("Título do email não pode estar vazio")

        email_repository = EmailRepository(db)
        service = EmailService(email_repository, OpenAIIntegration())
        result = await service.submit_email(email_data)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dados inválidos: {str(e)}"
        ) from e
    except Exception as e:
        print(f"Erro ao processar email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        ) from e


@router.get("/", response_model=EmailSubmissionList)
async def list_submissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session)
):
    """Lista submissões com paginação (máx. 100)."""
    try:
        if skip < 0:
            raise ValueError("Parâmetro 'skip' deve ser maior ou igual a zero")
        if limit <= 0:
            raise ValueError("Parâmetro 'limit' deve ser maior que zero")
        if limit > 100:
            limit = 100

        email_repository = EmailRepository(db)
        service = EmailService(email_repository)
        result = await service.get_submissions(skip=skip, limit=limit)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Parâmetros inválidos: {str(e)}"
        ) from e
    except Exception as e:
        print(f"Erro ao buscar submissões: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        ) from e
