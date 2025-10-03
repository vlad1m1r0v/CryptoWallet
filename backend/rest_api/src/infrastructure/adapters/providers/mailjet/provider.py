from jinja2 import Environment
from mailjet_rest import Client

from src.application.ports.providers.mail import MailProvider


class MailjetProvider(MailProvider):
    def __init__(self, jinja2_env: Environment, mailjet_client: Client):
        self._jinja2_env = jinja2_env
        self._mailjet_client = mailjet_client

    def send_welcome_email(self, to: str, username: str) -> None:
        template = self._jinja2_env.get_template("welcome.html")

        data = {
            "Messages": [
                {
                    "From": {
                        "Email": "mypochtav@gmail.com",
                        "Name": "CryptoWallet"
                    },
                    "To": [
                        {"Email": to}
                    ],
                    "Subject": "Welcome to CryptoWallet",
                    "TextPart": f"Dear {username}, welcome to CryptoWallet.",
                    "HTMLPart": template.render(username=username),
                }
            ]
        }

        self._mailjet_client.send.create(data=data)