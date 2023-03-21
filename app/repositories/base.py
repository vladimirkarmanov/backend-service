import functools
from asyncio import shield
from typing import Generic, TypeVar

from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, Update, Delete

from core.database import create_async_session

T = TypeVar("T")


def transaction(commit: bool = True):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(self, *args, **kwargs):
            session = create_async_session()
            try:
                self.session = session
                result = await func(self, *args, **kwargs)
                if commit:
                    await session.commit()
            except DBAPIError as e:
                await session.rollback()
                raise e
            except Exception:
                await session.rollback()
                raise
            finally:
                if session:
                    await shield(session.close())
            return result

        return wrapped

    return wrapper


class BaseRepository(Generic[T]):
    def __init__(self):
        self.session: AsyncSession | None = None

    @transaction()
    async def save(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    @transaction(commit=False)
    async def one_or_none(self, statement: Select) -> T | None:
        return (await self.session.execute(statement)).scalars().one_or_none()

    @transaction(commit=False)
    async def first(self, statement: Select) -> T | None:
        return (await self.session.execute(statement)).scalars().first()

    @transaction()
    async def execute(self, statement: Select | Update | Delete) -> CursorResult:
        return await self.session.execute(statement)
