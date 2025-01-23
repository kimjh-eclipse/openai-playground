import os
from pathlib import Path

from dotenv import load_dotenv


class EnvironmentManager:
    def __init__(self):
        load_dotenv(dotenv_path=Path(".env"))
        self._environment_variables = {}
    def _set_os_env(self):
        self._environment_variables.update(os.environ)
    def get(self, key: str, default=None) -> str:
        return self._environment_variables.get(key, default)


env_manager = EnvironmentManager()
