import re
import sys

from ..utils.video import VideoInfo
from ..utils.bangumi import BangumiInfo
from ..utils.tools import *
from ..utils.config import Config

def show_error_info(code):
    if code == 400:
        msg = "请求失败，请检查地址是否有误"

    elif code == 401:
        msg = "无法获取视频下载地址"

    print("\033[33m\nError：{}\n\033[0m".format(msg))

def show_version_info(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    print("{}\n".format(Config.app_name))

    print("下载 Bilibili 视频/番剧/电影/纪录片 等资源\n")

    print("当前版本：{}".format(Config.app_version))
    print("发布日期：{}".format(Config.app_date))
    print("项目主页：{}".format(Config.app_website))
    print("开发者：Scott Sloan\n")

    print("本程序遵循 MIT 开源协议。\n")

    ctx.exit()

def show_video_info():
    if Config.download_all:
        return

    print("视频信息：\n", flush = True)

    print("名称：" + VideoInfo.title)
    print("\n简介：" + VideoInfo.desc)

    print("\n播放：" + VideoInfo.view)
    print("点赞：" + VideoInfo.like)
    print("投币：" + VideoInfo.coin)
    print("弹幕：" + VideoInfo.danmaku)
    print("收藏：" + VideoInfo.favorite)
    print("评论：{}\n".format(VideoInfo.reply))

def show_bangumi_info():
    if Config.download_all:
        return

    print("视频信息：\n", flush = True)

    print("类型：" + BangumiInfo.type)
    print("名称：" + BangumiInfo.title)
    print("状态：" + BangumiInfo.newep)
    print("\n简介：" + BangumiInfo.desc)

    print("\n播放：" + BangumiInfo.view)
    print("投币：" + BangumiInfo.coin)
    print("弹幕：" + BangumiInfo.danmaku)
    print("收藏：" + BangumiInfo.favorite)
    print("评分：{}\n".format(BangumiInfo.score))

def get_episodes_selection(episodes_list):
    episodes_count = len(episodes_list)

    print("\n剧集列表 (共 {} 个视频)\n   ".format(episodes_count), end = '', flush = True)
    print("\n   ".join(episodes_list))

    while True:
        pages_selection = input("\n请选择要下载的视频（填序号，0 为全部下载）：")
        result = re.findall("^\d*$", pages_selection)

        if len(result) == 0 or int(result[0]) not in range(0, episodes_count + 1):
            print("\033[31m输入无效，请重试\033[0m")

        else:
            break
    
    print()

    return int(pages_selection)

def show_episodes_selection(type):
    if type == "video":
        if VideoInfo.collection:
            episodes_list = ["{}.{}".format(index + 1, value["title"]) for index, value in enumerate(VideoInfo.episodes)]
        else:
            episodes_list = ["{}.{}".format(i["page"], i["part"] if VideoInfo.multiple else VideoInfo.title) for i in VideoInfo.pages]
    else:
        episodes_list = ["{}.{}".format(index + 1, format_bangumi_title(value)) for index, value in enumerate(BangumiInfo.episodes)]
    
    return 0 if Config.download_all else get_episodes_selection(episodes_list)

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

def check_ffmpeg_available(exit = False):
    if not Config.ffmpeg_available:
        if Config.platform.startswith("Windows"):
            detail = "请访问项目主页查看安装方法"
        else:
            detail = '请执行 "sudo apt install ffmpeg" 命令安装'

        print("\033[33m\nNotice: 尚未安装 ffmpeg，{}\n项目地址：{}\n\033[0m".format(detail, Config.app_website))

        if exit: 
            remove_files(Config.download_path, ["video.mp4", "audio.mp3"])

            sys.exit()

def check_arguments():
    check_quality()

    check_thread()

    check_codec()

    if not os.path.exists(Config.download_path):
        os.makedirs(Config.download_path)

def check_quality():
    if Config.default_quality not in list(quality_wrap.values()):
        print("\033[33mWaning: 清晰度参数无效\n\033[0m")
        
        print("可用的清晰度：")
        print("|------------------------|")
        print("| 描述         | 清晰度  |")
        print("| -------------|---------|")
        print("| 超高清 8K    | 127     |")
        print("| 杜比视界     | 126     |")
        print("| 真彩 HDR     | 125     |")
        print("| 超清 4K      | 120     |")
        print("| 高清 1080P60 | 116     |")
        print("| 高清 1080P+  | 112     |")
        print("| 高清 1080P   | 80      |")
        print("| 高清 720P    | 64      |")
        print("| 清晰 480P    | 32      |")
        print("| 流畅 360P    | 16      |")
        print("|------------------------|")

        sys.exit()

def check_thread():
    if Config.max_thread < 1 or Config.max_thread > 16:
        print("\033[33mWaning: 线程参数无效\n\033[0m")

        print("线程数应在 1 - 16 之间")
        sys.exit()

def check_codec():
    if Config.codec not in list(codec_wrap.keys()):
        print("\033[33mWaning: 视频编码参数无效\n\033[0m")

        print("可用的视频编码：")
        print("|----------------------|")
        print("| 类型       | 编码    |")
        print("|------------|---------|")
        print("| AVC/H.264  | AVC     |")
        print("| HEVC/H.265 | HEVC    |")
        print("| AV1        | AV1     |")
        print("|----------------------|")

        sys.exit()