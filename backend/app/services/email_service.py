"""Serviços de lógica de negócio para emails."""
from sqlalchemy.orm import Session

from app.schemas.email import EmailSubmissionCreate, EmailSubmissionResponse, EmailSubmissionList
from app.integrations.ai import OpenAIIntegration
from app.repositories.email_repository import EmailRepository


class EmailService:
    """Serviço de lógica de negócio para operações com emails."""

    def __init__(self, email_repository: EmailRepository, ai_integration: OpenAIIntegration = None):
        """Inicializa o service com uma sessão de banco de dados."""
        self.email_repository = email_repository
        self.ai_integration = ai_integration

    async def submit_email(self, email_data: EmailSubmissionCreate) -> EmailSubmissionResponse:
        """Cria uma nova submissão de email no repositório com classificação de IA."""
        ai_result = None
        try:
            if self.ai_integration:
                ai_result = await self.ai_integration.classify_email(email_data.message)
        except Exception as e:
            print(f"Erro ao processar email com IA: {str(e)}")

        submission = self.email_repository.create(email_data, ai_result)
        return EmailSubmissionResponse.model_validate(submission)

    async def get_submissions(self, skip: int = 0, limit: int = 100) -> EmailSubmissionList:
        """Lista submissões com paginação e contagem total."""
        submissions = self.email_repository.get_all(skip=skip, limit=limit)
        total = self.email_repository.count()

        return EmailSubmissionList(
            submissions=[EmailSubmissionResponse.model_validate(sub) for sub in submissions],
            total=total
        )
