
character com
```
AC_Replication_SubSystem -> 网络同步中枢 负责将角色所有组件的变化状态广播给服务器及周围客户端
AC_Inventory_Advanced -> 背包数据仓库 负责管理角色背包内所有物品的增删改查与堆叠逻辑
AC_UI_Manager_Basic -> UI显示调度器 负责将各组件数据（血条、快捷栏、移动状态）绑定到屏幕控件
AC_Extended_Movement_Advanced -> 扩展运动执行器 负责冲刺/攀爬/蹲伏等复杂移动状态，并实时读取属性组件判定动作可行性
AC_Pawns_In_Radius_Advanced -> 感知探头 负责持续扫描角色周围单位，为战斗选敌与仇恨判定提供目标列表
AC_Equipment_Manager_Example -> 装备转换枢纽 负责切换武器/防具，同步修改属性组件数值并更新角色视觉挂载
AC_Attribute_Manager_Example -> 角色数值银行 负责存储与管理生命/魔力/体力等核心属性，数值变化时自动广播通知其他组件
```

controller com
```
AC_InformationPrompt_Manager -> 信息提示调度器 负责管理玩家收到的各类提示信息（任务通知/系统消息/操作反馈/弹窗警告），统一排队与显示逻辑
AC_AbilityManager_Advanced -> 技能管理中枢 负责管理角色拥有的所有技能列表，包含技能解锁/冷却/等级/切换等状态，并作为技能触发的前置调度器
```


-------------


动作模板
Map_Example_Ability_System -> AbilitySystem V3 map
BP_GameMode_AbilitySystem -> GameMode
BP_Character_AbilitySystem -> Chara
```
    -> AC_Replication_SubSystem -> 复制子系统组件，用于集中管理该角色所有需要网络同步的属性和事件，确保多人环境下数据一致性。
    -> AC_Inventory_Advanced -> 高级库存组件，用于管理角色背包中的物品槽位，支持物品的添加、移除、交换、堆叠、重量计算，以及物品数据的持久化存储。
    -> AC_UI_Manager_Basic -> 基础UI管理器组件，用于管理角色相关UI界面的打开、关闭、刷新和层级控制，属于轻量级UI控制器。
    -> AC_Extended_Movement_Advanced -> 高级扩展移动组件，用于增强角色的移动能力，支持滑铲、攀爬、翻越、蹲伏、冲刺等高级动作及动画状态切换。
    -> AC_Pawns_In_Radius_Advanced -> 高级范围内Pawn检测组件，用于持续检测角色周围一定半径内的其他Pawn，支持筛选阵营、类型，提供进入/离开范围的事件通知。
    -> AC_Attribute_Manager_Example -> 示例属性管理器组件，用于管理角色的基础属性（生命、耐力等），提供属性增减、回复的示例实现，结构较简洁，适合作为自定义属性系统的起点模板。
    -> AC_Equipment_Manager_Example -> 示例装备管理器组件，用于处理角色装备的穿戴/卸下，管理装备插槽的基础逻辑，结构较简洁，适合作为自定义装备系统的起点模板。
        AC_Attribute_Manager_Example <- 原为 AC_Attribute_Manager_Advanced
        -> 从“高级属性管理器”降级为“示例属性管理器”，功能从完整生存属性系统变为基础属性示例模板
        AC_Equipment_Manager_Example <- 原为 AC_Equipment_Manager_Advanced
        -> 从“高级装备管理器”降级为“示例装备管理器”，功能从完整装备插槽/显示/属性加成系统变为基础装备示例模板
```
HUD_AutoCreate -> HUD
BP_PlayerController_Ability_System -> controller
    -> AC_InformationPrompt_Manager -> com
    -> AC_AbilityManager_Advanced -> com
BP_GameState_AbilitySystem -> State 游戏状态类
    -> AC_GameState_TagMapper_Ability -> com
    -> AC_GameState_TagMapper_Items -> com


---------

MST模板
Map_MainMenu_Cave_MustPro 游戏默认菜单地图
Map_Example_AutoLandscape -> MST Task Map 编辑器开始地图 车载地图
BP_MovementTask -> GameMode
```
    -> AC_GameMode_SaveManager -> 游戏模式保存管理器组件，用于管理游戏全局存档的读写逻辑，触发自动保存/手动保存，管理每个玩家的存档数据、世界状态序列化，以及存档文件的创建、加载和删除。
    -> AC_Respawn_Handler -> 重生处理器组件，用于管理玩家死亡后的重生逻辑，包括选择重生点（最近的床/出生点/队友附近）、管理重生冷却时间、处理多人模式下的队伍复活机制，以及重生时的物品保留规则。
    -> AC_ItemAllocationGenerator_GameMode -> 游戏模式物品分配生成器组件，用于为战利品箱、供应商、资源点等生成物品分配方案，基于概率表、稀有度权重、玩家等级动态计算掉落物品，确保战利品产出的平衡性和随机性。
```
BP_Basic_Character_Female_Echo_MST_Pro -> Chara
```
    -> AC_Interact_Advanced -> 高级交互组件，用于处理玩家与世界中物体的交互（按E键、长按、距离检测、视线检测），管理交互提示的显示与隐藏。
    -> AC_Footsteps_Advanced -> 高级脚步声组件，用于根据玩家移动速度、地面物理材质播放不同的脚步声效，支持第一人称与第三人称切换。
    -> AC_Attribute_Manager_Advanced -> 高级属性管理器组件，用于管理角色的生命值、耐力、饥饿、口渴等核心生存属性，处理属性增减、回复、上限修改及属性变化事件的广播。
    -> AC_Inventory_Advanced -> 高级库存组件，用于管理角色背包中的物品槽位，支持物品的添加、移除、交换、堆叠、重量计算，以及物品数据的持久化存储。
    -> AC_Pawns_In_Radius_Advanced -> 高级范围内Pawn检测组件，用于持续检测角色周围一定半径内的其他Pawn，支持筛选阵营、类型，提供进入/离开范围的事件通知。
    -> AC_Swimming_Advanced -> 高级游泳组件，用于控制角色在水中的浮力、游泳速度、耐力消耗、潜水深度，以及水面溅水特效和换气逻辑。
    -> AC_BuildingSystem_Advanced -> 高级建筑系统组件，用于处理玩家放置建筑构件的逻辑，包括预览、对齐、合法性检测（支撑/重叠/权限）、资源扣除和网络同步。
    -> AC_Farming_Advanced -> 高级农业系统组件，用于管理角色的农耕操作（播种、浇水、施肥、收割），跟踪作物生长阶段，处理土壤状态和产量计算。
    -> AC_Vendor_Advanced -> 高级供应商组件，用于处理玩家与NPC商店的交易逻辑，包括打开交易UI、物品买卖、价格计算、库存刷新。
    -> AC_Outliner_Advanced -> 高级轮廓绘制组件，用于控制选中物体的高亮描边效果，支持自定义颜色、闪烁频率和描边粗细。
    -> AC_UI_Manager_Basic -> 基础UI管理器组件，用于管理角色相关UI界面的打开、关闭、刷新和层级控制，属于轻量级UI控制器。
    -> AC_Extended_Movement_Advanced -> 高级扩展移动组件，用于增强角色的移动能力，支持滑铲、攀爬、翻越、蹲伏、冲刺等高级动作及动画状态切换。
    -> AC_Ragdoll -> 布娃娃组件，用于控制角色在受击、死亡时切换为物理模拟状态，处理碰撞响应、肢体约束和与场景物体的物理交互。
    -> AC_Replication_SubSystem -> 复制子系统组件，用于集中管理该角色所有需要网络同步的属性和事件，确保多人环境下数据一致性。
    -> AC_Crafting_Advanced -> 高级制作组件，用于处理玩家在制作台或随身制作中的配方匹配、材料消耗、成品生成，以及制作时间/队列管理。
    -> AC_Hotbar_Advanced -> 高级快捷栏组件，用于管理角色的快捷栏物品槽位，支持物品的快捷使用、槽位切换（数字键）、冷却显示和数量更新。
    -> AC_Equipment_Manager_Advanced -> 高级装备管理器组件，用于处理角色装备的穿戴/卸下，管理装备插槽，控制装备的显示隐藏和属性加成应用。
    -> AC_Voice -> 声音组件，用于控制角色发出的语音，支持3D空间定位播放，配合语音管理器根据角色性别/类型自动匹配音色。
    -> AC_WorldDialogue_Manager -> 世界对话管理器组件，用于触发和播放角色与NPC之间的对话，管理对话树状态、分支选择，以及对话中的摄像机切换和动画同步。
    -> AC_Fishing_Advanced -> 高级钓鱼组件，用于管理钓鱼小游戏的完整流程（抛竿、等待咬钩、收线QTE、鱼挣扎），根据水域类型和鱼饵计算渔获品质。
    -> AC_InventoryLootBagSpawner -> 库存战利品袋生成器组件，用于在角色/敌人死亡时根据其库存内容生成可交互的战利品袋实例放置在世界中供其他玩家拾取。
```
HUD_AutoCreateWithSettings -> HUD
BP_PlayerController_MSTPro -> controller 
    -> AC_InformationPrompt_Manager -> com
    -> AC_AbilityManager_Advanced -> com **新添加 来自ability system**
    -> AC_PlayerController_SaveManager -> com
BP_GameState_MST_Pro -> State 游戏状态类
    -> AC_GameState_TagMapper_Recipes -> com
    -> AC_GameState_TagMapper_Ability -> com **新添加 来自ability system**
    -> AC_GameState_TagMapper_Items -> com

