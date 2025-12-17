from typing import TypedDict, NotRequired


class Message(TypedDict):
    user_id: str
    text: str
    image: NotRequired[str]
    created_at: str