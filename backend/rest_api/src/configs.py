from os import environ as env

import pathlib

from pydantic import Field, BaseModel
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent


class FrontendConfig(BaseModel):
    url: str = Field(alias="FRONTEND_URL")


class SecurityConfig(BaseModel):
    private_key_path: pathlib.Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: pathlib.Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    password_pepper: str = Field(alias="PASSWORD_PEPPER")
    aes_secret_key: str = Field(alias="AES_SECRET_KEY")


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")


class MailingConfig(BaseModel):
    api_key: str = Field(alias="MAILJET_API_KEY")
    secret_key: str = Field(alias="MAILJET_SECRET_KEY")


class S3Config(BaseModel):
    space_name: str = Field(alias="S3_SPACE_NAME")
    space_region: str = Field(alias="S3_SPACE_REGION")
    access_key: str = Field(alias="S3_ACCESS_KEY")
    secret_key: str = Field(alias="S3_SECRET_KEY")
    base_file_url: str = Field(alias="S3_BASE_FILE_URL")


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RABBITMQ_HOST")
    port: int = Field(alias="RABBITMQ_PORT")
    user: str = Field(alias="RABBITMQ_USER")
    password: str = Field(alias="RABBITMQ_PASSWORD")
    vhost: str = Field(alias="RABBITMQ_VHOST")

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"


class Config(BaseModel):
    frontend: FrontendConfig = Field(default_factory=lambda: FrontendConfig(**env))
    security: SecurityConfig = Field(default_factory=lambda: SecurityConfig(**env))
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    mailing: MailingConfig = Field(default_factory=lambda: MailingConfig(**env))
    s3: S3Config = Field(default_factory=lambda: S3Config(**env))
    rabbit_mq: RabbitMQConfig = Field(default_factory=lambda: RabbitMQConfig(**env))


config = Config()
