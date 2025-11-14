from src.domain.enums import (
    TransactionStatusEnum,
    OrderStatusEnum
)
from src.domain.ports import SecretEncryptor
from src.domain.value_objects import (
    EntityId,
    Timestamp,
    TransactionStatus,
    TransactionHash,
    EncryptedPrivateKey,
    Balance,
    OrderStatus
)

from src.application.ports.transaction import TransactionManager
from src.application.ports.gateways import (
    TransactionGateway,
    WalletGateway,
    OrderGateway
)
from src.application.ports.events import EventPublisher
from src.application.dtos.request import UpdateTransactionRequestDTO


class CompleteTransactionInteractor:
    def __init__(
            self,
            transaction_gateway: TransactionGateway,
            wallet_gateway: WalletGateway,
            order_gateway: OrderGateway,
            transaction_manager: TransactionManager,
            event_publisher: EventPublisher,
            secret_encryptor: SecretEncryptor
    ) -> None:
        self._transaction_gateway = transaction_gateway
        self._wallet_gateway = wallet_gateway
        self._order_gateway = order_gateway
        self._transaction_manager = transaction_manager
        self._event_publisher = event_publisher
        self._secret_encryptor = secret_encryptor

    async def __call__(self, data: UpdateTransactionRequestDTO) -> None:
        await self._transaction_gateway.update_many(
            created_at=Timestamp(data.created_at),
            status=TransactionStatus(data.transaction_status),
            tx_hash=TransactionHash(data.hash),
        )

        order = await self._order_gateway.get_order_by_tx_hash(tx_hash=TransactionHash(data.hash))

        if order:

            if order["status"] == OrderStatusEnum.NEW:
                # payment transaction is complete
                if order["payment_transaction"]["transaction_hash"] == data.hash:
                    # if payment transaction failed
                    if data.transaction_status == TransactionStatusEnum.FAILED:
                        # change status to FAILED
                        await self._order_gateway.update(
                            order_id=EntityId(order["id"]),
                            status=OrderStatus(OrderStatusEnum.FAILED)
                        )
                        # change status to FAILED in marketplace microservice
                        await self._event_publisher.update_order(
                            order_id=order["id"],
                            status=OrderStatusEnum.FAILED
                        )
                        # create return transaction
                        await self._event_publisher.create_transaction(
                            # from product seller
                            private_key=self._secret_encryptor.decrypt(
                                EncryptedPrivateKey(order["product"]["wallet"]["encrypted_private_key"])
                            ).value,
                            # to customer
                            to_address=order["wallet"]["address"],
                            amount=order["product"]["price"] - 1.5 * order["payment_transaction"]["transaction_fee"],
                            return_order_id=order["id"]
                        )

                    # if payment transaction completed successfully
                    if data.transaction_status == TransactionStatusEnum.SUCCESSFUL:
                        await self._event_publisher.pay_order(order_id=order["id"])

        if data.transaction_status != TransactionStatusEnum.SUCCESSFUL:
            return

        tx = await self._transaction_gateway.get_one_by_hash(TransactionHash(data.hash))

        from_wallet = await self._wallet_gateway.read_by_address(tx.from_address)

        if from_wallet:
            await self._wallet_gateway.decrement_balance(
                wallet_id=from_wallet.id_,
                amount=Balance(tx.transaction_fee.value + tx.value.value)
            )

        to_wallet = await self._wallet_gateway.read_by_address(tx.to_address)

        if to_wallet:
            await self._wallet_gateway.increment_balance(
                wallet_id=to_wallet.id_,
                amount=Balance(tx.value.value)
            )

        await self._transaction_manager.commit()
