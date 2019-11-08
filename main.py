import sys

import webview

from api import JsApi


def is_frozen():
    return hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS')


if __name__ == "__main__":
    api = JsApi()
    url = "view/dist/index.html" if is_frozen() else "http://localhost:8080"

    window = webview.create_window("Private File Bucket", url=url, js_api=api, width=660,
                                   height=800)
    webview.start(debug=False)
