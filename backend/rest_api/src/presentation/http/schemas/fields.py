from typing import Annotated
from pydantic import StringConstraints, BeforeValidator
import re

UsernameBase = Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=32)]
PasswordBase = Annotated[str, StringConstraints(min_length=8, max_length=20)]
AddressBase = Annotated[str, StringConstraints(strip_whitespace=True, min_length=42, max_length=42)]
TransactionHashBase = Annotated[str, StringConstraints(min_length=66, max_length=66)]


def validate_username_logic(value: str) -> str:
    PATTERN_START = re.compile(r"^[a-zA-Z0-9]")
    PATTERN_ALLOWED_CHARS = re.compile(r"[a-zA-Z0-9._-]*")
    PATTERN_NO_CONSECUTIVE_SPECIALS = re.compile(r"^[a-zA-Z0-9]+([._-]?[a-zA-Z0-9]+)*[._-]?$")
    PATTERN_END = re.compile(r".*[a-zA-Z0-9]$")

    if not re.match(PATTERN_START, value):
        raise ValueError("Username must start with a letter or digit.")
    if not re.fullmatch(PATTERN_ALLOWED_CHARS, value):
        raise ValueError("Username contains invalid characters.")
    if not re.fullmatch(PATTERN_NO_CONSECUTIVE_SPECIALS, value):
        raise ValueError("Username has consecutive special characters.")
    if not re.match(PATTERN_END, value):
        raise ValueError("Username must end with a letter or digit.")
    return value


def validate_password_logic(value: str) -> str:
    PATTERN = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,20}$"
    )
    if not re.fullmatch(PATTERN, value):
        raise ValueError(
            "Password must be 8–20 chars, contain upper, lower, digit, special."
        )
    return value


def validate_address_logic(value: str) -> str:
    if not value.startswith("0x"):
        raise ValueError(
            "Address must start with '0x'."
        )

    return value


def validate_transaction_hash_logic(value: str) -> str:
    TRANSACTION_HASH_PATTERN = re.compile(r"^0x[a-fA-F0-9]{64}$")
    if not re.fullmatch(TRANSACTION_HASH_PATTERN, value):
        raise ValueError("Transaction hash must start with '0x'.")

    return value


UsernameStr = Annotated[UsernameBase, BeforeValidator(validate_username_logic)]
PasswordStr = Annotated[PasswordBase, BeforeValidator(validate_password_logic)]
AddressStr = Annotated[AddressBase, BeforeValidator(validate_address_logic)]
TransactionHashStr = Annotated[TransactionHashBase, BeforeValidator(validate_transaction_hash_logic)]

__all__ = ["UsernameStr", "PasswordStr", "AddressStr", "TransactionHashStr"]
