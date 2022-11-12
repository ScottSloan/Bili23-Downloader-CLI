from setuptools import setup, find_packages

setup(
    name = "bili23",
    version = "0.0.7",
    keywords = ["pip", "bilibili", "video-downloader", "cli"],
    description = "下载 Bilibili 视频/番剧/电影/纪录片 等资源",
    long_description = "Bili23 Downloader CLI 命令行版本：下载 Bilibili 视频/番剧/电影/纪录片 等资源",
    license = "MIT License",
    url = "https://github.com/ScottSloan/Bili23-Downloader-CLI",
    author = "Scott Sloan",
    author_email = "scottsloan@petalmail.com",

    packages = find_packages(),
    install_requires = ["click", "requests", "colorama"],
    platforms = "any",

    entry_points = '''
    [console_scripts]
    bili23=bili23.bili23:main
    '''
)
