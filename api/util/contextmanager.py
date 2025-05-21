"""
Fix PyCharm problem with type inference of return type of context managers

Usage:
::
    # Async code
    async def func() -> typing.AsyncGenerator[int]:
        yield 123

    func = async_manager(func)

    async with func() as result:
        print(result.to_bytes())

    # Sync code
    def func() -> typing.Generator[int, None, None]:
        yield 123

    func = sync_manager(func)

    with func() as result:
        print(result.to_bytes())
"""

import typing
from contextlib import asynccontextmanager, contextmanager

__all__ = [
    "sync_manager",
    "async_manager",
]

T = typing.TypeVar("T")
P = typing.ParamSpec("P")


def async_manager(
    func: typing.Callable[P, typing.AsyncGenerator[T]],
) -> typing.Callable[P, typing.AsyncContextManager[T]]:
    return asynccontextmanager(func)


def sync_manager(
    func: typing.Callable[P, typing.Generator[T, None, None]],
) -> typing.Callable[P, typing.ContextManager[T]]:
    return contextmanager(func)
