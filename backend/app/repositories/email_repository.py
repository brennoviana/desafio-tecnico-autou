"""Repositório para operações de banco de dados relacionadas a emails."""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.email import EmailSubmission
from app.schemas.email import EmailSubmissionCreate


class EmailRepository:
    """Repositório para operações de banco de dados com emails."""
    
    def __init__(self, db: Session):
        """Inicializa o repositório com uma sessão de banco de dados."""
        self.db = db
    
    def create(self, email_data: EmailSubmissionCreate) -> EmailSubmission:
        """Cria uma nova submissão de email no banco de dados."""
        db_email = EmailSubmission(
            name=email_data.name,
            email=email_data.email,
            message=email_data.message
        )
        self.db.add(db_email)
        self.db.commit()
        self.db.refresh(db_email)
        return db_email
    
    def get_by_id(self, email_id: int) -> Optional[EmailSubmission]:
        """Busca uma submissão de email pelo ID."""
        return self.db.query(EmailSubmission).filter(EmailSubmission.id == email_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[EmailSubmission]:
        """Lista submissões com paginação."""
        return self.db.query(EmailSubmission).offset(skip).limit(limit).all()
    
    def count(self) -> int:
        """Retorna o total de submissões no banco de dados."""
        return self.db.query(EmailSubmission).count()
