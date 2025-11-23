from uuid import UUID
import datetime

from src.application.ports.tasks import TaskRunner

from src.infrastructure.adapters.tasks.taskiq_broker import (
    redis_source,
    give_chat_permission_to_user
)


class TaskIqTaskRunner(TaskRunner):
    async def give_chat_access(self, user_id: UUID) -> None:
        await give_chat_permission_to_user.schedule_by_time(
            redis_source,
            datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=5),
            user_id=user_id
        )