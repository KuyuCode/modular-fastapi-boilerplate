import typing

if typing.TYPE_CHECKING:
    from .error import APIError


class DefineErrorProtocol(typing.Protocol):
    def __call__(self, code: str, message: str, status_code: int) -> "APIError": ...
