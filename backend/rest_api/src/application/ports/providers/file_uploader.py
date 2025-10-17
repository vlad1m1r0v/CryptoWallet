from abc import ABC, abstractmethod

from src.domain.value_objects.url import URL
from src.domain.value_objects.uploaded_file import UploadedFile


class FileUploader(ABC):
    @abstractmethod
    def upload_image(self, file: UploadedFile) -> URL:
        ...
