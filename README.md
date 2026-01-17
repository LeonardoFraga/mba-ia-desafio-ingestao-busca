# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto implementa um sistema de ingestão e busca de documentos PDF usando IA, com armazenamento vetorial em PostgreSQL via PGVector.

## Como Executar

### 1. Instalar Dependências
Instale os pacotes Python listados em `requirements.txt`:
```
pip install -r requirements.txt
```

### 2. Subir o Banco de Dados
Inicie o PostgreSQL via Docker Compose:
```
docker compose up -d
```

### 3. Configurar Variáveis de Ambiente
- Copie o arquivo `.env.example` para `.env`:
  ```
  cp .env.example .env
  ```
- Edite o `.env` e adicione as chaves de API necessárias (Google, OpenAI) e outras configurações.

### 4. Executar Ingestão do PDF
- Se estiver em Mac ou Linux:
  ```
  make ingest
  ```
- Caso contrário:
  ```
  python3 src/ingest.py
  ```

Isso processará o PDF especificado em `PDF_PATH`, dividirá o texto em chunks, gerará embeddings e armazenará no banco de dados.