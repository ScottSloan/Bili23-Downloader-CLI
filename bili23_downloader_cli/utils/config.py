import os
import platform
import subprocess
from configparser import RawConfigParser
from typing import Optional


class Config:
    class APP:
        name = "Bili23 Downloader CLI"

        version = "1.20"
        version_code = 1200

        release_date = "2023-10-7"

        homepage = "https://github.com/ScottSloan/Bili23-Downloader-CLI"

        platform = platform.platform()

    class Proxy:
        proxy = auth = False

        ip = None
        port = None
        uname = None
        passwd = None

    class User:
        sessdata = None

    class Download:
        path: Optional[str] = None
        max_thread: Optional[int] = None
        codec: Optional[str] = None
        quality: Optional[int] = None
        """清晰度"""

        ffmpeg_available = False
        ffmpeg_path = None

    class Type:
        VIDEO = 1
        BANGUMI = 2

    class Argument:
        download_all = False
        show_quality_list = False
        quiet = False
        edit = False


class Download:
    pass


class ConfigUtils:
    def __init__(self):
        self.path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "config.conf"
        )

        self.config = RawConfigParser()
        self.config.read(self.path, encoding="utf-8")

        self.load_config()

        self.check_ffmpeg_status()

    def load_config(self):
        # download
        Config.Download.path = self.config.get("download", "path")
        Config.Download.max_thread = self.config.getint("download", "max_thread")
        Config.Download.quality = self.config.getint("download", "quality")
        Config.Download.codec = self.config.get("download", "codec")

        # user
        Config.User.sessdata = self.config.get("user", "sessdata")

        # proxy
        Config.Proxy.ip = self.config.get("proxy", "ip")
        Config.Proxy.port = self.config.get("proxy", "port")

        Config.Proxy.uname = self.config.get("proxy", "uname")
        Config.Proxy.passwd = self.config.get("proxy", "passwd")

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            self.config.write(f)

    def check_ffmpeg_status(self):
        process = subprocess.Popen(
            "ffmpeg -version",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.wait()

        Config.Download.ffmpeg_available = (
            True if "ffmpeg version" in str(process.stdout.read()) else False
        )


conf = ConfigUtils()
conf.load_config()
