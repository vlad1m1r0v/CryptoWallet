from uuid import UUID

from src.domain.enums import AssetNetworkTypeEnum
from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException
)
from src.domain.value_objects import (
    EntityId,
    ProductName,
    ProductPrice,
    UploadedFile,
    Filename
)
from src.domain.services import ProductService

from src.application.dtos.request import CreateProductRequestDTO
from src.application.dtos.response import ProductResponseDTO
from src.application.ports.providers import FileUploader
from src.application.ports.gateways import (
    WalletGateway,
    ProductGateway,
    AssetGateway
)
from src.application.ports.transaction import TransactionManager


class CreateProductInteractor:
    def __init__(
            self,
            product_service: ProductService,
            wallet_gateway: WalletGateway,
            product_gateway: ProductGateway,
            asset_gateway: AssetGateway,
            file_uploader: FileUploader,
            transaction_manager: TransactionManager
    ):
        self._product_service = product_service
        self._wallet_gateway = wallet_gateway
        self._product_gateway = product_gateway
        self._asset_gateway = asset_gateway
        self._file_uploader = file_uploader
        self._transaction_manager = transaction_manager

    async def __call__(self, user_id: UUID, data: CreateProductRequestDTO) -> ProductResponseDTO:
        user_id = EntityId(user_id)
        wallet_id = EntityId(data.wallet_id)
        wallet = await self._wallet_gateway.read_by_id(wallet_id)

        if not wallet:
            raise WalletNotFoundException()

        if wallet.user_id != user_id:
            raise UserIsNotOwnerOfWalletException(user_id, wallet.address)

        filename = Filename(self._file_uploader.upload_image(UploadedFile(data.photo).value))

        sepolia_asset = await self._asset_gateway.read_by_network_type(AssetNetworkTypeEnum.SEPOLIA)

        price = data.price * (10 ** sepolia_asset.decimals.value)

        entity = self._product_service.create_product(
            wallet_id=wallet.id_,
            name=ProductName(data.name),
            price=ProductPrice(price),
            photo_filename=filename
        )

        self._product_gateway.add(entity)
        await self._transaction_manager.commit()

        return await self._product_gateway.read_by_id(entity.id_)
