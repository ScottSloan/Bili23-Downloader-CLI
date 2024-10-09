import re
import os
import json
import math
import requests

from .config import Config

quality_map = {
    "超高清 8K": 127,
    "杜比视界": 126,
    "真彩 HDR": 125,
    "超清 4K": 120,
    "高清 1080P60": 116,
    "高清 1080P+": 112,
    "高清 1080P": 80,
    "高清 720P": 64,
    "清晰 480P": 32,
    "流畅 360P": 16,
}
codec_map = {"AVC/H.264": "avc", "HEVC/H.265": "hevc", "AV1": "av1"}


def process_shortlink(url: str):
    if not url.startswith("https"):
        url = "https://" + url

    return requests.get(url, headers=get_header()).url


def get_legal_name(name: str):
    return re.sub('[/\:*?"<>|]', "", name)


def get_header(referer_url=None, cookie=None, chunk_list=None) -> dict:
    """
    构建请求头
    """
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "Cookie": "CURRENT_FNVAL=4048"
    }

    if referer_url:
        header["Referer"] = referer_url

    if chunk_list:
        header["Range"] = "bytes={}-{}".format(chunk_list[0], chunk_list[1])

    if cookie and cookie:
        header["Cookie"] += ";SESSDATA=" + cookie

    return header


def remove_files(path: str, name: list):
    for i in name:
        os.remove(os.path.join(path, i))


def format_size(size: int) -> str:
    """
    格式化大小
    """
    if size > 1048576:
        return "{:.1f} GB".format(size / 1024 / 1024)
    elif size > 1024:
        return "{:.1f} MB".format(size / 1024)
    else:
        return "{:.1f} KB".format(size)


def get_file_from_url(url, name, subtitle=False):
    request = requests.get(url, headers=get_header())
    request.encoding = "utf-8"

    with open(
        os.path.join(Config.dir, get_legal_name(name)), "w", encoding="utf-8"
    ) as f:
        if subtitle:
            f.write(convert_json_to_srt(request.text))
        else:
            f.write(request.text)


def convert_json_to_srt(data):
    json_data = json.loads(data)

    file = ""

    for index, value in enumerate(json_data["body"]):
        file += "{}\n".format(index)
        start = value["from"]
        end = value["to"]
        file += (
            format_subtitle_timetag(start, False)
            + " --> "
            + format_subtitle_timetag(end, True)
            + "\n"
        )
        file += value["content"] + "\n\n"

    return file


def find_str(pattern: str, string: str):
    if len(re.findall(pattern, string)) != 0:
        return True
    else:
        return False


def format_bangumi_title(episode):
    from .bangumi import BangumiInfo

    if BangumiInfo.type == "电影":
        return "{} {}".format(BangumiInfo.title, episode["title"])
    else:
        return episode["share_copy"]


def format_data(data: int) -> str:
    if data >= 100000000:
        return "{:.1f}亿".format(data / 100000000)
    elif data >= 10000:
        return "{:.1f}万".format(data / 10000)
    else:
        return str(data)


def format_duration(duration: int):
    if duration > 10000:
        duration = duration / 1000

    hours = int(duration // 3600)
    mins = int((duration - hours * 3600) // 60)
    secs = int(duration - hours * 3600 - mins * 60)

    return (
        str(hours).zfill(2) + ":" + str(mins).zfill(2) + ":" + str(secs).zfill(2)
        if hours != 0
        else str(mins).zfill(2) + ":" + str(secs).zfill(2)
    )


def format_subtitle_timetag(timetag, end):
    hours = math.floor(timetag) // 3600
    mins = (math.floor(timetag) - hours * 3600) // 60
    secs = math.floor(timetag) - hours * 3600 - mins * 60

    if not end:
        msecs = int(math.modf(timetag)[0] * 100)
    else:
        msecs = abs(int(math.modf(timetag)[0] * 100 - 1))

    return (
        str(hours).zfill(2)
        + ":"
        + str(mins).zfill(2)
        + ":"
        + str(secs).zfill(2)
        + ","
        + str(msecs).zfill(2)
    )

def get_proxy():
    if Config.Proxy.proxy:
        return {
            "http": f"{Config.Proxy.ip}:{Config.Proxy.port}",
            "https": f"{Config.Proxy.ip}:{Config.Proxy.port}"
        }
    else:
        return {}