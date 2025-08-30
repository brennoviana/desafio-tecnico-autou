"""Endpoints da API para submissão e listagem de emails."""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.schemas.email import EmailSubmissionResponse, EmailSubmissionList, TextEmailRequest, FileEmailRequest, ListEmailRequest
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

        if not request.email_title or not request.content:
            raise ValueError("Título e conteúdo são obrigatórios")
        
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
    request: FileEmailRequest,
    file: UploadFile = File(..., description="Arquivo .txt ou .pdf"),
    db: Session = Depends(get_db_session)
):
    """
    Cria uma nova submissão de email a partir de arquivo (.txt ou .pdf).
    
    Parâmetros:
    - request: dados do email (email_title)
    - file: arquivo .txt ou .pdf contendo o conteúdo do email
    """
    try:
        if not request.email_title:
            raise ValueError("Título é obrigatório")
            
        email_repository = EmailRepository(db)
        service = EmailService(email_repository, OpenAIIntegration())
        result = await service.submit_file_email(
            email_title=request.email_title,
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


@router.get("/", response_model=EmailSubmissionList, status_code=status.HTTP_200_OK)
async def list_submissions(
    request: ListEmailRequest,
    db: Session = Depends(get_db_session)
):
    """Lista submissões com paginação (máx. 100)."""
    try:
        skip = request.skip
        limit = request.limit

        
        if skip < 0:
            raise ValueError("Parâmetro 'skip' deve ser maior ou igual a zero")
        if limit <= 0 or limit > 100:
            raise ValueError("Parâmetro 'limit' deve ser maior que zero")


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
