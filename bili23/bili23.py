import time
import click
import colorama
from threading import Thread

from .utils.video import VideoInfo, VideoParser
from .utils.bangumi import BangumiInfo, BangumiParser
from .utils.audio import AudioInfo, AudioParser
from .utils.tools import *

from .cli.download import DownloadUtils
from .cli.common import *

colorama.init(autoreset = True)

class Info:
    type = ""

def parse(url, info = False):
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
    
    elif find_str("au|am", url):
        AudioParser(show_error_info).parse_url(url)

        show_audio_info()

        Info.type = "audio"
    else:
        show_error_info(400)

    if info: return

    if not Config.download_all:
        time.sleep(1.5)

    if len(VideoInfo.pages) > 1 or len(VideoInfo.episodes) > 1 or len(BangumiInfo.episodes) > 1:
        episodes_selection = show_episodes_selection(Info.type)
    
    elif AudioInfo.count > 1:
        episodes_selection = show_audio_selection()
        
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
@click.option("--i", "--info", help = "显示视频链接")
@click.option("--p", "--parse", help = "解析视频链接")
@click.option("--d", "--dir", default = os.getcwd(), help = "指定下载目录，默认为当前运行目录")
@click.option("--t", "--thread", default = Config.thread, help = "指定下载所用线程数，默认为 4 个线程")
@click.option("--q", "--quality", default = Config.quality, help = "指定下载的清晰度，默认为 80 (1080P)")
@click.option("--c", "--codec", default = Config.codec, help = "指定下载的视频编码，默认为 HEVC (HEVC/H.265)")
@click.option("--danmaku", is_flag = True, help = "下载弹幕")
@click.option("--subtitle", is_flag = True, help = "下载字幕")
@click.option("--lyric", is_flag = True, help = "下载歌词")
@click.option("--quiet", is_flag = True, help = "静默输出")
@click.option("--a", "--all", is_flag = True, help = "下载全部视频")
@click.option("--edit-config", is_flag = True, help = "编辑配置文件")
@click.option("--v", "--version", callback = show_version_info, expose_value = False, is_eager = True, is_flag = True, help = "显示版本信息")
def main(i, p, d, t, q, c, danmaku, subtitle, lyric, quiet, a, edit_config):
    check_ffmpeg_available()
    
    Config.dir = d
    Config.thread = t
    Config.download_all = a
    Config.quality = q
    Config.codec = c
    Config.danmaku = danmaku
    Config.subtitle = subtitle
    Config.lyric = lyric
    Config.quiet = quiet
    Config.edit = edit_config

    check_arguments()

    if p:
        Thread(target = parse, args = (p, )).start()
    elif i:
        Config.show_quality_list = True
        
        Thread(target = parse, args = (i, True, )).start()
    else:
        print("Bili23 Downloader CLI {}\n".format(Config.app_version))

        print("用法：")
        print("bili23 [OPTIONS]")
        print('\n键入 "bili23 --help" 获取帮助。')

if __name__ == "__main__":
    main()