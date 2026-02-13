from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    embedding_model: str
    openai_api_key: str | None
    faiss_index_path: str
    top_k: int
    similarity_threshold: float


def get_settings() -> Settings:
    return Settings(
        embedding_model=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        faiss_index_path=os.getenv("FAISS_INDEX_PATH", "./faiss.index"),
        top_k=int(os.getenv("TOP_K", "5")),
        similarity_threshold=float(os.getenv("SIMILARITY_THRESHOLD", "0.2")),
    )
