from enum import Enum
from ipaddress import IPv4Address
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Annotated, Any, Dict, Optional

from typer import Argument, Option, Typer

from bili23_downloader_cli.config import check_config, get_config
from bili23_downloader_cli.utils.constant import VideoCodec, VideoQuality

app = Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Bilibili视频下载器",
    epilog="Made with :heart:  in [blue]Seven Dreamer[/blue]",
)


class VideoType(Enum):
    Bangumi = "番剧"
    """番剧"""
    Movie = "电影"
    """电影"""
    Guochuang = "国创"
    """国创"""
    Documentary = "纪录片"
    """纪录片"""
    Normal = "用户投稿视频"
    """用户投稿视频"""


def get_video_type(video_type: int) -> VideoType:
    """
    通过视频信息判断视频的是什么类型
    """
    match video_type:
        case 1:
            return VideoType.Bangumi
        case 2:
            return VideoType.Movie
        case 3:
            return VideoType.Guochuang
        case 4:
            return VideoType.Guochuang
        case _:
            return VideoType.Normal


def get_version() -> str:
    """从pyproject.toml中获取版本"""
    raise NotImplementedError


def show_version(enabled: bool):
    """显示版本信息"""
    if enabled:
        version = get_version()
        print(f"Bili23 Version: {version}")


def get_video_info(url: str) -> Dict[str, Any]:
    """
    获取视频信息
    """
    # TODO: 这里发送请求过去，大概就是写一个 request.get()  什么的方法过去就是了

    raise NotImplementedError


# command 它们就应该留在这个目录或者 cli.py
########################################
@app.command()
def download(
    url: Annotated[
        str,
        Argument(help="视频链接,暂不支持输入多个url地址", show_default=False),
    ],
    show_info: Annotated[
        bool, Option("--info", "-i")
    ] = False,  # 下载的时候默认不显示视频的信息，如果需要显示，则跟 --info / -i
):
    """下载"""
    check_config()
    # config = get_config()

    # video_info = get_video_info(url)
    # get_video_type(video_info["type"])

    if show_info:
        # TODO： 需要接rich 打印视频的信息
        ...

    # TODO: 这里可以跟上promt 进行交互
    # 是否选择 视频品质，默认为配置的value
    # 是否选择 音频品质, 同上
    # ...


@app.command()
def repo():
    """
    本地仓库列表

    用来查看已经下载的视频，所在的位置，查看视频的详情信息等，
    """
    raise NotImplementedError


@app.command()
def config():
    """查看 or 编辑 配置"""
    raise NotImplementedError


# TODO： 需要支持输入多个url 进行下载
@app.callback()
def main(
    version: Annotated[
        bool,
        Option(
            "--version", "-v", callback=show_version, help="show version", is_eager=True
        ),
    ] = False,
):
    """
    BiliBili 视频下载工具
    """
