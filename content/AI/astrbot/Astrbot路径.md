## 日志：astrbot 实际安装路径确认（uv 部署环境）

### 环境
- 操作系统：Windows
- 包管理工具：`uv`
- 安装方式：`uv tool install astrbot`（推测）

### 问题背景
你在命令行中使用 `uv` 部署了 `astrbot`，并在 `C:\Users\Admin\.local\bin` 目录下只发现了四个文件：`uvx`、`uvw`、`uv`、`astrbot`（`.exe` 文件）。你希望确认 `astrbot` 的完整安装位置，因为 `.local\bin` 目录下仅有启动脚本，但 `uv pip list` 未显示 `astrbot` 包。

### 排查过程

#### 1. 查看 `astrbot` 是否通过 `uv pip` 安装
执行命令：
```cmd
uv pip show astrbot
```
输出：
```
Using Python 3.12.1 environment at: AppData\Local\Programs\Python\Python312
warning: Package(s) not found for: astrbot
```
**结论**：`astrbot` 并未安装在当前 Python 环境（`Python312`）中。

#### 2. 查看当前 Python 环境中的所有包
执行命令：
```cmd
uv pip list
```
输出中不包含 `astrbot`（仅有其他依赖包），进一步确认 `astrbot` 不是通过 `uv pip install` 安装的。

#### 3. 检查 `uv tool` 安装的工具
`uv` 支持使用 `tool` 子命令安装独立命令行工具，这类工具会创建独立虚拟环境，并将启动脚本放入 `.local\bin`。  
执行命令：
```cmd
uv tool list
```
输出：
```
astrbot v4.20.0
- astrbot
```
未显示路径，但表明 `astrbot` 是通过 `uv tool` 安装的。

#### 4. 显示工具的具体安装路径
使用 `--show-paths` 参数：
```cmd
uv tool list --show-paths
```
输出：
```
astrbot v4.20.0 (C:\Users\Admin\AppData\Roaming\uv\tools\astrbot)
- astrbot (C:\Users\Admin\.local\bin\astrbot.exe)
```

### 最终结论
- **真实代码及虚拟环境位置**：  
  `C:\Users\Admin\AppData\Roaming\uv\tools\astrbot`  
  该目录下是一个独立的 Python 虚拟环境，包含 `astrbot` 的所有源代码和依赖。

- **启动脚本位置**：  
  `C:\Users\Admin\.local\bin\astrbot.exe`  
  该文件是 `uv` 自动生成的启动器，负责激活上述虚拟环境并运行 `astrbot`。

- **为什么 `.local\bin` 下只有四个文件？**  
  这是正常现象：`uv tool install` 仅将命令行入口放入 `.local\bin`，而包本体和依赖保存在 `uv` 的工具管理目录中，保证了环境隔离。

### 后续操作建议
- 如需查看 `astrbot` 源代码，可进入 `C:\Users\Admin\AppData\Roaming\uv\tools\astrbot\Lib\site-packages\astrbot`。
- 更新 `astrbot` 使用：`uv tool upgrade astrbot`
- 卸载 `astrbot` 使用：`uv tool uninstall astrbot`
- 不要手动修改工具目录内的文件，以免破坏工具管理。
