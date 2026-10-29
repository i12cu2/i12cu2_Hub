# i12cu2 Hub · 全库聚合索引

本仓库是 i12cu2 的聚合索引仓，用于汇总 GitHub 上的相关仓库，并记录个人职业生涯中的全流程开发笔记。

> 说明：
> 由于仓库数量较多，各仓库维护频率不一，仓库入口与索引状态以本仓库为准；具体内容以各子仓库 README 为准。

各层级目录均配有对应 README，提供更详细的说明。由于内容会持续更新，根目录仅保留概要索引。

> 注意：
> 本仓库体积较大（预计超过 1GB），不建议完整克隆。请按需下载所需目录或文件，或使用稀疏检出等方式按需获取。

<pre>
目录
├── .vscode - vscode配置文件
├── assets - 笔记的图片资源汇总(使用vs code 的 PasteImage插件实现)
├── content - 是笔记的源文件
│   ├── AI - AI相关的使用日志
│   │   ├── <a href="https://github.com/AstrBotDevs/AstrBot">astrbot Agent聊天机器人(相关开发日志)</a>
│   │   │   └── <a href="https://github.com/i12cu2/astrbot_plugin_HonorOfKings">astrbot_plugin_HonorOfKings 温雅的农药查询工具</a>
│   │   ├── output 使用AI导出的部分有用有趣话题
│   │   └── test AI功能测试以及破限
│   ├── Android - 安卓相关调试文档
│   │   └── 转译pc 骁龙系U总结的部分转译pc游戏相关日志
│   ├── AutoHotKey - 自动化任务脚本
│   │   └── <a href="https://github.com/i12cu2/AutoHotkey-quick-click-Follow">自动跟随脚本AutoHotkey-quick-click-Follow</a>
│   ├── cmake - cpp配置文件
│   ├── ComputerGraphics - 计算机图形学
│   ├── cpp - C++相关代码
│   │   ├── 配置环境 - cpp相关配置和编译器资料汇总以及介绍 boost &amp; cpp20 &amp; Clangd &amp; MinGW &amp; vcpkg &amp; LLVM &amp; MSVC &amp; MSYS
│   │   ├── 书 - C++相关书籍总结
│   │   ├── 算法 - C++相关算法
│   │   │   ├── <a href="https://github.com/i12cu2/Octree-Cpp">八叉树Octree - 八叉树</a>
│   │   │   ├── <a href="https://github.com/i12cu2/Bezier-Curve-Cpp">贝塞尔曲线B-Plus-Tree - 贝塞尔曲线</a>
│   │   │   ├── <a href="https://github.com/i12cu2/BVH-Cpp">层次包围盒BVH - 边界体积层次结构</a>
│   │   │   ├── <a href="https://github.com/i12cu2/BSP-Tree-Cpp">二叉空间划分BSP-Tree - BSP 树</a>
│   │   │   ├── <a href="https://github.com/i12cu2/NURBS-Cpp">非均匀有理B样条曲线NURBS - 非均匀有理B样条</a>
│   │   │   ├── <a href="https://github.com/i12cu2/Ray-Tracing-Cpp">光线追踪Ray-Tracing - 光线追踪</a>
│   │   │   ├── <a href="https://github.com/i12cu2/Huffman-Compression-Algorithm-Cpp">哈夫曼编码HuffmanCompression - 哈夫曼压缩</a>
│   │   │   ├── <a href="https://github.com/i12cu2/Red-Black-Tree-Cpp">红黑树Red-Black-Tree - 红黑树</a>
│   │   │   ├── <a href="https://github.com/i12cu2/MCPT-Cpp">蒙特卡洛路径追踪MCPT - 蒙特卡洛路径追踪</a>
│   │   │   ├── <a href="https://github.com/i12cu2/BRDF-Cpp">双向反射分布函数BRDF - 双向反射率分布函数</a>
│   │   │   ├── <a href="https://github.com/i12cu2/BSSRDF-Cpp">双向散射表面反射分布函数BSSRDF - 双向表面散射反射率分布函数</a>
│   │   │   ├── <a href="https://github.com/i12cu2/Convex-hull-Algorithm-Cpp">凸包ConvexHullAlgorithm - 凸包算法</a>
│   │   │   ├── <a href="https://github.com/i12cu2/AVL-Tree-Cpp">AVL-Tree - AVL树</a>
│   │   │   ├── <a href="https://github.com/i12cu2/B-Plus-Tree-Cpp">B+树 - B+树</a>
│   │   │   └── <a href="https://github.com/i12cu2/KD-Tree-Cpp">KD-Tree - KD树</a>
│   │   ├── 执行文件 - C++相关执行文件
│   │   │   ├── CheckGccVersion.c &amp; CheckGccVersion.cpp - gcc版本检查
│   │   │   ├── ChinPersonNumber - 暴力计算后四位身份证(可能性)
│   │   │   ├── connect_file - 合并文件
│   │   │   ├── Conversion_of_Number_Systems - 任意进制转换成任意进制(36进制以内)
│   │   │   ├── define_class_test - 用于测试define用法
│   │   │   ├── inherit - 用于测试继承用法
│   │   │   ├── LargetNumbersArithmetic - 大数四则运算(含扩展的小数点运算)
│   │   │   ├── mauss - 摩斯电码转换(英/码互转)
│   │   │   ├── max_heap - 大顶堆求数组中前 k 小元素的索引
│   │   │   ├── OpenMP - OpenMP 测试
│   │   │   ├── os_file - 操作文件 同名不同类型文件 克隆指定位置
│   │   │   ├── power_calculate - 幂次计算 大数乘法
│   │   │   ├── quine - 自指魔术代码
│   │   │   └── vtable - 用于测试虚表用法
│   │   ├── c++特性 - C++相关特性汇总 boost &amp; common &amp; cpp98 &amp; cpp11 &amp; cpp14 &amp; cpp17 &amp; cpp20 ...
│   │   │   ├── boost
│   │   │   ├── common
│   │   │   ├── compare
│   │   │   ├── cpp98
│   │   │   ├── cpp11
│   │   │   ├── cpp14
│   │   │   ├── cpp17
│   │   │   ├── cpp20
│   │   │   ├── other
│   │   │   └── stl
│   │   └── tests - 题库训练
│   │       ├── Leetcode Code - 力扣题库
│   │       ├── LuoGu Code - 洛谷题库
│   │       └── PAT - PAT题库
│   ├── exe
│   │   ├── FastCopy - 快速复制程序
│   │   ├── FastDelete - 快速删除程序
│   │   └── FastDelete注册表 - 快速删除注册表程序
│   ├── GameExp - 个人游戏攻略总结
│   ├── Git - git相关文档
│   │   ├── 撤销git提交
│   │   ├── 更新git仓库
│   │   └── 输出到git仓库
│   ├── Github - 从github上获取到的一些重要资讯
│   ├── JavaScript - JavaScript相关文档
│   │   └── <a href="https://github.com/i12cu2/Automatically-Agree-To-Scripts">自动点赞脚本(AutoAgree) - QQ空间自动点赞脚本</a>
│   ├── Linux - Linux工具相关文档总结
│   │   ├── 进程管理和查看工具
│   │   ├── 开发和调试工具
│   │   ├── 命令操作笔记
│   │   ├── 其他实用工具
│   │   ├── 软件包管理工具
│   │   ├── 软件测试工具
│   │   ├── 网络分析工具
│   │   └── 系统监控工具
│   ├── lua - lua相关学习测试文档
│   ├── matlab - matlab相关算法程序(数值代数/数值逼近/数据挖掘/智能计算/最优化理论与算法/偏微分方程数值解法等算法)
│   │   ├── <a href="https://github.com/i12cu2/Numerical-Methods-for-PDE-Matlab">偏微分方程数值解法(NumericalMethodsForPDEMatlab)</a>
│   │   │   ├── PDE fun - 偏微分方程
│   │   │   ├── Finite difference method - 有限差分法
│   │   │   ├── Finite element difference method - 有限元差分法
│   │   │   ├── Calculus of differences - 差分算子法
│   │   │   ├── Two dimensional heat conduction equation - 二维热传导方程
│   │   │   ├── ADI - 交替方向隐式法
│   │   │   ├── Wave equation - 波动方程
│   │   │   └── Diffusion-convection equation - 扩散-对流方程
│   │   ├── <a href="https://github.com/i12cu2/Data-Mining-Algorithm-Matlab">数据挖掘(DataMiningAlgorithm)</a>
│   │   │   ├── Apriori - 先验算法
│   │   │   ├── K-means - K均值算法
│   │   │   ├── Hierarchical clustering - 层次聚类
│   │   │   ├── ID3 - ID3分类器
│   │   │   ├── Naive bayes classifier - 朴素贝叶斯分类器
│   │   │   ├── Support vector machine - 支持向量机
│   │   │   └── Fuzzy C-means clustering algorithm - 模糊C均值聚类算法
│   │   ├── <a href="https://github.com/i12cu2/Numerical-Approximation-Matlab">数值逼近(NumericalApproximation)</a>
│   │   │   ├── Lagrange&#x27;s interpolation - 拉格朗日插值
│   │   │   ├── Newton interpolation - 牛顿插值
│   │   │   ├── Analogue function - 模拟函数
│   │   │   ├── Hermite interpolation function - 赫米尔特插值函数
│   │   │   ├── Spline interpolation - 样条插值
│   │   │   ├── Polynomial canonical orthogonal fit - 多项式规范正交你和
│   │   │   ├── Newton-cotes formula - 牛顿-科斯特公式
│   │   │   └── Euler&#x27;s method - 欧拉方法
│   │   ├── <a href="https://github.com/i12cu2/Numerical-Algebra-Matlab">数值代数</a>
│   │   │   ├── Gaussian elimination method - 高斯消元法
│   │   │   ├── Column pivot elimination - 列主元消元法
│   │   │   ├── Chasing method - 追逐法
│   │   │   ├── Root-squaring method - 平方根法
│   │   │   ├── Jacobi iteration method - 雅可比迭代法
│   │   │   ├── Gaussian iteration method - 高斯迭代法
│   │   │   ├── JOR method - JOR方法
│   │   │   ├── SOR method - SOR方法
│   │   │   ├── Steepest descent method - 最速下降法
│   │   │   ├── Conjugate gradient methods - 共轭梯度法
│   │   │   ├── The steepest descent method and the rate of convergence - 最速下降法与收敛速度
│   │   │   ├── Newton iteration method - 牛顿迭代法
│   │   │   ├── Secant method - 割线法
│   │   │   └── Iteration method -迭代法
│   │   ├── <a href="https://github.com/i12cu2/Intelligent-Computing-Matlab">智能计算(IntelligentComputing)</a>
│   │   │   ├── BP neural network - BP神经网络
│   │   │   ├── Hopfield neural network - 霍普菲尔德神经网络
│   │   │   ├── Radial basis function - 径向基函数
│   │   │   ├── Genetic algorithm - 遗传算法
│   │   │   ├── Particle swarm optimization - 粒子群优化算法
│   │   │   └── Ant colony algorithm - 蚁群算法
│   │   └── <a href="https://github.com/i12cu2/Optimization-Theory-and-Algorithms-Matlab">最优化理论与算法(OptimizationTheoryAndAlgorithms)</a>
│   │       ├── Linear programming - 线性规划
│   │       ├── Golden cut algorithm - 黄金分割
│   │       ├── Ternary quadratic interpolation method - 三元二次插值法
│   │       ├── Steepest descent method - 最速下降法
│   │       ├── Newton method - 牛顿法
│   │       ├── Conjugate gradient methods - 共轭梯度法
│   │       ├── Uadratic programming - 二次规划
│   │       └── Rosen&#x27;s gradient projection method - 罗森梯度投影法
│   ├── md - markdown相关语法
│   ├── Network - 计算机网络
│   ├── OperatingSystem - 计算机操作系统
│   ├── python - python相关算法程序(机器学习算法/模块执行文件/文件转化工具)
│   │   ├── 0algorithm 算法
│   │   │   ├── 机器学习算法 - python相关机器学习算法(机器学习/进化算法/强化学习/深度学习/算法模块/NLP/其他算法等)
│   │   │   │   ├── <a href="https://github.com/i12cu2/Machine-Learning-Algorithm">机器学习算法(MachineLearningAlgorithm)</a>
│   │   │   │   │   ├── Adaboost 集成算法
│   │   │   │   │   ├── DecisionTrees 决策树
│   │   │   │   │   ├── GradientBoosting 梯度提升
│   │   │   │   │   ├── LinearRegression 线性回归
│   │   │   │   │   ├── LogisticRegression 逻辑回归
│   │   │   │   │   ├── NeuralNetworks 神经网络
│   │   │   │   │   ├── RandomForests 随机森林
│   │   │   │   │   └── SupportVectorMachines 支持向量机
│   │   │   │   ├── <a href="https://github.com/i12cu2/Evolutionary-Algorithm">进化算法(EvolutionaryAlgorithm)</a>
│   │   │   │   │   ├── GeneticAlgorithm 遗传算法
│   │   │   │   │   └── ParticleSwarmOptimization 粒子群优化
│   │   │   │   ├── <a href="https://github.com/i12cu2/Other-Artificial-Intelligence-Algorithm">其他人工智能算法(OtherAlgorithm)</a>
│   │   │   │   │   ├── KNN(K-NearestNeighbors) K最近邻
│   │   │   │   │   └── MarkovChains 马尔可夫链
│   │   │   │   ├── <a href="https://github.com/i12cu2/Reinforcement-Learning-Algorithm">强化学习算法(UnsupervisedLearningArithmeticAlgorithm)</a>
│   │   │   │   │   ├── Deep Q-Network 深度Q网络
│   │   │   │   │   ├── Policy Gradient 策略梯度
│   │   │   │   │   └── Q-Learning Q学习
│   │   │   │   ├── <a href="https://github.com/i12cu2/Deep-Learning-Algorithm">深度学习算法(DeepLearningAlgorithm)</a>
│   │   │   │   │   ├── Autoencoders 自编码器
│   │   │   │   │   ├── Convolutional Neural Networks 卷积神经网络
│   │   │   │   │   ├── Gated Recurrent Unit 门控循环单元
│   │   │   │   │   ├── Long Short-Term Memory Networks 长短期记忆网络
│   │   │   │   │   └── Recurrent Neural Networks 循环神经网络
│   │   │   │   ├── <a href="https://github.com/i12cu2/Unsupervised-Learning-Arithmetic-Algorithm">无监督学习算法(UnsupervisedLearningArithmeticAlgorithm)</a>
│   │   │   │   │   ├── Autoencoders 自编码器
│   │   │   │   │   ├── Hierarchical Clustering 层次聚类
│   │   │   │   │   ├── K-Means Clustering K均值聚类
│   │   │   │   │   └── Principal Component Analysis 主成分分析
│   │   │   │   └── <a href="https://github.com/i12cu2/Natural-Language-Processing-Algorithm">自然语言处理算法(NaturalLanguageProcessingAlgorithm)</a>
│   │   │   │       ├── ConvolutionalNeuralNetwork(CNN) 卷积神经网络
│   │   │   │       ├── LogisticRegression 逻辑回归
│   │   │   │       ├── LongShortTermMemory(LSTM) 长短时记忆网络
│   │   │   │       ├── NaiveBayes 朴素贝叶斯
│   │   │   │       ├── RecurrentNeuralNetwork(RNN) 循环神经网络
│   │   │   │       └── SupportVectorMachine(SVN) 支持向量机
│   │   │   ├── 加密算法
│   │   │   │   ├── 椭圆曲线乘法(比特币加密模拟)
│   │   │   │   └── 椭圆曲线密钥交换 (ECDH)-密钥派生函数 (PBKDF2)-XOR加密算法(通话加密)
│   │   │   └── 图形算法
│   │   │       ├── <a href="https://github.com/i12cu2/MSAA-Algorithm-Python">抗锯齿MSAA - MSAA 代码</a>
│   │   │       └── <a href="https://github.com/i12cu2/Mipmap-Algorithm-Python">图片压缩Mipmap - Mipmap 代码</a>
│   │   ├── 0environment - python相关配置 &amp; 编译器资料汇总 &amp; UE_python开发日志
│   │   ├── 0module note - python 特定模块开发日志
│   │   ├── 书 - python相关书籍
│   │   ├── Change - python的文件修改脚本(格式转换/规范/增删改查等)
│   │   │   ├── audio - 音频
│   │   │   │   ├── mov - mov格式文件相关python脚本
│   │   │   │   │   └── mov2mp4 - mov转mp4
│   │   │   │   ├── mp3 - mp3格式文件相关python脚本
│   │   │   │   │   ├── <a href="https://github.com/i12cu2/KugouDecoderByPython">KuGouMusic - 酷狗音乐(KGM)文件解码技术说明</a>
│   │   │   │   │   ├── CompressMp3 - 压缩mp3
│   │   │   │   │   ├── <a href="https://github.com/i12cu2/NetEase-Cache-To-Mp3">NetEaseMusicCache2mp3 - 将网易缓存转换为 mp3</a>
│   │   │   │   │   └── Voicebox MP3 Smart Clipper - 智能截取声音片段
│   │   │   │   └── <a href="https://github.com/FFmpeg/FFmpeg">mp4 - mp4格式文件相关python脚本(依赖ffmpeg)</a>
│   │   │   │       ├── <a href="https://github.com/i12cu2/BilibiliTools">BilibiliTools - b站工具箱</a>
│   │   │   │       │   ├── 二次处理(文本提取网址工具) - 下述代码运行后进行的二次处理脚本
│   │   │   │       │   ├── GetCover - 提取b站视频封面
│   │   │   │       │   ├── GetIntro - 提取b站视频简介(含合集提取简介)
│   │   │   │       │   ├── GetMusic - 提取b站音乐(视频转化音乐)
│   │   │   │       │   ├── GetVideo - 提取b站视频
│   │   │   │       │   └── BiliTools - 融合了上述全部脚本的大成之作
│   │   │   │       ├── <a href="https://github.com/i12cu2/Collapsible-Video">Collapsible-Video - FFMPEG工具脚本</a>
│   │   │   │       │   ├── OutputVideoMessage - 输出video相关参数
│   │   │   │       │   └── VideosCompress(ffmpeg) - 视频批量压缩(依赖ffmpeg) 
│   │   │   │       ├── <a href="https://github.com/i12cu2/VideoQuickEditing">VideoQuickEditing - 视频快剪辑</a>
│   │   │   │       │   ├── VideoQuickEditing - 视频快剪
│   │   │   │       │   ├── VideoQuickMerge - 视频合并
│   │   │   │       │   └── VideoQuickEditing - 视频集快剪
│   │   │   │       ├── Drop2720p - 将视频压缩到720p
│   │   │   │       ├── Drop21080p - 将视频压缩到1080p
│   │   │   │       ├── mp42mp3(ffmpeg) - mp4转mp3(依赖ffmpeg)
│   │   │   │       └── YoutubeDownload - 下载Youtube视频
│   │   │   ├── <a href="https://github.com/i12cu2/Merge-Binary-File-Python">binary - 二进制文件修改 用于合并&quot;bin&quot;文件的程序</a>
│   │   │   ├── document - 文档
│   │   │   │   ├── docx - office格式文件相关python脚本
│   │   │   │   │   └── <a href="https://github.com/i12cu2/Docx-To-Pdf">docx转pdf - docx转pdf</a>
│   │   │   │   ├── epub - epub格式文件相关python脚本
│   │   │   │   │   ├── <a href="https://github.com/i12cu2/Epub-to-Pdf">epub转pdf - epub转pdf</a>
│   │   │   │   │   └── <a href="https://github.com/i12cu2/Epub-To-Txt">epub转txt - epub转txt</a>
│   │   │   │   ├── md - markdown格式文件相关python脚本
│   │   │   │   │   ├── ban &amp; pick md转化html格式(BP信息示例)
│   │   │   │   │   ├── 打印文件夹信息
│   │   │   │   │   ├── 热更新文件信息
│   │   │   │   │   ├── 输出文件列表
│   │   │   │   │   ├── 整合路径下md文件
│   │   │   │   │   ├── md2md - md格式转换(特定)
│   │   │   │   │   ├── md层级转换树形结构
│   │   │   │   │   └── md文件分割提取
│   │   │   │   ├── pdf - pdf格式文件相关python脚本(OCR/PyPDF2等)
│   │   │   │   │   ├── 去掉头尾页面
│   │   │   │   │   ├── 同名pdf和epub(移除)
│   │   │   │   │   ├── pdf转pdf(page)
│   │   │   │   │   ├── pdf转png
│   │   │   │   │   ├── <a href="https://github.com/i12cu2/Pdf-to-Txt-By-EasyOCR">pdf转txt - pdf转txt(EasyOcr方式)</a>
│   │   │   │   │   ├── <a href="https://github.com/i12cu2/PDF-to-TXT-And-Merge">pdf转txt - pdf转txt并合并</a>
│   │   │   │   │   └── <a href="https://github.com/i12cu2/PDF-Cancel-Password">pdf解除密码限制 - pdf解除密码</a>
│   │   │   │   ├── txt - txt格式文件相关python脚本
│   │   │   │   │   ├── 递归合并含日期的txt文件
│   │   │   │   │   ├── 合并同目录下所有txt文件
│   │   │   │   │   ├── 批量格式化txt文件
│   │   │   │   │   ├── 批量替换txt文件中的指定内容
│   │   │   │   │   ├── 删除非特定后缀文件
│   │   │   │   │   ├── 删除根目录txt特殊字符
│   │   │   │   │   ├── 删除目录txt的换行
│   │   │   │   │   ├── 删除目录txt的换行和空格
│   │   │   │   │   ├── 删除目录txt中的指定内容
│   │   │   │   │   ├── 搜寻该字符串在目录txt哪些文件中出现
│   │   │   │   │   └── 统计输入字符串在目标txt中出现的次数
│   │   │   │   └── words - 单词文本文件相关python脚本
│   │   │   │       ├── 单词差集
│   │   │   │       ├── 单词库下载
│   │   │   │       ├── 单词去重
│   │   │   │       ├── 单词提取
│   │   │   │       └── 单词转化指令
│   │   │   ├── language - 翻译相关python脚本
│   │   │   │   ├── 繁体简体互转
│   │   │   │   └── 英语汉语互转
│   │   │   ├── picture
│   │   │   │   ├── jpg - jpg格式文件相关python脚本(OCR等)
│   │   │   │   │   └── jpg转txt(依赖OCR)
│   │   │   │   ├── png - png格式文件相关python脚本(OCR)
│   │   │   │   │   └── png转txt(OCR)
│   │   │   │   ├── compress_by_ratio - 按比例统一压缩图片
│   │   │   │   └── compress_by_width - 按宽度阈值压缩图片
│   │   │   ├── Web - 网页
│   │   │   │   ├── html - html格式文件相关python脚本
│   │   │   │   │   ├── 根据内容中的发布日期批量重命名文件
│   │   │   │   │   ├── html2markdown - html转md
│   │   │   │   │   └── html2txt - html转txt
│   │   │   │   └── mht - mht格式文件相关python脚本
│   │   │   │       └── mht2txt - mht格式转txt
│   │   ├── <a href="https://github.com/i12cu2/CodeFormatterByPython">CodeFormatter - 规范Python代码中标识符的智能工具</a>
│   │   ├── <a href="https://github.com/i12cu2/Compressed_package_Operation_by_Python">CompressedPackageOperation - 压缩包相关脚本</a>
│   │   │   ├── 7Z
│   │   │   │   ├── 7Z 加密
│   │   │   │   ├── 7Z 异常检测
│   │   │   │   ├── 7Z 解密
│   │   │   │   └── 7Z 转RAR
│   │   │   ├── more - 更多补充
│   │   │   │   └──  检锁 - 检查是否有密码锁
│   │   │   ├── RAR
│   │   │   │   ├── DangerScript - RAR删除相关脚本
│   │   │   │   ├── Special - RAR相关特殊脚本
│   │   │   │   │   ├── <a href="https://github.com/i12cu2/Picture_Seed">图种</a>
│   │   │   │   │   ├── RAR检查文件存在 - 检查特定文件是否存在于RAR中
│   │   │   │   │   ├── RAR解压图片 - 解压RAR中特定路径图片
│   │   │   │   │   └── RAR前缀 - 规范RAR文件命名
│   │   │   │   ├── RAR 导出层级 - 输出文件层级
│   │   │   │   ├── RAR 加密
│   │   │   │   ├── RAR 检二压 - 检查是否为包中包(有设定路径以及拖动脚本上生效两个方案)
│   │   │   │   ├── RAR 检损 - 检查损坏
│   │   │   │   ├── RAR 解密
│   │   │   │   ├── RAR 压缩
│   │   │   │   ├── RAR 压中cocos - 检查是否为cocos项目
│   │   │   │   ├── RAR 压中H5 - 检查是否为H5项目
│   │   │   │   ├── RAR 压中Scratch3 - 检查是否为Scratch3项目
│   │   │   │   └── RAR 压中Unity - 检查是否为Unity项目
│   │   │   └── ZIP
│   │   │       ├── ZIP 加密
│   │   │       ├── ZIP 检损 - 检查损坏
│   │   │       ├── ZIP 解密
│   │   │       └── ZIP 转RAR
│   │   ├── <a href="https://github.com/i12cu2/FileBrowserAndEditorByPython">FileBrowserAndEditor - Python可视化开发界面</a>
│   │   ├── FileHandling - 文件处理(增删改查)
│   │   │   ├── compare - 比对并处理
│   │   │   ├── delete - (符合特定条件)删除[危险操作]
│   │   │   ├── move - (符合特定条件)移动
│   │   │   ├── rename - 批量改名
│   │   │   ├── search - 搜索
│   │   │   └── tree - 构建文件层级树
│   │   ├── <a href="https://github.com/i12cu2/Financial-Credit-Analysis-Graduation-Project-Python">FinancialCreditAnalysisGraduationProject - 数学建模毕业设计</a>
│   │   │   └── <a href="https://github.com/i12cu2/Mathematical-Modeling-Python">旧款(可忽略)</a>
│   │   ├── <a href="https://github.com/i12cu2/FloatingClipboardManagerByPython">FloatingClipboardManager - 浮动剪贴板管理工具</a>
│   │   ├── <a href="https://github.com/i12cu2/github_archive_kit">github_archive_kit - Github归档工具集</a>
│   │   │   ├── GithubPullScripts - Github 仓库批量拉取脚本
│   │   │   ├── GitHubRepoBatchZIPDownloader&amp;Checker - GitHub 仓库批量 ZIP 下载与完整性检查工具
│   │   │   └── GitHubStarsCrawler&amp;URLDiffTool - GitHub Stars 爬虫 &amp; URL 差异比较工具
│   │   ├── <a href="https://github.com/i12cu2/HotkeyAutoClickerByPython">HotkeyAutoClicker - 一个简洁的全局热键连点器，通过热键控制鼠标自动点击</a>
│   │   ├── page_spider - 学习的爬虫项目
│   │   ├── <a href="https://github.com/i12cu2/PortableExecutableFile">PortableExecutableFile - 可移植可执行文件</a>
│   │   │   ├── 成功过程 - 转化二进制代码
│   │   │   ├── 打包结果 - 可移植可执行程序集
│   │   │   └── 目标源代码 - 可移植可执行程序集源代码
│   │   │       ├── 复制桌面lib - 将桌面 lib 文件夹同步到 U 盘 lib 文件夹的工具，只复制新增或已更改的文件、跳过相同文件，并生成 CSV 操作日志
│   │   │       ├── 删除rar缓存 - 删除RAR压缩包中特定文件集(不依赖rar.exe)二进制便携式程序
│   │   │       ├── 压缩包解压 - 支持将拖入的 .7z/.zip/.rar 文件或文件夹解压到同名目录，自动避免重名、显示进度，并在结束后清理临时工具
│   │   │       ├── 一键转化端 - 先把 ZIP/7Z 转换为 RAR 并删除原文件，再对生成的及原有的 RAR 按预设模式删除冗余文件，并输出控制台/CSV 报告
│   │   │       ├── 转RAR - 将拖动的文件/文件夹中的ZIP和7Z文件转换为RAR格式
│   │   │       ├── Python一键打包工具 - 将拖放的Python文件打包成EXE文件
│   │   │       ├── python代码打包exe - 简易Python打包工具(修复兼容问题)
│   │   │       ├── RAR前缀覆盖 - 扫描指定文件/文件夹中的 RAR，解析其内部唯一顶层文件夹名，去掉原 [..] 前缀后重命名为 [提取名]原文件名
│   │   │       └── UE版本检测工具 - 内置 WinRAR 提取解压工具，扫描 RAR 中的 .uproject/.uplugin 文件并解析引擎版本，最后输出检测报告
│   │   ├── Tests - 相关测试
│   │   │   ├── 测试服务器是否监听
│   │   │   ├── 检查网络连接
│   │   │   ├── 内存条频率测试
│   │   │   ├── 网络诊断工具
│   │   │   ├── 修复防火墙问题
│   │   │   ├── 终端示例
│   │   │   └── UpdateMoreLib - 更新全部python库
│   │   ├── <a href="https://github.com/i12cu2/UEAssetsToolkit">UEAssetsToolkit - 用于对资源包及项目文件进行分类、提取、清理和筛选的Python脚本</a>
│   │   │   ├── UEAssetsAnimationFilter - 深度查找单位内是否存在 `Animation` / `Animations` 文件夹，命中则移动整个单位到目标目录
│   │   │   ├── UEAssetsClassify - 按 `.uproject` / `.uplugin` 将单位分类为项目工程、插件、素材，并移动到对应目录
│   │   │   ├── UEAssetsCleanup - 深度删除指定文件夹（如“库文件”）和文件（如 `Read Me !.txt`、`manifest`），再回收空目录
│   │   │   ├── UEAssetsContentExtract - 在单位内识别“类 Content 文件夹”，若排除后有效子文件夹恰好一个，则提取并回收原单位
│   │   │   ├── UEAssetsExeFilter - 深度查找 `.exe`，命中则移动整个单位到 exe 目录
│   │   │   ├── UEAssetsFolderList - 读取源目录下所有一级子文件夹名，逐行写入指定 txt 文件；只读源目录，不改动任何内容
│   │   │   ├── UEAssetsFxFilter - 单位名包含 `fx` / `vfx`（不区分大小写）时，移动整个单位
│   │   │   ├── UEAssetsFxFolderFilter - 单位内部存在恰好名为 `fx` / `vfx`（不区分大小写）的文件夹时，移动整个单位
│   │   │   ├── UEAssetsHarvest - 剥离单位的多层空壳嵌套，沿单链下钻，收割真正的内容根文件夹并回收原单位
│   │   │   ├── UEAssetsProjectContentExtract - 在项目单位中定位 `.uproject` 同级的 `Content`，若排除名单后仅剩一个有效子文件夹，则提取该文件夹并回收原单位
│   │   │   ├── UEAssetsProjectNormalize - 找到 `.uproject`，将其父文件夹按 `.uproject` 前缀重命名，移动到目标目录并回收原单位
│   │   │   ├── UEAssetsProjectRename - 就地重命名项目单位：以 `.uproject` 前缀为名，冲突时追加 `_1`、`_2`
│   │   │   ├── UEAssetsProjectScanner - 只读扫描，列出所有含 `.uproject` 的单位及具体文件路径，不做任何修改
│   │   │   └── UEAssetsUnityFilter - 深度查找 `.unitypackage`，命中则移动整个单位到 Unity 目录
│   │   └── zhihu - 知乎杂谈回答整理
│   │       ├── 整理 - 下方temp经过py脚本处理后的文件示例
│   │       └── 整理temp到整理文件夹 - 将回答以分类形式保存特定目录
│   ├── Qt - Qt开发相关笔记
│   ├── Shader - Shader开发相关笔记
│   ├── Software - 软件以及协议等分析总结归档
│   │   ├── Adobe - Adobe相关介绍总结
│   │   ├── AutoDesk - AutoDesk相关介绍总结
│   │   ├── JetBrains - JetBrains相关介绍总结
│   │   └── vs code - vs code相关配置和插件
│   ├── sql - sql数据库相关笔记
│   ├── Tattle 杂谈
│   │   ├── 凡人修仙传
│   │   ├── 杰哥观察者模式启动中
│   │   ├── <a href="https://github.com/i12cu2/SinyaLee">李新野</a>
│   │   ├── 林霖心医
│   │   ├── 马督工
│   │   ├── 赛雷三分钟
│   │   ├── 斯奎奇大王
│   │   ├── 孙宇晨
│   │   ├── <a href="https://github.com/i12cu2/Crown_of_Tokamak">托卡马克之冠</a>
│   │   ├── 小约翰可汗
│   │   ├── 永恒的胖猫
│   │   └── Script - 相关处理的脚本(不赘述)
│   ├── UE - 虚幻引擎相关文档(以UE5.2/5.4/5.8为例)
│   │   ├── 书 - UE相关书籍笔记
│   │   ├── Application - 开发应用
│   │   │   ├── Plugins - 开发的插件
│   │   │   │   ├── Debug_Log - 插件跨版本日志 - [插件]+引擎初始版本+引擎目标版本
│   │   │   │   ├── <a href="https://github.com/i12cu2/Blueprint-Function-Libraries-from-mine">FileOperations - 蓝图库节点插件</a>
│   │   │   │   └── <a href="https://github.com/i12cu2/Add-Tag-plugins-for-Unreal-Engine-Cpp">TP - 为UE修改Tag插件</a>
│   │   │   └── Project - 开发的项目
│   │   │       ├── <a href="https://github.com/i12cu2/UCharts">UCharts - 图表蓝图</a>
│   │   │       ├── <a href="https://github.com/i12cu2/UPlayer">Uplayer - Android 音乐播放器(极简版)</a>
│   │   │       └── <a href="https://github.com/i12cu2/UWebCompiler">UWebCompiler - 图表实时编译器</a>
│   │   ├── Doc - 部分开发零散文档
│   │   ├── Editor - UE相关编辑器笔记
│   │   ├── Font - UE项目中 TextRenderActor可测试的中文字体
│   │   ├── Notes - 关开发实现的视频教学中笔者记下的笔记
│   │   │   ├── bili - b站
│   │   │   ├── url - 个人网站
│   │   │   └── zhihu - 知乎
│   │   ├── OpenSourceProject - UE开源项目研究日志(项目过多不在此赘述)
│   │   ├── Package - UE打包相关日志
│   │   ├── Plugins - UE相关插件笔记
│   │   │   ├── Debug_Log - 插件跨版本日志 - [插件]+引擎初始版本+引擎目标版本
│   │   │   └── <a href="https://github.com/i12cu2/MagicNodeTask">MagicNode - cpp魔术节点</a>
│   │   ├── Source - UE相关代码笔记
│   │   │   └── ... - 以UE-cpp版本解决方案为分类的代码解析
│   │   ├── SourceAvailableProject - UE网络来源项目研究日志(项目过多不在此赘述)
│   │   └── Tools - UE相关工具介绍总结
│   ├── unity - unity(c#)相关代码 (历史代码存在部分遗失,不在该库中,已停更)
│   │   └── Application
│   │       ├── <a href="https://github.com/i12cu2/Battle-City-Unity-Game">Battle-City 打砖块 3d</a>
│   │       ├── Tank 坦克大战
│   │       ├── <a href="https://github.com/i12cu2/Hit-the-bricks-Unity-Game">Hit-the-bricks</a>
│   │       ├── <a href="https://github.com/i12cu2/Pacman-Unity-Game">Pacman 吃豆人 2d (已完成)</a>
│   │       ├── <a href="https://github.com/i12cu2/Tower-Defense-Unity-Game">Tower-Defense 塔防小游戏 3d (已完成)</a>
│   │       ├── <a href="https://github.com/i12cu2/Flash-Master-Unity-Game">Flash-Master 捕鱼达人 2d (已完成)</a>
│   │       ├── <a href="https://github.com/i12cu2/Chru-Unity-Game">Chru 自制游戏 3d探索类 (半成品)</a>
│   │       ├── <a href="https://github.com/i12cu2/Moba-Unity-Game">Moba 自制游戏 2.5d竞技类 (半成品)</a>
│   │       └── <a href="https://github.com/i12cu2/Baba-is-you-Unity-Game">Baba is you 同名重置版解谜游戏</a>
│   ├── Web - UE相关的web开发笔记(图表/web实时编译器工程等)
│   │   └── TampermonkeyScripts - 油猴插件脚本
│   │       ├── B站回复消息批量删除工具
│   │       └── <a href="https://github.com/i12cu2/ZhihuBlocking">ZhihuBlocking - 知乎内容自定义屏蔽词过滤器</a>
│   └── Windows - Windows相关工具和文档
│       ├── 工具 - windows相关工具文档
│       ├── 环境配置 - windows相关配置汇总
│       ├── 浏览器 - 浏览器相关文档
│       └── BatchScript - 批处理脚本执行文件
│           ├── 安卓安卓脚本Install_[Android_Project_Name]-arm64
│           ├── 同步下载我的抖音作品(byDouK-Downloader_V5.7_Windows_X64)
│           ├── 卸载安卓脚本Uninstall_[Android_Project_Name]-arm64
│           ├── 一键启动AstrBot-v4.20.0+NapCat
│           ├── 一键启动WorldMonitor
│           ├── 一键GitPull
│           ├── Win菜单转换CastToWin10Menu
│           ├── Win移动到路径脚本WindowsFileMoveTo
│           └── <a href="https://github.com/i12cu2/Windows-File-Move-To-Android_Batch_Script">Win移动到Android脚本(WindowsFileMoveToAndroid) - 将windows指定文件夹根目录下所有文件迁移到Android指定文件夹根目录</a>
└── 更多待研究...
</pre>









