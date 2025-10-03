from abc import ABC, abstractmethod

class MailProvider(ABC):
    @abstractmethod
    def send_welcome_email(self, to: str, username: str) -> None:
        ...