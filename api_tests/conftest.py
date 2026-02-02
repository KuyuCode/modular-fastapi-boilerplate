import pytest
import asyncio
from api import make_app
from api_tests import helpers
from contextlib import ExitStack
from async_asgi_testclient import TestClient


@pytest.fixture(autouse=True)
def _app():
    with ExitStack():
        yield make_app(test_mode=True)


@pytest.fixture
async def client(_app):
    async with TestClient(_app) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop(request):
    _ = request
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def timer() -> helpers.timer.DebugBreakpointTimer:  # type: ignore
    """
    Used to test for slowness of application

    Usage:
    ::
        def test_something(debug_timer):
            with debug_timer.timeit("fibonacci") as timer:
                fib = fibonacci(1024)

            with debug_timer.timeit("sleep") as timer:
                time.sleep(1)

            assert timer.took < 1.01

            # To see timer results in teardown output
            assert debug_timer.echo
    """

    timer = helpers.timer.DebugBreakpointTimer()

    try:
        with timer.timeit("test"):
            yield timer  # type: ignore
    finally:
        print()
        print("--------------------------- TEST TIMER ".ljust(80, "-"))
        print()
        timer.print()
        print()
        print("--------------------------- TEST TIMER ".ljust(80, "-"))
        print()
