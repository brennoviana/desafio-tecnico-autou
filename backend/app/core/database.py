from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

Base = declarative_base()


class DatabaseManager:
    """Gerenciador de conexões e sessões do banco de dados."""
    
    def __init__(self):
        self.engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            pool_recycle=300
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )
    
    def get_session(self) -> Generator[Session, None, None]:
        """Fornece uma sessão de banco de dados por request e garante o fechamento."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def create_tables(self, drop_first: bool = False):
        """Cria todas as tabelas no banco de dados."""
        if drop_first:
            # Remove todas as tabelas existentes e recria
            Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)


db_manager = DatabaseManager()

def get_db_session() -> Generator[Session, None, None]:
    """Fornece uma sessão de banco de dados por request e garante o fechamento."""
    yield from db_manager.get_session()
