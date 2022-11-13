# Bili23-Downloader-CLI
![Version](https://img.shields.io/github/v/release/ScottSloan/Bili23-Downloader-CLI?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square) 

Bili23 Downloader CLI 命令行版本

下载 Bilibili 视频/番剧/电影/纪录片 等资源

+ [使用说明](#使用说明)
+ [开发日志](#开发日志)
+ [联系方式](#联系方式)

# 使用说明
## 安装
### 使用 pip 安装
终端中执行以下命令

```
pip install bili23
```

### 安装 ffmpeg
由于 `dash` 格式视频依赖 `ffmpeg` 进行合成，需事先安装

### Windows 用户请按照下面的步骤安装：  
ffmpeg 下载地址：[蓝奏云](https://wwf.lanzout.com/iTYX00ft3u4h)  密码:h9ge  

解压压缩包，记录 `ffmpeg` 所在文件夹的路径，按照以下步骤创建环境变量：

> 此电脑 -> 右键 -> 属性 -> 高级系统设置 -> 环境变量 -> 系统变量 -> Path -> 编辑 -> 新建 -> ffmpeg 所在文件夹的路径

详细步骤请看[这里](https://scott.o5g.top/index.php/archives/120/)

### Linux 用户请执行以下命令安装：  

```
sudo apt install ffmpeg
```
## 更新
运行以下命令更新 Bili23 Downloader CLI：

```
pip install bili23 --upgrade
```

## 使用
用法：
```
bili23 [OPTIONS]
```

| 参数 | 说明 |
| ---- | ---- |
| --i, --info URL | 获取视频信息 |
| --p, --parse URL | 解析视频链接 |
| --d, --dir | 指定下载目录，默认为当前运行目录 |
| --t, --thread | 指定下载线程数，默认为 4 个线程 |
| --q, --quality | 指定下载的清晰度，默认为 80 (1080P) |
| --codec | 指定下载的视频编码，默认为 HEVC (HEVC/H.265) |
| --a, --all | 下载全部视频 |
| --v, --version | 显示版本信息 |
| --h, --help | 显示帮助信息 |

**注意：URL 链接需加上引号**

### --i, --info 参数
打印输出视频信息

示例
```
bili23 --i "BV1fd4y117xT"
```

[![zi2yd0.png](https://s1.ax1x.com/2022/11/12/zi2yd0.png)](https://imgse.com/i/zi2yd0)

### --p, --parse 参数
解析视频链接并下载

配合以下参数使用：
| 参数 | 说明 |
| ---- | ---- |
| --d, --dir | 指定下载目录，默认为当前运行目录 |
| --t, --thread | 指定下载线程数，默认为 4 个线程 |
| --q, --quality | 指定下载的清晰度，默认为 80 (1080P) |
| --codec | 指定下载的视频编码，默认为 HEVC (HEVC/H.265) |
| --a, --all | 下载全部视频 |

示例
```
bili23 --p "BV1fd4y117xT"
```

[![zi2bFK.png](https://s1.ax1x.com/2022/11/12/zi2bFK.png)](https://imgse.com/i/zi2bFK)

对于分P，合集视频或番组等类型视频，程序将显示剧集列表，用户需手动输入序号（输入 0 即代表全部下载）

[![zi2hQJ.png](https://s1.ax1x.com/2022/11/12/zi2hQJ.png)](https://imgse.com/i/zi2hQJ)


通过指定 --a 参数可跳过剧集选择，直接下载全部视频  

示例
```
bili23 --p "BV1fd4y117xT" --a
```

[![ziRHns.png](https://s1.ax1x.com/2022/11/12/ziRHns.png)](https://imgse.com/i/ziRHns)

### --q, --quality 参数
指定下载的清晰度
| 描述 | 清晰度 |
| ---- | ---- |
| 超高清 8K | 127 |
| 杜比视界 | 126 |
| 真彩 HDR | 125 |
| 超清 4K | 120 |
| 高清 1080P60 | 116 |
| 高清 1080P+ | 112 |
| 高清 1080P | 80 |
| 高清 720P | 64 |
| 清晰 480P | 32 |
| 流畅 360P | 16 |

### --codec 参数
指定下载的视频编码
| 类型 | 编码 |
| ---- | ---- |
| AVC/H.264 | AVC |
| HEVC/H.265 | HEVC |
| AV1 | AV1 |

# 更新日志
### Version 1.02 (2022-11-13)
本次更新内容如下：
* 支持 --q, --codec 参数，详情请查看[使用说明](https://github.com/ScottSloan/Bili23-Downloader-CLI)
* 修复部分已知问题

<details>
<summary>Version 1.01</summary>

### Version 1.01 (2022-11-12)
本次更新内容如下：
* 支持 --d, --t, --a 参数，详情请查看[使用说明](https://github.com/ScottSloan/Bili23-Downloader-CLI)
* 优化程序逻辑
* 支持 Linux 平台
* 修复部分已知问题

</details>

<details>
<summary>Version 1.00</summary>

### Version 1.00 (2022-11-11)
Bili23 Downloader CLI 命令行版本正式发布！

CLI 版本延续 Bili23 Downloader 系列简便易用的的设计理念，与 GUI 版本一道，为用户带来最佳的使用体验。

本次更新内容如下：
* 支持下载用户投稿视频和番组类型的视频
* 多线程高速下载视频

</details>

# 联系方式
Email: scottsloan@petalmail.com  
Blog: https://scott.o5g.top