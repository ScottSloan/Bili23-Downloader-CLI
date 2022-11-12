import platform
import subprocess

class Config:
    download_path = ""

    max_thread = 4
    codec = "HEVC"
    default_quality = 80
    download_all = False
    
    user_sessdata = ""

    app_name = "Bili23 Downloader CLI"
    app_version = "1.01"
    app_version_code = 101
    app_date = "2022-11-12"
    app_website = "https://github.com/ScottSloan/Bili23-Downloader-CLI"

    platform = platform.platform()

    ffmpeg_available = True if subprocess.call(args = "ffmpeg -version", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE) == 0 else False