import os
import re
import requests
import json
import argparse
import subprocess
from send2trash import send2trash

# 设置FFmpeg和FFprobe的绝对路径（请根据你的实际安装路径修改）
# 下载路径 https://ffmpeg.org/download.html#get-packages
FFMPEG_PATH = r"C:\Program File\ffmpeg\bin\ffmpeg.exe"  # 替换为你的ffmpeg.exe绝对路径
FFPROBE_PATH = r"C:\Program File\ffmpeg\bin\ffprobe.exe"  # 替换为你的ffprobe.exe绝对路径
SAVE_PATH = r"C:\Users\Admin\Desktop"  # 可以修改为任意路径


class BilibiliCollectionDownloader:
    """B站下载器：支持单视频、多P视频、合集(ugc_season)批量下载并转MP3"""

    def __init__(self, save_path="./downloads"):
        """
        初始化下载器
        :param save_path: 视频保存路径
        """
        self.save_path = save_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        })

        # 设置ffmpeg的绝对路径
        self.ffmpeg_path = FFMPEG_PATH

        # 检查ffmpeg是否存在
        if not os.path.exists(self.ffmpeg_path):
            print(f"警告: 在路径 {self.ffmpeg_path} 未找到ffmpeg，MP3转换功能将不可用")
            print("请修改代码中的ffmpeg_path变量为正确的ffmpeg路径")

        # 创建保存目录
        if not os.path.exists(save_path):
            os.makedirs(save_path)

    # ------------------------------------------------------------------
    # 工具方法
    # ------------------------------------------------------------------
    def extract_bvid(self, input_str):
        """
        从输入中提取BV号，支持带有查询参数的URL
        :param input_str: 可以是BV号或B站视频URL（可以带有查询参数）
        :return: 提取到的BV号，如果提取失败返回None
        """
        # 如果是BV号格式直接返回
        if re.match(r'^BV[0-9A-Za-z]{10}$', input_str):
            return input_str

        # 尝试从URL中提取BV号，支持带有查询参数的URL
        bvid_patterns = [
            r'/(BV[0-9A-Za-z]{10})(?:\?|/|$)',                       # 常规URL格式
            r'bilibili\.com/video/(BV[0-9A-Za-z]{10})(?:\?|/|$)',    # 另一种URL格式
            r'^BV[0-9A-Za-z]{10}$',                                  # 纯BV号格式
        ]

        for pattern in bvid_patterns:
            match = re.search(pattern, input_str)
            if match:
                # 如果有捕获组，返回第一个捕获组；否则返回整个匹配
                return match.group(1) if match.groups() else match.group(0)

        return None

    def sanitize_filename(self, filename):
        """
        清理文件名中的非法字符
        :param filename: 原始文件名
        :return: 清理后的文件名
        """
        if not filename:
            return "未命名"

        # 移除或替换文件名中的非法字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')

        # 去掉首尾空白和结尾的点（Windows 不允许以点结尾）
        filename = filename.strip().strip('.')
        if not filename:
            filename = "未命名"

        # 限制文件名长度，避免路径过长
        if len(filename) > 100:
            filename = filename[:100]
        return filename

    # ------------------------------------------------------------------
    # 网络请求
    # ------------------------------------------------------------------
    def get_video_info(self, bvid):
        """
        获取视频基本信息（包含 ugc_season 合集信息、pages 分P信息）
        :param bvid: 视频BV号
        :return: 视频信息字典
        """
        info_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        response = self.session.get(info_url)
        data = response.json()

        if data['code'] != 0:
            raise Exception(f"获取视频信息失败: {data.get('message', '未知错误')}")

        return data['data']

    def build_task_list(self, info_data):
        """
        根据视频信息构建下载任务列表
        :param info_data: get_video_info 返回的 data 字段
        :return: (合集标题 or None, [task, ...])
                 task = {'bvid':..., 'cid':..., 'title':..., 'index':...}
        """
        tasks = []
        season_title = None

        # 1) 优先处理合集（ugc_season）
        season = info_data.get('ugc_season')
        if season:
            season_title = season.get('title') or info_data.get('title')
            index = 0
            for section in season.get('sections', []):
                for ep in section.get('episodes', []):
                    ep_bvid = ep.get('bvid')
                    ep_cid = ep.get('cid')
                    if not ep_bvid or not ep_cid:
                        continue
                    index += 1
                    tasks.append({
                        'bvid': ep_bvid,
                        'cid': ep_cid,
                        'title': ep.get('title') or ep.get('part') or f"P{index}",
                        'index': index,
                    })

        # 2) 没有合集信息时，检查是否为多P视频
        if not tasks:
            pages = info_data.get('pages', [])
            if len(pages) > 1:
                for page in pages:
                    tasks.append({
                        'bvid': info_data.get('bvid'),
                        'cid': page.get('cid'),
                        'title': page.get('part') or f"P{page.get('page')}",
                        'index': page.get('page', 0),
                    })
            else:
                # 3) 单个视频
                tasks.append({
                    'bvid': info_data.get('bvid'),
                    'cid': info_data.get('cid'),
                    'title': info_data.get('title'),
                    'index': 0,
                })

        return season_title, tasks

    def get_video_url(self, bvid, cid):
        """
        获取指定视频的直链
        :param bvid: 视频BV号
        :param cid: 视频cid
        :return: 视频直链
        """
        play_url = f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=80&type=&otype=json"
        play_response = self.session.get(play_url)
        play_data = play_response.json()

        if play_data['code'] != 0:
            raise Exception(f"获取播放链接失败: {play_data.get('message', '未知错误')}")

        durl = play_data.get('data', {}).get('durl')
        if not durl:
            raise Exception("未获取到视频直链（该视频可能为 DASH 格式或需要登录）")

        # 获取最高清晰度的视频链接
        return durl[0]['url']

    # ------------------------------------------------------------------
    # 下载 / 转换
    # ------------------------------------------------------------------
    def download_video(self, video_url, filename):
        """
        下载视频文件
        :param video_url: 视频下载链接
        :param filename: 保存的文件名（不含扩展名）
        :return: 下载的文件路径
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }

        # 获取视频内容
        response = self.session.get(video_url, headers=headers, stream=True)
        response.raise_for_status()

        # 确定文件扩展名
        content_type = response.headers.get('content-type', '')
        if 'mp4' in content_type:
            ext = '.mp4'
        elif 'flv' in content_type:
            ext = '.flv'
        else:
            ext = '.mp4'  # 默认使用mp4

        filepath = os.path.join(self.save_path, f"{filename}{ext}")

        # 下载视频
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    # 显示下载进度
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"\r下载进度: {progress:.2f}% ({downloaded_size}/{total_size} bytes)", end='')

        print(f"\n视频下载完成: {filepath}")
        return filepath

    def convert_mp4_to_mp3(self, mp4_path):
        """
        将MP4文件转换为MP3文件
        :param mp4_path: MP4文件路径
        :return: MP3文件路径，如果转换失败返回None
        """
        if not os.path.exists(self.ffmpeg_path):
            print("ffmpeg未找到，无法进行MP3转换")
            return None

        if not os.path.exists(mp4_path):
            print(f"MP4文件不存在: {mp4_path}")
            return None

        # 生成MP3文件路径（同目录，同名，扩展名为.mp3）
        mp3_path = os.path.splitext(mp4_path)[0] + '.mp3'

        try:
            print("开始转换MP4为MP3...")

            # 构建ffmpeg命令
            # -i 输入文件
            # -vn 不处理视频流
            # -acodec libmp3lame 使用MP3编码器
            # -q:a 0 最高音频质量（0-9，0为最高）
            # -y 覆盖输出文件
            cmd = [
                self.ffmpeg_path,
                '-i', mp4_path,
                '-vn',                    # 不包含视频
                '-acodec', 'libmp3lame',  # 使用MP3编码
                '-q:a', '0',              # 最高音频质量
                '-y',                     # 覆盖已存在文件
                mp3_path
            ]

            # 修复编码问题：使用subprocess.Popen并指定正确的编码
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,   # 以文本模式处理输出
                encoding='utf-8',          # 指定编码为UTF-8
                errors='ignore'            # 忽略编码错误
            )

            stdout, stderr = process.communicate(timeout=300)

            if process.returncode == 0:
                print(f"MP3转换完成: {mp3_path}")
                return mp3_path
            else:
                print(f"MP3转换失败，错误信息: {stderr}")
                if not stderr:
                    print("ffmpeg返回非零退出码，但无法获取错误信息")
                return None

        except subprocess.TimeoutExpired:
            print("MP3转换超时")
            return None
        except UnicodeDecodeError as e:
            # 如果仍然有编码错误，尝试不捕获输出
            print(f"编码错误，尝试直接运行ffmpeg: {e}")
            try:
                result = subprocess.run(cmd, timeout=300, check=True)
                if result.returncode == 0:
                    print(f"MP3转换完成: {mp3_path}")
                    return mp3_path
                else:
                    print("MP3转换失败")
                    return None
            except subprocess.CalledProcessError as e:
                print(f"MP3转换失败: {e}")
                return None
            except Exception as e:
                print(f"MP3转换过程中发生错误: {e}")
                return None
        except Exception as e:
            print(f"MP3转换过程中发生错误: {e}")
            return None

    # ------------------------------------------------------------------
    # 主流程
    # ------------------------------------------------------------------
    def download(self, input_str, convert_to_mp3=True):
        """
        主下载函数：自动识别单视频 / 多P视频 / 合集
        :param input_str: 可以是BV号或B站视频URL（可以带有查询参数）
        :param convert_to_mp3: 是否转换为MP3
        :return: 结果列表 [(视频路径 or None, MP3路径 or None), ...]
        """
        # 提取BV号
        bvid = self.extract_bvid(input_str)
        if not bvid:
            raise ValueError("无法从输入中提取BV号")

        print(f"提取到BV号: {bvid}")

        # 获取视频信息
        print("获取视频信息中...")
        info_data = self.get_video_info(bvid)

        # 构建任务列表
        season_title, tasks = self.build_task_list(info_data)

        total = len(tasks)
        if total > 1:
            if season_title:
                print(f"检测到合集《{season_title}》，共 {total} 个视频，开始批量下载...")
            else:
                print(f"检测到多P视频，共 {total} 个分P，开始批量下载...")
        else:
            print(f"视频标题: {tasks[0]['title']}")
            print("开始下载视频...")

        results = []
        for i, task in enumerate(tasks, 1):
            base_title = self.sanitize_filename(task['title'])

            # 多个视频时加上序号前缀，保证顺序和唯一性
            if total > 1:
                filename = f"{task['index']:02d}_{base_title}" if isinstance(task['index'], int) and task['index'] > 0 \
                    else f"{i:02d}_{base_title}"
            else:
                filename = base_title

            # 如果目标MP3已存在则跳过
            expected_mp3 = os.path.join(self.save_path, f"{filename}.mp3")
            if convert_to_mp3 and os.path.exists(expected_mp3):
                print(f"\n[{i}/{total}] 已存在 MP3，跳过: {expected_mp3}")
                results.append((None, expected_mp3))
                continue

            print(f"\n[{i}/{total}] 处理中: {task['title']}")

            try:
                # 获取直链
                video_url = self.get_video_url(task['bvid'], task['cid'])

                # 下载视频
                filepath = self.download_video(video_url, filename)

                # mp3_path = None
                # # 如果下载的是视频文件且需要转换为MP3
                # if convert_to_mp3 and filepath.lower().endswith(('.mp4', '.flv')):
                #     print("开始转换为MP3格式...")
                #     mp3_path = self.convert_mp4_to_mp3(filepath)
                #
                # results.append((filepath, mp3_path))

                mp3_path = None
                # 如果下载的是视频文件且需要转换为MP3
                if convert_to_mp3 and filepath.lower().endswith(('.mp4', '.flv')):
                    print("开始转换为MP3格式...")
                    mp3_path = self.convert_mp4_to_mp3(filepath)

                    # 转换成功后，把原视频文件移到回收站
                    if mp3_path and os.path.exists(mp3_path):
                        try:
                            send2trash(filepath)
                            print(f"已将原视频移动到回收站: {filepath}")
                        except Exception as e:
                            print(f"移动到回收站失败: {e}")

                results.append((filepath, mp3_path))

            except Exception as e:
                print(f"[{i}/{total}] 处理失败: {e}")
                results.append((None, None))

        # 汇总
        print("\n" + "=" * 50)
        print("全部任务完成，结果汇总：")
        success = sum(1 for _, mp3 in results if mp3)
        for i, (video, mp3) in enumerate(results, 1):
            if mp3:
                print(f"  [{i}] MP3: {mp3}")
            elif video:
                print(f"  [{i}] 视频: {video}")
            else:
                print(f"  [{i}] 失败")
        print(f"共 {total} 个任务，成功生成 {success} 个 MP3 文件。")
        print("=" * 50)

        return results


def main():
    parser = argparse.ArgumentParser(description='B站视频/合集下载工具')
    parser.add_argument('input', help='B站视频BV号或URL（可以带有查询参数）')
    parser.add_argument('-o', '--output', default=SAVE_PATH, help='视频保存路径')
    parser.add_argument('--no-convert', action='store_true', help='不自动转换为MP3')

    args = parser.parse_args()

    try:
        downloader = BilibiliCollectionDownloader(args.output)
        downloader.download(args.input, convert_to_mp3=not args.no_convert)
    except Exception as e:
        print(f"下载失败: {e}")


if __name__ == "__main__":
    # 创建下载器实例
    downloader = BilibiliCollectionDownloader(SAVE_PATH)

    # 持续输入网址进行下载
    while True:
        try:
            # 获取用户输入的网址
            url = input("请输入B站视频网址（输入'quit'退出程序）: ").strip()

            # 检查退出条件
            if url.lower() == 'quit':
                print("程序退出")
                break

            # 检查网址是否为空
            if not url:
                print("网址不能为空，请重新输入")
                continue

            # 下载视频
            print(f"开始下载: {url}")
            downloader.download(url, True)

        except KeyboardInterrupt:
            print("\n程序被用户中断")
            break
        except Exception as e:
            print(f"下载失败: {e}")
            print("请检查网址是否正确，或稍后重试")