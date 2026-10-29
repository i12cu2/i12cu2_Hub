# BiliTools

一个整合了 B站视频下载、音频提取、封面下载、简介提取的懒人工具。

支持单个视频、视频合集、UP主主页三种输入，一键处理。

---

## 功能一览

| 输入         | 动作                                                   |
| ------------ | ------------------------------------------------------ |
| `链接`       | 下载视频（合集会自动全部下载，UP主主页会下载全部作品） |
| `链接 mp3`   | 下载视频，自动转成 MP3，然后删掉视频                   |
| `链接 cover` | 只下载视频的封面图片                                   |
| `链接 intro` | 提取视频简介，保存成 txt 文件                          |
| `链接 all`   | 下载视频 + 封面 + 简介（不转 MP3）                     |

三种输入对应的处理范围：

- **单个视频**：处理这一个视频
- **视频合集**：自动识别，处理合集里的全部分P
- **UP主主页**：通过 yt-dlp 拉取视频列表，处理全部作品

另外还支持**拖拽模式**：把一个或多个 MP4 文件（或包含 MP4 的文件夹）拖到程序图标上，自动批量转成同名 MP3。

---

## 环境要求

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html)（用于 MP3 转换，需将 `bin` 目录加入系统 PATH）
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)（用于获取 UP 主视频列表）

安装 Python 依赖：

```bash
pip install requests yt-dlp
```

推荐安装最新版 yt-dlp：

```bash
pip install -U yt-dlp
```

---

## 使用方法

### 方式一：双击运行

直接双击脚本运行，进入交互模式：

```
=======================================================
BiliTools
=======================================================
链接 → 下载视频（合集会自动全部下载，UP主主页会下载全部作品）
链接 mp3 → 下载视频，自动转成 MP3，然后删掉视频
链接 cover → 只下载这张视频的封面图片
链接 intro → 提取视频简介，保存成 txt 文件
链接 all → 下载视频 + 封面 + 简介（不转 MP3）
       （合集或UP主会把对应全部都提取出来）
保存路径：  ...
=======================================================
输入指令:
```

按提示粘贴链接即可，想结束直接关闭窗口。

### 方式二：拖拽运行

把 MP4 文件或包含 MP4 的文件夹拖到程序图标上，自动批量转 MP3。

---

## 配置说明

代码顶部有两个配置项，用于处理需要登录态的情况（主要是 UP 主主页功能）：

```python
# 方式一：指定 cookies.txt 文件路径（推荐，跨设备通用）
COOKIES_FILE = r"C:\Users\Admin\bili_cookies.txt"

# 方式二：从浏览器直接读取 Cookie（仅在本机使用方便）
COOKIES_FROM_BROWSER = "firefox"   # 可选：firefox / chrome / edge
```

优先级：`COOKIES_FILE` 存在且有效时优先使用，否则使用 `COOKIES_FROM_BROWSER`。

### 如何获取 cookies.txt

1. 浏览器安装扩展 **"Get cookies.txt LOCALLY"**
2. 打开并登录 bilibili.com
3. 点击扩展图标 → Export → 保存为 `cookies.txt`
4. 把文件路径填入 `COOKIES_FILE`

### 关于 `COOKIES_FROM_BROWSER`

- **Firefox 最稳**，数据库不会被锁定，直接可用
- **Chrome / Edge 常常报错** `Could not copy Chrome cookie database`，原因是浏览器运行中会锁定 Cookie 数据库。这时推荐改用 `cookies.txt` 方案

---

## 输出目录结构

所有文件保存到**程序所在目录**（脚本运行取 `.py` 所在目录，打包成 exe 后取 exe 所在目录）。

### 单个视频 + all

```
程序目录/
  视频标题/
    视频标题.mp4
    视频标题_封面.jpg
    视频标题_简介.txt
```

### 视频合集

```
程序目录/
  合集标题/
    P1_第一节.mp4
    P1_第一节_封面.jpg
    P1_第一节_简介.txt
    P2_第二节.mp4
    ...
```

### UP主主页 + video / mp3

```
程序目录/
  UP主名字/
    视频标题1.mp4
    视频标题2.mp4
    ...
```

### UP主主页 + all

```
程序目录/
  UP主名字/
    视频标题1/
      视频标题1.mp4
      视频标题1_封面.jpg
      视频标题1_简介.txt
    视频标题2/
      ...
```

### 单独下载封面或简介

不建文件夹，直接放在程序目录：

```
程序目录/
  视频标题_封面.jpg
  视频标题_简介.txt
```

---

## 常见问题

### Q: 提示 `未找到 ffmpeg`？

安装 FFmpeg 并把它的 `bin` 目录加入系统环境变量 PATH，或者把它放在以下路径之一：

```
C:\Program File\ffmpeg\bin
C:\Program Files\ffmpeg\bin
C:\Program Files (x86)\ffmpeg\bin
C:\ffmpeg\bin
```

### Q: 提示 `未找到 yt-dlp`？

```bash
pip install yt-dlp
```

### Q: UP主主页获取失败，提示 `访问权限不足`？

B站对空间接口有登录态要求。请配置好 `COOKIES_FILE` 或 `COOKIES_FROM_BROWSER`，确保使用的浏览器已经登录 B站。

### Q: 报错 `Could not copy Chrome cookie database`？

Chrome / Edge 的 Cookie 数据库会被浏览器运行时锁定。三个解决办法：

1. 完全关闭浏览器后台进程（任务管理器里结束所有浏览器进程）
2. 换用 Firefox：`COOKIES_FROM_BROWSER = "firefox"`
3. 导出 `cookies.txt`，用 `COOKIES_FILE` 指定

### Q: 转换 MP3 失败？

代码会打印 ffmpeg 的具体报错信息。常见原因：

- 源视频没有音轨
- 磁盘空间不足
- ffmpeg 安装不完整

### Q: 视频下载到一半中断了？

代码使用 `.part` 临时文件机制。中断后留下的是 `.xxx.part` 文件，不会和正式文件混淆。下次运行会重新下载，不会误认为是完整文件。

---

## 已知限制

- **视频清晰度**：默认最高 1080P（qn=80）。更高清晰度需要登录且为大会员，本工具暂不处理。
- **分P下载**：默认只下载第一个分P的视频流，多P合集会逐个下载。
- **封面模式 + UP主主页**：不支持批量下封面，会给出提示。
- **断点续传**：不支持，中断后重新下载。
- **简介接口限速**：UP主 intro 模式同步逐个获取，视频多时会比较慢。

---

## 依赖的外部工具

本项目的核心能力依赖以下两个成熟工具，请尊重它们的开源协议：

- **FFmpeg** —— 音视频处理，[GPL/LGPL](https://ffmpeg.org/legal.html)
- **yt-dlp** —— 视频列表获取，[Unlicense](https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE)

---

## 免责声明

本工具仅供个人学习与研究使用。请勿用于批量下载、二次分发或其他侵犯版权的行为。使用本工具产生的任何后果由使用者自行承担。