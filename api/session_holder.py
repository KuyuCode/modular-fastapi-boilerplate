from contextlib import AbstractAsyncContextManager
from collections.abc import AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncConnection,
    async_sessionmaker,
    create_async_engine,
)

from api import util


__all__ = ["SessionHolder"]


class SessionHolder:
    def __init__(self, url: str):
        self._url: str = url
        self._engine: AsyncEngine = create_async_engine(url, echo=False)
        self._session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            bind=self._engine,
        )
        self._closed: bool = False

    async def close(self):
        if self._closed:
            raise RuntimeError("SessionHolder closed")

        await self._engine.dispose()
        self._closed = True

    @property
    def connect(self) -> Callable[[], AbstractAsyncContextManager[AsyncConnection]]:
        async def inner() -> AsyncGenerator[AsyncConnection]:
            if self._closed is None:
                raise RuntimeError("SessionHolder is closed")

            async with self._engine.begin() as connection:
                try:
                    yield connection
                except Exception:
                    await connection.rollback()
                    raise

        return util.contextmanager.async_manager(inner)

    @property
    def session(self) -> Callable[[], AbstractAsyncContextManager[AsyncSession]]:
        async def inner() -> AsyncGenerator[AsyncSession]:
            if self._session_maker is None:
                raise RuntimeError("SessionHolder is closed")

            session = self._session_maker()

            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

        return util.contextmanager.async_manager(inner)
