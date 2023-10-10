import os
from setuptools import setup, find_packages

current_path = os.path.abspath(os.path.dirname(__file__))

setup(
    name = "bili23",
    version = "1.2.0",
    keywords = ["pip", "bilibili", "video-downloader", "cli"],
    description = "下载 Bilibili 视频/番剧/电影/纪录片 等资源",
    long_description = open(os.path.join(current_path, "README.rst"), encoding = "utf-8").read(),
    license = "MIT License",
    url = "https://github.com/ScottSloan/Bili23-Downloader-CLI",
    project_urls = {
        "Home Page": "https://github.com/ScottSloan/Bili23-Downloader-CLI",
        "Bug Tracker": "https://github.com/ScottSloan/Bili23-Downloader-CLI/issues"
    },
    author = "Scott Sloan",
    author_email = "world1019@sina.com",

    packages = find_packages(),
    include_package_data = True,
    install_requires = ["click", "requests", "colorama"],
    platforms = "any",
    python_requires = ">=3.10",

    classifiers = [
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],

    entry_points = '''
    [console_scripts]
    bili23=bili23.bili23:main
    '''
)
