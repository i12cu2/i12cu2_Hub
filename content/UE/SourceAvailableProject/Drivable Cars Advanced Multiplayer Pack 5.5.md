
1.
UE项目打开后报错:
LoginId:09a97c9641738214a0680484b0622337
EpicAccountId:d76460e405eb4634b9e1d235aae2e93b

Assertion failed: SizeInfo.ResultSize != 0 [File:D:\build\++UE5\Sync\Engine\Source\Runtime\D3D12RHI\Private\D3D12RayTracing.cpp] [Line: 2870] 
Unexpected acceleration structure buffer size (0).
Geometry initializer details:
DebugName=PlanarReflectionPlane NumSegments=1 NumPrims=2048 IndexStride=2


UnrealEditor_D3D12RHI
UnrealEditor_D3D12RHI
UnrealEditor_RenderCore
UnrealEditor_RenderCore
UnrealEditor_RenderCore
UnrealEditor_RenderCore
UnrealEditor_Engine
UnrealEditor_Engine
UnrealEditor_Engine
UnrealEditor_Engine
UnrealEditor_Engine
UnrealEditor_CoreUObject
UnrealEditor_Engine
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_Engine
UnrealEditor_Engine
UnrealEditor_Engine
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_Engine
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor_CoreUObject
UnrealEditor
UnrealEditor
UnrealEditor
UnrealEditor
UnrealEditor
UnrealEditor
kernel32
ntdll

方法1:
Config/DefaultEngine.ini 文件末尾添加,这个方法可能会导致打包出问题
```
[SystemSettings]
r.RayTracing=0
r.ReflectionMethod=1

[/Script/WindowsTargetPlatform.WindowsTargetSettings]
DefaultGraphicsRHI=Default

[ConsoleVariables]
r.RayTracing=0
r.ReflectionMethod=1
```

方法2:
项目直接升级到5.6,目前暂无遇到相关问题

原因分析:
DirectX 12光线追踪加速结构在构建时计算出了零大小的缓冲区 D3D12RHI计算几何数据大小 → 结果为0 → 断言失败 → 引擎崩溃 


2.

该项目的汽车转轴出现了万向节死锁问题

修复方法:

蓝图BP_NewBaseVehicle -> 

EnhancedInputAction IA_VehicleCamera -> 注释Turn模块 -> (Target -> Spring Arm 改为 Cameras)Add Relative Rotation

注意,这个方案会导致C键的切换视角出现偏差问题,因而需要修正置0

EnhancedInputAction IA_ChangeCamera -> (末尾新加) Cameras -> Set Relative Rotation (X 0 Y 0 Z 0)

当然我们还需要在这里声明一个bool来存储视角状态

同样,我们回到

EnhancedInputAction IA_VehicleCamera -> 注释Turn模块 

更正为 -> 如果是第一人称 则使用最初的 Spring Arm -> Add Relative Rotation

加分支 -> 如果是第三人称 则使用最初的 Cameras -> Add Relative Rotation

# 优化手感 EnhancedInputAction IA_VehicleCamera -> 注释pitch limitation模块 -> Srping Arm -> Pitch > 0 (改为 > 10)