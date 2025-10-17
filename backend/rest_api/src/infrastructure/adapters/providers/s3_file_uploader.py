import io
import uuid

from botocore.client import BaseClient

from src.configs import S3Config

from src.application.ports.providers.file_uploader import FileUploader

from src.domain.value_objects.url import URL
from src.domain.value_objects.uploaded_file import UploadedFile


class S3FileUploader(FileUploader):
    def __init__(self, s3_config: S3Config, client: BaseClient):
        self._s3_config = s3_config
        self._client = client

    def upload_image(self, file: UploadedFile) -> URL:
        ext = "png"
        mime = "image/png"
        file_obj = io.BytesIO(file.value)
        name = f"{uuid.uuid4()}.{ext}"

        self._client.upload_fileobj(
            file_obj,
            self._s3_config.space_name,
            name,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": mime
            }
        )

        return URL(f"https://{self._s3_config.space_name}.{self._s3_config.space_region}.digitaloceanspaces.com/{name}")
