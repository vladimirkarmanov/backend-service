from uuid import UUID

from sqlalchemy import select

from models.transaction import Transaction
from repositories.base import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    async def create(self, transaction: Transaction) -> Transaction:
        return await self.save(transaction)

    async def get_by_uid(self, uid: UUID) -> Transaction | None:
        statement = select(Transaction).filter(Transaction.uid == uid)
        return await self.one_or_none(statement)
