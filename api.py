from typing import Mapping

from core.configs.manager import ConfigManager
from core.syncer import Syncer


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

    def is_initialized(self, *args):
        return self.config_manager.is_initialized()

    # ConfigManager
    def list_configs(self, *args):
        return self.config_manager.all()

    def set_configs(self, values: Mapping[str, str]):
        return self.config_manager.set_many(values)

    def list_configurables(self):
        """
        :return: a list of configurable parameters
        """
        return self.config_manager.list_configurables()

    # Syncer
    def scan(self, path=None):
        if path is None:
            path = self.config_manager.get("TARGET_PATH")

        return self.syncer.scan(path)

    def sync(self):
        path = self.config_manager.get("TARGET_PATH")
        return self.syncer.sync(path)
