import json
import requests
import subprocess

from ..utils.video import VideoInfo
from ..utils.bangumi import BangumiInfo
from ..utils.audio import AudioInfo
from ..utils.tools import *
from ..utils.download import Downloader

class Info:
    quality = 0

class DownloadUtils:
    def __init__(self, type, episodes_selection, onError):
        self.type, self.episodes_selection, self.onError = type, episodes_selection, onError

        self.download_list = []

    @property
    def video_durl_api(self):
        return "https://api.bilibili.com/x/player/playurl?bvid={}&cid={}&qn=0&fnver=0&fnval=4048&fourk=1".format(self.info["bvid"], self.info["cid"])

    @property
    def bangumi_durl_api(self):
        return  "https://api.bilibili.com/pgc/player/web/playurl?bvid={}&cid={}&qn=0&fnver=0&fnval=4048&fourk=1".format(self.info["bvid"], self.info["cid"])

    @property
    def audio_durl_api(self):
        return "https://www.bilibili.com/audio/music-service-c/web/url?sid={}".format(self.info["sid"])

    @property
    def get_full_url(self):
        return "https://www.bilibili.com/video/" + self.info["bvid"]

    def get_video_durl_via_api(self):
        type = self.info["type"]

        try:
            if type == "video":
                request = requests.get(self.video_durl_api, headers = get_header(self.info["url"], Config.sessdata))
            elif type == "bangumi":
                request = requests.get(self.bangumi_durl_api, headers = get_header(self.info["url"], Config.sessdata))
        
            request_json = json.loads(request.text)
            json_dash = request_json["result"]["dash"]

        except:
            self.onError(401, self.info["badge"])


        return json_dash

    def get_video_durl_via_html(self):
        re_pattern = r"window.__playinfo__=(.*?)</script>"
        
        request = requests.get(self.get_full_url, headers = get_header(self.info["url"], Config.sessdata))

        json_raw = re.findall(re_pattern, request.text, re.S)[0]

        return json.loads(json_raw)["data"]["dash"]

    def get_video_durl(self, quality_id):
        if Config.mode == "api":
            json_dash = self.get_video_durl_via_api()
        elif Config.mode == "html":
            json_dash = self.get_video_durl_via_html()

        Info.quality = json_dash["video"][0]["id"] if json_dash["video"][0]["id"] < quality_id else quality_id

        temp_video_durl = [i["baseUrl"] for i in json_dash["video"] if i["id"] == Info.quality]
        self.video_durl = temp_video_durl[codec_wrap[Config.codec]] if len(temp_video_durl) > 1 else temp_video_durl[0]
        
        temp_audio_durl = sorted(json_dash["audio"], key = lambda x: x["id"], reverse = True)
        self.audio_durl = [i for i in temp_audio_durl if (i["id"] - 30200) == Info.quality or (i["id"] - 30200) < Info.quality][0]["baseUrl"]

        return self.get_video_durl_list()

    def get_audio_durl(self):
        audio_request = requests.get(self.audio_durl_api, headers = get_header(self.info["url"]))
        audio_json = json.loads(audio_request.text)

        self.audio_durl = audio_json["data"]["cdns"][0]
        
        return self.get_audio_durl_list()

    def get_video_durl_list(self):
        video_info = {
            "url": self.video_durl,
            "type": "视频",
            "referer_url": self.info["url"],
            "file_name": "video.mp4"
        }

        audio_info = {
            "url": self.audio_durl,
            "type": "音频",
            "referer_url": self.info["url"],
            "file_name": "audio.mp3"
        }

        self.get_danmaku()
        self.get_subtitle()

        return [video_info, audio_info]
    
    def get_audio_durl_list(self):
        audio_info = {
            "url": self.audio_durl,
            "type": "音频",
            "referer_url": self.info["url"],
            "file_name": "{}.mp3".format(get_legal_name(self.info["title"]))
        }

        self.get_lyric()

        return [audio_info]

    def get_download_info(self, url, title, type, bvid = None, cid = None, sid = None, lyric = None, badge = None):
        return {
            "url": url,
            "title": title,
            "bvid": bvid,
            "cid": cid,
            "sid": sid,
            "lyric": lyric,
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
                info = self.get_download_info(VideoInfo.url, i["part"], "video", bvid = VideoInfo.bvid, cid = i["cid"])

                self.download_list.append(info)
            
        elif VideoInfo.collection:
            for i in VideoInfo.down_pages:
                info = self.get_download_info(VideoInfo.url, i["title"], "video", bvid = i["bvid"], cid = i["cid"])

                self.download_list.append(info)

        else:
            info = self.get_download_info(VideoInfo.url, VideoInfo.title, "video", bvid = VideoInfo.bvid, cid = VideoInfo.cid)

            self.download_list.append(info)

    def get_bangumi_download_list(self):
        if self.episodes_selection != 0:
            BangumiInfo.down_episodes = [BangumiInfo.episodes[self.episodes_selection - 1]]
        else:
            BangumiInfo.down_episodes = BangumiInfo.episodes

        for i in BangumiInfo.down_episodes:
            info = self.get_download_info(BangumiInfo.url, format_bangumi_title(i), "bangumi", bvid = i["bvid"], cid = i["cid"], badge = i["badge"])

            self.download_list.append(info)

    def get_audio_download_list(self):
        if self.episodes_selection != 0:
            AudioInfo.down_list = [AudioInfo.playlist[self.episodes_selection - 1]]
        else:
            AudioInfo.down_list = AudioInfo.playlist

        if AudioInfo.isplaylist:
            for i in AudioInfo.down_list:
                info = self.get_download_info(AudioInfo.url, i["title"], "audio", sid = i["id"], lyric = i["lyric"])

                self.download_list.append(info)
        else:
            info = self.get_download_info(AudioInfo.url, AudioInfo.title, "audio", sid = AudioInfo.sid, lyric = AudioInfo.lyric)

            self.download_list.append(info)

    def start_download(self):
        quality_temp = dict(map(reversed, quality_wrap.items()))
        codec_temp = {"AVC": "AVC/H.264", "HEVC": "HEVC/H.265", "AV1": "AV1"}

        if self.type != "audio":
            print("当前清晰度：{}   当前编码：{}\n".format(quality_temp[Config.quality], codec_temp[Config.codec]))

        print("准备开始下载...\n")

        download_count = len(self.download_list)

        for index, episode in enumerate(self.download_list):
            self.info = episode
            title = episode["title"]
            
            downloader = Downloader(self.onDownload)
            
            if self.type != "audio":
                download_list = self.get_video_durl(episode["quality_id"])
            else:
                download_list = self.get_audio_durl()

            print("\r[{}/{}] 正在下载：{}".format(index + 1, download_count, title), flush = True)

            downloader.start_download(download_list)
            
            self.clear_line()

            self.merge_video(title)
            
        print("\n下载完成\n")

    def merge_video(self, title):
        if self.type == "audio":
            return

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

    def get_danmaku(self):
        if not Config.danmaku:
            return
        
        durl = "https://api.bilibili.com/x/v1/dm/list.so?oid={}".format(self.info["cid"])

        get_file_from_url(durl, "{}.xml".format(self.info["title"]))

    def get_subtitle(self):
        if not Config.subtitle:
            return

        subtitle_url = "https://api.bilibili.com/x/player.so?id=cid:{}&bvid={}".format(self.info["cid"], self.info["bvid"])
        req = requests.get(subtitle_url, headers = get_header())

        subtitle_raw = re.findall(r'<subtitle>(.*?)</subtitle>', req.text)[0]
        subtitle_json = json.loads(subtitle_raw)["subtitles"]

        subtitle_num = len(subtitle_json)

        if subtitle_num == 0:
            return

        elif subtitle_num == 1:
            durl = "https:{}".format(subtitle_json[0]["subtitle_url"])
        
            get_file_from_url(durl, "{}.srt".format(self.info["title"]), True)

        else:
            for i in range(subtitle_num):
                lan_name = subtitle_json[i]["lan_doc"]
                durl = "https:{}".format(subtitle_json[i]["subtitle_url"])
            
                get_file_from_url(durl, "({}) {}.srt".format(lan_name, self.info["title"]), True)

    def get_lyric(self):         
        if not Config.lyric or self.info["lyric"] == "":
            return
    
        get_file_from_url(self.info["lyric"], "{}.lrc".format(self.info["title"]))
