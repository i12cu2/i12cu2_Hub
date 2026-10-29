@echo off
chcp 65001 >nul
cd /d "D:\0code\DouK-Downloader_V5.7_Windows_X64" || (
    echo 错误：程序目录不存在，请检查路径或修改脚本
    pause
    exit /b 1
)
(
    echo 5
    echo 1
    echo 3
    echo D:\0code\DouK-Downloader_V5.7_Windows_X64\mine
) | main.exe

:: 新增功能：程序执行完成后自动打开下载内容所在文件夹
explorer "D:\0code\DouK-Downloader_V5.7_Windows_X64\_internal\Volume"

pause

REM ============================================================================
REM 脚本说明：DouK-Downloader_V5.7 自动启动脚本（标准输入管道方案）
REM 功能：
REM   1. 启动main.exe并自动输入 5→回车→1→回车→3→回车→mine路径→回车
REM   2. 执行完成后自动打开资源管理器，定位到下载内容存储路径
REM   3. 窗口悬停等待用户操作
REM 
REM 【关键修改点】（跨设备部署时必看）
REM 1. 第5行路径：修改为实际安装目录（需包含main.exe）
REM 2. 第11行路径：同步修改mine目录的完整路径（建议提前创建该文件夹）
REM 3. 第21行路径：修改为下载内容的实际存储路径（需与程序配置一致）
REM 4. 若遇中文乱码：将第2行 chcp 65001 改为 chcp 936（GBK）或删除该行
REM 
REM 【使用注意】
REM - 保存脚本时请选择 ANSI 或 UTF-8 无BOM 编码（记事本"另存为"可选）
REM - 若杀毒软件拦截：右键脚本 → "以管理员身份运行" 或添加信任
REM - 窗口闪退排查：临时删除首行 "@echo off" 查看具体错误
REM - 本方案依赖程序读取标准输入（主流控制台程序均支持）
REM 
REM 【路径说明】
REM - mine目录：存放待采集账号链接的文本文件
REM - _internal\Volume：程序下载的视频/图片默认存储位置
REM 
REM 【备用方案】
REM 若输入无效（程序不响应管道输入）：
REM   1. 尝试方案二（VBScript模拟按键脚本）
REM   2. 或手动运行：启动main.exe后依次输入 5,1,3,路径
REM 
REM 文档版本：v1.3 | 适用系统：Windows 7 SP1 及以上
REM 项目路径 https://github.com/JoeanAmier/TikTokDownloader/releases/tag/5.7
REM -> 下载到 D:\DouK-Downloader_V5.7_Windows_X64\main.exe
REM 5 回车 -> 终端交互模式
REM 1 回车 -> 1. 批量下载账号作品(抖音)
REM 3 回车 -> 3. 从文本文档读取待采集的账号链接
REM D:\DouK-Downloader_V5.7_Windows_X64\mine 回车 -> 目标路径的文件中存储下载采集账号的链接(以Enter分割)
REM ============================================================================