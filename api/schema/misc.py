import typing

from pydantic import Field

from .model import Schema


__all__ = ["Paginated"]


class PaginationData(Schema):
    total: int = Field(ge=0, description="Total number of items")
    page: int = Field(ge=1, description="Number of page")
    pages: int = Field(ge=0, description="Total number of pages")


T_s = typing.TypeVar("T_s", bound=Schema)


class Paginated(typing.Generic[T_s]):
    """
    Paginated response model generator.

    Usage::

        @router.method("path", response_model=Paginated[ItemModel])
    """

    __models__: dict[str, type[Schema]] = {}

    pagination: PaginationData
    items: list[T_s]

    def __class_getitem__(cls, item_model: type[T_s]) -> type[Schema]:
        model_name = item_model.__qualname__ + "Pagination"

        if model_name in cls.__models__:
            return cls.__models__[model_name]

        model = typing.cast(
            type[Schema],
            type(
                model_name,
                (Schema,),
                dict(
                    __annotations__=dict(
                        pagination=PaginationData, items=list[item_model]
                    ),
                    pagination=Field(description="Information about the pagination"),
                    items=Field(description="List of items"),
                ),
            ),
        )

        cls.__models__[model_name] = model

        return model
