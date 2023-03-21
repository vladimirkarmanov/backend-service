from datetime import datetime

from models.user import UserTransaction
from repositories.user import UserTransactionRepository
from schemas.user_transaction import UserTransactionCreateSchema, UserTransactionRetrieveSchema
from .base import UserTransactionServiceMixin


class UserTransactionService(UserTransactionServiceMixin):
    @property
    def repository(self) -> UserTransactionRepository:
        return self.user_transaction_repository

    async def create(self, user_trx: UserTransactionCreateSchema) -> UserTransactionRetrieveSchema:
        user_trx = await self.repository.create(UserTransaction(**user_trx.dict()))
        return UserTransactionRetrieveSchema.from_orm(user_trx)

    async def get_user_balance_by_date(self, user_id: int, date: datetime) -> float:
        user_transaction = await self.repository.get_user_transaction_before_date(user_id, date)
        if user_transaction:
            return user_transaction.balance_after_trx
        return 0.0
