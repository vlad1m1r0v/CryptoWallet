from enum import StrEnum, auto


class AssetNetworkTypeEnum(StrEnum):
    ETHEREUM = auto()
    SEPOLIA = auto()
    POLYGON = auto()
    BSC = auto()
    AVALANCHE = auto()


class AssetTypeEnum(StrEnum):
    NATIVE = auto()
    ERC20 = auto()
    ERC721 = auto()
