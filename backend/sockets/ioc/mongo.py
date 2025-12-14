from dishka import Provider, Scope, provide, from_context

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from configs import Config

from mongo.repositories import (
    UserCollection,
    MessageCollection,
    UserRepository,
    MongoUserRepository,
    MessageRepository,
    MongoMessageRepository
)


class MongoProvider(Provider):
    scope = Scope.REQUEST
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def mongo_client(self, cfg: Config) -> AsyncMongoClient:
        return AsyncMongoClient(cfg.mongo.uri)

    @provide(scope=Scope.APP)
    def mongo_database(self, mongo_client: AsyncMongoClient, cfg: Config) -> AsyncDatabase:
        return mongo_client[cfg.mongo.database]

    @provide(scope=Scope.REQUEST)
    def user_collection(self, mongo_database: AsyncDatabase) -> UserCollection:
        return UserCollection(mongo_database["users"])

    @provide(scope=Scope.REQUEST)
    def message_collection(self, mongo_database: AsyncDatabase) -> MessageCollection:
        return MessageCollection(mongo_database["messages"])

    user_repository = provide(
        source=MongoUserRepository,
        provides=UserRepository
    )

    message_repository = provide(
        source=MongoMessageRepository,
        provides=MessageRepository
    )
