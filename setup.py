from setuptools import setup, find_packages

setup(
    name = "bili23",
    version = "1.0.3b0",
    keywords = ["pip", "bilibili", "video-downloader", "cli"],
    description = "下载 Bilibili 视频/番剧/电影/纪录片 等资源",
    readme = "README.rst",
    license = "MIT License",
    url = "https://github.com/ScottSloan/Bili23-Downloader-CLI",
    project_urls = {
        "Home Page": "https://github.com/ScottSloan/Bili23-Downloader-CLI",
        "Bug Tracker": "https://github.com/ScottSloan/Bili23-Downloader-CLI/issues"
    },
    author = "Scott Sloan",
    author_email = "scottsloan@petalmail.com",

    packages = find_packages(),
    install_requires = ["click", "requests", "colorama"],
    platforms = "any",
    python_requires = ">=3.6",

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
