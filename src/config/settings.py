from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BASE_DIR = Path(__file__).resolve().parents[2]

    DATA_DIR = BASE_DIR / "docs"

    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = Settings()