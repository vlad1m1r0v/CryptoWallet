from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.presentation.http.schemas.fields import UsernameStr

class GetOtherProfileResponseSchema(BaseModel):
    id: UUID
    username: UsernameStr
    avatar_url: Optional[str]
    total_messages: int

