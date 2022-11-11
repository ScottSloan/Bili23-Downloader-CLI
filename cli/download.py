import json
import requests
import subprocess

from utils.video import VideoInfo
from utils.bangumi import BangumiInfo

from utils.tools import *
from utils.download import Downloader

class Info:
    quality = 0

class DownloadUtils:
    def __init__(self, type, episodes_selection):
        self.type, self.episodes_selection = type, episodes_selection

        self.download_list = []

    def get_video_durl(self, referer_url, bvid, cid, quality_id):
        if self.type == "video":
            url = "https://api.bilibili.com/x/player/playurl?bvid={}&cid={}&qn=0&fnver=0&fnval=4048&fourk=1".format(bvid, cid)

            request = requests.get(url, headers = get_header(referer_url, Config.user_sessdata), proxies = get_proxy())
            request_json = json.loads(request.text)
            json_dash = request_json["data"]["dash"]

        elif self.type == "bangumi":
            url = "https://api.bilibili.com/pgc/player/web/playurl?bvid={}&cid={}&qn=0&fnver=0&fnval=4048&fourk=1".format(bvid, cid)

            request = requests.get(url, headers = get_header(referer_url, Config.user_sessdata), proxies = get_proxy())
            request_json = json.loads(request.text)
            json_dash = request_json["result"]["dash"]

        Info.quality = json_dash["video"][0]["id"] if json_dash["video"][0]["id"] < quality_id else quality_id

        temp_video_durl = [i["baseUrl"] for i in json_dash["video"] if i["id"] == Info.quality]
        self.video_durl = temp_video_durl[codec_wrap[Config.codec]] if len(temp_video_durl) > 1 else temp_video_durl[0]
        
        temp_audio_durl = sorted(json_dash["audio"], key = lambda x: x["id"], reverse = True)
        self.audio_durl = [i for i in temp_audio_durl if (i["id"] - 30200) == Info.quality or (i["id"] - 30200) < Info.quality][0]["baseUrl"]

        return self.get_durl_list(referer_url)

    def get_durl_list(self, referer_url):
        video_info = {
            "url": self.video_durl,
            "type": "视频",
            "referer_url": referer_url,
            "file_name": "video.mp4"
        }

        audio_info = {
            "url": self.audio_durl,
            "type": "音频",
            "referer_url": referer_url,
            "file_name": "audio.mp3"
        }

        return [video_info, audio_info]
    
    def get_video_download_list(self):
        if self.episodes_selection != 0:
            if VideoInfo.multiple:
                VideoInfo.down_pages =  [VideoInfo.pages[self.episodes_selection - 1]]
            elif VideoInfo.collection:
                VideoInfo.down_pages = [VideoInfo.episodes[self.episodes_selection - 1]]
        
        else:
            if VideoInfo.multiple:
                VideoInfo.down_pages = VideoInfo.pages
            elif VideoInfo.collection:
                VideoInfo.down_pages = VideoInfo.episodes

        if VideoInfo.multiple:
            # 分 p 视频
            for i in VideoInfo.down_pages:
                info = {
                    "url": VideoInfo.url,
                    "title": i["part"],
                    "bvid": VideoInfo.bvid,
                    "cid": i["cid"],
                    "quality_id": Config.default_quality,
                    "type": "video"
                }

                self.download_list.append(info)
            
        elif VideoInfo.collection:
        # 合集视频
            for i in VideoInfo.down_pages:
                info = {
                    "url": VideoInfo.url,
                    "title": i["title"],
                    "bvid": i["bvid"],
                    "cid": i["cid"],
                    "quality_id": Config.default_quality,
                    "type": "video"
                }

                self.download_list.append(info)

        else:
            # 单个视频
            info = {
                "url": VideoInfo.url,
                "title": VideoInfo.title,
                "bvid": VideoInfo.bvid,
                "cid": VideoInfo.cid,
                "quality_id": Config.default_quality,
                "type": "video"
            }

            self.download_list.append(info)

    def get_bangumi_download_list(self):
        if self.episodes_selection != 0:
            BangumiInfo.down_episodes = [BangumiInfo.episodes[self.episodes_selection - 1]]
        else:
            BangumiInfo.down_episodes = BangumiInfo.episodes

        for i in BangumiInfo.down_episodes:
            info = {
                "url": BangumiInfo.url,
                "title": format_bangumi_title(i),
                "bvid": i["bvid"],
                "cid": i["cid"],
                "quality_id": Config.default_quality,
                "type": "bangumi"
            }

            self.download_list.append(info)

    def download_video(self):
        for episode in self.download_list:
            title = episode["title"]
            
            downloader = Downloader(self.onDownload)

            download_list = self.get_video_durl(episode["url"], episode["bvid"], episode["cid"], episode["quality_id"])

            print("\r正在下载：{}".format(title), flush = True)

            downloader.start_download(download_list)
            
            self.clear_line()

            self.merge_video(title)
            
        print("\n视频下载完成\n")

    def merge_video(self, title):
        print("\r正在合成视频...", end = "")

        if not os.path.exists(os.path.join(os.getcwd(), "ffmpeg.exe")):
            print("\n")
            print("\033[33mError：尚未安装 ffmpeg，无法合成视频，下载已终止\033[0m")
            print()
            
            exit()

        legal_title = get_legal_name(title)

        cmd = f'''cd "{Config.download_path}" && "{Config.ffmpeg_path}" -v quiet -i audio.mp3 -i video.mp4 -acodec copy -vcodec copy "{legal_title}.mp4"'''
            
        merge_process = subprocess.Popen(cmd, shell = True)
        merge_process.wait()

        remove_files(Config.download_path, [f"video.mp4", f"audio.mp3"])
    
        self.clear_line()

    def clear_line(self):
        width = os.get_terminal_size().columns

        print("\r{}".format(" " * (width - 2)), end = "", flush = True)
        print("\r", end = "", flush = True)

    def onDownload(self, progress, speed):
        print("\r{}% | {}{}  |  {}".format(progress, "█" * (progress // 4), " " * (25 - progress // 4), speed), end = "", flush = True)