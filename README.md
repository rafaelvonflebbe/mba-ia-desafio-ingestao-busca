# PDF Ingestion and Semantic Search System

A Python-based system that ingests PDF documents and enables semantic search through a command-line interface using LangChain, PostgreSQL with pgVector, and Docker.

## Project Overview

This system allows you to:
- Ingest PDF documents and split them into manageable chunks
- Convert text chunks into vector embeddings
- Store vectors in a PostgreSQL database with pgVector extension
- Perform semantic search on the ingested documents
- Interact with the documents through a command-line interface

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Google API key (for embeddings and LLM)
- A PDF document to ingest

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd langchain_introduction/mba-ia-desafio-ingestao-busca
```

### 2. Set Up Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```bash
# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_EMBEDDING_MODEL='models/embedding-001'
GOOGLE_LLM_MODEL='gemini-2.5-flash-lite'

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag

# Vector Store Configuration
PG_VECTOR_COLLECTION_NAME=document_embeddings

# Document Configuration
PDF_PATH=document.pdf
```

### 3. Start the Database

Start the PostgreSQL database with pgVector using Docker Compose:

```bash
docker-compose up -d
```

Wait for the database to be ready (this may take a few moments).

### 4. Create and Activate Virtual Environment

Create a Python virtual environment to isolate dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 5. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 6. Ingest the PDF Document

Ingest the PDF document into the vector database:

```bash
python src/ingest.py
```

This will:
- Load the PDF document
- Split it into chunks of 1000 characters with 150 character overlap
- Create embeddings for each chunk
- Store the vectors in PostgreSQL

## Usage

### Start the Chat Interface

After ingesting the PDF, you can start the interactive chat interface:

```bash
python src/chat.py
```

### Example Usage

```

=== Sistema de Busca Semântica ===
Digite 'sair' para encerrar o chat.

Você: Qual o faturamento da Empresa Suprema Serviços LTDA?
Processando sua pergunta...

Resposta:

--------------------------------------------------
O faturamento foi de 10 milhões de reais.
--------------------------------------------------

Você: Quantos clientes temos em 2024?
Processando sua pergunta...

Resposta:
--------------------------------------------------
Não tenho informações necessárias para responder sua pergunta.
--------------------------------------------------

Você: sair
Encerrando o chat. Até logo!
```

## Project Structure

```
├── docker-compose.yml          # Docker configuration for PostgreSQL
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .env                       # Environment variables (not committed)
├── src/
│   ├── ingest.py              # PDF ingestion script
│   ├── search.py              # Search functionality
│   └── chat.py                # CLI chat interface
├── document.pdf               # PDF document for ingestion
└── README.md                  # This file
```

## Configuration Details

### Environment Variables

- `GOOGLE_API_KEY`: Your Google API key for embeddings and LLM
- `GOOGLE_EMBEDDING_MODEL`: Model for text embeddings (default: 'models/embedding-001')
- `GOOGLE_LLM_MODEL`: Model for LLM responses (default: 'gemini-2.5-flash-lite')
- `DATABASE_URL`: PostgreSQL connection string
- `PG_VECTOR_COLLECTION_NAME`: Name for the vector collection (default: 'document_embeddings')
- `PDF_PATH`: Path to the PDF document to ingest

### Database Configuration

The system uses PostgreSQL with the pgVector extension. The Docker Compose file sets up:
- PostgreSQL 17 with pgVector extension
- Database named 'rag'
- User 'postgres' with password 'postgres'
- Port 5432 exposed to the host

## License

This project is for educational purposes.
