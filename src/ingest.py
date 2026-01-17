import os

from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from validators.enviroment_variables_validator import validate_variables
import psycopg2


from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

def ingest_pdf():
    """Realiza ingestão de documentos PDF, enriquecimento e armazenamento no banco de dados PostgreSQL usando PGVector."""

    try:
        validate_variables()

        docs = PyPDFLoader(str(PDF_PATH)).load()
        if not docs:
            raise FileNotFoundError(f"Nenhum documento foi carregado do caminho especificado: {PDF_PATH}")

        embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))

        text_splitter = _text_splitter(docs)
        
        enriched_documents, ids = _prepare_documents_with_metadata(text_splitter)

        _store_documents(enriched_documents, ids, embeddings)

    except EnvironmentError as e:
        print(e)
        raise SystemExit("Variáveis de ambiente inválidas ou ausentes.")


def _text_splitter(docs):
    """Divide documentos em chunks menores para processamento.
    
    Args:
        docs: Lista de documentos carregados.
    
    Returns:
        Lista de documentos divididos.
    """
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=False,
        ).split_documents(docs)

    if not text_splitter:
        raise SystemExit("Nenhum documento foi dividido. Verifique o arquivo PDF e os parâmetros de divisão.")
    
    return text_splitter
    

def _prepare_documents_with_metadata(text_splitter):
    """Enriquece os documentos com metadados adicionais.
    Args:
        text_splitter: Lista de documentos divididos.

    Returns:
        Tupla contendo a lista de documentos enriquecidos e suas IDs.
    """

    enriched_documents = [
        Document(
            page_content=doc.page_content,
            metadata={
                k: v for k, v in doc.metadata.items() if v not in (None, "")
            },
        )
        for doc in text_splitter
    ]

    ids = [f"doc-{i}" for i in range(len(enriched_documents))]

    return enriched_documents, ids


def _store_documents(enriched_documents, ids, embeddings):
    """Armazena os documentos enriquecidos no banco de dados PostgreSQL usando PGVector.
    Args:
        enriched_documents: Lista de documentos enriquecidos.
        ids: Lista de IDs dos documentos.
        embeddings: Modelo de embeddings para converter texto em vetores.
    """

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )

    try:
        _cleanup_collection(store)
        store.add_documents(documents=enriched_documents, ids=ids)
        print(f"Documentos armazenados com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao armazenar os documentos: {e}")
        raise SystemError("Falha ao armazenar os documentos no banco de dados.")
        


def _cleanup_collection(store):
    """Limpa a coleção existente no banco de dados PostgreSQL.
        Isso permite a execução repetida do script sem duplicação de dados, além de tornar a atualização do PDF mais simples.
    Args:
        store: Instância do PGVector.
    """


    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    
    cur.execute("SELECT uuid FROM langchain_pg_collection WHERE name = %s", (store.collection_name,))
    result = cur.fetchone()
    if not result:
        raise ValueError(f"Coleção '{store.collection_name}' não encontrada.")
    collection_uuid = result[0]
    
    cur.execute("DELETE FROM langchain_pg_embedding WHERE collection_id = %s", (collection_uuid,))
    conn.commit()
    cur.close()
    conn.close()
    print("Coleção limpa com sucesso.")



if __name__ == "__main__":
    ingest_pdf()