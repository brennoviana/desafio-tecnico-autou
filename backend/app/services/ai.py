"""Serviço de IA para classificação e processamento de emails."""
from typing import Optional
from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.core.config import settings


class AIService:
    """Serviço para operações de IA utilizando OpenAI."""

    def __init__(self):
        """Inicializa o serviço de IA com a configuração da API."""
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY não configurada nas variáveis de ambiente")
        
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def classify_email(self, email_text: str) -> Optional[str]:
        """
        Classifica um email como PRODUTIVO ou IMPRODUTIVO e sugere uma resposta.
        
        Args:
            email_text: Texto do email a ser classificado
            
        Returns:
            Resultado da classificação e sugestão de resposta
            
        Raises:
            ValueError: Se o texto do email estiver vazio
            Exception: Para erros da API do OpenAI
        """
        if not email_text or not email_text.strip():
            raise ValueError("Texto do email não pode estar vazio")

        prompt = f"""
        Classifique o seguinte email como PRODUTIVO ou IMPRODUTIVO, de acordo com as definições abaixo:

        - PRODUTIVO: Emails que requerem ação ou resposta específica (ex.: solicitações de suporte, atualização sobre casos em aberto, dúvidas sobre o sistema).
        - IMPRODUTIVO: Emails que não necessitam de ação imediata (ex.: felicitações, agradecimentos).

        Depois de classificar, sugira uma resposta automática apenas se for PRODUTIVO. 
        Se for IMPRODUTIVO, indique que não é necessária ação.

        Formato de resposta:
        Categoria: <Produtivo/Improdutivo>
        Sugestão de resposta: <texto ou "Nenhuma ação necessária">

        Email: "{email_text}"
        """

        try:
            response: ChatCompletion = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Erro ao classificar email: {str(e)}")
            
            # Tratamento específico para diferentes tipos de erro
            if "insufficient_quota" in str(e):
                raise Exception("Cota da API OpenAI excedida. Verifique seu plano e faturamento.")
            elif "rate_limit" in str(e):
                raise Exception("Limite de taxa da API OpenAI excedido. Tente novamente em alguns segundos.")
            else:
                raise Exception(f"Erro na API OpenAI: {str(e)}")