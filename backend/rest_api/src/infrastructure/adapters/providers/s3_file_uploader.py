import io
import uuid

from botocore.client import BaseClient

from src.configs import S3Config

from src.application.ports.providers.file_uploader import FileUploader


class S3FileUploader(FileUploader):
    def __init__(self, s3_config: S3Config, client: BaseClient):
        self._s3_config = s3_config
        self._client = client

    def upload_image(self, file: bytes) -> str:
        ext = "png"
        mime = "image/png"
        file_obj = io.BytesIO(file)
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

        return name
