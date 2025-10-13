from src.domain.exceptions.base import DomainFieldError


class InvalidEmailFormatError(DomainFieldError):
    message = "Invalid email format."


class InvalidPasswordError(DomainFieldError):
    message = \
        f"Password must be 8-20 characters long, " \
        "contain at least one lowercase, one uppercase, one digit, " \
        "and one special character."


class InvalidURLError(DomainFieldError):
    message = f"Invalid URL format."


class InvalidUsernameLengthError(DomainFieldError):
    message = \
        f"Username must be between " \
        f"5 and " \
        f"32 characters."


class InvalidUsernameStartError(DomainFieldError):
    message = f"Username must start with a letter (A-Z, a-z) or a digit (0-9)."


class InvalidUsernameCharacterError(DomainFieldError):
    message = \
        "Username can only contain letters (A-Z, a-z), digits (0-9), " \
        "dots (.), hyphens (-), and underscores (_)."


class InvalidUsernameConsecutiveCharactersError(DomainFieldError):
    message = \
        "Username cannot contain consecutive special characters" \
        " like .., --, or __."


class InvalidUsernameEndError(DomainFieldError):
    message = f"Username must end with a letter (A-Z, a-z) or a digit (0-9)."