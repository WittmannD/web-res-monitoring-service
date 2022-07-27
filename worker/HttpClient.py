import asyncio
from asyncio import Task
from typing import Union

import aiohttp


def debounce(wait):
    def wrap(fn):
        task = None

        async def debounced(*args, **kwargs):
            nonlocal task

            async def call_it(wait_for):
                await asyncio.sleep(wait_for)
                await fn(*args, **kwargs)

            if isinstance(task, Task):
                task.cancel()
                task = None

            task = asyncio.create_task(call_it(wait))

        return debounced

    return wrap


class HttpClientMeta(type):
    session_close_delay = 10

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._session: Union[aiohttp.ClientSession, None] = None

    @property
    def session(cls) -> aiohttp.ClientSession:
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession()
        return cls._session

    @debounce(session_close_delay)
    async def close(cls) -> None:
        if cls._session is not None:
            await cls._session.close()


class HttpClient(metaclass=HttpClientMeta):
    @classmethod
    async def request(cls, method, url, payload, resolve):
        session = cls.session

        async with session.request(method=method, url=url, data=payload) as response:
            await resolve(response)

        await cls.close()
