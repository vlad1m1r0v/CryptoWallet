from dataclasses import dataclass
from typing import Any

from src.domain.exceptions import InvalidChoiceException

from src.domain.enums import AssetTypeEnum

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class AssetType(ValueObject):
    value: AssetTypeEnum

    def __post_init__(self):
        super(AssetType, self).__post_init__()
        self._validate_asset_type(asset_type=self.value)

    @staticmethod
    def _validate_asset_type(asset_type: Any) -> None:
        if not isinstance(asset_type, AssetTypeEnum):
            raise InvalidChoiceException(field="asset_type", enum_cls=AssetTypeEnum, actual_value=asset_type)
