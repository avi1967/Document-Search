import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    # Config
    USE_OPENAI = False  # ← change to True when you have credits
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Models
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL", "text-embedding-3-small"
    )

    # Vector DB
    VECTOR_DIM = 384
    TOP_K = int(os.getenv("TOP_K", 5))

    # Paths
    RAW_DOCS_PATH = os.getenv("RAW_DOCS_PATH", "data/raw_docs")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "data/vector_index")

    # App
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
