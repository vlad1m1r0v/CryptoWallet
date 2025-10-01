from os import environ as env

import pathlib

from pydantic import Field, BaseModel
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent


class SecurityConfig(BaseModel):
    private_key_path: pathlib.Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: pathlib.Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    password_pepper: str = Field(alias="PASSWORD_PEPPER")


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")


class MailingConfig(BaseModel):
    MAILJET_API_KEY: str = Field(alias="MAILJET_API_KEY")
    MAILJET_SECRET_KEY: str = Field(alias="MAILJET_SECRET_KEY")


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RABBITMQ_HOST")
    port: int = Field(alias="RABBITMQ_PORT")
    login: str = Field(alias="RABBITMQ_USER")
    password: str = Field(alias="RABBITMQ_PASS")


class Config(BaseModel):
    security: SecurityConfig = Field(default_factory=lambda: SecurityConfig(**env))
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
