"""Endpoints da API para submissão e listagem de emails."""
from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.schemas.email import EmailSubmissionCreate, EmailSubmissionResponse, EmailSubmissionList, TextEmailRequest
from app.services.email_service import EmailService
from app.integrations.ai import OpenAIIntegration
from app.repositories.email_repository import EmailRepository


router = APIRouter()

@router.post("/text", response_model=EmailSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_text_email(
    request: TextEmailRequest,
    db: Session = Depends(get_db_session)
):
    """
    Cria uma nova submissão de email a partir de texto direto.
    
    Recebe JSON com:
    - email_title: título do email
    - content: conteúdo do email como texto direto
    """
    try:
        email_repository = EmailRepository(db)
        service = EmailService(email_repository, OpenAIIntegration())
        result = await service.submit_text_email(
            email_title=request.email_title,
            content=request.content
        )
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


@router.post("/file", response_model=EmailSubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_file_email(
    email_title: str = Form(..., min_length=2, max_length=255, description="Título do email"),
    file: UploadFile = File(..., description="Arquivo .txt ou .pdf"),
    db: Session = Depends(get_db_session)
):
    """
    Cria uma nova submissão de email a partir de arquivo (.txt ou .pdf).
    
    Parâmetros:
    - email_title: título do email
    - file: arquivo .txt ou .pdf contendo o conteúdo do email
    """
    try:
        email_repository = EmailRepository(db)
        service = EmailService(email_repository, OpenAIIntegration())
        result = await service.submit_file_email(
            email_title=email_title,
            file=file
        )
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
