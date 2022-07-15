import asyncio
from typing import Awaitable, Callable, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def _async(func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    """
    Wraps a blocking function to be executed asynchronously.
    ```
    @_async
    def request(url: str) -> str:
        return requests.get(url).text

    async def main():
        print(await request("https://www.google.com"))
    ```
    """

    def decorator(*args: P.args, **kwargs: P.kwargs) -> Awaitable[R]:
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, func, *args, **kwargs)

    return decorator


__all__ = ["_async"]
