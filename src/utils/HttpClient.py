from typing import Union, Callable
import requests


class HttpClient:
    @classmethod
    def request(cls, method, url, payload, resolve: Callable[[requests.Response], None]):
        with requests.Session() as s:
            response = s.request(method=method, url=url, data=payload)

            if response.encoding is None:
                response.encoding = 'utf-8'

            resolve(response)
