import os
import yaml
import re
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class ConfigLoader:
    _instance = None

    def __new__(cls, config_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = cls._instance._load_config(config_path)
        return cls._instance

    def __getattr__(self, name):
        """Enable dot notation access for top-level and nested attributes."""
        value = self._config.get(name)
        if isinstance(value, dict):  # Convert dictionaries to ConfigLoader for deeper dot access
            return ConfigLoader._dict_to_attr(value)
        return value

    def _load_config(self, config_path=None):
        """Loads the configuration from a YAML file and applies environment variable substitution."""
        load_dotenv()
        config_path = Path(config_path) if config_path else Path(__file__).parent / 'config.yaml'
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        return self._substitute_env_vars(config)

    def _substitute_env_vars(self, value):
        """Recursively replace environment variables in the config, including inline values."""
        if isinstance(value, dict):
            return {k: self._substitute_env_vars(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._substitute_env_vars(v) for v in value]
        if isinstance(value, str):
            return re.sub(r'\${(\w+)}', lambda m: os.getenv(m.group(1), m.group(0)), value)
        return value

    @staticmethod
    def _dict_to_attr(d):
        """Convert a dictionary to an object supporting dot notation."""
        class AttrDict(dict):
            """Dictionary subclass that allows attribute-style access."""
            def __getattr__(self, item):
                value = self.get(item)
                if isinstance(value, dict):
                    return ConfigLoader._dict_to_attr(value)
                return value
        return AttrDict(d)
