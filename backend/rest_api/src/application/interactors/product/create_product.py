from uuid import UUID
import logging

from src.domain.enums import AssetNetworkTypeEnum
from src.domain.exceptions import (
    UserIsNotOwnerOfWalletException,
    WalletNotFoundException
)
from src.domain.value_objects import (
    EntityId,
    Address,
    ProductName,
    ProductPrice,
    UploadedFile,
    Filename
)
from src.domain.services import ProductService

from src.application.ports.providers import FileUploader
from src.application.ports.gateways import (
    WalletGateway,
    ProductGateway,
    AssetGateway
)
from src.application.ports.transaction import TransactionManager
from src.application.ports.events import EventPublisher
from src.application.dtos.request import CreateProductRequestDTO
from src.application.dtos.response import ProductResponseDTO
from src.application.dtos.events import SaveProductEventDTO

logger = logging.getLogger(__name__)


class CreateProductInteractor:
    def __init__(
            self,
            product_service: ProductService,
            wallet_gateway: WalletGateway,
            product_gateway: ProductGateway,
            asset_gateway: AssetGateway,
            file_uploader: FileUploader,
            transaction_manager: TransactionManager,
            event_publisher: EventPublisher
    ):
        self._product_service = product_service
        self._wallet_gateway = wallet_gateway
        self._product_gateway = product_gateway
        self._asset_gateway = asset_gateway
        self._file_uploader = file_uploader
        self._transaction_manager = transaction_manager
        self._event_publisher = event_publisher

    async def __call__(self, user_id: UUID, data: CreateProductRequestDTO) -> ProductResponseDTO:
        user_id = EntityId(user_id)
        wallet_id = EntityId(data.wallet_id)

        logger.info("Checking if wallet with given id exists...")

        wallet = await self._wallet_gateway.read(wallet_id=wallet_id.value)

        if not wallet:
            raise WalletNotFoundException()

        logger.info("Checking if user is owner of wallet...")

        if wallet["user_id"] != user_id.value:
            raise UserIsNotOwnerOfWalletException(user_id, Address(wallet["address"]))

        logger.info("Uploading product photo to S3 bucket...")

        filename = self._file_uploader.upload_image(UploadedFile(data.photo).value)

        logger.info("Getting Sepolia asset from database...")

        sepolia_asset = await self._asset_gateway.read(network_type=AssetNetworkTypeEnum.SEPOLIA)

        price = data.price * (10 ** sepolia_asset["decimals"])

        logger.info("Inserting new product record into database...")

        entity = self._product_service.create_product(
            wallet_id=EntityId(wallet["id"]),
            name=ProductName(data.name),
            price=ProductPrice(price),
            photo_filename=Filename(filename)
        )

        self._product_gateway.add(entity)
        await self._transaction_manager.commit()

        product = await self._product_gateway.read(product_id=entity.id_.value)

        logger.info("Emitting event rest_api.save_product...")

        await self._event_publisher.save_product((
            SaveProductEventDTO(
                product_id=product["id"],
                name=product["name"],
                price=product["price"] / (10 ** product["wallet"]["asset"]["decimals"]),
                photo_filename=product["photo_filename"],
                asset_symbol=product["wallet"]["asset"]["symbol"],
                wallet_address=product["wallet"]["address"],
                created_at=product["created_at"]
            )
        ))

        return product
