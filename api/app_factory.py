import fastapi
from typing import Callable
from . import schema, error, util
from fastapi import APIRouter, FastAPI
from .route import router as root_router
from .session_holder import session_holder
from contextlib import AbstractAsyncContextManager
from .error_handlers import default_handler, error_handler, validation_error_handler


def create_lifespan(
    test_mode: bool = True,
) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
    async def lifespan(app: fastapi.FastAPI):
        # Do something to optimize tests run
        # Note: test mode is not development mode. Test mode only used for pytest to run.
        # For development just configure project to local environment
        if test_mode:
            pass
        else:
            session_holder.init(util.settings.sqalchemy.url)  # type: ignore
            util.fastapi.setup_route_errors(app)

        yield

        if not test_mode:
            await session_holder.close()

    return util.contextmanager.async_manager(lifespan)


def make_app(test_mode: bool = False) -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        lifespan=create_lifespan(test_mode=test_mode),
        redoc_url=None,
        responses={422: dict(model=schema.ValidationErrorModel)},
        title=util.settings.app.title,  # type: ignore
        version=util.settings.app.version,  # type: ignore
    )

    router: APIRouter = getattr(app, "router")
    router.default = default_handler

    app.include_router(root_router)

    app.add_exception_handler(error.APIError, error_handler)  # type: ignore
    app.add_exception_handler(fastapi.exceptions.RequestValidationError, validation_error_handler)  # type: ignore

    return app


@root_router.get(
    "/",
    response_class=fastapi.responses.RedirectResponse,
    include_in_schema=False,
)
async def root():
    return fastapi.responses.RedirectResponse(
        "/docs", status_code=fastapi.status.HTTP_308_PERMANENT_REDIRECT
    )


@root_router.get(
    "/errors", summary="List all defined errors", operation_id="list_errors"
)
async def errors() -> dict[str, dict[str, tuple[str, int]]]:
    return error.errors
