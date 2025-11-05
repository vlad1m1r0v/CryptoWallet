from uuid import UUID

from pydantic import BaseModel


class FreeETHRequestSchema(BaseModel):
    wallet_id: UUID