from abc import ABC, abstractmethod
from src.domain.value_objects.email import Email

class MailProvider(ABC):
    @abstractmethod
    async def send_welcome_email(self, to: Email, username: str) -> None:
        ...