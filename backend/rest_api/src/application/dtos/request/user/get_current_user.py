from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class GetCurrentUserRequestDTO:
    access_token: str
