import json
import multiprocessing
import os
from pathlib import Path
from core.log_utils import logger


class ConfigManager:
    """
    ConfigManager,
    An interface to update and manipulate configurations.
    """
    _default_config = {
        # Transfer Config
        'READ_CHUNK_SIZE': 8 * 1024,  # 8KB
        'MULTIPART_THRESHOLD': 1 * 1024 ** 2,  # 1MB
        'MULTIPART_CHUNKSIZE': 8 * 1024 ** 2,  # 1MB
        'MAX_CONCURRENCY': multiprocessing.cpu_count(),
        'AWS_ACCESS_KEY_ID': None,
        'AWS_SECRET_ACCESS_KEY': None,
        'AWS_REGION': None,
        'DEFAULT_BUCKET_NAME': None,
        'TARGET_PATH': None
    }

    def __init__(self, config_file_path=None):
        self._CONFIG_FILE = config_file_path or os.path.join(str(Path.home()), '.pfs/config.json')
        os.makedirs(os.path.dirname(self._CONFIG_FILE), exist_ok=True)

        self._config = self._read_config()

    def __getattr__(self, item):
        return self._config[item]

    def _read_config(self):
        try:
            with open(self._CONFIG_FILE, "r") as f:
                self._config = json.load(f)
        except FileNotFoundError:
            self._config = self._create_config()

        return self._config

    def _create_config(self):
        with open(self._CONFIG_FILE, "w") as f:
            json.dump(self._default_config, f)

        return self._default_config

    def _save_config(self):
        with open(self._CONFIG_FILE, "w") as f:
            json.dump(self._config, f)

    def set(self, key, value):
        if key not in self._default_config:
            raise AssertionError(f"Unknown key: {key}")

        self._config[key] = value
        self._save_config()

        return self._config

    def set_many(self, values):
        for k in values.keys():
            if k not in self._default_config:
                raise AssertionError(f"Unknown key: {k}")

        self._config = {
            **self._config,
            **values
        }
        self._save_config()

        return self._config

    def get(self, key):
        return self._config[key]

    def all(self):
        """
        All config values
        """
        return self._config

    def list_configurables(self):
        """
        List configurable parameters
        """
        return self._default_config.keys()

    def is_initialized(self):
        """
        It is initialized when all Configs are set (not None)
        """
        return None not in self.all().values()

    def reset_configs(self):
        logger.warning(f"Deleting config file {self._CONFIG_FILE}")
        if os.path.exists(self._CONFIG_FILE):
            os.remove(self._CONFIG_FILE)
            logger.info("Config file successfully removed")
        self._config = self._default_config
        return self._config
