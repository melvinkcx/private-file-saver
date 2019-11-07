import webview

from api import JsApi


if __name__ == "__main__":
    api = JsApi()
    window = webview.create_window("Private File Bucket", url="http://localhost:8080/index.html", js_api=api, width=660,
                                   height=800)
    webview.start(debug=True)
