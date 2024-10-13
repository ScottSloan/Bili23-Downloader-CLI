from pathlib import Path
from typing import List, Tuple


def get_user_config_path() -> Path:
    """
    返回系统用户的.config目录
    - win -> C:\\Users\\username\\\\.config
    - linux/macOS -> ~/.config
    """

    return Path.home() / ".config"


def calc_chunk(total_size: int, chunk: int) -> List[Tuple[int, int]]:
    piece_size = int(total_size / chunk)
    chunk_list: List[Tuple[int, int]] = []

    for i in range(chunk):
        start = i * piece_size + 1 if i != 0 else 0
        end = (i + 1) * piece_size if i != chunk - 1 else total_size

        chunk_list.append((start, end))

    return chunk_list
