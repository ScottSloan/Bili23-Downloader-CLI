import json
import requests
import subprocess

from ..utils.video import VideoInfo
from ..utils.bangumi import BangumiInfo

from ..utils.tools import *
from ..utils.download import Downloader

class Info:
    quality = 0

class DownloadUtils:
    def __init__(self, type, episodes_selection, onError):
        self.type, self.episodes_selection, self.onError = type, episodes_selection, onError

        self.download_list = []

    def get_video_durl(self, referer_url, bvid, cid, quality_id, badge = None):
        try:
            if self.type == "video":
                url = "https://api.bilibili.com/x/player/playurl?bvid={}&cid={}&qn=0&fnver=0&fnval=4048&fourk=1".format(bvid, cid)

                request = requests.get(url, headers = get_header(referer_url, Config.sessdata))
                request_json = json.loads(request.text)
                json_dash = request_json["data"]["dash"]

            elif self.type == "bangumi":
                url = "https://api.bilibili.com/pgc/player/web/playurl?bvid={}&cid={}&qn=0&fnver=0&fnval=4048&fourk=1".format(bvid, cid)

                request = requests.get(url, headers = get_header(referer_url, Config.sessdata))
                request_json = json.loads(request.text)
                json_dash = request_json["result"]["dash"]
        except:
            self.onError(401, badge)

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
    
    def get_download_info(self, url, title, bvid, cid, badge, type):
        return {
            "url": url,
            "title": title,
            "bvid": bvid,
            "cid": cid,
            "quality_id": Config.quality,
            "badge": badge,
            "tpye": type
        }

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
            for i in VideoInfo.down_pages:
                info = self.get_download_info(VideoInfo.url, i["part"], VideoInfo.bvid, i["cid"], "video")

                self.download_list.append(info)
            
        elif VideoInfo.collection:
            for i in VideoInfo.down_pages:
                info = self.get_download_info(VideoInfo.url, i["title"], i["bvid"], i["cid"], "video")

                self.download_list.append(info)

        else:
            info = self.get_download_info(VideoInfo.url, VideoInfo.title, VideoInfo.bvid, VideoInfo.cid, "video")

            self.download_list.append(info)

    def get_bangumi_download_list(self):
        if self.episodes_selection != 0:
            BangumiInfo.down_episodes = [BangumiInfo.episodes[self.episodes_selection - 1]]
        else:
            BangumiInfo.down_episodes = BangumiInfo.episodes

        for i in BangumiInfo.down_episodes:
            info = self.get_download_info(BangumiInfo.url, format_bangumi_title(i), i["bvid"], i["cid"], i["badge"], "bangumi")

            self.download_list.append(info)

    def download_video(self):
        quality_temp = dict(map(reversed, quality_wrap.items()))
        codec_temp = {"AVC": "AVC/H.264", "HEVC": "HEVC/H.265", "AV1": "AV1"}

        print("当前清晰度：{}   当前编码：{}\n".format(quality_temp[Config.quality], codec_temp[Config.codec]))
        print("准备开始下载...\n")

        download_count = len(self.download_list)

        for index, episode in enumerate(self.download_list):
            title = episode["title"]
            
            downloader = Downloader(self.onDownload)

            download_list = self.get_video_durl(episode["url"], episode["bvid"], episode["cid"], episode["quality_id"], episode["badge"])

            print("\r[{}/{}] 正在下载：{}".format(index + 1, download_count, title), flush = True)

            downloader.start_download(download_list)
            
            self.clear_line()

            self.merge_video(title)
            
        print("\n视频下载完成\n")

    def merge_video(self, title):
        from .common import check_ffmpeg_available

        print("\r正在合成视频...", end = "")

        check_ffmpeg_available(True)

        legal_title = get_legal_name(title)

        cmd = f'''cd {Config.dir} && ffmpeg -v quiet -i audio.mp3 -i video.mp4 -acodec copy -vcodec copy "{legal_title}.mp4"'''
            
        merge_process = subprocess.Popen(cmd, shell = True)
        merge_process.wait()

        remove_files(Config.dir, ["video.mp4", "audio.mp3"])
    
        self.clear_line()

    def clear_line(self):
        width = os.get_terminal_size().columns

        print("\r{}".format(" " * width), end = "", flush = True)
        print("\r", end = "", flush = True)

    def onDownload(self, progress, speed, size):
        print("\r{}% | {}{}  |  {}   {}".format(progress, "█" * (progress // 5), " " * (20 - progress // 5), speed, size), end = "", flush = True)
