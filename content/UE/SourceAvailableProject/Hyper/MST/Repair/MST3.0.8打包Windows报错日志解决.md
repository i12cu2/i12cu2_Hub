1.
屏蔽报错(这是编译报错,就不介绍起因了) (预估这些是移植兼容MST_V2的时候没有清除的缓存项,避免出错先不删除)
/All/Game/Hyper/UI/Widgets/Specific/Attribute/Active_State_effects/UI_ActiveEffects_List_Vertical
/All/Game/Hyper/UI/Widgets/Specific/Attribute/PlayerStats/UI_PlayerStats
/All/Game/Hyper/UI/Widgets/Main_Widgets/UI_InGame_HUD_Advanced
/All/Game/Hyper/UI/Widgets/Main_Widgets/UI_InGame_Menu_Advanced_CommonUI
/All/Game/Hyper/UI/Main_Menu/Settings/UI_Setting_Audio
/All/Game/Hyper/UI/Main_Menu/Settings/UI_Setting_Controls
/All/Game/Hyper/UI/Main_Menu/Settings/UI_Setting_Gameplay
/All/Game/Hyper/UI/Main_Menu/Settings/UI_Setting_Inputs_Gamepad
/All/Game/Hyper/UI/Main_Menu/Settings/UI_Setting_Inputs_Keyboard
/All/Game/Hyper/UI/Main_Menu/Settings/UI_Setting_Video

2.
```
PackagingResults: Warning: Script call stack:
PackagingResults: Warning: Script Msg: Attempted to set an invalid index on array MaterialsRef [-1/1]!
PackagingResults: Warning: Script call stack:
PackagingResults: Warning: Script Msg: Attempted to set an invalid index on array MaterialsRef [-1/3]!
PackagingResults: Warning: Script call stack:
```
/All/Game/DD_Vehicles_Advanced/Blueprints/Vehicles/BP_NewBaseVehicle蓝图
-> BP_NewBase_Vehicle -> Save Mats On Pieces -> PaintDestructiblePieces
CheckInheritMainMaterial 后面的Get Material Slot Names 中Find出现的越界问题(没找到所以是显示-1访问报错)
用branch 跳过FIND -1结果即可

3.
```
PackagingResults: Warning: Scale for /Game/FluidNinja/Levels/Usecases11_VolumeGeneric_Medium.Usecases11_VolumeGeneric_Medium:PersistentLevel.MovingBall5_7.Sphere has a component set to zero, which will result in a bad body instance. Scale:X=0.000 Y=0.000 Z=0.000
PackagingResults: Warning: Initialising Body : Scale3D is (nearly) zero: MovingBall5_7 /Game/FluidNinja/Levels/Usecases11_VolumeGeneric_Medium.Usecases11_VolumeGeneric_Medium:PersistentLevel.MovingBall5_7.Sphere
PackagingResults: Warning: Scale for /Game/FluidNinja/Levels/Usecases11_VolumeGeneric_Medium.Usecases11_VolumeGeneric_Medium:PersistentLevel.MovingBall5_7.Sphere has a component set to zero, which will result in a bad body instance. Scale:X=0.000 Y=0.000 Z=0.000
PackagingResults: Warning: Initialising Body : Scale3D is (nearly) zero: MovingBall5_7 /Game/FluidNinja/Levels/Usecases11_VolumeGeneric_Medium.Usecases11_VolumeGeneric_Medium:PersistentLevel.MovingBall5_7.Sphere
PackagingResults: Warning: Scale for /Game/FluidNinja/Levels/Usecases11_VolumeGeneric_Medium.Usecases11_VolumeGeneric_Medium:PersistentLevel.MovingBall5_7.Sphere has a component set to zero, which will result in a bad body instance. Scale:X=0.000 Y=0.000 Z=0.000
PackagingResults: Warning: Initialising Body : Scale3D is (nearly) zero: MovingBall5_7 /Game/FluidNinja/Levels/Usecases11_VolumeGeneric_Medium.Usecases11_VolumeGeneric_Medium:PersistentLevel.MovingBall5_7.Sphere
```
Usecases11_VolumeGeneric_Medium关卡
找到MovingBall5_7删除即可

4.
/All/Game/Hyper/ResourcePack/Weapons/Hatchet/Legend/Materials/M_Hatchet_Legend
/All/Game/Hyper/ResourcePack/Weapons/Daggers/Legend/Materials/M_Dagger_Legend
节点过多导致,去掉部分background即可

5.
```
PackagingResults: Warning: [AssetLog] D:\0code\MST3P\Content\FluidNinja\Usecases\ParallaxMapping\TempMaterials\M_FlipBookPreview1.uasset: Failed to compile Material for platform PCD3D_SM5, Default Material will be used in game.
PackagingResults: Warning: [AssetLog] D:\0code\MST3P\Content\FluidNinja\Usecases\ParallaxMapping\TempMaterials\M_FlipBookPreview1.uasset: Failed to compile Material for platform PCD3D_SM6, Default Material will be used in game.
PackagingResults: Warning: Cooking a material resource (in M_FlipBookPreview1 hierarchy) that doesn't have a valid ShaderMap! Shadermap pointer is null.
PackagingResults: Warning: Cooking a material resource (in M_FlipBookPreview1 hierarchy) that doesn't have a valid ShaderMap! Shadermap pointer is null.
LogMaterial: Warning: [AssetLog] D:\0code\MST3P\Content\FluidNinja\Usecases\ParallaxMapping\TempMaterials\M_FlipBookPreview1.uasset: Failed to compile Material for platform PCD3D_SM6, Default Material will be used in game.
```
/All/Game/FluidNinja/Usecases/ParallaxMapping/TempMaterials/M_FlipBookPreview1
/All/Game/FluidNinja/Usecases/ParallaxMapping/TempMaterials/M_FlipBookPreview3
采样器类型->颜色

6.
```
PackagingResults: Warning: [AssetLog]D:\0code\MST3P\Content\FluidNinja\Core\BP_ResetEditorViewport.uasset：[编译器]指定非默认值的输入引脚  Class Name  已不存在于节点  按类获取资产  上。请刷新节点或重置引脚为默数值来移除引脚。
```
/All/Game/FluidNinja/Core/BP_ResetEditorViewport
-> Construction Script -> Get Assets by Class -> Class Name -> 右键 重置为默认值

7.
```
PackagingResults: Warning: [AssetLog]D:\0code\MST3P\Content\FluidNinja\Core\BP_ResetEditorViewport.uasset：[编译器]设置关卡视口摄像机信息 ：“设置关卡视口摄像机信息”的使用已废弃。The Editor Scripting Utilities Plugin is deprecated - Use the function in Unreal Editor Subsystem
```
/All/Game/FluidNinja/Core/BP_ResetEditorViewport
搜索节点 Set Level Viewport Camera Info 删除使用

8.
```
PackagingResults: Warning: [AssetLog] D:\0code\MST3P\Content\Hyper\ResourcePack\Environments\Trees\ScotsPine_01\ScotsPineSpline\M_ScotsPineSpline_Leaves.uasset: Failed to compile Material for platform PCD3D_SM5, Default Material will be used in game.
PackagingResults: Warning: [AssetLog] D:\0code\MST3P\Content\Hyper\ResourcePack\Environments\Trees\ScotsPine_01\ScotsPineSpline\M_ScotsPineSpline_Leaves.uasset: Failed to compile Material for platform PCD3D_SM6, Default Material will be used in game.
PackagingResults: Warning: Cooking a material resource (in M_ScotsPineSpline_Leaves hierarchy) that doesn't have a valid ShaderMap! Shadermap pointer is null.
PackagingResults: Warning: Cooking a material resource (in M_ScotsPineSpline_Leaves hierarchy) that doesn't have a valid ShaderMap! Shadermap pointer is null.
```
/All/Game/Hyper/ResourcePack/Environments/Trees/ScotsPine_01/ScotsPineSpline/M_ScotsPineSpline_Leaves
/All/Game/Hyper/ResourcePack/Environments/Trees/ScotsPine_01/ScotsPineSpline/M_ScotsPineSpline_Leaves_Mat
-> 左上Texture Sample -> 采样器类型 -> 线性颜色
-> 右下Texture Sample -> 采样器类型 -> 虚拟法线

9.
```
PackagingResults: Warning: [AssetLog]D:\0code\MST3P\Content\DD_Vehicles_Advanced\Blueprints\GameStates\BP_NetGameState.uasset：[编译器]基于C++父类 /Script/Engine.GameState 的蓝图不允许使用  事件Tick ，因此它将不会Tick！
PackagingResults: Warning: [AssetLog]D:\0code\MST3P\Content\DD_Vehicles_Advanced\Blueprints\GameStates\BP_NetGameState.uasset：[编译器]解决此问题的几种办法：
PackagingResults: Warning: [AssetLog]D:\0code\MST3P\Content\FluidNinja\BP_FluidNinja.uasset：[编译器]基于C++父类 /Script/Blutility.EditorUtilityActor 的蓝图不允许使用  事件Tick ，因此它将不会Tick！
```
使用节点set timer by event (事件连接到Begin event初始化),自定义函数引用事件行为

10.
```
UATHelper: 打包 (Windows): LogBlueprint: Warning: [AssetLog]D:\0code\MST3P\Content\FluidNinja\BP_FluidNinja.uasset：[编译器]基于C++父类 /Script/Blutility.EditorUtilityActor 的蓝图不允许使用  事件Tick ，因此它将不会Tick！
PackagingResults: Warning: [AssetLog]D:\0code\MST3P\Content\FluidNinja\BP_FluidNinja.uasset：[编译器]基于C++父类 /Script/Blutility.EditorUtilityActor 的蓝图不允许使用  事件Tick ，因此它将不会Tick！
UATHelper: 打包 (Windows): LogBlueprint: Warning: [AssetLog]D:\0code\MST3P\Content\FluidNinja\BP_FluidNinja.uasset：[编译器]解决此问题的几种办法：
UATHelper: 打包 (Windows):   1)使用Timer，不使用Tick。
UATHelper: 打包 (Windows):   2)在父C++类中添加元=（ChildCanTick）
UATHelper: 打包 (Windows):   3)重设蓝图父项到AActor或UActorComponent中（其可随时tick）。
PackagingResults: Warning: [AssetLog]D:\0code\MST3P\Content\FluidNinja\BP_FluidNinja.uasset：[编译器]解决此问题的几种办法：
```
使用节点set timer by event  用来代替Event Tick
Float触发Tick 默认为0.0167(秒,60帧)

11.
```
UATHelper: 打包 (Windows): LogPhysics: Warning: Scale for /Game/FluidNinja/Levels/Usecases11_VolumeGeneric_Medium.Usecases11_VolumeGeneric_Medium:PersistentLevel.MovingBall5_7.Sphere has a component set to zero, which will result in a bad body instance. Scale:X=0.000 Y=0.000 Z=0.000
UATHelper: 打包 (Windows): LogPhysics: Warning: Initialising Body : Scale3D is (nearly) zero: MovingBall5_7 /Game/FluidNinja/Levels/Usecases11_VolumeGeneric_Medium.Usecases11_VolumeGeneric_Medium:PersistentLevel.MovingBall5_7.Sphere
```
/Game/FluidNinja/Levels/Usecases11_VolumeGeneric_Medium关卡
搜索MovingBall5_7,将Scale 改为1,1,1




修复失败:
```
PackagingResults: Warning: 插槽节点：动画实例类ABP_Mannequin_Base_C中已存在“DefaultSlot”。从此类的动画图表中删除重复项。
PackagingResults: Warning: 插槽节点：动画实例类ABP_Mannequin_Base_C中已存在“FullBody”。从此类的动画图表中删除重复项。
```
/All/Game/Hyper/Locomotion/Chars/Mannequin_UE5/Anims/ABP_Mannequin_Base
搜索DefaultSlot和FullBody丢掉一个其中的,发现动画会出现半身停滞
