
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

from utils.enviroment_variables_validator import validate_variables

load_dotenv()

def initialize_pgvector_store():
    validate_variables()

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )

    return store