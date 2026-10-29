1.
```
PackagingResults: Error: Fatal error: [File:D:\build\++UE5\Sync\Engine\Source\Runtime\Engine\Private\ShaderCompiler\ShaderCompilerUtil.cpp] [Line: 70]
PackagingResults: Error: Corrupted ShaderCompileWorker output file
PackagingResults: Error: File path: "C:/Users/Admin/AppData/Local/Temp/UnrealShaderWorkingDir/.../WorkerOutputOnly.out"
PackagingResults: Error: Expecting single job header ID 0x00000053, got 0x00000000 instead!
PackagingResults: Error: Crash in runnable thread ShaderCompilingThread
PackagingResults: Error: Unknown Cook Failure
```
文件损坏.根目录清除缓存重新打包即可

2.
```
PackagingResults: Error: SCW 10 Queued Jobs, Finished 10 single jobs
PackagingResults: Error: Job 0 [Single] Failed: M_InternalShapeGlow_425af4066f1ff99b/Default/FNaniteVertexFactory/TBasePassCSFPrecomputedVolumetricLightmapLightingPolicySkylight/0:/Engine/Private/BasePassPixelShader.usf|MainCS VF 'FNaniteVertexFactory' Type 'TBasePassCSFPrecomputedVolumetricLightmapLightingPolicySkylight' '/Engine/Private/BasePassPixelShader.usf' Entry 'MainCS' Permutation 0
PackagingResults: Error: Job 1 [Single] Failed: M_Bubble_56277636d8a5ed4c/Default/FParticleSpriteVertexFactory/TBasePassPSFNoLightMapPolicySkylight/0:/Engine/Private/BasePassPixelShader.usf|MainPS VF 'FParticleSpriteVertexFactory' Type 'TBasePassPSFNoLightMapPolicySkylight' '/Engine/Private/BasePassPixelShader.usf' Entry 'MainPS' Permutation 0
PackagingResults: Error: Job 2 [Single] Failed: M_tree-rings-wood-log_b56fb390f78d988e/Default/TGPUSkinVertexFactoryDefault/TBasePassVSFPrecomputedVolumetricLightmapLightingPolicy/0:/Engine/Private/BasePassVertexShader.usf|Main VF 'TGPUSkinVertexFactoryDefault' Type 'TBasePassVSFPrecomputedVolumetricLightmapLightingPolicy' '/Engine/Private/BasePassVertexShader.usf' Entry 'Main' Permutation 0
PackagingResults: Error: Job 3 [Single] Failed: M_LightDart_RadialBlur_40b5254c823478e8/Default/FLocalVertexFactory/FLumenCardVS/0:/Engine/Private/Lumen/LumenCardVertexShader.usf|Main VF 'FLocalVertexFactory' Type 'FLumenCardVS' '/Engine/Private/Lumen/LumenCardVertexShader.usf' Entry 'Main' Permutation 0
PackagingResults: Error: Job 4 [Single] Failed: M_SoundRipple_205309661d597c60/Default/FNiagaraSpriteVertexFactory/FDistortionMeshPS/0:/Engine/Private/DistortAccumulatePS.usf|Main VF 'FNiagaraSpriteVertexFactory' Type 'FDistortionMeshPS' '/Engine/Private/DistortAccumulatePS.usf' Entry 'Main' Permutation 0
PackagingResults: Error: Job 5 [Single] Failed: M_SoundRipple_205309661d597c60/Default/FNiagaraSpriteVertexFactory/TBasePassPSFCachedPointIndirectLightingPolicySkylight/0:/Engine/Private/BasePassPixelShader.usf|MainPS VF 'FNiagaraSpriteVertexFactory' Type 'TBasePassPSFCachedPointIndirectLightingPolicySkylight' '/Engine/Private/BasePassPixelShader.usf' Entry 'MainPS' Permutation 0
PackagingResults: Error: Job 6 [Single] Failed: M_Fur_ff16866d62c81566/Low/FNaniteVertexFactory/TBasePassCSTDistanceFieldShadowsAndLightMapPolicyHQSkylight/0:/Engine/Private/BasePassPixelShader.usf|MainCS VF 'FNaniteVertexFactory' Type 'TBasePassCSTDistanceFieldShadowsAndLightMapPolicyHQSkylight' '/Engine/Private/BasePassPixelShader.usf' Entry 'MainCS' Permutation 0
PackagingResults: Error: Job 7 [Single] Failed: M_Fur_ff16866d62c81566/Low/FLocalVertexFactory/TShadowDepthVSVertexShadowDepth_PerspectiveCorrect/0:/Engine/Private/ShadowDepthVertexShader.usf|Main VF 'FLocalVertexFactory' Type 'TShadowDepthVSVertexShadowDepth_PerspectiveCorrect' '/Engine/Private/ShadowDepthVertexShader.usf' Entry 'Main' Permutation 0
PackagingResults: Error: Job 8 [Single] Failed: M_Fur_ff16866d62c81566/Low/FLocalVertexFactory/TBasePassPSFNoLightMapPolicySkylight/0:/Engine/Private/BasePassPixelShader.usf|MainPS VF 'FLocalVertexFactory' Type 'TBasePassPSFNoLightMapPolicySkylight' '/Engine/Private/BasePassPixelShader.usf' Entry 'MainPS' Permutation 0
PackagingResults: Error: Job 9 [Single] Failed: M_Fur_ff16866d62c81566/Low/FHWRasterizePS/130:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizePS Type 'FHWRasterizePS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizePS' Permutation 130
PackagingResults: Error: ShaderCompileWorker failed
PackagingResults: Error: SCW 10 Queued Jobs, Finished 10 single jobs
PackagingResults: Error: Job 0 [Single] Failed: M_tree-rings-wood-log_2cbb65f97cfd2414/Default/FLocalVertexFactory/TBasePassPSFCachedPointIndirectLightingPolicy/0:/Engine/Private/BasePassPixelShader.usf|MainPS VF 'FLocalVertexFactory' Type 'TBasePassPSFCachedPointIndirectLightingPolicy' '/Engine/Private/BasePassPixelShader.usf' Entry 'MainPS' Permutation 0
PackagingResults: Error: Job 1 [Single] Failed: M_Dirt_29c87b6c0f309d00/Default/FHWRasterizeVS/145:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizeVS Type 'FHWRasterizeVS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizeVS' Permutation 145
PackagingResults: Error: Job 2 [Single] Failed: M_Plain_Color_ff2c65a8c7d93976/Default/FInstancedStaticMeshVertexFactory/TBasePassPSFCachedVolumeIndirectLightingPolicySkylight/0:/Engine/Private/BasePassPixelShader.usf|MainPS VF 'FInstancedStaticMeshVertexFactory' Type 'TBasePassPSFCachedVolumeIndirectLightingPolicySkylight' '/Engine/Private/BasePassPixelShader.usf' Entry 'MainPS' Permutation 0
PackagingResults: Error: Job 3 [Single] Failed: M_SoundRipple_205309661d597c60/Default/FNiagaraSpriteVertexFactory/TBasePassPSFNoLightMapPolicySkylight/0:/Engine/Private/BasePassPixelShader.usf|MainPS VF 'FNiagaraSpriteVertexFactory' Type 'TBasePassPSFNoLightMapPolicySkylight' '/Engine/Private/BasePassPixelShader.usf' Entry 'MainPS' Permutation 0
PackagingResults: Error: Job 4 [Single] Failed: M_Fur_ff16866d62c81566/Low/FLocalVertexFactory/FHitProxyVS/0:/Engine/Private/HitProxyVertexShader.usf|Main VF 'FLocalVertexFactory' Type 'FHitProxyVS' '/Engine/Private/HitProxyVertexShader.usf' Entry 'Main' Permutation 0
PackagingResults: Error: Job 5 [Single] Failed: M_Fur_ff16866d62c81566/Low/FMicropolyRasterizeCS/65:/Engine/Private/Nanite/NaniteRasterizer.usf|MicropolyRasterize Type 'FMicropolyRasterizeCS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'MicropolyRasterize' Permutation 65
PackagingResults: Error: Job 6 [Single] Failed: M_Fur_ff16866d62c81566/Low/FMicropolyRasterizeCS/89:/Engine/Private/Nanite/NaniteRasterizer.usf|MicropolyRasterize Type 'FMicropolyRasterizeCS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'MicropolyRasterize' Permutation 89
PackagingResults: Error: Job 7 [Single] Failed: M_Fur_ff16866d62c81566/Low/FMicropolyRasterizeCS/93:/Engine/Private/Nanite/NaniteRasterizer.usf|MicropolyRasterize Type 'FMicropolyRasterizeCS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'MicropolyRasterize' Permutation 93
PackagingResults: Error: Job 8 [Single] Failed: M_Fur_ff16866d62c81566/Low/FHWRasterizePS/138:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizePS Type 'FHWRasterizePS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizePS' Permutation 138
PackagingResults: Error: Job 9 [Single] Failed: M_Fur_ff16866d62c81566/Low/FHWRasterizePS/163:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizePS Type 'FHWRasterizePS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizePS' Permutation 163
PackagingResults: Error: ShaderCompileWorker failed
PackagingResults: Error: SCW 10 Queued Jobs, Finished 10 single jobs
PackagingResults: Error: Job 0 [Single] Failed: M_Fur_effe6671f6019635/Default/FHWRasterizePS/177:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizePS Type 'FHWRasterizePS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizePS' Permutation 177
PackagingResults: Error: Job 1 [Single] Failed: M_Fur_effe6671f6019635/Default/FHWRasterizePS/185:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizePS Type 'FHWRasterizePS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizePS' Permutation 185
PackagingResults: Error: Job 2 [Single] Failed: M_Fern_01_1ffb0f638ad8b518/Default/FInstancedStaticMeshVertexFactory/FLumenCardVS/0:/Engine/Private/Lumen/LumenCardVertexShader.usf|Main VF 'FInstancedStaticMeshVertexFactory' Type 'FLumenCardVS' '/Engine/Private/Lumen/LumenCardVertexShader.usf' Entry 'Main' Permutation 0
PackagingResults: Error: Job 3 [Single] Failed: M_Fern_01_1ffb0f638ad8b518/Default/FInstancedStaticMeshVertexFactory/TBasePassPSFPrecomputedVolumetricLightmapLightingPolicy/0:/Engine/Private/BasePassPixelShader.usf|MainPS VF 'FInstancedStaticMeshVertexFactory' Type 'TBasePassPSFPrecomputedVolumetricLightmapLightingPolicy' '/Engine/Private/BasePassPixelShader.usf' Entry 'MainPS' Permutation 0
PackagingResults: Error: Job 4 [Single] Failed: M_Fern_01_1ffb0f638ad8b518/Default/FLocalVertexFactory/TLightMapDensityPSTLightMapPolicyHQ/0:/Engine/Private/LightMapDensityShader.usf|MainPixelShader VF 'FLocalVertexFactory' Type 'TLightMapDensityPSTLightMapPolicyHQ' '/Engine/Private/LightMapDensityShader.usf' Entry 'MainPixelShader' Permutation 0
PackagingResults: Error: Job 5 [Single] Failed: M_Fern_01_1ffb0f638ad8b518/Default/FHWRasterizePS/74:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizePS Type 'FHWRasterizePS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizePS' Permutation 74
PackagingResults: Error: Job 6 [Single] Failed: M_Fern_01_1ffb0f638ad8b518/Default/FHWRasterizePS/83:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizePS Type 'FHWRasterizePS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizePS' Permutation 83
PackagingResults: Error: Job 7 [Single] Failed: M_Fern_01_1ffb0f638ad8b518/Default/FHWRasterizeVS/53:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizeVS Type 'FHWRasterizeVS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizeVS' Permutation 53
PackagingResults: Error: Job 8 [Single] Failed: M_Fern_01_1ffb0f638ad8b518/Default/FHWRasterizePS/89:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizePS Type 'FHWRasterizePS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizePS' Permutation 89
PackagingResults: Error: Job 9 [Single] Failed: M_Fern_01_1ffb0f638ad8b518/Default/FHWRasterizeVS/49:/Engine/Private/Nanite/NaniteRasterizer.usf|HWRasterizeVS Type 'FHWRasterizeVS' '/Engine/Private/Nanite/NaniteRasterizer.usf' Entry 'HWRasterizeVS' Permutation 49
PackagingResults: Error: ShaderCompileWorker failed
PackagingResults: Error: Unknown Cook Failure
```
火绒的实时文件监控和恶意行为拦截，干扰了 ShaderCompileWorker 对临时文件的正常读写，并误将其高频进程活动判定为威胁而强制终止，导致着色器编译输出损坏或进程崩溃。关闭火绒后解决

3.
中文兼容流程:
[搁置]蓝图BP_DemoDisplay中文兼容失败,历史遗留问题,暂且无办法解决
蓝图UI_Active_Abilities_Info_Description -> Creating the styled text for resources -> Break Struct Gameplay Tag Attribute(Attribute 节点) -> Get Gameplay Tag Name(Name 节点) -> 输出"Mana"以中文表达"魔法"

4.
指令~ -> ShowDebug EnhancedInput 增强输入调试显示
场景部分功能迁移,技能模块以及靶场

5.
**兼容ability sysytem 功能模块** && **兼容I键快捷栏 人物属性栏上方模块**
BP_PlayerController_MSTPro -> controller 控制器 (原有组件省略表达)
    -> AC_AbilityManager_Advanced -> com **新添加 来自ability system** 这个组件实现了右下角的技能栏以及I键启用的上方技能快捷栏设计
BP_GameState_MST_Pro -> State 游戏状态类 (原有组件省略表达)
    -> AC_GameState_TagMapper_Ability -> com **新添加 来自ability system** 技能执行中枢与UI数据源，负责管理角色的技能列表、冷却与消耗判定，同时驱动右下角技能栏的显示与I键呼出的技能快捷设置面板
IM_Abilities 输入映射的IA_Ability_01~04 快捷键1234修改为QERT,但出现报错:快捷栏功能丢失.
[原因]AC_AbilityManager_Advanced 检测到输入重叠后销毁了热键栏组件
    [报错日志]-> LogBlueprintUserMessages: [AC_AbilityManager_Advanced] Hotbar component destroyed because it has overlapping inputs
解决方法
AC_AbilityManaget_Advanced -> Event Begain Play -> Disable Hotbar
    ->这个"Disable Hotbar"是用来禁用快捷栏的,取消链接即可

6.
无法使用技能,显示"not enough resources"(即没有 蓝Mana)
Character蓝图 -> AC_Attribute_Manager_Advanced组件 -> 细节面板 Use Mana 打勾



---

# 反思

为什么如此设计?
```
controller -> AC_AbilityManager_Advanced -> 这个组件实现了右下角的技能栏以及I键启用的上方技能快捷栏设计
State -> AC_GameState_TagMapper_Ability -> 技能执行中枢与UI数据源，负责管理角色的技能列表、冷却与消耗判定，同时驱动右下角技能栏的显示与I键呼出的技能快捷设置面板
```

-> 打个比方：一家连锁餐厅
AC_AbilityManager_Advanced（PlayerController） = 每个顾客手里的“点单小票”
记录着“我”点了什么菜、上菜进度、能不能退单。这些信息只跟“我”有关，不需要让隔壁桌知道。
AC_GameState_TagMapper_Ability（GameState） = 墙上挂着的“菜单”
写着“宫保鸡丁”对应哪个菜谱、“鱼香肉丝”对应哪个做法。所有顾客看到的菜单都一样，而且由店长（服务器）统一更新。

-> 这样设计的好处（四点核心）
1. 网络流量最小化（性能关键）
AC_AbilityManager_Advanced（私有数据）：只同步给该玩家自己，不会广播给其他人。如果放在 GameState 上，每次技能冷却变化都要通知所有人，浪费带宽。
AC_GameState_TagMapper_Ability（全局数据）：只同步一次，所有客户端共享，节省了重复传输的开销。
2. 职责单一，容易维护
AC_AbilityManager_Advanced：只管“执行”（冷却、消耗、触发），不关心“翻译”。
AC_GameState_TagMapper_Ability：只管“翻译”（标签 → 类），不关心“执行”。
如果以后要换一套技能表（比如节日活动模式），只需要修改 GameState 上的映射，技能管理器完全不用改。
3. 服务器权威，防止作弊
AC_GameState_TagMapper_Ability 由服务器持有并复制，客户端无法篡改“火球术对应哪个类”，从根源上阻止了外挂修改技能效果。
玩家的技能列表虽然在本地，但最终验证和消耗判定在服务器端的 AbilityManager 中执行。
4. 扩展灵活，支持动态内容
如果未来要做 “技能书学习系统” 或 “职业切换”，只需要在 PlayerController 层动态增删技能列表，GameState 的映射表完全不需要改动。
如果要做 “不同地图使用不同技能表”，只需要切换 GameState 上的 Mapper 组件，所有玩家的技能映射同步切换。

-> ❌ 如果合在一起会怎样？（反例对比）
如果把两个功能合并到一个组件里，放在 PlayerController 上：
❌ 每个玩家都要存储一份完整的“标签→类”映射表，内存浪费 100 倍。
❌ 每个客户端都要单独加载所有技能类，加载时间变长。
❌ 如果映射表需要更新（比如调整技能数值），必须让所有玩家重新登录才能生效。
如果合并到 GameState 上：
❌ 技能冷却状态会被广播给所有人，造成不必要的网络流量。
❌ 每个玩家看到的技能状态都一样，无法实现“我的火球术比你的强”这类差异化


“作业要按时交。”
“项目过期了，机会给别人。”

“过程不能只写一个答案。”
“你怎么做的、能不能复现、出了问题谁负责，比你嘴里的结果重要。”

“不会就早点问，别拖到考试前。”
“问题刚出现时，解决成本最低。等它烂到所有人都看见，处理的可能就是你。”

“别抄作业。”
“你可以参考别人，但不能永远靠复制。真轮到你独立负责时，没人把标准答案放在桌角给你看。”

“上课别一直玩手机。”
“注意力就是生产资料。谁能连续专注，谁就比别人多一块可以出售的能力。”

“这次没考好，先找原因。”
“没人关心你这次为什么没做好，只会根据结果决定下一次还要不要找你。”