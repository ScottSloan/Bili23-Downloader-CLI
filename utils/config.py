import os
import platform
from configparser import RawConfigParser

class Config:
    # 资源路径
    _res_path = os.path.join(os.getcwd(), "res")

    res_icon = os.path.join(_res_path, "icon.ico")
    res_pause = os.path.join(_res_path, "pause.png")
    res_continue = os.path.join(_res_path, "continue.png")
    res_delete = os.path.join(_res_path, "delete.png")

    # 下载设置
    download_path = os.path.join(os.getcwd(), "download")
    default_path = os.path.join(os.getcwd(), "download")

    max_thread = 4
    max_download = 3
    codec = "HEVC"
    default_quality = 80
    show_notification = False

    # 代理
    enable_proxy = False
    proxy_ip = ""
    proxy_port = ""

    # 显示设置
    show_sections = False
    save_danmaku = False
    danmaku_format = 0
    save_subtitle = False
    save_lyric = False
    
    # 杂项
    player_path = ""
    check_update = False
    debug = True
    
    # 用户信息
    user_uid = 0
    user_name = ""
    user_face = ""
    user_level = 0
    user_sessdata = ""
    user_expire = ""

    # 程序信息
    app_name = "Bili23 Downloader"
    app_version = "1.30"
    app_version_code = 130
    app_date = "2022-10-4"
    app_website = "https://github.com/ScottSloan/Bili23-Downloader"

    platform = platform.platform()
    ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg.exe") if platform.startswith("Windows") else "ffmpeg"

class LoadConfig:
    def __init__(self):
        conf = RawConfigParser()
        conf.read(os.path.join(os.getcwd(), "config.conf"), encoding = "utf-8")

        # 载入用户信息
        Config.user_uid = conf.get("user", "uid")
        Config.user_name = conf.get("user", "uname")
        Config.user_face = conf.get("user", "face")
        Config.user_level = conf.get("user", "level")
        Config.user_expire = conf.get("user", "expire")
        Config.user_sessdata = conf.get("user", "sessdata")

changelog = """Version 1.30 更新日志\n\n千门万户曈曈日，总把新桃换旧符。时隔 5 个月，Bili23 Downloader 迎来 Version 1.30 更新！
本次更新内容如下：
* 完全重写了程序，去除冗杂代码
* 优化窗口在高 DPI 下的显示效果
* 程序主界面可展示用户信息
* 登录界面二维码自动刷新
* 修复检查更新接口无效的问题
* 修复路径含有空格时无法合成视频的问题
* 支持调试功能
* 支持 Linux 平台
* 移除视频信息查看功能

自 Version 1.30 后，release 将提供编译版程序。
推荐使用编译版，无需安装相关依赖，简单易用。

因为学业的原因，现在更新频率相比之前慢了许多，
但我还会维护这个项目的，感谢大家的支持！:)"""

LoadConfig()