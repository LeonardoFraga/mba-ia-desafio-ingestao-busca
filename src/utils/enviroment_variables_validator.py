import os
from dotenv import load_dotenv

load_dotenv()

def validate_variables():
    required_vars = [
        "PDF_PATH", 
        "DATABASE_URL", 
        "PG_VECTOR_COLLECTION_NAME", 
        "GOOGLE_EMBEDDING_MODEL", 
        "GOOGLE_API_KEY", 
        "OPENAI_CHAT_MODEL"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    