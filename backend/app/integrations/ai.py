"""Serviço de IA para classificação e processamento de emails."""
from typing import Dict, Any
import re, json
from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.core.config import settings

from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
import nltk

from app.core.config import settings

nltk.download('rslp')
nltk.download('stopwords')
nltk.download('punkt_tab')


class OpenAIIntegration:
    """Serviço para operações de IA utilizando OpenAI."""

    def __init__(self):
        """Inicializa o serviço de IA com a configuração da API."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.training_examples = [
            {
                "email": "Preciso de ajuda com o sistema que não está funcionando",
                "classification": "PRODUTIVO",
                "reply": "Recebemos sua solicitação de suporte. Nossa equipe técnica irá analisar o problema e retornar em até 24 horas com uma solução."
            },
            {
                "email": "Obrigado pelo excelente atendimento da equipe",
                "classification": "IMPRODUTIVO", 
                "reply": "Nenhuma ação necessária"
            },
            {
                "email": "Quando será lançada a nova versão do sistema?",
                "classification": "PRODUTIVO",
                "reply": "Obrigado pela pergunta. A nova versão está prevista para lançamento no próximo trimestre. Manteremos você informado sobre atualizações."
            },
            {
                "email": "Parabéns pelo sucesso do projeto!",
                "classification": "IMPRODUTIVO",
                "reply": "Nenhuma ação necessária"
            }
        ]

    def classify_email(self, email_text: str) -> Dict[str, Any]:
        """
        Classifica um email como PRODUTIVO ou IMPRODUTIVO e sugere uma resposta.
        
        Args:
            email_text: Texto do email a ser classificado
            
        Returns:
            Dicionário com classificação e sugestão extraída
            
        Raises:
            ValueError: Se o texto do email estiver vazio
            Exception: Para erros da API do OpenAI
        """

        try:
            processed_text = self._preprocess_text(email_text, advanced_preprocessing=True)

            prompt = self._build_dynamic_prompt(processed_text)

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
        Extrai a classificação e sugestão de resposta da resposta JSON da IA.
        """
        try:
            if not ai_response:
                return {"classification": "INDEFINIDO", "suggested_reply": "Erro no processamento"}
            
            data = json.loads(ai_response)

            classification = data.get("classification", "INDEFINIDO").upper()
            suggested_reply = data.get("suggested_reply", "Nenhuma sugestão extraída")

            return {
                "classification": classification,
                "suggested_reply": suggested_reply
            }

        except Exception as e:
            return {
                "classification": "INDEFINIDO",
                "suggested_reply": "Erro ao interpretar resposta da IA"
            }


    def _preprocess_text(self, text: str, advanced_preprocessing: bool = False) -> str:
        """
        Pré-processamento NLP conforme especificações do desafio.
        
        Técnicas aplicadas:
        1. Tokenização - Divisão em palavras individuais
        2. Normalização - Conversão para lowercase
        3. Remoção de stopwords - Remove palavras sem valor semântico
        4. Stemming - Reduz palavras ao radical para generalização
        5. Filtragem - Remove tokens não alfabéticos e muito curtos
        """
        if not text or not text.strip():
            return ""
        
        text = re.sub(r'http[s]?://\S+', '[URL]', text)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        text = re.sub(r'\s+', ' ', text)
    
        if advanced_preprocessing:
            stemmer = RSLPStemmer()
            stop_words = set(stopwords.words("portuguese"))
            
            tokens = word_tokenize(text.lower())
            tokens = [
                stemmer.stem(w) for w in tokens 
                if w.isalpha() and w not in stop_words and len(w) > 2
            ]
            return " ".join(tokens)
        
        return text.strip()

    def _build_dynamic_prompt(self, email_text: str) -> str:
        """
        Constrói prompt dinâmico usando os exemplos de treinamento.
        """
        examples_text = ""
        for example in self.training_examples:
            examples_text += f"""
            Email: "{example['email']}"
            Categoria: {example['classification']}
            Sugestão de resposta: "{example['reply']}"
            """
        
        return f"""
            Você é um assistente especializado em classificação de emails corporativos.

            DEFINIÇÕES:
            - PRODUTIVO: Emails que requerem ação ou resposta específica.
            - IMPRODUTIVO: Emails que não necessitam de ação imediata.

            EXEMPLOS:
            {examples_text}

            AGORA CLASSIFIQUE O EMAIL ABAIXO:

            Email: "{email_text}"

            INSTRUÇÕES IMPORTANTES:
            - Só utilize as categorias PRODUTIVO ou IMPRODUTIVO.
            - A sugestão de resposta deve ser objetiva e em tom profissional.
            - Responda APENAS no formato JSON abaixo, sem texto extra:

            {{
            "classification": "<PRODUTIVO ou IMPRODUTIVO>",
            "suggested_reply": "<texto ou 'Nenhuma ação necessária'>"
            }}
        """
