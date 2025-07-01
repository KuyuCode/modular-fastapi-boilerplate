import math
import typing
import collections.abc

from .. import constants
from dynaconf import Dynaconf
from . import string, fastapi, pydantic, datetime, contextmanager


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.yaml", ".secrets.yaml"],
)

__all__ = [
    "string",
    "fastapi",
    "pydantic",
    "datetime",
    "settings",
    "contextmanager",
    "paginated_response",
    "get_offset_and_limit",
]


def get_offset_and_limit(page: int, size: int = constants.misc.DEFAULT_PAGE_SIZE):
    return (page - 1) * size, size


def paginated_response(
    items: collections.abc.Sequence[typing.Any],
    total: int,
    offset: int,
    limit: int,
):
    return {
        "items": items,
        "pagination": {
            "total": total,
            "page": (offset / limit) + 1,
            "pages": math.ceil(total / limit),
        },
    }
