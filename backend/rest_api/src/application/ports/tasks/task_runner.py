from typing import Protocol
from uuid import UUID


class TaskRunner(Protocol):
    async def give_chat_access(self, user_id: UUID) -> None:
        ...