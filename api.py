class JsApi:
    """
    JsAPI is the JS correspondent to PythonAPI in view/api.js
    This is the interface Python communicates to our View layer (Frontend, Vue.js)

    Caveat:
    - JS will send at least 1 positional argument.(None,)
    """
    def ping(self, *args):
        return "Pong"
