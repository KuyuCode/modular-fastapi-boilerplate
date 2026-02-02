import typing
from fastapi import Request
from collections.abc import AsyncGenerator
from api.session_holder import SessionHolder

from sqlalchemy.ext.asyncio import AsyncSession


async def acquire_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session_holder = typing.cast(SessionHolder, request.state.session_holder)

    async with session_holder.session() as session:
        yield session
