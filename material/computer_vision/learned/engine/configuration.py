import json
from typing import Dict


def load_config(config_pathname: str) -> Dict:
    """
    Load a configuration from a JSON file on disk.

    @p config_pathname A pathname to a JSON file to load.
    @return The loaded configuration.
    """
    with open(config_pathname, "r") as f:
        config = json.load(f)
    return config
