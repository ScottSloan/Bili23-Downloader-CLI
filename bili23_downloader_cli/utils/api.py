"""
统一放置需要用到的接口
"""

from typing import Any, Optional
from enum import Enum, auto

BASE_URL = "https://bilibili.com"
BASE_API_URL = "https://api.bilibili.com"
BASE_LIVE_API_URL = "https://api.live.bilibili.com"
BASE_QRLOGIN_URL = "https://passport.bilibili.com"


class APIType(Enum):
    """视频分类"""

    Video = auto()
    Bangumi = auto()
    Audio = auto()
    AudioPlayList = auto()
    Live = auto()
    Cheese = auto()


def bvid_url_api(bvid: str, p: Optional[str] = "") -> str:
    return f"{BASE_URL}/video/{bvid}{'?p=' if p else ''}{p}"


def epid_url_api(epid: str) -> str:
    return f"{BASE_URL}/bangumi/play/ep{epid}"


def bvid_short_link_api(bvid: str) -> str:
    return f"https://b23.tv/{bvid}"


def danmuku_api(cid: str) -> str:
    return f"{BASE_API_URL}/x/v1/dm/list.so?oid={cid}"


def subtitle_api(cid: str, bvid: str) -> str:
    return f"{BASE_API_URL}/x/player.so?id=cid:{cid}&bvid={bvid}"


def aid_url_api(aid: str) -> str:
    return f"{BASE_API_URL}/x/web-interface/archive/stat?aid={aid}"


# def info_api(type:APIType, bvid: Optional[str] = None, argument: Optional[str] = None, value:Optional[str] = None, sid: Optional[str] = None, amid: Optional[str] = None) -> str:


def info_api(type: APIType, **kwargs: Any) -> str:
    match type:
        case APIType.Video:
            # if not bvid:
            #     raise KeyError(f"bvid: {bvid}")
            return f"{BASE_API_URL}/x/web-interface/view?bvid={kwargs.get("bvid")}"
        case APIType.Bangumi:
            # if not argument or not value:
            #     raise KeyError(f"argument: {argument}, value: {value}")
            # return f"{BASE_API_URL}/pgc/view/web/season?{argument}={value}"
            return f"{BASE_API_URL}/pgc/view/web/season?{kwargs.get("argument")}={kwargs.get("value")}"
        case APIType.Audio:
            # if not sid:
            #     raise KeyError(f"sid: {sid}")
            return f"{BASE_URL}/audio/music-service-c/web/song/info?sid={kwargs.get("sid")}"
        case APIType.AudioPlayList:
            return f"{BASE_URL}/audio/music-service-c/web/song/of-menu?sid={kwargs.get("amid")}&pn=1&ps=100"
        case APIType.Live:
            return f"{BASE_LIVE_API_URL}/xlive/web-room/v1/index/getRoomBaseInfo?room_ids={kwargs.get("id")}&req_biz=web_room_componet"
        case APIType.Cheese:
            return f"{BASE_API_URL}/pugv/view/web/season?{kwargs.get("argument")}={kwargs.get("value")}"
        case _:  # type: ignore
            raise NotImplementedError


# TODO: 需要重新修改形参， 应该改成**kwargs的形式, 参数应该有调用它的方法传入


def download_api(
    type: APIType,
    bvid: Optional[str] = None,
    cid: Optional[str] = None,
    sid: Optional[str] = None,
    avid: Optional[str] = None,
    epid: Optional[str] = None,
) -> str:
    match type:
        case APIType.Video:
            return f"{BASE_API_URL}/x/player/playurl?bvid={bvid}&cid={cid}&qn=0&fnver=0&fnval=4048&fourk=1"
        case APIType.Bangumi:
            return f"{BASE_API_URL}/pgc/player/web/playurl?bvid={bvid}&cid={cid}&qn=0&fnver=0&fnval=4048&fourk=1"
        case APIType.Audio:
            return f"{BASE_URL}/audio/music-service-c/web/url?sid={sid}"
        case APIType.Cheese:
            return f"{BASE_API_URL}/pugv/player/web/playurl?avid={avid}&ep_id={epid}&cid={cid}"

        case _:
            raise NotImplementedError


def mid_api(mid: str) -> str:
    return f"{BASE_API_URL}/pgc/review/user?media_id={mid}"


def sid_url_api(sid: str) -> str:
    return f"{BASE_URL}/audio/au{sid}"


def amid_url_api(amid: str) -> str:
    return f"{BASE_URL}/audio/am{amid}"


def playurl_api(room_id: str) -> str:
    return f"{BASE_LIVE_API_URL}/xlive/web-room/v1/playUrl/playUrl?cid={room_id}&platform=h5&otype=json&quality=1"


def qrcode_url_api() -> str:
    return f"{BASE_QRLOGIN_URL}/x/passport-login/web/qrcode/generate"


def qrcode_status_api(qrcode_key: str) -> str:
    return (
        f"{BASE_QRLOGIN_URL}/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}"
    )


def user_info_api() -> str:
    return f"{BASE_API_URL}/x/web-interface/nav"
