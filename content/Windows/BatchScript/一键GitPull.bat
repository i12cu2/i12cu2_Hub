@echo off
setlocal enabledelayedexpansion

echo 开始遍历当前目录下的 Git 项目...
echo.

for /d %%i in (*) do (
    if exist "%%i\.git" (
        echo 正在更新项目: %%i
        pushd "%%i"
        git pull
        popd
        echo.
    ) else (
        echo 跳过非 Git 项目: %%i
    )
)

echo 所有 Git 项目已更新完毕。
pause

REM ============================================================================
REM 脚本说明：批量更新 Git 项目
REM 功能：遍历当前目录下的所有子文件夹，若包含 .git 目录则执行 git pull
REM 
REM 【使用注意】
REM 1. 确保 Git 已安装且 git 命令可用（已添加至系统环境变量 PATH）
REM 2. 脚本需放在包含多个 Git 项目文件夹的父目录中运行
REM 3. 若控制台中文显示乱码，请将文件保存为 ANSI 编码，或在脚本首行添加 chcp 65001
REM 4. 如有本地未提交的修改，git pull 可能失败，脚本会跳过继续执行其他项目
REM 
REM 适用系统：Windows 7 及以上（需安装 Git）
REM ============================================================================