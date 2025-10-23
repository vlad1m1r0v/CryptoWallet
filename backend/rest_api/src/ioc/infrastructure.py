from pathlib import Path

from dishka import Provider, Scope, provide, from_context

from jinja2 import Environment, ChoiceLoader, FileSystemLoader

from botocore.client import BaseClient
import boto3

from mailjet_rest import Client

from faststream.rabbit import RabbitBroker

from src.configs import Config

BASE_DIR = Path(__file__).resolve().parents[1]
PROVIDERS_DIR = BASE_DIR / "infrastructure" / "adapters" / "providers"


class InfrastructureProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def provide_jinja2_env(self) -> Environment:
        template_dirs = [
            str(path) for path in providers_dir.rglob("templates") if path.is_dir()
        ]

        loader = ChoiceLoader(
            [FileSystemLoader(dir_path) for dir_path in template_dirs]
        )

        return Environment(
            loader=loader,
            autoescape=True,
        )

    @provide(scope=Scope.APP)
    def provide_mailjet_client(self, config: Config) -> Client:
        return Client(auth=(config.mailing.api_key, config.mailing.secret_key), version="v3.1")

    @provide(scope=Scope.APP)
    def provide_s3_client(self, config: Config) -> BaseClient:
        return boto3.client(
            "s3",
            region_name=config.s3.space_region,
            aws_access_key_id=config.s3.access_key,
            aws_secret_access_key=config.s3.secret_key,
            endpoint_url=f"https://{config.s3.space_region}.digitaloceanspaces.com"
        )

    @provide(scope=Scope.APP)
    async def provide_rabbitmq_client(self, config: Config) -> RabbitBroker:
        broker = RabbitBroker(url=config.rabbit_mq.url)
        await broker.start()
        return broker
