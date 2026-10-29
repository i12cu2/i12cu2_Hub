1.
```
PackagingResults: Warning: [AssetLog]E:\MSTV3Backup\Content\Hyper\Attribute_System\Blueprints\BP_Effect_Fire.uasset：[编译器]指定非默认值的输入引脚  State Effect  已不存在于节点  Event server: Add or Remove State Effect  上。请刷新节点或重置引脚为默数值来移除引脚。
```
BP_Effect_Fire -> Event Server: Add Or Remove State Effect -> 刷新节点

2.
Unable to generate long package name, Map_Must_Example...

项目设置 -> 地图和模式 -> 默认地图 -> 高级 -> 服务器默认地图 -> 清除

3.
在特征等级SMS6 编译错误 
M_jacaranda_tree_trunk
M_Khaimera_Body 等角色材质

方案1(没有成功)
使用Nantie资产需要Shader Model 6(SM6)。

请在此启用：项目设置→平台→Windows→xxxx目标着色器格式（这步换成：SM6）

方案2(将Texture Sample) -> 对应纹理的采样器类型改成 -> 颜色 

-> SM_jacaranda_tree(可能受到影响的模型)

4.
```
LogNavigation: Warning: FNavigationOctree::AddNode: Empty bounds, ignoring ProceduralMeshComponent /Game/Hyper/MultiplayerSurvivalTemplate/Map/MST_Pro/Map_MST_Pro.Map_MST_Pro:PersistentLevel.BP_MaterialBased_ChoppableTree_Placeable_PineLarge_02_C_1450.ProceduralMesh.
```
应该是AI导航与相关蓝图(树)产生八叉树上的识别异常问题

BP_MaterialBased_ChoppableTree_Placeable_pineSmall_a -> ProceduralMesh -> 程序性网格 -> 将复杂性用作简单碰撞

5.
LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+376, getting last resort font data ../../../Engine/Content/Slate/Fonts/DroidSansFallback.ttf

U+376特殊字体出错,具体说来是字符的字体丢失

方法1(失败)
本地化控制板查找完整字符来源(搜索):�
This item seems worthless� -> DT_Items -> 173 basket -> Generic Attributes -> Description
What an amazing sword! I can feel it�s energy. -> DT_Items -> 181 Legendary_Sword_of_Minas_Anor -> Generic Attributes -> Description

方法2(成功)
将使用的字体族群调度DroidSansFallback.ttf字体

字体路径Epic Games\UE_5.6\Engine\Content\Slate\Fonts\DroidSansFallback.ttf

6.
```
PackagingResults: Warning: LoadPackage: SkipPackage: /Game/Hyper/UI/CommonUI/RichText/BP_CommonUIRichTextData (0xD21E5360647EA369) - The package to load does not exist on磁盘 or in the loader
PackagingResults: Warning: 寻找对象“Object /Game/Hyper/UI/CommonUI/RichText/BP_CommonUIRichTextData.BP_CommonUIRichTextData_C”失败
```

在对应路径新建一个对应名字的蓝图即可

7.
```
PackagingResults: Warning: [AssetLog] ...Invalid GameplayTag AnimEffect.Footstep.Land...
PackagingResults: Warning: [AssetLog] ...Invalid GameplayTag Attribute.Persistent.Character.Movement Speed...
PackagingResults: Warning: [AssetLog] ...Invalid GameplayTag Platform.Trait.CanExitApplication...
```
Tag未定义问题

# 1. 打开 GameplayTag 管理器
# 2. 添加缺失的Tag或更正拼写错误
# 正确的Tag应该像：
Attribute.Persistent.Character.MovementSpeed
Platform.Trait.CanExitApplication
AnimEffect.Footstep.Land

DT_State_Effects.uasset 中有记载使用

UATHelper: 打包 (Windows): LogInit: Display: NOTE: Only first 50 warnings displayed.
UATHelper: 打包 (Windows): LogInit: Display: Success - 0 error(s), 103 warning(s)

8.
```
PackagingResults: Warning: Unable to generate long package name, Map_MainMenu. 输入“Map_MainMenu”并非现有挂载点的子项。
PackagingResults: Warning: Unable to generate long package name, Map_Startup. 输入“Map_Startup”并非现有挂载点的子项。
（同样适用于 Map_MainMenu, Map_Startup）
```

这些地图文件不存在或路径不正确，可能已被删除或重命名

删除 /Game/Hyper/UI/Main_Menu/Map/Map_MainMenu_Cave_MustPro

9.
```
Setting the console variable 'r.VT.MaxAnisotropy' with 'SetByScalability' was ignored as it is lower priority than the previous 'SetByProjectSetting'. Value remains '4'
Setting the console variable 'r.Streaming.PoolSize' with 'SetByScalability' was ignored as it is lower priority than the previous 'SetByProjectSetting'. Value remains '12288'
```
项目设置中的值优先级高于可伸缩性设置

5.6引擎将该文件参数设置迁移到了 config/DefaultEngine.ini 文件中

把对应初始化删除即可

10.
```
PackagingResults: Warning: PoseAsset/Game/Hyper/Locomotion/Chars/Mannequin_UE5/Rig/Poses/Quinn/Quinn_upperarm_r_pose.Quinn_upperarm_r_pose已经过时，它的源动画/Game/Hyper/Locomotion/Chars/Mannequin_UE5/Rig/Poses/Quinn/Anim_Quinn_upperarm_r_anim.Anim_Quinn_upperarm_r_anim 799E453D1F53700BCBF31ADE6FE99CE5 vs 45C9349E90CE819467A6664D9F8772D6
```
打开对应资产(比如Quinn_upperarm_r_pose) -> 资产详情 -> 源 -> 更新源 -> 保存

11.
```
PackagingResults: Warning: Saving FText "" which has been initialized from FString at cook time resave of source packag
```
它表示在资源cook时，有一个空的FText被从FString初始化，这可能会导致本地化问题
```
# 重新保存所有过时的包
ResavePackages /Game/Hyper/Core/FarmingSystem/Blueprints/BP_Farming_Abstract

# 或者重新保存整个目录
ResavePackages /Game/Hyper/Core/FarmingSystem/Blueprints/
```
解决方案跳转至23

12.
```
UATHelper: 打包 (Windows): LogMaterial: Warning: [AssetLog] E:\MSTV3Backup\Content\Hyper\ResourcePack\Environments\Trees\HillTree_Bush_01\M_HillTree_Bush_01_Billboard.uasset: Failed to compile Material for platform SF_VULKAN_SM6, Default Material will be used in game.
PackagingResults: Warning: Cooking a material resource (in M_WeaponLions_SIberian2 hierarchy) that doesn't have a valid ShaderMap! Shadermap pointer is null.
```
这通常是由于材质节点配置错误或缺失输入纹理导致的。需要检查相关材质的节点配置，确保所有输入纹理和参数都正确设置

方法1(失败)
项目设置 -> 项目 -> 描述 -> 打包 -> 共享材质着色器代码 (share material shader code) -> 取消打勾

方法2(成功了一部分)
//项目设置 -> 项目 -> 描述 -> 平台 -> Windows -> D3D12 Targeted Shader Formats -> SM6 -> 取消打勾
项目设置 -> 项目 -> 描述 -> 平台 -> Windows -> Vulkan Targeted Shader Formats -> SM6 -> 取消打勾
之后会出现SM5启用失败,说明项目并不是单纯使用SM6出问题,根本问题是材质文件本身出了问题
例如
```
PackagingResults: Warning: [AssetLog] E:\MSTV3Backup\Content\Hyper\ResourcePack\Environments\Trees\HillTree_Bush_01\M_HillTree_Bush_01_Billboard.uasset: Failed to compile Material for platform PCD3D_SM5, Default Material will be used in game.
```
并且不启用之后会放弃使用nanite特性,会无法使用虚拟阴影贴图,会无法使用Nanite资产

13.
```
UATHelper: 打包 (Windows): LogMaterial: Warning: [AssetLog] E:\MSTV3Backup\Content\Hyper\ResourcePack\Environments\Trees\HillTree_Bush_01\M_HillTree_Bush_01_Billboard.uasset: Failed to compile Material for platform PCD3D_SM5, Default Material will be used in game.
PackagingResults: Warning: [AssetLog] E:\MSTV3Backup\Content\Hyper\ResourcePack\Environments\Trees\HillTree_Bush_01\M_HillTree_Bush_01_Billboard.uasset: Failed to compile Material for platform PCD3D_SM5, Default Material will be used in game.
```

SM5 -> Sampler type is 颜色,should be 线性颜色 for...

对应节点参数将颜色改成线性颜色即可

14.
```
UATHelper: 打包 (Windows): LogMaterial: Warning: [AssetLog] E:\MSTV3Backup\Content\Hyper\ResourcePack\Environments\Trees\jacaranda_tree\Material\M_jacaranda_tree_trunk_NoOffset.uasset: Failed to compile Material for platform PCD3D_SM5, Default Material will be used in game.
PackagingResults: Warning: [AssetLog] E:\MSTV3Backup\Content\Hyper\ResourcePack\Environments\Trees\jacaranda_tree\Material\M_jacaranda_tree_trunk_NoOffset.uasset: Failed to compile Material for platform PCD3D_SM5, Default Material will be used in game.
```

SM5 -> Sampler type is 线性颜色,should be 颜色 for...

逻辑同上

15.
```
LogNavigation: Warning: FNavigationOctree::AddNode: Empty bounds, ignoring ProceduralMeshComponent /Game/Hyper/MultiplayerSurvivalTemplate/Map/MST_Pro/Map_MST_Pro.Map_MST_Pro:PersistentLevel.BP_MaterialBased_ChoppableTree_Placeable_PineSmall_a_C_324.ProceduralMesh.
```
导航系统警告：空边界问题

这个警告表明导航系统尝试将一个程序化网格(ProceduralMeshComponent)添加到导航八叉树中，但由于该网格的边界(bounds)为空，系统忽略了它

打开蓝图BP_InstantBreakableTree_Master

选择Procedural Mesh(Component)

将Can Affect Navigation设为false

16.
Map_MST_Pro地图中的Landscape 地形显示出现了问题,物理效果仍旧存在,但是地面材质变成透明

抑或是移动Landscape撤销后 地形出现丢失.

打开项目config/DefaultEngine.ini文件
```
[/Script/Engine.RendererSettings]
; 将此值从 False 改为 1
r.Nanite.ProjectEnabled=1
```
根本原因：MST V3将Nanite设为地形渲染的强制依赖。当r.Nanite.ProjectEnabled=False时，拖动Landscape会触发MST的安全机制，将地形强制设为透明（防止崩溃）。

解决原理：启用Nanite(r.Nanite.ProjectEnabled=1)满足了MST的核心渲染要求，自动重置了内部状态机并恢复完整材质加载路径，无需修改其他配置。

撤销失效原因：UE5的撤销(Undo)系统只记录显式资产修改（如位置/旋转），不跟踪MST内部状态机（如bForceTransparent标志）。撤销能恢复Landscape位置，但无法重置被锁定的透明状态。

17.
打包发现画质过低问题

项目设置 -> 默认设置 -> 抗锯齿方法 -> 临时超分辨率(TSR)

18.
```
LogSkeletalMesh: Warning: Invalid material [MI_Khaimera_Beast_V2_Trail] used on Nanite skeletal mesh [SKM_Khaimera]. Only opaque or masked blend modes are currently supported, [BLEND_Translucent] blend mode was specified.
```
原因：Nanite技术目前不支持半透明(Translucent)材质用在骨骼网格上，而您的角色SKM_Khaimera使用的材质MI_Khaimera_Beast_V2_Trail是半透明的。
解决方案：

打开文件SKM_Khaimera,打开资产详情,将nanite设置关闭(记得点下方的应用设置,否则设置不生效)

19.
```
LogShaderCompilers: Warning: Failed to compile Material /Game/Hyper/ResourcePack/Weapons/Hatchet/Legend/Materials/M_Hatchet_Legend.M_Hatchet_Legend for platform PCD3D_SM6, Default Material will be used in game.
Shader is using too many SRVs: 65 (only 64 supported)
```
着色器编译失败错误:斧头材质无法正确编译,游戏运行时会使用默认灰色材质替代

解决方法:打开文件M_Hatchet_Legend删除那些没有实际效果或不重要的纹理然后保存

可到SM_Hatchet_Legend文件查看效果

20.
V2和V3工程合并历史遗留问题
| 序号 | 资产完整路径                                            | 错误类型 | 具体问题描述                                                                            |
| ---- | ------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------- |
| 1    | `/Game/Hyper/UI/Widgets/UI_ActiveEffects_List_Vertical` | 枚举无效 | `[编译器]枚举到字符串含有无效枚举值'(INVALID)'`                                         |
| 2    | `/Game/Hyper/UI/Widgets/UI_PlayerStats`                 | 节点失效 | `正在使用的引脚Current Magic已不存在于节点Mana_playerstates_hud_values上`               |
| 3    | `/Game/Hyper/UI/Widgets/UI_InGame_HUD_Advanced`         | 函数缺失 | `在'BFL_InventoryCrafting_C'中找不到名为"Get Equipment info from Inventory Slot"的函数` |
| 4    | `/Game/Hyper/UI/Widgets/UI_Inventory_Main`              | 函数缺失 | `在'BFL_InventoryCrafting_C'中找不到"Get Item Data from Slot"函数`                      |
| 5    | `/Game/Hyper/UI/Widgets/UI_Equipment_Slot`              | 引脚断裂 | `节点"Get Equipment Stats"的输出引脚"Damage"已不存在`                                   |
| 6    | `/Game/Hyper/UI/Widgets/UI_Crafting_Panel`              | 蓝图循环 | `检测到循环依赖：UI_Crafting_Recipe_Item → UI_Crafting_Panel`                           |
| 7    | `/Game/Hyper/UI/Widgets/UI_Quest_Tracker`               | 事件缺失 | `事件图表中引用了不存在的"Quest Completed"事件`                                         |

5是有的,1~7(除5)是V2特定错误,移除即可

| 文件路径                                                                | 错误类型       | 根本原因                                                                     |
| ----------------------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------- |
| `Content/Hyper/UI/Main_Menu/Settings/UI_Setting_Audio.uasset`           | 引脚类型不兼容 | `不能连接引脚 Output Get 和 Saved Settings：BP Save Settings 对象引用不兼容` |
| `Content/Hyper/UI/Main_Menu/Settings/UI_Setting_Controls.uasset`        | 引脚类型不兼容 | 同上（相同错误模式）                                                         |
| `Content/Hyper/UI/Main_Menu/Settings/UI_Setting_Gameplay.uasset`        | 引脚类型不兼容 | 同上                                                                         |
| `Content/Hyper/UI/Main_Menu/Settings/UI_Setting_Inputs_Gamepad.uasset`  | 引脚类型不兼容 | 同上                                                                         |
| `Content/Hyper/UI/Main_Menu/Settings/UI_Setting_Inputs_Keyboard.uasset` | 引脚类型不兼容 | 同上                                                                         |
| `Content/Hyper/UI/Main_Menu/Settings/UI_Setting_Video.uasset`           | 引脚类型不兼容 | 同上                                                                         |

V2的故障蓝图,屏蔽即可

```
LogBlueprint: Error: [AssetLog]...UI_InGame_Menu_Advanced_CommonUI.uasset：[编译器]从 Component 到 Target 的引脚连接无效：HUD Abstract 对象引用不兼容
LogBlueprint: Error: [AssetLog]...UI_InGame_Menu_Advanced_CommonUI.uasset：[编译器]不能连接引脚 As HUD Abstract 从扩展而生成 Get HUD 和 Target
```

V2的故障蓝图,屏蔽即可

------------------------------------------------------------------未解决------------------------------------------------------------------


21.
```
:: 在打包前执行
ren "Content\Hyper\ResourcePack\Audio\MetaSounds" _DISABLED_MetaSounds
ren "Content\Hyper\ResourcePack\Audio\Sounds" _DISABLED_Sounds
```
禁用metasound插件


22.
```
LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+376, getting last resort font data ../../../Engine/Content/Slate/Fonts/DroidSansFallback.ttf
```
目前解决方案未知

23.
```
UATHelper: 打包 (Android (ASTC)): LogInit: Display: LogText: Warning: Saving FText "" which has been initialized from FString at cook time resave of source package /Game/Hyper/Core/FarmingSystem/Blueprints/BP_Farming_Abstract may fix issue.
UATHelper: 打包 (Android (ASTC)): LogInit: Display: LogText: Warning: Saving FText "" which has been initialized from FString at cook time resave of source package /Game/Hyper/BuildingSystem/Save/Struct_Saved_Buildables may fix issue.
UATHelper: 打包 (Android (ASTC)): LogInit: Display: LogText: Warning: Saving FText "" which has been initialized from FString at cook time resave of source package /Game/Hyper/Core/AbilitySystem/Datamodel/Structures/Struct_Active_Ability may fix issue.
UATHelper: 打包 (Android (ASTC)): LogInit: Display: LogText: Warning: Saving FText "" which has been initialized from FString at cook time resave of source package /Game/Hyper/Core/FarmingSystem/Datamodel/Structures/Struct_Plant may fix issue.
```
把对应的结构体中出现的FText为空的文本改为"None"即可


------------------------------------------------------------------未解决------------------------------------------------------------------
<div>
20.
```
LogStreaming: Warning: Failed to read file '../../../Engine/Platforms/VisionOS/Content/Editor/Slate/Launcher/Platform_VisionOS_128x.png' error.
LogStreaming: Warning: Failed to read file '../../../Engine/Content/Slate/Common/ButtonHoverHint.png' error.
```
VisionOS平台资源缺失
DefaultEngine.ini文件修改
```
; ===== 1. 移除 VisionOS 作为目标平台 =====
[/Script/IOSRuntimeSettings.IOSRuntimeSettings]
MinimumiOSVersion=IOS_15
+TargetedMobilePlatforms=IOS
-TargetedMobilePlatforms=VisionOS  ; ← 关键：删除此行或注释掉
; ===== 2. 禁用 VisionOS 打包支持 =====
[/Script/UnrealEd.ProjectPackagingSettings]
bIncludeVisionOS=False  ; ← 确保为 False（若不存在则新增）
bSkipVisionOS=true      ; ← 新增：强制跳过 VisionOS
; ===== 3. 阻止引擎加载 VisionOS 模块（核心！）=====
[/Script/Engine.Engine]
-ModulesToAlwaysLoad=AppleVisionOS  ; ← 删除或注释掉此行（若存在）
```
21.
项目过大(超过2G)需要分包apk打包
| 日志内容     | 空模板成功日志     | 您的项目失败日志                               |
| ------------ | ------------------ | ---------------------------------------------- |
| 关键错误行   | 无                 | `DistributionSigning settings are not all set` |
| ExitCode     | 0 (Success)        | 1 (Error_Unknown)                              |
| 打包配置标识 | 无Shipping相关校验 | 明确触发DistributionSigning校验                |
项目设置
(搜索Distribution) -> 项目 -> 用于分布 -> 取消打勾
(搜索Chunks) -> 打包 -> 生成文件块 -> 打勾
Package game data inside .apk? -> 取消打勾
Allow large OBB files. -> 打勾
Allow patch OBB files. -> 打勾
Allow overflow OBB files. -> 打勾
Max Chunk Size Override (KB) (注意这是在Android下的) -> 2096128
22.
材质兼容问题
MI_Stairs_PInst1
M_JungleArchitecture
MI_JunglePillarBlock01A
MM_Marble_Metal_Arch
M_Khaimera_Body_SkinSnake
M_KhaimeraWeaponLionSnake
M_Khaimera_Body_Bengal
M_Khai_WeaponLions_Bengal
M_Khaimera_Body
M_WeaponLions_SIberian2
M_Khai_Body_Skin_Siberia
M_Khaimera_Body_Siberian
M_WeaponLoins_Grux2
M_Khaimera_Grux_Torso
M_Khaimera_WeaponLoins
M_Khai_ArmsLegs_Skin_Sib
M_Hatchet_Legend
M_Dagger_Legend
M_PostProcess_MovingRadialBlur_Drunk
M_PostProcess_MovingRadialBlur_Stunned
M_PostProcess_MovingRadialBlur_Poisoned
M_Bow_Legend
M_Head_Echo
23.
纹理兼容问题
```
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenDiffuseMap_VT.BaseFlattenDiffuseMap_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenDiffuseMap_VT.BaseFlattenDiffuseMap_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenEmissiveMap_VT.BaseFlattenEmissiveMap_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenEmissiveMap_VT.BaseFlattenEmissiveMap_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenGrayscaleMap_VT.BaseFlattenGrayscaleMap_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenGrayscaleMap_VT.BaseFlattenGrayscaleMap_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenLinearColor_VT.BaseFlattenLinearColor_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenLinearColor_VT.BaseFlattenLinearColor_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenNormalMap_VT.BaseFlattenNormalMap_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/BaseFlattenNormalMap_VT.BaseFlattenNormalMap_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/Black_1x1_EXR_Texture_VT.Black_1x1_EXR_Texture_VT is marked for virtual streaming but virtual texture streaming is not available.
UATHelper: 打包 (Android (ASTC)): LogTexture: Display: /Engine/EngineMaterials/Black_1x1_EXR_Texture_VT.Black_1x1_EXR_Texture_VT is marked for virtual streaming but virtual texture streaming is not available.
```
纹理 右键 -> 将虚拟纹理转换为常规纹理
</div>

