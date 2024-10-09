import os
import time
import click
import colorama
from threading import Thread

from bili23_downloader_cli.cli.common import (
    check_arguments,
    check_ffmpeg_available,
    show_bangumi_info,
    show_episodes_selection,
    show_error_info,
    show_version_info,
    show_video_info,
)
from bili23_downloader_cli.utils.config import Config
from bili23_downloader_cli.utils.tools import find_str, process_shortlink
from bili23_downloader_cli.utils.video import VideoInfo, VideoParser
from bili23_downloader_cli.utils.bangumi import BangumiInfo, BangumiParser
from bili23_downloader_cli.cli.download import DownloadUtils

colorama.init(autoreset=True)


class Info:
    type = ""


def parse(url: str, info: bool = False):
    if find_str("b23.tv", url):
        url = process_shortlink(url)

    if find_str("BV|av", url):
        VideoParser(show_error_info, None).parse_url(url)

        show_video_info()

        Info.type = "video"

    elif find_str("ep|ss|md", url):
        BangumiParser(show_error_info).parse_url(url)

        show_bangumi_info()

        Info.type = "bangumi"
    else:
        show_error_info(400)

    if info:
        return

    if not Config.download_all:
        time.sleep(1.5)

    if (
        len(VideoInfo.pages) > 1
        or len(VideoInfo.episodes) > 1
        or len(BangumiInfo.episodes) > 1
    ):
        episodes_selection = show_episodes_selection(Info.type)

    else:
        episodes_selection = 0

    downloader = DownloadUtils(Info.type, episodes_selection, show_error_info)

    if Info.type == "video":
        downloader.get_video_download_list()
    elif Info.type == "bangumi":
        downloader.get_bangumi_download_list()
    elif Info.type == "audio":
        downloader.get_audio_download_list()

    downloader.start_download()


@click.command()
@click.option("--i", "--info", help="显示视频链接")
@click.option("--p", "--parse", help="解析视频链接")
@click.option(
    "--d", "--dir", default=os.getcwd(), help="指定下载目录，默认为当前运行目录"
)
@click.option(
    "--t",
    "--thread",
    default=Config.Download.max_thread,
    help="指定下载所用线程数，默认为 4 个线程",
)
@click.option(
    "--q",
    "--quality",
    default=Config.Download.quality,
    help="指定下载的清晰度，默认为 80 (1080P)",
)
@click.option(
    "--c",
    "--codec",
    default=Config.Download.codec,
    help="指定下载的视频编码，默认为 hevc (HEVC/H.265)",
)
@click.option("--quiet", is_flag=True, help="静默输出")
@click.option("--a", "--all", is_flag=True, help="下载全部视频")
@click.option("--edit-config", is_flag=True, help="编辑配置文件")
@click.option(
    "--v",
    "--version",
    callback=show_version_info,
    expose_value=False,
    is_eager=True,
    is_flag=True,
    help="显示版本信息",
)
def main(
    i: str, p, d: str, t: int, q: int, c: str, quiet: bool, a: bool, edit_config: bool
):
    check_ffmpeg_available()

    Config.Download.path = d
    Config.Download.max_thread = t
    Config.Argument.download_all = a
    Config.Download.quality = q
    Config.Download.codec = c

    Config.Argument.quiet = quiet
    Config.Argument.edit = edit_config

    check_arguments()

    if p:
        Thread(target=parse, args=(p,)).start()
    elif i:
        Config.Argument.show_quality_list = True

        Thread(
            target=parse,
            args=(
                i,
                True,
            ),
        ).start()
    else:
        print("Bili23 Downloader CLI {}\n".format(Config.APP.version))

        print("用法：")
        print("bili23 [OPTIONS]")
        print('\n键入 "bili23 --help" 获取帮助。')


if __name__ == "__main__":
    main()
