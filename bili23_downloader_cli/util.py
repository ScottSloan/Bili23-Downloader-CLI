from pathlib import Path


def get_user_config_path() -> Path:
    """
    返回系统用户的.config目录
    - win -> C:\\Users\\username\\\\.config
    - linux/macOS -> ~/.config
    """

    return Path.home() / ".config"
