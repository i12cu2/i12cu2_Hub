更新日志

Adventure_Pack -> 骨骼替换至BP_Basic_Character_Female_Echo_MST_Pro以供使用
CemeteryFullPack ->放置AI攻击状态 适配了BP_Respawn_Location_OpenWorld出生点
FluidNinjaLive -> 默认完美迁移 暂且不用
LowPolyRainforest -> 热带雨林情况暂且不用
ZombiePackV1 -> 构建DT_items和DT_Equipment (武器隐藏)AI_Enum 以供 ZombiePack使用 NewBP_AI_Humanoid_Basic_MaleCombatZone是表现内容 
Hyper MST Pro V2 ->将所有相关枚举窗口等风格方式更换成了RobotoTiny,由于部分widget强关联Play_Font,因而将强制SetFont全部取消切换为RT
更换强制启用编辑器英文的问题(强制更换为中文) 将"本地化控制板"完整适配中英文切换
出现帧率偶尔骤降问题,暂且锁帧60
扩展DT_items(AI武器镜像) 调整部分子弹叠加上限 
扩展DT_Equipment(AI攻击模式) 
扩展DT_Loot_Lists(宝箱物品刷新内容)
修改BP_Basic_Character_Female_Echo_MST_Pro 骨骼网格体 以及 组件AC_Hotbar_Advanced(快捷栏内容) 以及 AC_Inventory_Advanced(背包子弹编辑)
修复金项链Golden_Necklace金戒指Golden_Ring等图纸原料丢失的问题,DT_items中配方的命名错误.Crafting Attributes -> Recipe -> Item -> 行命令 Golden_Igont 改为Gold_Ingot
出现中文适配问题:目标信息UI_Tooltip需要对其单独进行Switch分支,写在了UI_Tooltip -> Construct Recipe UI Rows Based On Array -> Collapse Graph ->Temp Text Switch On String 使用文本定义之后可在本地化控制板中识别出来从而达到言语切换
构建NewBP_AI_Humanoid_Basic_MaleCombatZone 启用了AC_Combat_Advanced(原本是Basic丢失受击反馈) 更改为ZombiePackV1 8大攻击方式7大人物模组随机切换
屏蔽ABP_Manny报错中的Control Rig节点,可使得UE4骨骼网格体运动兼容
功能UI_Credits隐藏于UI_MainMenu_home-> Event Construct -> UI Button Master Credits -> Set visibility Collapsed
导航系统警告：空边界问题 -> 蓝图BP_MaterialBased_ChoppableTree_Placeable_PineSmal等树蓝图 选择Procedural Mesh(Component) 将Can Affect Navigation设为false
修复Echo人物与HairGroom头发组件动画协调问题
Survival_Character和Adventure_Pack模块因为兼容问题移除(UE5.6断言导致程序崩溃
由于打包会出错,因此对BP_Basic_Character_Female_Echo_MST_Pro蓝图的AC_Respawn_Manager_OpenWorld组件进行删除(后续在蓝图的继承子蓝图中添加该组件即可,这条没用上...
注意AC_Respawn_Handler蓝图组件中Spawn Player分支中的SpawnActor发生改动:强制其以Gamemode中的Pawn类为设定,避免改动人物蓝图后造成出错问题(注意要添加对应的22个组件
为项目添加Metahumans项目,包含11个具体人物以及一个通用人物组件,将Metahuman继承前者的Echo尝试编辑可定义人物模型
BP_Teuthisan -> AnyDamage 怪兽处于饥饿状态会有 空Instigated By对象,访问时会报空指针错误


兼容失败
强行兼容UniversalCharacterCustomi失败,人物模型出现错配问题,手臂发生异常形变
尝试兼容XandraCharacterCreator(5.6)失败,人物(可能是骨骼也可能是蓝图框架)有巨大的差异

2026.3

加入CarSystem模块报错 -> 添加插件ChaosVehiclesPlugins (City_Traffic_Pro/DD_Vehicles_Advanced/EasyRain/Helicopter/BikeControlPlugin等模块组合)
TimeManagerSystemV3/AutoLandscapeMaterialV3 模块 -> 相关文档不赘述
FluidNinja LIVE 1.9.54.4/Fluid Ninja VFX Tools_v1.8.54.1 模块 -> 相关文档不赘述
放弃Android打包方案

DD_Vehicles_Advanced 兼容失败移除

暂时这样吧 2026.4.30

缺少: AbilitySystem V3 等

开发日志 2026.7.23 起