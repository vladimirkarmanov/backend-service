from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from config import Config

config = Config()


def create_engines(config: Config) -> tuple[Engine, AsyncEngine]:
    sync_engine: Engine = create_engine(
        config.DATABASE_URL.replace("+aiosqlite", "")
    )
    async_engine: AsyncEngine = create_async_engine(
        config.DATABASE_URL,
    )
    return sync_engine, async_engine


def create_sessions(
        engine: Engine, async_engine: AsyncEngine
) -> tuple[Callable[[], Session], Callable[[], AsyncSession]]:
    create_async_session: Callable[[], AsyncSession] = async_sessionmaker(
        bind=async_engine, expire_on_commit=False
    )
    create_session: Callable[[], Session] = sessionmaker(bind=engine, expire_on_commit=False)
    return create_session, create_async_session


engine, async_engine = create_engines(config)
create_session, create_async_session = create_sessions(engine, async_engine)
