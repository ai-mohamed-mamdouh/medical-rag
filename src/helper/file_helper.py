import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class FileHelper :
    def __init__(self) :
        TEMP_DIR = Path("temp")
        self.TEMP_DIR.mkdir(parents=True, exist_ok=True)

    def get_file_extension(self, file: UploadFile) -> str:
        """
        Get the uploaded file extension.

        Args:
            file: FastAPI UploadFile object.

        Returns:
            File extension without the dot.
            Example: "pdf", "txt", "docx"
        """

        # Extract the extension from the uploaded filename.
        extension = Path(file.filename).suffix.lower()

        # Remove the leading dot.
        return extension.lstrip(".")


    def save_temp_file(self, file: UploadFile) -> str:
        '''return temp file path'''

        suffix = Path(file.filename).suffix.lower()
        temp_path = self.TEMP_DIR / f"{uuid4()}{suffix}"

        with open(temp_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        return str(temp_path)