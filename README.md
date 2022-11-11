# Bili23-Downloader-CLI
![Version](https://img.shields.io/github/v/release/ScottSloan/Bili23-Downloader-CLI?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square) 

Bili23 Downloader CLI 命令行版本

下载 Bilibili 视频/番剧/电影/纪录片 等资源

# 使用说明
## 安装
### 方式一：使用 pip 安装
```
pip install bili23-cli
```

安装后，终端中执行 `bili23` 即可启动启动程序

### 方式二：编译版安装
请前往 Release 页面中下载最新版本

### 安装 ffmpeg
由于 dash 格式视频依赖 ffmpeg 合成视频，需要事先下载安装。

[蓝奏云](https://wwf.lanzout.com/iKl7j0fobykf) 密码:4kk0

下载后，将 bin 目录下的 ffmpeg.exe 解压至程序运行目录下即可

## 使用
用法：
```
bili23 [OPTIONS]
```

> 如果使用的是编译版，在程序运行目录下打开终端，使用 `./bili23.exe` 命令即可

| 选项 | 说明 |
| ---- | ---- |
| --i, --info URL | 获取视频信息 |
| --p, --parse URL | 解析视频链接 |
| --v, --version | 显示版本信息 |
| --h, --help | 显示帮助信息 |

### --i, --info 选项
打印输出视频信息

示例
```
bili23 --i https://www.bilibili.com/video/BV1fd4y117xT
```

[![zCqVpt.png](https://s1.ax1x.com/2022/11/11/zCqVpt.png)](https://imgse.com/i/zCqVpt)

### --p, --parse 选项
解析视频链接并下载

示例
```
bili23 --p https://www.bilibili.com/video/BV1fd4y117xT
```

对于分P，合集视频或番组等类型视频，程序将显示剧集列表，用户需手动输入序号（输入 0 即代表全部下载）。

[![zCqtXT.png](https://s1.ax1x.com/2022/11/11/zCqtXT.png)](https://imgse.com/i/zCqtXT)

[![zCqUnU.png](https://s1.ax1x.com/2022/11/11/zCqUnU.png)](https://imgse.com/i/zCqUnU)

## 更新日志
### Version 1.00
Bili23 Downloader CLI 命令行版本正式发布！

CLI 版本延续 Bili23 Downloader 系列简便易用的的设计理念，与 GUI 版本一道，为用户带来最佳的使用体验。

本次更新内容如下：
* 支持下载用户投稿视频和番组类型的视频
* 多线程高速下载视频