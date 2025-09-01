# 📧 Sistema de Classificação Inteligente de Emails

Sistema web para classificação automática de emails utilizando Inteligência Artificial, desenvolvido com FastAPI, React e OpenAI GPT-4.

## 🚀 Funcionalidades

- **Classificação Inteligente**: Classifica emails como "Produtivo" ou "Improdutivo" usando GPT-4
- **Processamento de Arquivos**: Suporte para upload de arquivos PDF, TXT e texto puro
- **Interface Moderna**: Dashboard responsivo com estatísticas
- **Busca e Filtros**: Pesquisa por título e filtros avançados
- **Gerenciamento**: Exclusão em lote e paginação
- **NLP Avançado**: Pré-processamento com tokenização, stemming e remoção de stopwords

## 🛠 Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **OpenAI GPT-4** - Modelo de linguagem para classificação
- **NLTK** - Processamento de linguagem natural
- **PyPDF2** - Extração de texto de PDFs
- **Pydantic** - Validação e gerenciamento de dados em Python

### Frontend
- **React** - Biblioteca para interfaces de usuário
- **TypeScript** - JavaScript com tipagem estática
- **Ant Design** - Biblioteca de componentes UI
- **Vite** - Build tool moderna
- **Bun** - Runtime JavaScript rápido

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Nginx** - Proxy reverso com suporte a SSL/HTTPS
- **Let's Encrypt** - Certificados SSL
- **Poetry** - Gerenciamento de dependências Python

## 📋 Pré-requisitos

- Docker e Docker Compose
- Chave da API OpenAI
- Git

## 🔧 Configuração e Instalação

### 1. Clone o repositório

### 2. Configure as variáveis de ambiente
Copie o arquivo `.env.docker.example` para `.env` e configure as variáveis:

```bash
cp .env.docker.example .env
```

**⚠️ Importante**: Para obter a chave da API OpenAI, entre em contato comigo, pois este repositório é público e não posso expor a chave.

### 3. Execute o projeto
```bash
docker-compose up -d
```

### 4. Acesse a aplicação
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

> 🔒 **Produção**: O sistema está configurado com nginx e certificados SSL para deployment em servidor, proporcionando acesso seguro via HTTPS.

## 🎯 Como Usar

### 1. Classificar Email por Texto
1. Clique em "Novo Email"
2. Selecione "Texto Direto"
3. Digite o título e conteúdo do email
4. Clique em "Processar"

### 2. Classificar Email por Arquivo
1. Clique em "Novo Email"
2. Selecione "Upload Arquivo"
3. Digite o título
4. Faça upload do arquivo (.txt ou .pdf, máx. 5MB)
5. Clique em "Processar"

### 3. Gerenciar Emails
- **Buscar**: Use a barra de pesquisa para filtrar por título
- **Ordenar**: Clique nos cabeçalhos das colunas
- **Excluir**: Selecione emails e clique em "Deletar"
- **Visualizar**: Passe o mouse sobre textos longos para ver o conteúdo completo

## 📊 Categorias de Classificação

### 📈 Produtivo
Emails que requerem ação ou resposta:
- Solicitações de suporte
- Perguntas sobre produtos/serviços
- Pedidos de informação
- Reclamações que precisam de resolução

### 📉 Improdutivo  
Emails que não requerem ação específica:
- Agradecimentos
- Confirmações automáticas
- Newsletters
- Spam ou conteúdo irrelevante

## 🔍 Processamento de IA

O sistema utiliza técnicas avançadas de NLP:

1. **Pré-processamento**:
   - Tokenização
   - Normalização (lowercase)
   - Remoção de stopwords
   - Stemming (RSLP para português)
   - Filtragem de URLs e emails

2. **Classificação**:
   - Prompt engineering com exemplos
   - GPT-4 para análise semântica
   - Parsing estruturado da resposta

3. **Resposta Sugerida**:
   - Geração contextual baseada na classificação
   - Adequada ao tipo de email identificado

## 🚨 Troubleshooting

### Problema: Erro de conexão com OpenAI
- Verifique se a `OPENAI_API_KEY` está configurada corretamente
- Confirme se há créditos na conta OpenAI

### Problema: Frontend não carrega
- Verifique se `VITE_API_BASE_URL` aponta para o backend correto
- Confirme se o backend está rodando na porta 8000

### Problema: Erro no banco de dados
- Execute: `docker-compose down -v && docker-compose up -d`
- Isso recria o volume do PostgreSQL

## 📈 Métricas e Monitoramento

O sistema fornece estatísticas
- Total de emails processados
- Distribuição por categoria (Produtivo/Improdutivo)
- Tipos de arquivo processados (PDF, TXT, Texto Puro)

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🎥 Demo

[Adicione aqui o link para o vídeo de demonstração ou GIFs mostrando o sistema em funcionamento]

---