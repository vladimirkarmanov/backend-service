from datetime import datetime

from aiohttp import web

from models.user import User
from repositories.user import UserRepository
from schemas.user import UserCreateSchema, UserRetrieveSchema, UserBalanceRetrieveSchema
from .base import UserServiceMixin, TransactionServiceMixin, UserTransactionServiceMixin


class UserService(UserServiceMixin, TransactionServiceMixin, UserTransactionServiceMixin):
    @property
    def repository(self) -> UserRepository:
        return self.user_repository

    async def get_last_created_user(self) -> UserRetrieveSchema:
        user = await self.repository.get_last_created_user()
        return UserRetrieveSchema.from_orm(user)

    async def create(self, user_payload: UserCreateSchema) -> UserRetrieveSchema:
        user = await self.repository.create(User(**user_payload.dict()))
        return UserRetrieveSchema.from_orm(user)

    async def get_user_balance(self, id: int, date: str | None = None) -> UserBalanceRetrieveSchema | None:
        user = await self.repository.get_by_id(id)
        if not user:
            raise web.HTTPNotFound

        if date is not None:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
            balance = await self.user_transaction_service.get_user_balance_by_date(id, date)
        else:
            balance = user.balance
        return UserBalanceRetrieveSchema(balance=balance)

    async def increase_balance(self, user_id: int, amount: float) -> float:
        user = await self.repository.get_by_id(user_id)
        if user:
            user = await self.repository.increase_balance(user, amount)

        return user.balance

    async def decrease_balance(self, user_id: int, amount: float):
        user = await self.repository.get_by_id(user_id)
        if user:
            user = await self.repository.decrease_balance(user, amount)

        return user.balance
