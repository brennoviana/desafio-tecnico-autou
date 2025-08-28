"""Serviços de lógica de negócio para emails."""
from sqlalchemy.orm import Session

from app.repositories.email_repository import EmailRepository
from app.schemas.email import EmailSubmissionCreate, EmailSubmissionResponse, EmailSubmissionList


class EmailService:
    """Serviço de lógica de negócio para operações com emails."""

    def __init__(self, db: Session):
        """Inicializa o service com uma sessão de banco de dados."""
        self.repository = EmailRepository(db)

    async def submit_email(self, email_data: EmailSubmissionCreate) -> EmailSubmissionResponse:
        """Cria uma nova submissão de email no repositório."""
        submission = self.repository.create(email_data)

        return EmailSubmissionResponse.model_validate(submission)

    async def get_submissions(self, skip: int = 0, limit: int = 100) -> EmailSubmissionList:
        """Lista submissões com paginação e contagem total."""
        submissions = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()

        return EmailSubmissionList(
            submissions=[EmailSubmissionResponse.model_validate(sub) for sub in submissions],
            total=total
        )
