#include <iostream>

using namespace std;
class A
{
public:
    int mA;
public:
    A()
    {
        mA = 0;
        cout<<"A的无参构造 mA="<<mA<<endl;
    }
    explicit A(int a)
    {
        mA = a;
        cout<<"A的有参构造mA="<<mA<<endl;
    }
    ~A()
    {
        cout<<"A的析构函数 mA = "<<mA<<endl;
    }
};

class B
{
public:
    int mB;
    A ob;//成员对象
public:
    B()
    {
        cout<<"B类的无参构造"<<endl;
    }
    //初始化列表 成员对象 必须使用对象名+（）
    B(int a, int b):mB(b),ob(a)
    {
        cout<<"B类的有参构造"<<endl;
    }
    ~B()
    {
       cout<<"B的析构函数"<<endl;
    }
};


void test01()
{
    B ob1(10,20);
    cout<<"mA ="<<ob1.ob.mA<<", mB ="<<ob1.mB<<endl;
}
void test02()
{
    //对象数组 每个元素都会自动调用构造和析构函数
    //对象数组不初始化  每个元素 调用无参构造
    A arr1[5];

    //对象数组的初始化 必须显示使用有参构造 逐个元素初始化
    A arr2[5]={A(10),A(20),A(30),A(40),A(50) };
    int n =sizeof(arr2)/sizeof(arr2[0]);
    int i=0;
    for(i=0;i<n;i++)
    {
        cout<<arr2[i].mA<<" ";
    }
    cout<<endl;
}
void test03()
{
    A ob1=100;
}

int main(int argc, char *argv[])
{
    test03();
    return 0;
}
