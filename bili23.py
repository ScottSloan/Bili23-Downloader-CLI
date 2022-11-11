import re
import time
import click
import colorama
#import qrcode_terminal
from threading import Thread

from utils.video import VideoInfo, VideoParser
from utils.bangumi import BangumiInfo, BangumiParser
from utils.login import Login, LoginInfo

from utils.tools import *

from cli.download import DownloadUtils

class Info:
    type = ""

def show_version_info(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    print("Bili23 Downloader CLI\n")

    print("下载 Bilibili 视频/番剧/电影/纪录片 等资源\n")

    print("当前版本：1.00")
    print("发布日期：20221111")
    print("开发者：Scott Sloan\n")

    print("本程序遵循 MIT 开源协议。\n")

    ctx.exit()

def login(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    print("请使用哔哩哔哩客户端扫码登录\n")

    login = Login()

    #qrcode_terminal.draw(LoginInfo.url)


    ctx.exit()
    
def parse(url, info = False):
    if find_str("BV|av", url):
        video_parser.parse_url(url)

        show_video_info()

        Info.type = "video"

    elif find_str("ep|ss|md", url):
        bangumi_parser.parse_url(url)

        show_bangumi_info()

        Info.type = "bangumi"
    else:
        print("错误：无法识别的链接，请检查链接是否正确")

    if info: return

    time.sleep(1.5)
    input("按回车键继续...")
    episodes_selection = 0

    if len(VideoInfo.pages) > 1 or len(VideoInfo.episodes) > 1:
        episodes_selection = show_pages_selection()

    if len(BangumiInfo.episodes) > 1:
        episodes_selection = show_episodes_selection()

    downloader = DownloadUtils(Info.type, episodes_selection)
    
    if Info.type == "video":   
        downloader.get_video_download_list()
    else :
        downloader.get_bangumi_download_list()
    
    downloader.download_video()

def show_video_info():
    print("视频信息：\n", flush = True)

    print("名称：" + VideoInfo.title)
    print("\n简介：" + VideoInfo.desc)

    print("\n播放：" + VideoInfo.view)
    print("点赞：" + VideoInfo.like)
    print("投币：" + VideoInfo.coin)
    print("弹幕：" + VideoInfo.danmaku)
    print("收藏：" + VideoInfo.favorite)
    print("评论：" + VideoInfo.reply)
    print()

def show_bangumi_info():
    print("视频信息：\n", flush = True)

    print("类型：" + BangumiInfo.type)
    print("名称：" + BangumiInfo.title)
    print("状态：" + BangumiInfo.newep)
    print("\n简介：" + BangumiInfo.desc)

    print("\n播放：" + BangumiInfo.view)
    print("投币：" + BangumiInfo.coin)
    print("弹幕：" + BangumiInfo.danmaku)
    print("收藏：" + BangumiInfo.favorite)
    print("评分：{}".format(BangumiInfo.score))
    print()

def show_pages_selection():
    if VideoInfo.collection:
        pages_list = ["{}.{}".format(index + 1, value["title"]) for index, value in enumerate(VideoInfo.episodes)]
    else:
        pages_list = ["{}.{}".format(i["page"], i["part"] if VideoInfo.multiple else VideoInfo.title) for i in VideoInfo.pages]

    pages_count = len(pages_list)

    print("\n剧集列表：\n   ", end = '', flush = True)
    print("\n   ".join(pages_list))

    while True:
        pages_selection = input("\n请选择要下载的视频（填序号，0 为全部下载）：")
        result = re.findall("^\d*$", pages_selection)

        if len(result) == 0 or int(result[0]) not in range(0, pages_count + 1):
            print("\033[31m输入无效，请重试\033[0m")

        else:
            break
    
    print()

    return int(pages_selection)
    
def show_episodes_selection():
    episodes_list = ["{}.{}".format(index + 1, format_bangumi_title(value)) for index, value in enumerate(BangumiInfo.episodes)]
    episodes_count = len(episodes_list)
    
    print("\n剧集列表：\n   ", end = '', flush = True)
    print("\n   ".join(episodes_list))

    while True:
        episodes_selection = input("\n请选择要下载的视频（填序号，0 为全部下载）：")
        result = re.findall("^\d*$", episodes_selection)

        if len(result) == 0 or int(result[0]) not in range(0, episodes_count + 1):
            print("\033[31m输入无效，请重试\033[0m")

        else:
            break
    
    print()
    
    return int(episodes_selection)

def show_qualiy_selection():
    quality_list = ["{}.{}".format(index + 1, value) for index, value in enumerate(BangumiInfo.quality_desc)]
    print("\n清晰度列表：\n   ", end = '', flush = True)
    print("\n   ".join(quality_list))

    while True:
        quality_selection = input("\n请选择清晰度（填序号）：")
        result = re.findall("^\d*$", quality_selection)

        if len(result) == 0:
            print("\033[31m输入无效，请重试\033[0m")
            continue
        else:
            break

@click.command()
@click.option("--p", "--parse", help = "Parse video url.")
@click.option("--i", "--info", help = "Show video info.")
@click.option("--v", "--version", callback = show_version_info, expose_value = False, is_eager = True, is_flag = True, help = "Show version info.")
def main(p, i):
    if not os.path.exists(os.path.join(os.getcwd(), "ffmpeg.exe")):
        print("\033[33mNotice：尚未安装 ffmpeg，请访问项目主页下载\033[0m")
        print()
    if p:
        Thread(target = parse, args = (p, )).start()
    elif i:
        Thread(target = parse, args = (i, True, )).start()
    else:
        print("Bili23 Downloader CLI 1.00\n")

        print("用法：")
        print("bili23 [OPTIONS]")
        print('\n键入 "bili23 --help" 获取帮助。')

if __name__ == "__main__":
    video_parser = VideoParser(None, None)
    bangumi_parser = BangumiParser(None)

    colorama.init(autoreset = True)
    
    main()