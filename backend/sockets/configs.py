from os import environ as env
import pathlib
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parents[0]


class JwtConfig(BaseModel):
    private_key_path: pathlib.Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: pathlib.Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"


class MongoConfig(BaseModel):
    user: str = Field(alias="MONGO_USER")
    password: str = Field(alias="MONGO_PASSWORD")
    host: str = Field(alias="MONGO_HOST")
    database: str = Field(alias="MONGO_DB")

    @property
    def uri(self) -> str:
        # 1. Змінюємо протокол на mongodb://
        # 2. Додаємо порт :27017 (стандартний для Mongo)
        # 3. Додаємо authSource=admin
        # 4. Видаляємо tls=true (якщо ви не налаштовували SSL всередині Docker спеціально)
        return (
            f"mongodb://{self.user}:{self.password}@{self.host}:27017/"
            f"{self.database}?authSource=admin&retryWrites=true&w=majority"
        )


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RABBITMQ_HOST")
    port: int = Field(alias="RABBITMQ_PORT")
    user: str = Field(alias="RABBITMQ_USER")
    password: str = Field(alias="RABBITMQ_PASSWORD")
    vhost: str = Field(alias="RABBITMQ_VHOST")

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"


class RedisConfig(BaseModel):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    db: int = Field(alias="REDIS_DB")
    password: str | None = Field(alias="REDIS_PASSWORD", default=None)

    @property
    def url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"


class S3Config(BaseModel):
    space_name: str = Field(alias="S3_SPACE_NAME")
    space_region: str = Field(alias="S3_SPACE_REGION")
    access_key: str = Field(alias="S3_ACCESS_KEY")
    secret_key: str = Field(alias="S3_SECRET_KEY")
    base_file_url: str = Field(alias="S3_BASE_FILE_URL")


class Config(BaseModel):
    jwt: JwtConfig = Field(default_factory=lambda: JwtConfig(**env))
    mongo: MongoConfig = Field(default_factory=lambda: MongoConfig(**env))
    rabbit: RabbitMQConfig = Field(default_factory=lambda: RabbitMQConfig(**env))
    redis: RedisConfig = Field(default_factory=lambda: RedisConfig(**env))
    s3: S3Config = Field(default_factory=lambda: S3Config(**env))


config = Config()