"""Repositório para operações de banco de dados relacionadas a emails."""
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session

from app.models.email import EmailSubmission
from app.schemas.email import EmailSubmissionCreate


class EmailRepository:
    """Repositório para operações de banco de dados com emails."""
    
    def __init__(self, db: Session):
        """Inicializa o repositório com uma sessão de banco de dados."""
        self.db = db
    
    def create(self, email_data: EmailSubmissionCreate, ai_data: Dict[str, Any]) -> EmailSubmission:
        """Cria uma nova submissão de email no banco de dados."""
        db_email = EmailSubmission(
            email_title=email_data.email_title,
            message=email_data.content,
            type=email_data.type,
            ai_classification=ai_data.get("classification"),
            ai_suggested_reply=ai_data.get("suggested_reply")
        )
        self.db.add(db_email)
        self.db.commit()
        self.db.refresh(db_email)
        return db_email
    
    def get_by_id(self, email_id: int) -> Optional[EmailSubmission]:
        """Busca uma submissão de email pelo ID."""
        return self.db.query(EmailSubmission).filter(EmailSubmission.id == email_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, email_title: Optional[str] = None) -> List[EmailSubmission]:
        """Lista submissões com paginação e filtro opcional por título."""
        query = self.db.query(EmailSubmission)
        
        if email_title:
            query = query.filter(EmailSubmission.email_title.ilike(f"%{email_title}%"))
        
        return query.offset(skip).limit(limit).all()
    
    def count(self, email_title: Optional[str] = None) -> int:
        """Retorna o total de submissões no banco de dados com filtro opcional por título."""
        query = self.db.query(EmailSubmission)
        
        if email_title:
            query = query.filter(EmailSubmission.email_title.ilike(f"%{email_title}%"))
        
        return query.count()
    
    def delete_by_ids(self, ids: List[int]) -> Tuple[List[int], List[int]]:
        """
        Deleta emails por uma lista de IDs.
        
        Returns:
            Tuple contendo:
            - Lista de IDs que foram deletados com sucesso
            - Lista de IDs que não foram encontrados
        """
        # Primeiro, verifica quais IDs existem
        existing_emails = self.db.query(EmailSubmission).filter(EmailSubmission.id.in_(ids)).all()
        existing_ids = [email.id for email in existing_emails]
        not_found_ids = [id for id in ids if id not in existing_ids]
        
        # Deleta os emails encontrados
        if existing_ids:
            deleted_count = self.db.query(EmailSubmission).filter(EmailSubmission.id.in_(existing_ids)).delete(synchronize_session=False)
            self.db.commit()
        
        return existing_ids, not_found_ids
    
    def delete_by_id(self, email_id: int) -> bool:
        """
        Deleta um email pelo ID.
        
        Returns:
            True se deletado com sucesso, False se não encontrado
        """
        email = self.get_by_id(email_id)
        if email:
            self.db.delete(email)
            self.db.commit()
            return True
        return False