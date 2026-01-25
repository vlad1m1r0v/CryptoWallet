from typing import TypedDict, NotRequired


class Message(TypedDict):
    user_id: str
    text: NotRequired[str]
    image: NotRequired[str]
    created_at: str