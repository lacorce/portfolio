import tomllib
from types import SimpleNamespace

def open_config(key: str = None):
    with open('config.toml', 'rb') as f:
        config = tomllib.load(f)

    all_config = SimpleNamespace(**config)

    if key is None:
        return all_config
    return getattr(all_config, key, None)