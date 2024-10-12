"""
TODO: 重新编写的config.py, 删掉原来的utils.config.py 后记得删除这个注释
"""

from ipaddress import IPv4Address
from pathlib import Path
from pprint import pp
from typing import Optional, Tuple, Type

from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from bili23_downloader_cli.util import get_user_config_path
from bili23_downloader_cli.utils.constant import VideoCodec, VideoQuality
import rtoml


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
    quality: VideoQuality = Field(default=VideoQuality.HD_1080P, validate_default=True)
    codec: VideoCodec = Field(default=VideoCodec.HEVC, validate_default=True)

    # TODO: quality 配置文件存的是数字，但是在这里需要转化成 VideoQuality的key
    # TODO: codec 配置文件存的是value，但是在这里需要转化成 VideoQuality的key
    model_config = ConfigDict(use_enum_values=True)


class UserSettings(BaseModel):
    sessdata: Optional[str] = None


class ProxySettings(BaseModel):
    ip: Optional[IPv4Address] = None
    port: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class Config(BaseSettings):
    download: Optional[DownloadSettings] = DownloadSettings()
    user: Optional[UserSettings] = UserSettings()
    # proxy: ProxySettings  # = ProxySettings()

    # model_config = SettingsConfigDict(toml_file=get_config_file())

    # @classmethod
    # def settings_customise_sources(
    #     cls,
    #     settings_cls: Type[BaseSettings],
    #     init_settings: PydanticBaseSettingsSource,
    #     env_settings: PydanticBaseSettingsSource,
    #     dotenv_settings: PydanticBaseSettingsSource,
    #     file_secret_settings: PydanticBaseSettingsSource,
    # ) -> Tuple[PydanticBaseSettingsSource, ...]:
    #     return (TomlConfigSettingsSource(settings_cls),)


def has_config() -> bool:
    """
    检查是否有配置文件
    """
    config_file = get_config_file()
    return config_file.exists() and (config_file.read_text().__len__() > 0)


def save_config(config: Config):
    """保存配置"""
    rtoml.dump(config.model_dump(), get_config_file())


def load_config() -> Config:
    """从配置文件中加载配置"""
    return Config(**rtoml.load(get_config_file()))


def init_config():
    """
    初始化配置文件
    """
    # TODO: 将 Config 的默认配置值 写入到 .config/<Config.app.name>/config.toml 中
    # TODO: 使用交互式进行配置


def get_config() -> Config:
    """获取配置"""
    return Config()


def check_config():
    """检查配置文是否存在，是否初始化什么的
    然后如果存在异常的也需要print出去，或者让用户进行修改，记得提供可能存在的异常
    """
    if not has_config():
        # 如果app的配置目录不存在则创建目录
        config_path = get_config_path()
        if not config_path.exists():
            config_path.mkdir()

        get_config_file().touch()

        config = Config()
        pp(config)
        # save_config(config)

        # print(
        #     "发现你是第一次用，我们来配置一下配置文件吧!"
        # )  # TODO: 这个可以改成 rich的写法

        # init_config()
