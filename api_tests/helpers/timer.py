import time
from typing import Callable


class DebugContextTimer:
    def __init__(
        self, name: str, callback: Callable[[float], None] | None = None, echo: bool = True
    ):
        self.__start = time.time()
        self.__end: float | None = None
        self.__name = name
        self.__callback = callback
        self.__echo = echo

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _ = exc_type, exc_val, exc_tb
        self.__end = time.time()
        if self.__echo:
            print(f"[DebugTimer] {self.__name} took {self.__end - self.__start:.3f} seconds")

        if self.__callback:
            self.__callback(self.__end)

        return False

    @property
    def took(self) -> float:
        assert self.__end is not None
        return self.__end - self.__start


class DebugBreakpointTimer:
    # Use assert debug_time.echo to get outputs
    echo = False

    def __init__(self):
        self.__time = time.time()

        self._breaks = []

    def breakpoint(self, name: str) -> "DebugBreakpointTimer":
        self._breaks.append((name, time.time()))
        return self

    def timeit(self, name: str) -> DebugContextTimer:
        self._breaks.append((f"[start] {name}", time.time()))
        return DebugContextTimer(
            name, lambda end: self._breaks.append((f"[end] {name}", end)), False
        )

    def print(self):
        last_stamp = self.__time
        print("NAME".ljust(35), "STAMP".ljust(20), "TOOK", sep="")
        for name, stamp in self._breaks:

            print(
                name.ljust(35),
                f"{stamp:.3f}".ljust(20),
                f"{(stamp - last_stamp) * 1000:.3f}",
                sep="",
            )
            last_stamp = stamp
