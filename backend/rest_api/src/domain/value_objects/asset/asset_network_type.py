from dataclasses import dataclass
from typing import Any

from src.domain.exceptions.fields import InvalidChoiceException

from src.domain.enums.asset import AssetNetworkTypeEnum

from src.domain.value_objects.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class AssetNetworkType(ValueObject):
    value: AssetNetworkTypeEnum

    def __post_init__(self):
        super(AssetNetworkType, self).__post_init__()
        self._validate_asset_network_type(asset_network_type=self.value)

    @staticmethod
    def _validate_asset_network_type(asset_network_type: Any) -> None:
        if not isinstance(asset_network_type, AssetNetworkTypeEnum):
            raise InvalidChoiceException(
                field="asset_network_type",
                enum_cls=AssetNetworkTypeEnum,
                actual_value=asset_network_type
            )
