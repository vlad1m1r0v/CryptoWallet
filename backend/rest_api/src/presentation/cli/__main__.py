import logging
import asyncio

from dishka import make_async_container, Scope

import click

from src.domain.enums import (
    AssetNetworkTypeEnum,
    AssetTypeEnum,
)

from src.application.dtos.request import CreateAssetRequestDTO
from src.application.interactors import CreateAssetInteractor

from src.ioc import get_providers

from src.configs import (
    Config,
    config
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    datefmt='%H:%M:%S'
)


async def _create_sepolia_asset():
    container = make_async_container(*get_providers(), context={Config: config})

    async with container(scope=Scope.REQUEST) as nested_container:
        interactor = await nested_container.get(CreateAssetInteractor)

        dto = CreateAssetRequestDTO(
            name="Sepolia Ethereum",
            symbol="ETH",
            decimals=18,
            network=AssetNetworkTypeEnum.SEPOLIA,
            asset_type=AssetTypeEnum.NATIVE
        )

        await interactor(dto)


@click.command()
def main():
    asyncio.run(_create_sepolia_asset())


if __name__ == "__main__":
    main()
