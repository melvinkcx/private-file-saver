from logging import StreamHandler
from typing import Callable


class JsApiHandler(StreamHandler):
    """
    JsApiHandler is a misnomer, having a hard time naming this log handler
    """

    def __init__(self, send_func: Callable):
        self._send_func = send_func
        super().__init__()

    def emit(self, record):
        msg = self.format(record)
        self._send_func(msg)
