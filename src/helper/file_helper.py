import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


TEMP_DIR = Path("temp")


def save_temp_file(file: UploadFile) -> str:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    suffix = Path(file.filename).suffix.lower()
    temp_path = TEMP_DIR / f"{uuid4()}{suffix}"

    with open(temp_path, "wb") as temp_file:
        shutil.copyfileobj(file.file, temp_file)

    return str(temp_path)