import re
from dataclasses import dataclass
from typing import ClassVar

from src.domain.exceptions.fields import InvalidAssetNameException
from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class AssetName(ValueObject):
    """raises InvalidAssetNameException"""

    # Назва може бути з кількох слів, кожне починається з великої літери
    # Приклад: "Bitcoin", "Sepolia Ethereum", "Test Network"
    PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^[A-Z][a-z]+(?: [A-Z][a-z]+)*$"
    )

    value: str

    def __post_init__(self) -> None:
        super(AssetName, self).__post_init__()
        self._validate_asset_name(self.value)

    def _validate_asset_name(self, asset_name_value: str) -> None:
        if not re.fullmatch(self.PATTERN, asset_name_value.strip()):
            raise InvalidAssetNameException()