1.
[发现历史遗留问题]
运行报错:文件AC_BuildingSystem_Advanced文件出错需要修补
具体位置:搜索 Attach all parents and childs to the spawned buildables via their Global Unique IDentifier (GUID)
Local Spawned Buildables -> Attached Buildable GUIDS 连接中断
Sequence -> Then0 取消使用

原本V3版本(5.6)同样出现该问题,但未有解决,暂且屏蔽该功能

2.
```
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: Ensure condition failed: false  [File:...ConsoleManager.cpp] [Line: 4916]
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: r.Mobile.VirtualTextures is deprecated, use r.VirtualTextures in platform specific engine .ini files instead
```
打包报错:r.Mobile.VirtualTextures 已被弃用

去项目设置里取消勾选“启用虚拟纹理支持”（英文：Enable Virtual Texture Support）

3.
```
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: begin: stack for UAT
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: === Handled ensure: ===
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error:
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: Ensure condition failed: false  [File:D:\build\++UE5\Sync\Engine\Source\Runtime\Core\Private\HAL\ConsoleManager.cpp] [Line: 4916]
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: r.Mobile.VirtualTextures is deprecated, use r.VirtualTextures in platform specific engine .ini files instead
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: Stack:
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ffbe2dfcb18 UnrealEditor-Core.dll!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ffbe21481df UnrealEditor-Core.dll!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ffbe215d1c2 UnrealEditor-Core.dll!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ffbe2431fa0 UnrealEditor-Core.dll!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ffbe2411294 UnrealEditor-Core.dll!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ff7724ab893 UnrealEditor-Cmd.exe!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ff77249c263 UnrealEditor-Cmd.exe!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ff77249c5ba UnrealEditor-Cmd.exe!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ff7724a1256 UnrealEditor-Cmd.exe!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ff7724b5c74 UnrealEditor-Cmd.exe!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ff7724b838a UnrealEditor-Cmd.exe!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ffc2cb5e8d7 KERNEL32.DLL!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: [Callstack] 0x00007ffc2d45c34c ntdll.dll!UnknownFunction []
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error:
UATHelper: Error: 打包 (Windows): LogOutputDevice: Error: end: stack for UAT
```
/Config/DefaultEngine.ini 文件搜索
r.Mobile.VirtualTextures=False 这行删除

