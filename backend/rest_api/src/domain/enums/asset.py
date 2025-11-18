from enum import StrEnum


class AssetNetworkTypeEnum(StrEnum):
    ETHEREUM = "ETHEREUM"
    SEPOLIA = "SEPOLIA"
    POLYGON = "POLYGON"
    BSC = "BSC"
    AVALANCHE = "AVALANCHE"


class AssetTypeEnum(StrEnum):
    NATIVE = "NATIVE"
    ERC20 = "ERC20"
    ERC721 = "ERC721"
