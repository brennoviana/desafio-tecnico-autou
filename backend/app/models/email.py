"""Modelos SQLAlchemy para emails."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, func

from app.core.database import Base


class EmailSubmission(Base):
    
    __tablename__ = "email_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    email_title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(20), nullable=False)
    ai_classification = Column(String(50), nullable=False)
    ai_suggested_reply = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.timezone('America/Sao_Paulo', func.now()))
    
    def __repr__(self):
        return f"<EmailSubmission(id={self.id}, email_title={self.email_title}, classification={self.ai_classification})>"
