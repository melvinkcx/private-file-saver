import multiprocessing
import os
from pathlib import Path

import yaml


class ConfigManager:
    """
    ConfigManager,
    An interface to update and manipulate configurations.
    """
    default_config = {
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

    def __init__(self):
        self.CONFIG_FILE = os.path.join(str(Path.home()), '.pfs/config.yml')
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        
        self.config = self._read_config()

    def __getattr__(self, item):
        return self.default_config[item]

    def _read_config(self):
        try:
            with open(self.CONFIG_FILE, "r") as f:
                self.config = yaml.load(f.read())
        except FileNotFoundError:
            self.config = self._create_config()

        return self.config

    def _create_config(self):
        with open(self.CONFIG_FILE, "w") as f:
            f.write(yaml.dump(self.default_config))

        return self.default_config

    def _save_config(self):
        with open(self.CONFIG_FILE, "w") as f:
            f.write(yaml.dump(self.config))

    def set(self, key, value):
        if key not in self.default_config:
            raise AssertionError(f"Unknown key: {key}")

        self.config[key] = value
        self._save_config()

        return self.config

    def set_many(self, values):
        for k in values.keys():
            if k not in self.default_config:
                raise AssertionError(f"Unknown key: {k}")

        self.config = {
            **self.config,
            **values
        }
        self._save_config()

        return self.config

    def get(self, key):
        return self.config[key]

    def all(self):
        """
        All config values
        """
        return self.config

    def list_configurables(self):
        """
        List configurable parameters
        """
        return self.default_config.keys()

    def is_initialized(self):
        """
        It is initialized when all Configs are set (not None)
        """
        return None not in self.all().values()
