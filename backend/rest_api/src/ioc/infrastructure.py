from pathlib import Path

from dishka import Provider, Scope, provide, from_context
from jinja2 import Environment, ChoiceLoader, FileSystemLoader
from mailjet_rest import Client

from src.configs import Config

BASE_DIR = Path(__file__).resolve().parent.parent
providers_dir = BASE_DIR / "infrastructure" / "adapters" / "providers"


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
        return Client(auth=(config.mailing.api_key, config.mailing.secret_key))

