from src.domain.exceptions.base import DomainException


class ProductNotFoundException(DomainException):
    message = "Product was not found."