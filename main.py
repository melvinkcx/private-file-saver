import sys

import webview

from core.api import PFSApi

__version__ = '0.0.1'


def is_frozen():
    return hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS')


if __name__ == "__main__":
    api = PFSApi()
    url = "ui/index.html" if is_frozen() else "http://localhost:8080"

    window = webview.create_window("Private File Bucket", url=url, js_api=api, width=660,
                                   height=800)
    webview.start(debug=not is_frozen())
