import typing
import fastapi
from typing import cast
from . import util, protocols
from pydantic.fields import Field
from collections.abc import Mapping
from .schema import Schema, ErrorModel


__all__ = ["APIError", "define_error", "define_error_category"]

# {category: {code: (message, code)}}
errors: dict[str, dict[str, tuple[str, int]]] = {}


class APIError(fastapi.HTTPException):
    models: dict[str, type[ErrorModel]] = {}

    @property
    def model(self) -> type[ErrorModel]:
        """
        Generate error model for specific category and code.
        This used only for endpoint response schema generation
        """

        model_name = (
            "Error_"
            + util.string.snake_to_pascal(self.category, "/")
            + "_"
            + util.string.snake_to_pascal(self.code, "-")
        )

        if model_name in self.models:
            return self.models[model_name]

        origin_fields = ErrorModel.model_fields

        message_description = origin_fields["message"].description
        category_description = origin_fields["category"].description
        code_description = origin_fields["code"].description
        cat_description = origin_fields["cat"].description

        model = cast(
            type[ErrorModel],
            type(
                model_name,
                (Schema,),
                {
                    "__annotations__": {
                        "code": str,
                        "category": str,
                        "message": str,
                        "cat": str,
                    },
                    "code": Field(self.code, description=code_description),
                    "category": Field(self.category, description=category_description),
                    "message": Field(self.message, description=message_description),
                    "cat": Field(
                        "https://http.cat/{cat}".format(cat=self.status_code),
                        description=cat_description,
                    ),
                },
            ),
        )

        self.models[model_name] = model

        return model

    def __init__(
        self,
        category: str,
        code: str,
        message: str,
        status_code: int,
        headers: Mapping[str, str] | None = None,
        extra: Mapping[str, typing.Any] | None = None,
    ):
        self.code: str = code
        self.extra: Mapping[str, typing.Any] | None = extra
        self.headers: Mapping[str, str] | None = headers
        self.message: str = message
        self.category: str = category
        self.status_code: int = status_code

        self.formatted_message: str = self.message
        if self.extra is not None:
            self.formatted_message = self.message.format(**self.extra)

    def __repr__(self):
        return f"APIError<{self.category}:{self.code}:{self.status_code}>({self.message!r})"

    def __str__(self):
        return f"{self.category}+{self.code}: {self.formatted_message}"

    def __call__(
        self,
        extra: Mapping[str, typing.Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ):
        return APIError(
            self.category,
            self.code,
            self.message,
            self.status_code,
            headers or self.headers,
            extra,
        )

    @property
    def response(self) -> fastapi.responses.JSONResponse:
        return fastapi.responses.JSONResponse(
            content=ErrorModel(
                message=self.formatted_message,
                category=self.category,
                code=self.code,
                cat="https://http.cat/{cat}".format(cat=self.status_code),  # type: ignore
            ).model_dump(mode="json"),
            status_code=self.status_code,
            headers=self.headers,
        )


def define_error_category(category: str) -> protocols.DefineErrorProtocol:
    _category = errors.setdefault(category, {})

    def _define_error(code: str, message: str, status_code: int) -> APIError:
        message, status_code = _category.setdefault(code, (message, status_code))

        return APIError(category, code, message, status_code)

    return _define_error


def define_error(category: str, code: str, message: str, status_code: int) -> APIError:
    return define_error_category(category)(code, message, status_code)
