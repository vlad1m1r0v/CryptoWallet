from abc import ABC, abstractmethod


class FileUploader(ABC):
    @abstractmethod
    def upload_image(self, file: bytes) -> str:
        ...
