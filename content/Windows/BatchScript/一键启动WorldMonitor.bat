@echo off
chcp 65001 >nul

REM ============================================================================
REM WorldMonitor 开发服务器启动脚本
REM 功能：
REM   1. 自动切换到项目目录 D:\0code\WorldMonitor
REM   2. 检查 Node.js 和 npm 是否可用
REM   3. 执行 npm run dev 启动开发服务器
REM   4. 显示常用操作提示
REM ============================================================================

REM 【关键配置】请根据实际部署情况修改以下路径
set "PROJECT_DIR=D:\0code\WorldMonitor"
REM 若项目路径不同，请修改上述变量值

REM 1. 切换到项目目录（若目录不存在则报错退出）
cd /d "%PROJECT_DIR%" || (
    echo 错误：项目目录不存在，请检查路径或修改脚本
    echo 当前设定路径：%PROJECT_DIR%
    pause
    exit /b 1
)

echo 正在进入项目目录：%cd%

REM 2. 检查 Node.js 环境
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误：未检测到 Node.js，请先安装 Node.js 并确保其加入系统 PATH
    pause
    exit /b 1
)

where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误：未检测到 npm，请确认 Node.js 安装完整
    pause
    exit /b 1
)

REM 3. 检查 node_modules 是否存在（可选，避免忘记安装依赖）
if not exist "node_modules" (
    echo 警告：未找到 node_modules 目录，可能需要先运行 npm install
    echo 是否现在安装依赖？[Y/N]
    choice /c YN /n /m "请输入 Y 或 N："
    if errorlevel 2 (
        echo 跳过依赖安装，继续启动...
    ) else (
        echo 正在安装项目依赖，请稍候...
        call npm install
        if %errorlevel% neq 0 (
            echo 依赖安装失败，请检查网络或手动执行 npm install
            pause
            exit /b 1
        )
    )
)

REM 4. 启动开发服务器
echo.
echo ============================================
echo 正在启动 WorldMonitor 开发服务器...
echo 命令：npm run dev
echo 按 Ctrl + C 可停止服务器
echo ============================================
echo.

call npm run dev

REM 如果服务器进程被结束（或异常退出），暂停以查看错误信息
echo.
echo 开发服务器已停止。
pause

REM ============================================================================
REM 脚本说明：
REM   - 本脚本通过 cd /d 切换到项目目录，支持跨盘符切换
REM   - 自动检测 Node.js 环境，避免因环境缺失导致启动失败
REM   - 可选安装依赖功能，方便首次运行或依赖更新时使用
REM   - 执行后保持窗口打开，显示服务器输出；按 Ctrl+C 可终止服务器
REM   - 服务器退出后自动暂停，便于查看错误信息
REM
REM 【跨设备部署必改项】
REM   1. 第18行：修改 PROJECT_DIR 为实际项目所在路径
REM
REM 【常见问题】
REM   - 若出现中文乱码，将第2行 chcp 65001 改为 chcp 936（GBK）或删除该行
REM   - 如果 npm run dev 需要管理员权限，请右键脚本 → “以管理员身份运行”
REM   - 若端口被占用，请手动修改项目配置或关闭占用端口的进程
REM   - 保存脚本时建议使用 UTF-8 无 BOM 编码（记事本另存时可选）
REM
REM 【使用建议】
REM   - 将脚本放在桌面或任何方便的位置，双击即可启动项目
REM   - 可在脚本目录下创建快捷方式并设置图标，方便识别
REM
REM 脚本版本：v1.0 | 适用系统：Windows 7/8/10/11
REM 项目地址：https://github.com/koala73/worldmonitor
REM ============================================================================