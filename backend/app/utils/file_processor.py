"""Utilitários para processamento de arquivos."""
import io
from typing import Optional
from fastapi import UploadFile
import PyPDF2


class FileProcessor:
    """Classe para processar diferentes tipos de arquivo."""
    
    @staticmethod
    def extract_text_from_file(file: UploadFile) -> str:
        """
        Extrai texto de arquivos .txt ou .pdf.
        
        Args:
            file: Arquivo carregado via FastAPI
            
        Returns:
            Texto extraído do arquivo
            
        Raises:
            ValueError: Se o tipo de arquivo não for suportado
        """
        if not file.filename:
            raise ValueError("Nome do arquivo não encontrado")
        
        file_extension = file.filename.lower().split('.')[-1]
        
        if file_extension == 'txt':
            return FileProcessor._extract_text_from_txt(file)
        elif file_extension == 'pdf':
            return FileProcessor._extract_text_from_pdf(file)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: .{file_extension}. Apenas .txt e .pdf são aceitos.")
    
    @staticmethod
    def _extract_text_from_txt(file: UploadFile) -> str:
        """Extrai texto de arquivo .txt."""
        try:
            content = file.file.read()
            # Tenta decodificar em UTF-8, se falhar tenta latin-1
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                text = content.decode('latin-1')
            
            return text.strip()
        except Exception as e:
            raise ValueError(f"Erro ao ler arquivo de texto: {str(e)}")
        finally:
            file.file.seek(0)  # Reset file pointer
    
    @staticmethod
    def _extract_text_from_pdf(file: UploadFile) -> str:
        """Extrai texto de arquivo .pdf."""
        try:
            # Lê o conteúdo do arquivo
            pdf_content = file.file.read()
            pdf_file = io.BytesIO(pdf_content)
            
            # Usa PyPDF2 para extrair texto
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text_parts = []
            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())
            
            text = '\n'.join(text_parts).strip()
            
            if not text:
                raise ValueError("Não foi possível extrair texto do PDF")
            
            return text
        except Exception as e:
            raise ValueError(f"Erro ao ler arquivo PDF: {str(e)}")
        finally:
            file.file.seek(0)  # Reset file pointer
    
    @staticmethod
    def validate_file_size(file: UploadFile, max_size_mb: int = 5) -> None:
        """
        Valida o tamanho do arquivo.
        
        Args:
            file: Arquivo para validar
            max_size_mb: Tamanho máximo em MB
            
        Raises:
            ValueError: Se o arquivo for muito grande
        """
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        max_size_bytes = max_size_mb * 1024 * 1024
        if file_size > max_size_bytes:
            raise ValueError(f"Arquivo muito grande. Máximo permitido: {max_size_mb}MB")
    
    @staticmethod
    def validate_text_length(text: str, max_length: int = 10000) -> None:
        """
        Valida o comprimento do texto extraído.
        
        Args:
            text: Texto para validar
            max_length: Comprimento máximo permitido
            
        Raises:
            ValueError: Se o texto for muito longo
        """
        if len(text) > max_length:
            raise ValueError(f"Texto muito longo. Máximo permitido: {max_length} caracteres")
        
        if len(text) < 10:
            raise ValueError("Texto muito curto. Mínimo: 10 caracteres")
