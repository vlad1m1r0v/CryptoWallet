from dishka import Provider, Scope, provide, from_context

from botocore.client import BaseClient
import boto3

from s3 import (
    FileUploader,
    S3FileUploader
)

from configs import Config

class ImageStorageProvider(Provider):
    scope = Scope.REQUEST
    config = from_context(provides=Config, scope=Scope.APP)

    s3_file_uploader = provide(
        source=S3FileUploader,
        provides=FileUploader
    )


    @provide(scope=Scope.APP)
    def provide_s3_client(self, config: Config) -> BaseClient:
        return boto3.client(
            "s3",
            region_name=config.s3.space_region,
            aws_access_key_id=config.s3.access_key,
            aws_secret_access_key=config.s3.secret_key,
            endpoint_url=f"https://{config.s3.space_region}.digitaloceanspaces.com"
        )
