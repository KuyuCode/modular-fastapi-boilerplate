from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from api.session_holder import session_holder


async def acquire_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_holder.session() as session:
        yield session
