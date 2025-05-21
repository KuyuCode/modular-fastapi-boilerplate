import typing
from fastapi import FastAPI
from types import FunctionType, UnionType
from collections.abc import Callable
from fastapi.routing import APIRoute
from fastapi.utils import create_model_field
from fastapi.dependencies.models import Dependant

if typing.TYPE_CHECKING:
    from ..error import APIError
    from ..schema import ErrorModel

__all__ = ["api_errors", "setup_route_errors"]


def dependant_has_dependency(dependant: Dependant, call: FunctionType | Callable) -> bool:
    for dependency in dependant.dependencies:
        if dependency.call is call:
            return True

        if dependant_has_dependency(dependency, call):
            return True

    return False


def route_has_dependency(route: APIRoute, call: FunctionType | Callable) -> bool:
    return dependant_has_dependency(route.dependant, call)


dependency_errors: dict[Callable, tuple["APIError", ...]] = {}


def api_errors(*errors: "APIError"):
    def decorator(func):
        if func in dependency_errors:
            dependency_errors[func] = dependency_errors[func] + errors
        else:
            dependency_errors[func] = errors
        return func

    return decorator


def errors_to_models(errors: tuple["APIError", ...]) -> dict[int, "type[ErrorModel] | UnionType"]:
    """Combine errors by status code and return their models"""
    result: dict[int, type[ErrorModel] | UnionType] = {}

    for error in errors:
        if error.status_code not in result:
            result[error.status_code] = error.model
            continue

        result[error.status_code] |= error.model

    return result


def setup_route_errors(app: FastAPI):
    for call, errors in dependency_errors.items():
        error_models = errors_to_models(errors)
        for route in app.routes:
            if not isinstance(route, APIRoute):
                continue

            if route_has_dependency(route, call):
                for code, model in error_models.items():
                    field = create_model_field(
                        f"Response_{code}_{route.unique_id}",
                        model,
                        mode="serialization",
                    )
                    route.responses.setdefault(code, dict(model=model))
                    route.response_fields.setdefault(code, field)
