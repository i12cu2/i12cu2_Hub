@echo off
chcp 936 >nul
set "ASTRBOT_DIR=%USERPROFILE%"
set "NAPCAT_DIR=D:\0code\NapCat.Shell"

REM =============== 路径验证 ===============
if not exist "%NAPCAT_DIR%" (
    echo [错误] NapCat目录不存在：%NAPCAT_DIR%
    echo 请按以下步骤操作：
    echo   1. 检查NapCat是否安装在该路径
    echo   2. 修改脚本第4行的NAPCAT_DIR为实际路径
    pause
    exit /b 1
)

REM =============== 启动程序 ===============
start "AstrBot" /D "%ASTRBOT_DIR%" cmd /k "astrbot run"
start "NapCat_3371325585" /D "%NAPCAT_DIR%" cmd /k "launcher.bat 3371325585"

echo.
echo [成功] 已启动以下服务：
echo   ✓ AstrBot（工作目录：%ASTRBOT_DIR%）
echo   ✓ NapCat（QQ：3371325585）
echo.
timeout /t 2 >nul
exit /b 0

REM ============================================================================
REM 脚本名称：一键启动AstrBot与NapCat.bat
REM 功能说明：同时启动AstrBot机器人和NapCat QQ框架
REM 
REM 【使用前必读】
REM 1. 保存编码（最关键！）：
REM    - 用记事本打开 → 文件 → 另存为
REM    - 编码选择：ANSI（中文Windows系统下即GBK）
REM    - ❌ 禁止选择"UTF-8"或"带BOM的UTF-8"
REM 
REM 2. 路径配置（仅需改1处）：
REM    - 若NapCat不在D:\0code\NapCat.Shell：
REM      修改第4行：set "NAPCAT_DIR=您的实际路径"
REM      示例：set "NAPCAT_DIR=C:\QQ机器人\NapCat"
REM 
REM 3. 运行方式：
REM    - 双击脚本 → 自动弹出两个控制台窗口
REM    - AstrBot窗口：显示机器人运行日志
REM    - NapCat窗口：显示QQ登录及消息处理状态
REM 
REM 【常见问题解决】
REM 问题：窗口闪退/显示乱码
REM   → 重新用记事本打开脚本 → 另存为 → 编码选ANSI → 保存后重试
REM 
REM 问题：提示"astrbot不是内部命令"
REM   → 确保已安装AstrBot：pip install astrbot --upgrade
REM   → 或在用户目录（C:\Users\你的用户名）手动执行astrbot run验证
REM 
REM 问题：NapCat启动失败
REM   → 检查NAPCAT_DIR路径是否包含launcher.bat
REM   → 确认QQ号3371325585是否需要修改（第13行）
REM 
REM 问题：杀毒软件拦截
REM   → 右键脚本 →"以管理员身份运行"
REM   → 将脚本所在文件夹添加到杀毒软件信任区
REM 
REM 【技术说明】
REM - AstrBot工作目录：自动使用当前用户目录（%USERPROFILE%）
REM   （您之前在CMD直接输入astrbot run能成功，正是因为工作目录正确）
REM - 代码页设置：chcp 936 确保中文提示正常显示
REM - 窗口标题：明确标识服务类型，避免误关
REM - 验证逻辑：仅检查NapCat路径（AstrBot依赖系统环境变量，无需额外验证）
REM 
REM 【安全提示】
REM 本脚本仅调用本地已安装程序，不联网、不修改系统设置，安全可靠
REM 
REM 适用环境：
REM   Windows 10/11 中文版 | AstrBot v4.20.0+ | NapCat v3.0.0+
REM ============================================================================