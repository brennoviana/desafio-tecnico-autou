"""Serviços de lógica de negócio para emails."""
from typing import Optional, List
from fastapi import UploadFile
from app.schemas.email import EmailSubmissionCreate, EmailSubmissionResponse, EmailSubmissionList, DeleteEmailsResponse, EmailStatsResponse
from app.integrations.ai import OpenAIIntegration
from app.repositories.email_repository import EmailRepository
from app.utils.file_processor import FileProcessor


class EmailService:
    """Serviço de lógica de negócio para operações com emails."""

    def __init__(self, email_repository: EmailRepository, ai_integration: OpenAIIntegration = None):
        """Inicializa o service com uma sessão de banco de dados."""
        self.email_repository = email_repository
        self.ai_integration = ai_integration

    async def submit_text_email(
        self, 
        email_title: str,
        content: str
    ) -> EmailSubmissionResponse:
        """Cria submissão de email a partir de texto direto."""
        try:
            if not content or not content.strip():
                raise ValueError("Conteúdo não pode estar vazio")
            
            email_data = EmailSubmissionCreate(
                email_title=email_title,
                content=content.strip(),
                type="Texto puro"
            )
            
            ai_result = self.ai_integration.classify_email(email_data.content)

            submission = self.email_repository.create(email_data, ai_result)
            return EmailSubmissionResponse.model_validate(submission)
            
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Erro ao processar email de texto: {str(e)}")
            raise e

    async def submit_file_email(
        self, 
        email_title: str,
        file: UploadFile
    ) -> EmailSubmissionResponse:
        """Cria submissão de email a partir de arquivo (.txt ou .pdf)."""
        try:
            if not file.filename:
                raise ValueError("Nome do arquivo é obrigatório")
            
            file_extension = file.filename.lower().split('.')[-1]
            if file_extension not in ['txt', 'pdf']:
                raise ValueError("Apenas arquivos .txt e .pdf são aceitos")
            
            FileProcessor.validate_file_size(file, max_size_mb=5)
            
            if file_extension == 'txt':
                final_content = FileProcessor._extract_text_from_txt(file)
                file_type = "TXT"
            elif file_extension == 'pdf':
                final_content = FileProcessor._extract_text_from_pdf(file)
                file_type = "PDF"
            else:
                raise ValueError("Tipo de arquivo não suportado")
            
            FileProcessor.validate_text_length(final_content)
            
            if not final_content or not final_content.strip():
                raise ValueError("Não foi possível extrair conteúdo do arquivo")
            
            email_data = EmailSubmissionCreate(
                email_title=email_title,
                content=final_content.strip(),
                type=file_type
            )
            
            ai_result = self.ai_integration.classify_email(email_data.content)

            submission = self.email_repository.create(email_data, ai_result)
            return EmailSubmissionResponse.model_validate(submission)
            
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Erro ao processar email de arquivo: {str(e)}")
            raise e

    async def get_submissions(self, skip: int, limit: int, email_title: Optional[str] = None) -> EmailSubmissionList:
        """Lista submissões com paginação, contagem total e filtro opcional por título."""
        try:
            submissions = self.email_repository.get_all(skip=skip, limit=limit, email_title=email_title)
            total = self.email_repository.count(email_title=email_title)

            return EmailSubmissionList(
                submissions=[EmailSubmissionResponse.model_validate(sub) for sub in submissions],
                total=total
            )
        except Exception as e:
            print("Erro ao listar submissões")
            raise e

    async def delete_emails(self, ids: List[int]) -> DeleteEmailsResponse:
        """Deleta emails por uma lista de IDs."""
        try:
            if not ids:
                raise ValueError("Lista de IDs não pode estar vazia")
            
            if len(ids) > 100:
                raise ValueError("Não é possível deletar mais de 100 emails por vez")
            
            for email_id in ids:
                if not isinstance(email_id, int) or email_id <= 0:
                    raise ValueError(f"ID inválido: {email_id}")
            
            deleted_ids, not_found_ids = self.email_repository.delete_by_ids(ids)
            
            return DeleteEmailsResponse(
                deleted_count=len(deleted_ids),
                deleted_ids=deleted_ids,
                not_found_ids=not_found_ids if not_found_ids else None
            )
            
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Erro ao deletar emails: {str(e)}")
            raise e

    async def get_statistics(self) -> EmailStatsResponse:
        """Retorna estatísticas dos emails."""
        try:
            stats = self.email_repository.get_statistics()
            return EmailStatsResponse(**stats)
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {str(e)}")
            raise e