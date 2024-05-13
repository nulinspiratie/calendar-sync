from pathlib import Path
import tomllib
import calendar_sync


def get_root_folder():
    return Path(calendar_sync.__file__).parent.parent


def get_configuration():
    root_folder = get_root_folder()
    config_path = root_folder / "config.toml"
    config = tomllib.loads(config_path.read_text())
    return config
