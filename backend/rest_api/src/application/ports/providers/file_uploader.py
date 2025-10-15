from abc import ABC, abstractmethod

from src.domain.value_objects.url import URL


class FileUploader(ABC):
    @abstractmethod
    def upload_image(self, file: bytes) -> URL:
        ...