from pydantic import HttpUrl
from .model import Schema, Field


__all__ = ["ValidationErrorModel", "ErrorModel"]


class InvalidField(Schema):
    path: list[str | int] | None = Field(description="Path to deep fields")
    at: str = Field(description="Field location: path, query, body, header")
    message: str = Field(description="The message of the error")
    category: str = Field(description="The category of the error")


class ValidationErrorModel(Schema):
    fields: dict[str, InvalidField] = Field(
        description="Dictionary of fields that failed validation",
        examples=[
            {
                "nickname": InvalidField(
                    path=None,
                    at="body",
                    message="Nickname can contain only ascii-letters, numbers and underscores",
                    category="assertion_error",
                )
            },
        ],
    )
    general: str = Field(
        description="General error message",
        examples=[
            "Invalid field nickname: Nickname can contain only ascii-letters, numbers and underscores"
        ],
    )
    cat: HttpUrl = Field(description="Error cat", examples=["https://http.cat/422"])


class ErrorModel(Schema):
    message: str = Field(description="Error message", examples=["User not found"])
    category: str = Field(description="Error category", examples=["users"])
    code: str = Field(description="Error code", examples=["not-found"])
    cat: HttpUrl = Field(description="Error cat", examples=["https://http.cat/404"])
