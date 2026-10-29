打包出现蓝屏+崩溃现象
```
LoginId:a418dadc420ac7a2adddf1aff1a8fded
EpicAccountId:d76460e405eb4634b9e1d235aae2e93b

Unhandled Exception: EXCEPTION_ACCESS_VIOLATION reading address 0xffffffffffffffff

nvwgf2umx
nvwgf2umx
nvwgf2umx
nvwgf2umx
nvwgf2umx
nvwgf2umx
nvwgf2umx
nvwgf2umx
D3D12Core
D3D12Core
UnrealEditor_D3D12RHI!D3DX12Residency::Internal::ResidencyManagerInternal::ExecuteSubset() [D:\build\++UE5\Sync\Engine\Source\ThirdParty\Windows\D3DX12\include\D3DX12Residency.h:1188]
UnrealEditor_D3D12RHI!FD3D12Queue::ExecuteCommandLists() [D:\build\++UE5\Sync\Engine\Source\Runtime\D3D12RHI\Private\Windows\WindowsD3D12Device.cpp:2481]
UnrealEditor_D3D12RHI!`FD3D12DynamicRHI::FlushBatchedPayloads'::`2'::<lambda_2>::operator()() [D:\build\++UE5\Sync\Engine\Source\Runtime\D3D12RHI\Private\D3D12Submission.cpp:761]
UnrealEditor_D3D12RHI!FD3D12DynamicRHI::FlushBatchedPayloads() [D:\build\++UE5\Sync\Engine\Source\Runtime\D3D12RHI\Private\D3D12Submission.cpp:859]
UnrealEditor_D3D12RHI!FD3D12DynamicRHI::ProcessSubmissionQueue() [D:\build\++UE5\Sync\Engine\Source\Runtime\D3D12RHI\Private\D3D12Submission.cpp:493]
UnrealEditor_D3D12RHI!FD3D12Thread::Run() [D:\build\++UE5\Sync\Engine\Source\Runtime\D3D12RHI\Private\D3D12Submission.cpp:124]
UnrealEditor_Core!FRunnableThreadWin::Run() [D:\build\++UE5\Sync\Engine\Source\Runtime\Core\Private\Windows\WindowsRunnableThread.cpp:167]
```
-> nvwgf2umx 崩溃确实是 NVIDIA 驱动/D3D12 的典型症状，但它指向的是编辑器会话、后台 GPU 进程或驱动在 Cook 高压环境下的不稳定

解决办法是:
项目设置 搜索dire12
-> 目标RHI -> 默认RHI -> DirectX11 (设置11试试)
-> 成功
切换DirectX 12 
-> 也成功

```
0.(第一次d12打包)我d12打包的时候爆内存一直跳诊断,我重启了,(第二次d12打包)跳诊断爆内存的现象几乎没有了,但是打包一半的时候UE崩溃了+不到十几秒后电脑蓝屏)
1.(第一次d11打包)我改成d11之后打包成功了
2.(第三次d12打包)我切换成d12之后打包成功了
3.(第三次打包)2的这次d12打包成功和上次d12打包蓝屏失败的区别是:我上上次d12打包的时候,由于UE5.8一直显示诊断,爆内存了,导致我第二次打包d12的时候打开了诊断,在实时监测打包情况,而第三次d12打包的时候,我没有打开实时监测,最后成功了
```
一句话结论：**你的 D12 打包本身没有“显存不够导致借用内存”的问题；真正的问题是 NVIDIA 驱动在 D3D12 下不稳定，被 Cook 打包时的高内存/高磁盘/高 CPU 压力触发，诊断器只是额外加压、提高了触发概率。**

分开说清楚：

### 1. 第一次 D12“爆内存跳诊断”
这是**系统内存/环境压力**，不是显存问题。  
你重启后现象几乎消失，说明第一次是后台占用、缓存、全量 Cook 等叠加导致的内存紧张。

### 2. 第二次 D12 崩溃 + 蓝屏
崩溃栈是 `nvwgf2umx` + `D3D12Core`，这是 **NVIDIA 驱动/D3D12 层**的典型崩溃，不是 Cook 在大量用显存。  
你开了编辑器诊断器，它确实会增加 CPU、内存、磁盘 I/O 的额外负载，让系统在 Cook 高峰时更紧绷，所以它**可能是触发因素**，但不是根因。  
根因仍然是：**驱动/D3D12 在高负载环境下不稳定**。

### 3. 为什么 D11 能成功
D11 走 SM5，Shader 和渲染路径压力更小，不容易触发 D12 驱动问题，所以它是**兜底方案**，不是根治。

### 4. 为什么第三次 D12 又成功了
第三次日志完全正常：`ExitCode=0`、`BUILD SUCCESSFUL`，Cook 峰值内存约 14GB，对 62GB 机器不算爆。  
这说明 **D12 打包路径本身能跑通**。不开诊断器、环境干净，就没触发那个不稳定点。

### 5. 你的“显存不足 → 借用内存 → 驱动崩溃”链条
在 **Cook 打包阶段不成立**。  
日志里 `rhiname="Null"`，Cook 用的是 Null RHI，基本不做实际 GPU 渲染，所以 Cook 的瓶颈是**系统内存、CPU、磁盘**，不是 VRAM。  
`nvwgf2umx` 崩溃是驱动/D3D12 的问题，不等于“显存不够”。

### 所以到底是什么问题？
**不是“D12 打包一定爆内存”，也不是“5070Ti 显存不够导致内存连锁崩溃”。**  
而是：**NVIDIA 驱动 + D3D12 在编辑器/后台 GPU 进程里本来就有稳定性风险；Cook 的高负载和诊断器的额外监测把这个问题触发出来了。第三次环境干净、没开诊断器，所以没触发。**

### 你该怎么做
1. **DDU 清洁安装 NVIDIA Studio 驱动**，这是最针对 `nvwgf2umx` 的措施。  
2. **打包时不要开编辑器诊断器、HWiNFO、GPU-Z、Afterburner、Overlay 等工具**。  
3. **设置 `TdrDelay=10`**。  
4. **关闭内存 XMP/EXPO 验证稳定性**。  
5. **急用时切 D11 兜底**。  
6. 下次蓝屏记下终止代码，才能进一步确认是驱动、内存还是供电/散热。

**最简记忆：第一次是内存环境压力；第二次蓝屏是驱动/D3D12 不稳定被高负载和诊断器触发；第三次成功说明 D12 能跑，问题在触发条件，不在“显存不够”。**