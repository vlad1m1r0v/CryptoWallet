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


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")


class MailingConfig(BaseModel):
    api_key: str = Field(alias="MAILJET_API_KEY")
    secret_key: str = Field(alias="MAILJET_SECRET_KEY")


class Config(BaseModel):
    frontend: FrontendConfig = Field(default_factory=lambda: FrontendConfig(**env))
    security: SecurityConfig = Field(default_factory=lambda: SecurityConfig(**env))
    postgres: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    mailing: MailingConfig = Field(default_factory=lambda: MailingConfig(**env))


config = Config()