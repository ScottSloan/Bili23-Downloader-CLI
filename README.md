# Bili23-Downloader-CLI
![Version](https://img.shields.io/github/v/release/ScottSloan/Bili23-Downloader-CLI?style=flat-square) ![Python](https://img.shields.io/badge/Python-3.9.12-green?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-orange?style=flat-square) 

Bili23 Downloader CLI 命令行版本

下载 Bilibili 视频/番剧/电影/纪录片 等资源

### **导航**
+ [使用说明](#使用说明)
+ [更新日志](#更新日志)
+ [联系方式](#联系方式)

### **Bili23 Downloader 系列**
* [GUI 桌面端版本](https://github.com/ScottSloan/Bili23-Downloader) (主项目)
* CLI 命令行版本 (本项目)

# 使用说明
## 安装
### **安装主程序**
终端中执行以下命令

```
pip install bili23
```

### **安装 ffmpeg**
由于 `dash` 格式视频依赖 `ffmpeg` 进行合成，需事先安装

### **Windows 用户请按照下面的步骤安装**  
ffmpeg 下载地址：[蓝奏云](https://wwf.lanzout.com/iTYX00ft3u4h)  密码:h9ge  

解压压缩包，记录 `ffmpeg` 所在文件夹的路径，按照以下步骤创建环境变量：

> 此电脑 -> 右键 -> 属性 -> 高级系统设置 -> 环境变量 -> 系统变量 -> Path -> 编辑 -> 新建 -> ffmpeg 所在文件夹的路径

详细步骤请看[这里](https://scott.o5g.top/index.php/archives/120/)

### **Linux 用户请执行以下命令安装**  

```
sudo apt install ffmpeg
```

## 更新
运行以下命令更新程序

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
| --c, --codec | 指定下载的视频编码，默认为 HEVC (HEVC/H.265) |
| --danmaku | 下载弹幕 |
| --subtitle | 下载字幕 |
| --lyric | 下载歌词 |
| --quiet | 静默输出 |
| --a, --all | 下载全部视频 |
| --edit-config | 编辑本地配置文件 |
| --v, --version | 显示版本信息 |
| --h, --help | 显示帮助信息 |

### **支持输入的 URL 链接**
- 用户投稿类型视频链接
- 剧集（番剧，电影，纪录片等）链接
- 活动页链接
- 音乐，歌单链接
- b23.tv 短链接

### **部分类型可直接输入编号**
- 视频 av、BV 号
- 剧集 epid、md、ss 号
- 音乐 au 号，歌单 am 号

> **注意：URL 链接需加上双引号**

### **--i, --info 参数**
打印输出视频信息

示例
```
bili23 --i "BV1fd4y117xT"
```

[![zi2yd0.png](https://s1.ax1x.com/2022/11/12/zi2yd0.png)](https://imgse.com/i/zi2yd0)

### **--p, --parse 参数**
解析 URL 链接并下载

以下为可选参数
| 参数 | 说明 |
| ---- | ---- |
| --d, --dir | 指定下载目录，默认为当前运行目录 |
| --t, --thread | 指定下载线程数，默认为 4 个线程 |
| --q, --quality | 指定下载的清晰度，默认为 80 (1080P) |
| --c, --codec | 指定下载的视频编码，默认为 HEVC (HEVC/H.265) |
| --danmaku | 下载弹幕 |
| --subtitle | 下载字幕 |
| --lyric | 下载歌词 |
| --a, --all | 下载全部视频 |

> 不指定参数时，程序将使用本地配置文件内的设置，有关配置文件的设置，请看[这里](#配置文件)

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

### **--q, --quality 参数**
指定下载的清晰度，默认为 80
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

> 我们强烈建议您使用 Cookie，以避免无法下载 1080P 和大会员视频的情况，有关 Cookie 的使用，请看[这里](#关于-cookie-sessdata-字段)

### **--c, --codec 参数**
指定下载的视频编码，默认为 HEVC
| 类型 | 编码 |
| ---- | ---- |
| AVC/H.264 | AVC |
| HEVC/H.265 | HEVC |
| AV1 | AV1 |

### **配置文件**
使用以下命令编辑本地配置文件

```
bili23 --edit-config
```
[![zeuc8K.png](https://s1.ax1x.com/2022/11/17/zeuc8K.png)](https://imgse.com/i/zeuc8K)

配置文件参数说明
| 参数 | 说明 | 默认值 |
| ---- | ---- | ---- |
| dir | 下载目录 | null (不指定时为当前运行目录) |
| thread | 下载线程数 | 4 |
| quality | 视频清晰度 | 80 |
| codec | 视频编码 | HEVC |
| sessdata | Cookie SESSDATA 字段 | null |

### **关于 Cookie SESSDATA 字段**
此字段含用户大会员信息，可用于下载大会员视频

获取方法

> 浏览器登录B站 -> 开发人员工具 -> 应用程序 -> Cookie -> SESSDATA

[![zQDwnK.png](https://s1.ax1x.com/2022/11/21/zQDwnK.png)](https://imgse.com/i/zQDwnK)

# 更新日志
### **Version 1.11 (2022-12-11)**
本次更新内容如下：
* 优化代码结构
* 移除 html 解析方式，现在将以 api 接口方式解析视频
* 修复部分已知问题

# 联系方式
Email: scottsloan@petalmail.com  
Blog: https://scott.o5g.top