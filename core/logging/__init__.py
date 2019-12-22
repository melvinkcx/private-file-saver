import logging
from typing import Callable

from core.logging.handlers import JsApiHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Stream Handler
def add_stream_handler(logging_level=logging.DEBUG):
    stream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(logging_level)
    logger.addHandler(stream_handler)


# JsApi Handler
def add_jsapi_handler(send_func: Callable, logging_level=logging.DEBUG):
    jsapi_formatter = logging.Formatter('%(message)s')
    jsapi_handler = JsApiHandler(send_func=send_func)
    jsapi_handler.setFormatter(jsapi_formatter)
    jsapi_handler.setLevel(logging_level)
    logger.addHandler(jsapi_handler)
