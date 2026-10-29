```
Source
    Developer -> 开发部分
    Editor -> 编辑器部分
        SceneOutLiner -> 世界大纲
    Programs -> 程序部分
    Runtime -> 核心部分
    ThirdParty -> 第三方

Binaries
    配置文件以及第三方配置文件(xml),包含各平台图形库,声音库,物理库(PhysX3),VR,图形显卡,Mono

Build
    跨平台编译需要(Android,IOS,TVOS,HTML5 and so on)

Config
    平台参数设置

Documentation
    文档

Extras  
    额外第三方工具
    Maya动画Ragging工具,VSDebug

Plugins
    插件(.uplugin文件内存储插件相关信息)

2D(Paper2D)
    虚幻的基于Sprite的系统

AI
    AI模块(类似导航系统,AI行为树等)

Animation(LiveLink)
    LiveLink是能够在外部建模软件(比如maya)修改动画，然后在Unreal中能够实时显示修改后的动画的功能
    https://docs.unrealengine.com/en-us/Engine/Animation/Live-Link-Plugin

Blendable(Light Propagation Volume)
    是一种实时GI方法(格子和球谐)
    https://wiki.unrealengine.com/Light_Propagation_Volumes_GI
    https://docs.unrealengine.com/en-us/Engine/Rendering/LightingAndShadows/LightPropagationVolumes

Compositiong
    Composure插件，将游戏与现实中影像混合的插件，
    https://docs.unrealengine.com/en-us/Engine/Composure

lens 
    distortion插件，镜头畸变，内部还有shader代码,本质都是变换uv

openCV lens distortion插件

Developer:Blank Plugin一个空白的插件，可以提供给开发者开发插件参考

CLion 插件
    https://blog.jetbrains.com/clion/2016/10/clion-and-ue4/

codelite插件

Git源码管理插件
    https://wiki.unrealengine.com/Git_source_control_(Tutorial)

KDevelop插件

OneSky本地化服务插件

Perforce版本控制插件
    https://api.unrealengine.com/CHN/Engine/Basics/SourceControl/Perforce/index.html

RenderDoc着色器调试器
    源码：https://github.com/Temaran/UE4RenderDocPlugin
    https://wiki.unrealengine.com/RenderDoc_plugin
    https://forums.unrealengine.com/development-discussion/rendering/17347-new-plugin-shader-debugging-made-easy-with-renderdoc-for-ue4

```

---

```
Editor:一些编辑器编辑器插件

资源管理、蓝图材质贴图节点、面部动画编辑器，Gameplay Tags编辑器，mesh编辑器、Mobile Launcher Profile Wizard,SpeedTree导入插件，等等

Experimental:

Alembic文件导入插件(.abc插件)
    https://docs.unrealengine.com/en-us/Engine/Content/AlembicImporter

苹果图片工具、苹果视觉插件、蓝图统计插件、角色AI插件、代码浏览等等插件

FX:特效相关插件

Houdini Niagara插件

Media:媒体相关插件

Messaging:网络相关插件，TCP、UDP

Performance:Performance Monitor性能监控器

RunTime:
Google AR Core、Apple AR Kit、Apple Movie Player、Android Moview Player、Oculus VR等等

Programs
一些工具的参数，内部全是.ini文件

打补丁工具，shader编译，等等

Shaders
所有着色器，分为private，public，standalone
```

不可删除
```
Config：（不可删除）配置文件。
Content：（不可删除）平常最常用到，所有的资源和蓝图等都放在该目录里。
Source：（不可删除）代码文件。
Plugins：（不可删除）项目使用的插件文件加，项目中没有用到其它插件，这个文件夹就没有。
.uproject：（不可删除）ureal工程
```

可删除
```
Binaries：（可删除）存放编译生成的结果二进制文件。该目录可以gitignore,反正每次都会生成。
DerivedDataCache：（可删除）“DDC”，存储着引擎针对平台特化后的资源版本。比如同一个图片，针对不同的平台有不同的适合格式，这个时候就可以在不动原始的uasset的基础上，比较轻易的再生成不同格式资源版本。gitignore。
Intermediate：（可删除）中间文件（gitignore），存放着一些临时生成的文件。有：Build的中间文件，.obj和预编译头等 UHT预处理生成的.generated.h/.cpp文件 VS.vcxproj项目文件，可通过.uproject文件生成编译生成的Shader文件。AssetRegistryCache：Asset Registry系统的缓存文件，Asset Registry可以简单理解为一个索引了所有uasset资源头信息的注册表。CachedAssetRegistry.bin文件也是如此。
Saved：（可删除，但不建议删除，如果确定项目没有问题，则可以删除）存储自动保存文件，其他配置文件，日志文件，引擎崩溃日志，硬件信息，烘培信息数据等。gitignore
.vs：（可删除）C++智能提示等功能
.sln：（可删除）C++工程
```

---

将项目纳入版本控制需要上传的目录：
```
Config:配置
Content:上下文
Source:代码
Plugins:插件
[xxx].uproject:项目启动项
```

---

ue的缓存文件路径C:\Users\\[i12cu84]\AppData\Local\UnrealEngine\Common\DerivedDataCache(可删除)

---

ue的缓存文件路径设置修改,配置文件在C:\Program Files\Epic Games\UE_5.2\Engine\Config\BaseEngine.ini

用记事本打开它，然后搜索InstalledDerivedDataBackendGraph并找到%ENGINEVERSIONAGNOSTICUSERDIR%DerivedDataCache把它改为%GAMEDIR%DerivedDataCache

修改完后，项目的编译缓存文件会生成在项目目录中


详情资料
https://docs.unrealengine.com/5.2/zh-CN/unreal-engine-directory-structure/