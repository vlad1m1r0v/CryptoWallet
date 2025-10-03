from jinja2 import Environment
from mailjet_rest import Client

from src.application.ports.providers.mail import MailProvider
from src.domain.value_objects.email import Email


class MailjetProvider(MailProvider):
    def __init__(self, jinja2_env: Environment, mailjet_client: Client):
        self._jinja2_env = jinja2_env
        self._mailjet_client = mailjet_client

    async def send_welcome_email(self, to: Email, username: str) -> None:
        template = self._jinja2_env.get_template("welcome.html")

        data = {
            "FromEmail": "vladimirov.artem.prk@gmail.com",
            "FromName": "CryptoWallet",
            "Subject": "Welcome to CryptoWallet",
            "Text-part": f"Dear {username}, welcome to CryptoWallet.",
            "Html-part": template.render(username=username),
            "Recipients": [{"Email": str(Email)}],
        }

        self._mailjet_client.send.create(data=data)