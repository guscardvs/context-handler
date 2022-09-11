from typing import Callable

import requests

from context_handler import interfaces


class HttpAdapter(interfaces.Adapter[requests.Session]):
    def __init__(
        self,
        session_factory: Callable[[], requests.Session] = requests.Session,
    ) -> None:
        self._factory = session_factory

    def is_closed(self, client: requests.Session) -> bool:
        """Requests Session object is always
        valid so this method is just for the interface"""
        del client
        return False

    def release(self, client: requests.Session) -> None:
        client.close()

    def new(self):
        return self._factory()
