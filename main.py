import sys

import webview

from core.api import PFSApi

__version__ = '0.1.0'

from core.logging import add_stream_handler, add_jsapi_handler


def is_frozen():
    return hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS')


if __name__ == "__main__":
    api = PFSApi()
    url = "ui/index.html" if is_frozen() else "http://localhost:8080"

    add_stream_handler()
    add_jsapi_handler(send_func=api.set_current_log)

    window = webview.create_window("Private File Bucket", url=url, js_api=api, width=660,
                                   height=800)
    webview.start(debug=not is_frozen())
