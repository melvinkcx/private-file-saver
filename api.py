from typing import Mapping

from core.syncer import Syncer
from core.configs.manager import ConfigManager


class JsApi:
    """
    JsAPI is the JS correspondent to PythonAPI in view/api.js
    This is the interface Python communicates to our View layer (Frontend, Vue.js)

    Caveat:
    - JS will send at least 1 positional argument.(None,)
    """
    def __init__(self):
        self.config_manager = ConfigManager()
        self.syncer = Syncer()

    def ping(self, *args):
        return "Pong"

    # ConfigManager
    def get_configs(self, *args):
        return self.config_manager.all()

    def set_configs(self, values: Mapping[str, str]):
        return self.config_manager.set_many(values)

    # Syncer
    def get_files(self, path):
        return self.syncer.scan(path)

    def sync(self):
        pass
