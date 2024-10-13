"""
定义常量的文件
"""

from enum import Enum
from sys import version_info

# # 自定义字符串枚举
if version_info < (3,11):
    class StrEnum(str, Enum):
        """
        Enum where members are also (and must be) strings
        """

        def __new__(cls, *values):
            "values must already be of type `str`"
            if len(values) > 3:
                raise TypeError('too many arguments for str(): %r' % (values, ))
            if len(values) == 1:
                # it must be a string
                if not isinstance(values[0], str):
                    raise TypeError('%r is not a string' % (values[0], ))
            if len(values) >= 2:
                # check that encoding argument is a string
                if not isinstance(values[1], str):
                    raise TypeError('encoding must be a string, not %r' % (values[1], ))
            if len(values) == 3:
                # check that errors argument is a string
                if not isinstance(values[2], str):
                    raise TypeError('errors must be a string, not %r' % (values[2]))
            value = str(*values)
            member = str.__new__(cls, value)
            member._value_ = value
            return member

        def _generate_next_value_(name, start, count, last_values):
            """
            Return the lower-cased version of the member name.
            """
            return name.lower()
else:
    from enum import StrEnum

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


class VideoQuality(StrEnum):
    """视频品质"""

    UHD_8K = "超高清 8K"  # 127
    """超高清 8K"""
    DOLBY = "杜比视界"  # 126
    """杜比视界"""
    HDR = "真彩 HDR"  # 125
    """真彩 HDR"""
    UHD_4K = "超清 4K"  # 120
    """超清 4K"""
    HD_1080P60 = "高清 1080P60"  # 116
    """高清 1080P60"""
    HD_1080Plus = "高清 1080P+"  # 112
    """高清 1080P+"""
    HD_1080P = "高清 1080P"  # 80
    """高清 1080P"""
    HD_720P = "高清 720P"  # 64
    """高清 720P"""
    CLEAR = "清晰 480P"  # 32
    """清晰 480P"""
    SMOOTH = "流畅 360P"  # 16
    """流畅 360P"""


class VideoCodec(StrEnum):
    """视频编解码"""

    AVC = "AVC/H.264"  # "avc"
    HEVC = "HEVC/H.265"  # "hevc"
    AV1 = "AV1"  # "av1"
