from uuid import UUID

from taskiq_redis import ListQueueBroker, RedisScheduleSource
from taskiq import TaskiqScheduler

from dishka.integrations.taskiq import (
    FromDishka,
    inject
)

from src.application.dtos.events import GiveChatAccessEventDTO
from src.application.ports.transaction import TransactionManager
from src.application.ports.gateways import PermissionsGateway
from src.application.ports.events import EventPublisher

from src.configs import config

broker = ListQueueBroker(config.redis.url)

redis_source = RedisScheduleSource(config.redis.url)

scheduler = TaskiqScheduler(broker, sources=[redis_source])


@broker.task
@inject(patch_module=True)
async def give_chat_permission_to_user(
        user_id: UUID,
        gateway: FromDishka[PermissionsGateway],
        transaction_manager: FromDishka[TransactionManager],
        event_publisher: FromDishka[EventPublisher]
) -> None:
    await gateway.update(user_id=user_id)
    await transaction_manager.commit()
    await event_publisher.give_chat_access_to_user(
        GiveChatAccessEventDTO(user_id=user_id)
    )
