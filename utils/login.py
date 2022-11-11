import json
import requests

from .tools import get_header, get_proxy
from .config import Config

class LoginInfo:
    url = oauthKey = ""

class Login:
    def __init__(self):
        self.session = requests.session()

        self.init_qrcode()

    @property
    def qrcode_url(self):
        # 用户获取二维码
        return "https://passport.bilibili.com/qrcode/getLoginUrl"

    @property
    def login_info_url(self):
        # 用于获取用户扫码状态
        return "https://passport.bilibili.com/qrcode/getLoginInfo"

    @property
    def user_info_url(self):
        # 用于获取用户信息
        return "https://api.live.bilibili.com/User/getUserInfo"

    @property
    def user_detail_info_url(self):
        # 用于获取用户详细信息
        return "https://api.bilibili.com/x/space/acc/info?mid=" + Config.user_uid

    def init_qrcode(self):
        # 获取登录二维码
        req = self.session.get(self.qrcode_url, headers = get_header(), proxies = get_proxy())
        login_json = json.loads(req.text)

        LoginInfo.url = login_json["data"]["url"]
        LoginInfo.oauthKey = login_json["data"]["oauthKey"]
    
    def check_scan(self):
        # 检查用户是否扫描二维码
        data = {'oauthKey':LoginInfo.oauthKey, "gourl":"https://passport.bilibili.com/account/security"}

        req = self.session.post(self.login_info_url, data = data, headers = get_header(), proxies = get_proxy())
        req_json = json.loads(req.text)

        return {
            "status": req_json["status"],
            "code": req_json["data"] if not req_json["status"] else 0}
    
    def get_user_info(self) -> dict:
        # 获取用户基本信息
        info_requests = self.session.get(self.user_info_url, proxies = get_proxy())
        info_json = json.loads(info_requests.text)["data"]
                
        Config.user_uid = str(info_json["uid"])

        # 获取用户等级
        detail_request = self.session.get(self.user_detail_info_url, headers = get_header(), proxies = get_proxy())
        detail_json = json.loads(detail_request.text)["data"]
        
        # 返回用户信息
        return {
            "uid": info_json["uid"],
            "uname": info_json["uname"],
            "face": info_json["face"],
            "level": detail_json["level"],
            "sessdata": self.session.cookies["SESSDATA"]
        }