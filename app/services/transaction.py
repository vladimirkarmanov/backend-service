from uuid import UUID

from aiohttp import web

from models.transaction import Transaction
from repositories.transaction import TransactionRepository
from schemas.transaction import TransactionCreateSchema, TransactionRetrieveSchema, TransactionTypeEnum
from schemas.user_transaction import UserTransactionCreateSchema
from .base import TransactionServiceMixin, UserServiceMixin, UserTransactionServiceMixin


class TransactionService(TransactionServiceMixin, UserServiceMixin, UserTransactionServiceMixin):
    @property
    def repository(self) -> TransactionRepository:
        return self.transaction_repository

    async def _check_transaction_exists(self, uid: UUID) -> bool:
        transaction = await self.repository.get_by_uid(uid)
        return True if transaction else False

    async def create(
            self,
            user_id: int,
            transaction_payload: TransactionCreateSchema
    ) -> TransactionRetrieveSchema | None:
        if await self._check_transaction_exists(transaction_payload.uid):
            return
        transaction = await self.repository.create(Transaction(**transaction_payload.dict()))

        user = await self.user_service.get_user_balance(user_id)
        if transaction.type == TransactionTypeEnum.DEPOSIT:
            new_balance = await self.user_service.increase_balance(user_id, transaction.amount)
        elif transaction.type == TransactionTypeEnum.WITHDRAW and float(user.balance) >= transaction.amount:
            new_balance = await self.user_service.decrease_balance(user_id, transaction.amount)
        else:
            raise web.HTTPPaymentRequired

        user_trx = UserTransactionCreateSchema(
            **{
                "user_id": user_id,
                "transaction_id": transaction.id,
                "balance_after_trx": new_balance
            }
        )
        await self.user_transaction_service.create(user_trx)
        return TransactionRetrieveSchema.from_orm(transaction)

    async def get_transaction_info(self, uid: UUID) -> TransactionRetrieveSchema:
        user = await self.repository.get_by_uid(uid)
        if not user:
            raise web.HTTPNotFound
        return TransactionRetrieveSchema.from_orm(user)
