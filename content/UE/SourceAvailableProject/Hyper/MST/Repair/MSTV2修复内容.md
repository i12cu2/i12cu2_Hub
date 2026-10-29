游戏启动场景:Map_MainMenu_Cave_MustPro
游戏核心地图:Map_MST_Pro



1.高频切换Editor为英文问题
蓝图UI_Setting_Gameplay
事件Event Pre Construct
函数Set Selected Culture
去掉即可

2.视口功能正常,打包后输入映射(Option)显示Empty,输入功能丢失的问题
由于事先使用了关方Demo导致同名项目的缓存文件产生了变动,导致缓存读取异常的问题
将C:\Users\chru\AppData\Local\MST_Pro 文件夹删除即可

3.显示中文问题:"Play_Font"字体不支持中文,更改为"RobotoTiny"等支持中文字体即可

需要更改字体的文件:

BP_Style_Text_Master
BP_Style_Text_Master_Hovered
BP_Style_Text_Master_Normal
BP_Style_Text_Master_Selected
BP_Style_Text_Master_Selected_Disabled
BP_Style_Text_Master_Selected_Hovered
BP_Style_Text_Small
Struct_UI_Style
Struct_UI_Style_Equipment

注:下方Struct文件更改之后如果直接打包项目会出现"Unknown structure."报错问题,

因此需要引用查看器访问相关启用的蓝图,

点击左上角"文件"-> 刷新所有节点 -> 编译保存

4.出现帧率偶尔骤降问题,暂且锁帧60(升级到v3可解决该问题)

5.BP_AI_Humanoid_Basic_MaleCombatZone 丢失受击反馈,启用AC_Combat_Advanced组件(原本是Basic删除)

6.屏蔽ABP_Manny报错中的Control Rig节点,可使得UE4骨骼网格体运动兼容

7.修复金项链Golden_Necklace金戒指Golden_Ring等图纸原料丢失的问题,DT_items中配方的命名错误.Crafting Attributes -> Recipe -> Item -> 行命令 Golden_Igont 改为Gold_Ingot

8.空放运行消息日志显示空指针问题,排查后发现是受伤对象在长时间待机状态变成"饥饿"的情况下造成了无目标自损情况,而原有的仇恨机制会访问受伤目标,因自伤问题无法访问施伤主体从而触发空指针访问的问题(修复为极低自损不访问施伤对象仇恨的机制)

9.调试运行后发现放置后台仍旧会造成爆内存问题(可能是引擎设置问题,暂无法定位问题)

10.继承角色蓝图类后会引发AC组件的嵌套循环生成的bug,将组件移除在子继承蓝图中构建组件可避免这个问题
