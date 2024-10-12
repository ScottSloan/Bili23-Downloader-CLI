"""
TODO: 重新编写的config.py, 删掉原来的utils.config.py 后记得删除这个注释
"""

from ipaddress import IPv4Address
from pathlib import Path
from typing import Annotated, Optional, Tuple, Type

from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator, AfterValidator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from bili23_downloader_cli.util import get_user_config_path
from bili23_downloader_cli.utils.constant import VideoCodec, VideoQuality
import rtoml
from typer import prompt,confirm


APP_NAME = "bili23"


def get_config_path() -> Path:
    """
    获取 ~/.config/<APP_NAME> 目录
    """
    return get_user_config_path() / APP_NAME


def get_config_file() -> Path:
    """获取配置文件的位置"""
    return get_config_path() / "config.toml"


class DownloadSettings(BaseModel):
    path: Optional[str] = None
    """下载保存目录"""
    max_thread: int = 4
    """最大下载线程"""
    quality: Annotated[
        VideoQuality,
        AfterValidator(lambda v: VideoQuality(v)),
    ] = VideoQuality.HD_1080P
    codec: Annotated[
        VideoCodec,
        AfterValidator(lambda v: VideoCodec(v)),
    ] = VideoCodec.HEVC



class UserSettings(BaseModel):
    sessdata: Optional[str] = None


class ProxySettings(BaseModel):
    ip: Annotated[Optional[IPv4Address], BeforeValidator(lambda v: None if v == "" else v)] = None
    port: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class Config(BaseSettings):
    download: Optional[DownloadSettings] = DownloadSettings()
    user: Optional[UserSettings] = UserSettings()
    proxy: Optional[ProxySettings] = ProxySettings()

    model_config = SettingsConfigDict(
        toml_file=get_config_file()
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


def has_config() -> bool:
    """
    检查是否有配置文件
    """
    config_file = get_config_file()

    # 必须文件存在且不能是空文件
    return config_file.exists() and rtoml.load(config_file)


def save_config(config: Config):
    """保存配置"""
    config_dict = config.model_dump()
    # TODO: 可以写一个嵌套遍历，将Enum 转化成对应的value
    config_dict["download"]["quality"] = config.download.quality.value
    config_dict["download"]["codec"] = config.download.codec.value
    rtoml.dump(config_dict, get_config_file(),pretty=True, none_value="")


def load_config() -> Config:
    """从配置文件中加载配置"""
    return Config(**rtoml.load(get_config_file(), none_value=""))


def init_config(config: Config):
    """
    初始化配置文件
    """
    # TODO: 将 Config 的默认配置值 写入到 .config/<Config.app.name>/config.toml 中
    # TODO: 使用交互式进行配置
    # 下载地址
    # 最大下载线程
    # 视频质量
    # 视频编解格式
    
    # 是否扫码进行登录 # TODO: 这里需要说明登录之后有哪些好处，比如支持最高品质啥的
    
    # 是否需要添加代理
    if confirm("是否需要添加代理"):
        config.proxy.ip = prompt("代理地址ipv4格式")
        config.proxy.port = prompt("代理端口")
        config.proxy.username = prompt("代理账号")
        config.proxy.password = prompt("代理密码")

def check_config():
    """检查配置文是否存在，是否初始化什么的
    然后如果存在异常的也需要print出去，或者让用户进行修改，记得提供可能存在的异常
    """
    if not has_config():
        print("Initializing app configs ...")
        # 如果app的配置目录不存在则创建目录
        config_path = get_config_path()
        if not config_path.exists():
            config_path.mkdir()

        get_config_file().touch()

        config = Config()
        init_config(config)
        save_config(config)

    else:
        print("loading app configs ...")
        try:
            load_config()
        except Exception as e:
            print(f"config file has error: {e}")

