1.高频切换Editor为英文问题
蓝图UI_Setting_Gameplay
事件Event Pre Construct
函数Set Selected Culture -> Culture(zh-Hans)


2.打包后,设置中"中文"选项丢失的问题
工具 -> 本地化控制板 -> 语言 -> 添加新语言 -> 中文
项目设置 -> (搜索 语言) 项目 -> 打包 -> 高级 -> 要打包的语言 -> 显示本地化文本 -> 中文 (打勾)

3.切换中文后,字符丢失的问题
字体不支持中文,需要更换
将 /Script/Engine.Font'/Game/Hyper/ResourcePack/Fonts/Play/Play_Font.Play_Font'
文件删除时 替换为
orbitron 替换引用

3.
本地化控制板 -> 编译文本 -> LogLiveCoding: Display: Waiting for server 无后续反应问题

编辑器偏好设置 -> 启用实时代码编写(去掉勾)

4.
开始界面 -> 关闭未开发完成的 联网 以及 联机 功能窗口
UI_Play_With_Save -> Set Visibility(UI_Image_Button_Browse / UI_Image_Button_Host Collapsed)

5.
UI_Tooltip的详细资料中个别文本的间隙不均

create 了名为 UI_Diveider_Line蓝图 搜索后全部取消create即可

6.
关闭开局的任意键界面

UI_Startup -> Event Pre Construct 连接上 Any Key 的 Branch

7.
项目设为(默认)中文启动
UI_Setting_Gameplay 蓝图
-> Set selected Culture -> Set Current Culture(zh) -> Set Current Language(zh-Hans)
-> Save current selected settings -> Make Struct Gameplay Settings(Current Language -> zh)
-> Set Language Text -> Make String(zh) to Array -> For Each Loop with Break

将设置中的"游戏设置"移除隐藏(设置中的语言设置功能屏蔽)
UI_Settings 蓝图 
-> UI_Topbar_CommonUI_TabSwitcher -> Dynamic Creation Of Tabs -> Tabs To Construct -> UI_Setting_Gameplay (删除该元素)


8.
使用本地词库后,有七个位置没有成功汉化

-> UI_Attribute_Row -> SetColorText -> (Header)Set Text 将文本改为变量形式外显 (具体枚举方案可以直接打印)
```
Character Level
Base Damage
Critical Strike Chance
Critical Strike Multiplier
Armor Penetration Damage
Armor
Stun Damage
Range
Accuracy
Recoil
Oxygen Regeneration Rate
Oxygen Consumption Rate
Maximum Oxygen
Maximum Inventory Weight
Maximum Health
Health Regeneration Rate
Maximum Stamina
Stamina Consumption Rate
Stamina Regeneration Rate
Mana Consumption Rate
Mana Regeneration Rate
Maximum Mana
Maximum Hydration
Maximum Food
Food Consumption Rate
Maximum Energy
Energy Regeneration Rate
Energy Consumption Rate
Hydration Consumption Rate
Time Between Attacks
Area Of Effect Damage
Area Of Effect Radius
Projectile Life
Maximum Projectile Speed
Max Ammo
Initial Projectile Speed
```

-> UI_Active_Effect_Slot -> Set_Values -> State Name Text -> (State Name Text)Set Text 将文本改为变量形式外显(具体枚举方案在DT_State_Effects)
```
Healthy
Sick
Poisoned
Wounded
Fatigued
Drunk
Infected
Bleeding
VeryCold
Cold
NormalTemperature
Hot
VeryHot
OnFire
Wet
Warmed
Encumbered
LevelUp
ActiveEffects
Hungry
Thirsty
Lowenergy
LowHealth
LowOxygen
Stunned
In_Combat
Damp
```
UI_ToolTip -> Construct_TooltipContent_Atributes -> Persistant Generic Combat Attribute -> Create UI Tool Tip Row Weiget(初始化)
UI_ToolTip_Row -> Event Construct -> Switch On Enum_Tooltip_Color -> (Header Text)SetText 将文本改为变量形式外显(具体枚举方案在BFL_Attribute -> Gameplay标签 中)
```
# 1 Get Non-Persistent Character Attributes As Tag Container
Ammo
Energy
Food
Health
Hydration
Mana
Oxygen
Stamina
# 2 Get Persistent Character Attributes As Tag Container
Health Regeneration Rate
Mana Consumption Rate
Mana Regeneration Rate
Maximum Health
Maximum Inventory Weight
Maximum Mana
Maximum Oxygfn
Maximum Stamina
Oxygen Consumption Rate
Oxygfn Regeneration Rate
Stamina Consumption Rate
Stamina Regeneration Rate
# 3 Get Persistent Survival Attributes As Tag Container
Chill Temperature Penalty
Energy Consumption Rate
Energy Regeneration Rate
Food Consumption Rate
Hydration Consumption Rate
Maximum Energy
Maximum Food
Maximum Hydration
# 4 Get Persistent Generic Combat Attributes As Tag Container
Armor
Armor Penetration Damage
Base Damage
Critical Strike Chance
Critical Strike Multiplier
Stun Damage
Time Between Attacks
# 5 Get Persistent Ranged Combat Attributes As Tag Container
Accuracy
Area Of Effect Damage
Area Of Effect Radius
Initial Projectile Speed
Max Ammo
Maximum Projectile Speed
Projectile Life
Range Recoil
```

[!]
本地化控制板产生(状态)冲突,出现了哈希列表错误,例如
```
 - 03E4BC1F466CC72021629EA59F265A81 
	/Game/Hyper/UI/Widgets/Specific/Attribute/Active_State_effects/UI_Active_Effect_Slot.UI_Active_Effect_Slot_C:Set_Values [Script Bytecode] - "Healthy" 
	/Game/Hyper/UI/Widgets/Specific/Attribute/AttributeList/UI_Attribute_Row.UI_Attribute_Row_C:ExecuteUbergraph_UI_Attribute_Row [Script Bytecode] - "Character Level" 
	/Game/Hyper/UI/Widgets/Specific/Inventory/SubWidgets/Tooltip/UI_ToolTip_Row.UI_ToolTip_Row_C:ExecuteUbergraph_UI_ToolTip_Row [Script Bytecode] - "Armor" 
```
起因是复制了赋值节点之后,连带着把节点信息中的哈希内容也复制过来了,由于在不同蓝图中,运行测试的时候并没有发现异常,但在启用文本转化的时候会发现出现问题了!

重新将重叠的蓝图节点删除,(注意,不要再复制节点了!)然后重新输入新建蓝图节点即可解决

UI_Tooltip -> Construct_TooltipContent_Sellable -> Show Base Sell Price -> Format Text -> ItemName
```
将ItemName 使用 Make Literal Text -> Coins 即可(本次删除)
```

-> UI_Panel_Inventory -> 事件图表 -> Initialize Inventory 将文本改为变量形式外显(具体枚举方案需要自行输出日志获取)
```
Player Inventory
Cooking Pot
Forge
Smelter
Vendor: General Goods
Vendor: Fisher
Alchemy Lab
Workbench
Loot Bag
Small Storage Chest
Low Quality Loot Chest
Medium Quality Loot Chest
High Quality Loot Chest
```

-> UI_State_Tooltip -> Construct_TooltipContent_Generic -> State Effect -> Effect State -> State Effect Tag -> State Effect String 将文本改为变量形式外显(具体枚举方案在DT_State_Effects)
```
Healthy
Sick
Poisoned
Wounded
Fatigued
Drunk
Infected
Bleeding
VeryCold
Cold
NormalTemperature
Hot
VeryHot
OnFire
Wet
Warmed
Encumbered
LevelUp
ActiveEffects
Hungry
Thirsty
Lowenergy
LowHealth
LowOxygen
Stunned
In_Combat
Damp
```

UI_CanInteractButton -> Update_Intract_Text -> Secondary Interact Text
```
Vendor: General Goods
Vendor: Fisher
```


---

关卡
```
Map_MST_Pro - 世界场景全局
Map_MainMenu_Cave_MustPro - 开局场景菜单
```

与V2不同:
```
重生点 使用了 PlayerStart (V2使用的是蓝图以及Tag的形式定义重生位置)
添加了存档点功能(命名,额外存档等)
DT结构以及数据内容发生改动(DT_Buildables DT_Equipment DT_Items DT_Loot_Lists)
```

---

尝试迁移V2中的部分DT_Items时,出现item物品的icon异常问题(V2的Items参量 行命令 -> Generic Attributes-> Icon 所指向的纹理文件)
```
打开Icon文件
调整 -> 最小透明度 -> 1.0
调整 -> 最大透明度 -> 0.0
即可
```


---

新添功能块

添加AI丧尸多种攻击模式机制

找到DT_Items 和 DT_Equipment

新建(复制原有,并在前缀添加"AI")
```
Lengend_Balde
Lengend_Dagger
Lengend_Dual_Hatchet
Lengend_Dual_Heavy_Sword
Epic_Staff
Baseic_Dual_Sword
Legend_Light_Sword
Epic_Dual_Light_Swords
```

DT_Items
-> Coupled Equipment -> Data Table Row -> 行命令 选择(AI前缀的同名条目)

DT_Equipment 
-> Generic -> Linked Inventory Item -> 行命令 选择(AI前缀的同名条目)
-> Equip -> Static Mesh -> 清除(清空)

继承BP_AI_Basic_Combat_Male

Event:Equip
-> Target (组件AC_Equipment_Manager_Example)
-> Inventory Slot (Make Data Table Row Handle(DT_Items,(例)AIEpic_Sword) -> Make Struct Inventory Slot Item(Amout 1) -> Struct Inventory Slot Item)
 -> (Make Data Table Row Handle)

出现Slot Item为空的问题
AC_Equipment_Manager_Example -> Try Set Equipment Slot Data Automatically -> Get Inventory Manager(Is Valid)

---

装备(帽子)佩戴报错屏蔽 -> Trying to swap a master posed skeletal mesh but no master pose component is attached(试图交换主摆姿势的骨骼网格，但未附加主摆姿势组件)

由于在V3中更改了骨骼网格体,因此不会有配套的pose组件,直接移除后续后续打其他补丁即可

(可能不需要)DT_Equipment -> 目标装备 -> Equip -> Equipment Actor Class -> BP_Equipment_Base
DT_Equipment -> 目标装备 -> Equip -> Visual ammo actor socket -> (把False改成)None
DT_Equipment -> 目标装备 -> Equip -> Equip as Master Posed Skeletal Mesh -> 取消打勾(不启用即可)

并且发现 Feet_DarkBlack_Feminine参量丢失

---

累加入V2装备系统后由于装甲性别佩戴限制问题进行报错屏蔽 -> trying to equip something that is not accepted by this gender(试图给不被这个性别所接受的事物配备装备)

AC_Equipment_Manager_Advanced -> Check if equipment is accepted by your gender(pure) -> (更改为默认)True

---


ABP_Mannequin_Base -> 

Transition Drowning到Death is using an sntomatic transition rule but the source 序列播放器 'Anim_swim_choke' is set as looping. Please clear the 'Loop Animation' flag
Transition Hover_Start到Hovering is using an automatic transition rule but the source 序列播放器 'MM_Unarmed_Jump_Start' is set as looping. Please clear the 'Loop Animation' flag
-> 循环动画 -> 取消打勾
