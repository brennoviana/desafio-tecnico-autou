"""Serviço de IA para classificação e processamento de emails."""
from typing import Dict, Any
import re
from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.core.config import settings


class OpenAIIntegration:
    """Serviço para operações de IA utilizando OpenAI."""

    def __init__(self):
        """Inicializa o serviço de IA com a configuração da API."""
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def classify_email(self, email_text: str) -> Dict[str, Any]:
        """
        Classifica um email como PRODUTIVO ou IMPRODUTIVO e sugere uma resposta.
        
        Args:
            email_text: Texto do email a ser classificado
            
        Returns:
            Dicionário com classificação, resposta completa da IA e sugestão extraída
            
        Raises:
            ValueError: Se o texto do email estiver vazio
            Exception: Para erros da API do OpenAI
        """

        try:
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

            response: ChatCompletion = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            
            parsed_response = self._parse_ai_response(ai_response)
            
            return {
                "classification": parsed_response["classification"],
                "suggested_reply": parsed_response["suggested_reply"]
            }
            
        except Exception as e:
            print("Erro ao classificar email")
            raise e

    def _parse_ai_response(self, ai_response: str) -> Dict[str, str]:
        """
        Extrai a classificação e sugestão de resposta da resposta da IA.
        
        Args:
            ai_response: Resposta completa da IA
            
        Returns:
            Dicionário com classificação e sugestão extraídas
        """
        try:
            if not ai_response:
                return {"classification": "INDEFINIDO", "suggested_reply": "Erro no processamento"}
            
            classification_match = re.search(r'Categoria:\s*(Produtivo|Improdutivo|PRODUTIVO|IMPRODUTIVO)', ai_response, re.IGNORECASE)
            classification = classification_match.group(1).upper() if classification_match else "INDEFINIDO"
            
            suggestion_match = re.search(r'Sugestão de resposta:\s*(.+?)(?:\n|$)', ai_response, re.DOTALL)
            if suggestion_match:
                suggested_reply = suggestion_match.group(1).strip()
                suggested_reply = suggested_reply.strip('"').strip("'")
            else:
                suggested_reply = "Nenhuma sugestão extraída"
            
            return {
                    "classification": classification,
                    "suggested_reply": suggested_reply
                }
        except Exception as e:
            print("Erro ao processar resposta da IA")
            raise e