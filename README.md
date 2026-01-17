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

### 5. Executar o Chat
- Se estiver em Mac ou Linux:
  ```
  make chat
  ```
- Caso contrário:
  ```
  python3 src/chat.py
  ```

Isso iniciará um chat interativo para fazer perguntas baseadas nos documentos ingeridos.

## Exemplos de Uso

Aqui estão alguns exemplos de perguntas que você pode fazer no chat, baseadas nos documentos ingeridos:

- **Pergunta:** Qual o faturamento da Empresa SuperTechIABrazil?  
  **Resposta esperada:** Faturamento: R$ 10.000.000,00

- **Pergunta:** Qual o faturamento da empresa Alfa IA Indústria?  
  **Resposta esperada:** Faturamento: R$ 548.789.613,65

- **Pergunta:** Qual o ano de fundação da Atlas Biotech S.A.?  
  **Resposta esperada:** Ano de fundação: 2023

- **Pergunta:** Qual o faturamento da empresa Cobalto Turismo S.A.?  
  **Resposta esperada:** Faturamento: R$ 4.633.528.005,95

- **Pergunta:** Em qual ano a empresa Brava Cosméticos S.A. foi fundada?  
  **Resposta esperada:** Ano de fundação: 2021

- **Pergunta:** Qual o faturamento e o ano de fundação da empresa Alfa Tecnologia Holding?  
  **Resposta esperada:** Faturamento: R$ 66.776.155,12; Ano de fundação: 1950