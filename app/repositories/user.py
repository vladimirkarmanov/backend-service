from datetime import datetime

from sqlalchemy import select, and_

from models.transaction import Transaction
from models.user import User, UserTransaction
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    async def create(self, user: User) -> User:
        return await self.save(user)

    async def get_last_created_user(self) -> User | None:
        statement = select(User).order_by(User.id.desc())
        return await self.first(statement)

    async def get_by_id(self, id: int) -> User | None:
        statement = select(User).filter(User.id == id)
        return await self.one_or_none(statement)

    async def increase_balance(self, user: User, amount: float) -> User:
        user.balance += amount
        return await self.save(user)

    async def decrease_balance(self, user: User, amount: float) -> User:
        user.balance -= amount
        return await self.save(user)


class UserTransactionRepository(BaseRepository[UserTransaction]):
    async def create(self, user_transaction: UserTransaction) -> UserTransaction:
        return await self.save(user_transaction)

    async def get_user_transaction_before_date(self, user_id: int, date: datetime) -> UserTransaction | None:
        statement = (
            select(UserTransaction)
            .join(User, and_(User.id == user_id, User.id == UserTransaction.user_id))
            .join(Transaction, and_(UserTransaction.transaction_id == Transaction.id, Transaction.timestamp <= date))
            .order_by(Transaction.timestamp.desc())
            .limit(1)
        )
        return await self.one_or_none(statement)
