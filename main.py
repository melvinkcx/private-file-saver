import webview

from api import JsApi


if __name__ == "__main__":
    api = JsApi()
    webview.create_window("Private File Bucket", url="http://localhost:8081/index.html", js_api=api, width=660,
                          height=800)
    webview.start()
