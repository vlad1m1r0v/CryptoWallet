from enum import StrEnum


class AssetNetworkTypeEnum(StrEnum):
    ETHEREUM = "ethereum"
    SEPOLIA = "sepolia"
    POLYGON = "polygon"
    BSC = "bsc"
    AVALANCHE = "avalanche"


class AssetTypeEnum(StrEnum):
    NATIVE = "native"
    ERC20 = "erc20"
    ERC721 = "erc721"
