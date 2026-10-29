https://www.bilibili.com/video/BV1uGEt6CECx

```cpp
// ============================================================
// UCLASS
// ============================================================

UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
// ClassGroup = (Custom)：在编辑器里把这个类归到 “Custom” 分组下
// meta = (BlueprintSpawnableComponent)：让这个组件能出现在蓝图的“添加组件”列表里
class UMyComponent : public UActorComponent
{
    GENERATED_BODY()
};

UCLASS(Blueprintable, BlueprintType, Abstract)
// Blueprintable：可以基于这个 C++ 类创建蓝图子类
// BlueprintType：这个类可以作为蓝图里的变量类型
// Abstract：抽象类，不能在编辑器里直接创建实例
class UMyBaseObject : public UObject
{
    GENERATED_BODY()
};

UCLASS(meta = (DisplayName = "我的角色", ToolTip = "这是给策划看的说明"))
// meta = (DisplayName = "...")：在编辑器/蓝图里显示成这个名字，而不是代码类名
// meta = (ToolTip = "...")：鼠标悬停时显示提示文字
class AMyCharacter : public ACharacter
{
    GENERATED_BODY()
};


// ============================================================
// UPROPERTY
// ============================================================

UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats|Health")
// EditAnywhere：在类默认值和关卡实例的细节面板里都能编辑
// BlueprintReadWrite：蓝图里可以读，也可以写
// Category = "Stats|Health"：在细节面板里放到 Stats -> Health 分类下
float Health;

UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Stats")
// EditDefaultsOnly：只能在类默认值里改，放到关卡里的实例不能改
// BlueprintReadOnly：蓝图里只能读，不能写
float MaxHealth;

UPROPERTY(EditAnywhere, Category = "Stats", meta = (ClampMin = "0.0", ClampMax = "100.0"))
// meta = (ClampMin / ClampMax)：在编辑器里限制输入范围，最小 0，最大 100
float Stamina;

UPROPERTY(ReplicatedUsing = OnRep_Health, Transient, SaveGame)
// ReplicatedUsing = OnRep_Health：这个属性参与网络复制，复制到客户端后调用 OnRep_Health
// Transient：不保存到磁盘，临时数据
// SaveGame：这个属性会写进存档
float ReplicatedHealth;

UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
// VisibleAnywhere：在细节面板里能看到，但不能直接编辑
// 通常用于组件指针，比如 UStaticMeshComponent*
UStaticMeshComponent* MeshComp;


// ============================================================
// UFUNCTION
// ============================================================

UFUNCTION(BlueprintCallable, Category = "My|Action")
// BlueprintCallable：蓝图里可以调用这个函数
// Category：蓝图右键菜单里的分类
void DoSomething();

UFUNCTION(BlueprintPure, Category = "My|Get")
// BlueprintPure：蓝图纯函数，没有执行引脚，一般用来取值，不改变对象状态
float GetHealth() const;

UFUNCTION(BlueprintImplementableEvent, Category = "My|Event")
// BlueprintImplementableEvent：C++ 里只声明，具体逻辑在蓝图里实现
void OnThingHappened();

UFUNCTION(BlueprintNativeEvent, Category = "My|Event")
// BlueprintNativeEvent：C++ 里有默认实现，蓝图里也可以覆盖
void OnNativeEvent();

virtual void OnNativeEvent_Implementation();
// BlueprintNativeEvent 会自动要求你写这个 _Implementation 函数

UFUNCTION(CallInEditor, Category = "My|Editor")
// CallInEditor：在细节面板里显示一个按钮，点击就调用这个函数
void Rebuild();

UFUNCTION(BlueprintCallable, meta = (AdvancedDisplay = "Param2"))
// meta = (AdvancedDisplay = "Param2")：蓝图节点里把 Param2 折叠到“高级”里
void Test(int32 Param1, int32 Param2);


// ============================================================
// USTRUCT
// ============================================================

USTRUCT(BlueprintType)
// BlueprintType：这个结构体可以当蓝图变量类型用
struct FMyStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    // 结构体里面的成员也要用 UPROPERTY，才能在编辑器和蓝图里用
    float Health;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float Mana;
};

USTRUCT(meta = (DisplayName = "我的数据结构"))
// meta = (DisplayName = "...")：在蓝图里显示成这个名字
struct FMyData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Level;
};


// ============================================================
// UENUM
// ============================================================

UENUM(BlueprintType)
// BlueprintType：这个枚举可以当蓝图变量、函数参数用
enum class EMyState : uint8
{
    Idle UMETA(DisplayName = "待机"),   // 蓝图里显示成“待机”
    Running UMETA(DisplayName = "奔跑"), // 蓝图里显示成“奔跑”
    Dead UMETA(Hidden)                  // Hidden：在蓝图下拉菜单里隐藏这个值
};

UENUM(BlueprintType, meta = (Bitflags))
// meta = (Bitflags)：把这个枚举当成位标志用，编辑器里可以多选勾选
enum class EMyFlags : uint8
{
    None = 0,
    FlagA = 1 << 0,
    FlagB = 1 << 1
};


// ============================================================
// 速记
// ============================================================

// 能不能在编辑器里改：
// EditAnywhere / EditDefaultsOnly / EditInstanceOnly / VisibleAnywhere

// 蓝图能不能用：
// BlueprintReadOnly / BlueprintReadWrite / BlueprintCallable / BlueprintPure
// BlueprintType / Blueprintable / BlueprintImplementableEvent / BlueprintNativeEvent

// 编辑器里怎么显示：
// Category / meta = (DisplayName, ToolTip, ClampMin, ClampMax, AdvancedDisplay)

// 网络和保存：
// Replicated / ReplicatedUsing / Transient / SaveGame

// 这些参数不是每个都必须写，按需要加就行。
// 核心就是：说明符控制“能不能编辑、蓝图能不能用、网络复不复制”，
// meta 控制“编辑器里怎么显示、怎么提示、怎么限制输入”。
```
进度
76_锁蓝图_哔哩哔哩_bilibili
https://www.bilibili.com/video/BV1uGEt6CECx/?spm_id_from=333.788.player.switch&vd_source=f0bcad7c7cfef7d5344c43a4598edeea&p=75
