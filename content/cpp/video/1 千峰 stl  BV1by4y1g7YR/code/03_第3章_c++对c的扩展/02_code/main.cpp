#include <iostream>

using namespace std;
int a = 10;//全局区
void test01()
{
    int a = 20;//栈
    cout<<"局部变量a = "<<a<<endl;
    cout<<"全局变量a = "<<::a<<endl;
}

namespace A {
    //定义变量、函数、类型等
    int data = 10;
    namespace B {
        int data = 20;
    }
}

void test02()
{
    cout<<"A::data = "<<A::data<<endl;
    cout<<"A::B::data = "<<A::B::data<<endl;
}

namespace C {
    int data= 10;
}
//1000行代码
namespace C {
    void func(void)
    {
        cout<<"C中的func函数"<<endl;
    }
}
void test03()
{
    cout<<"data = "<<C::data<<endl;
    C::func();
}


namespace D {
    //在命名空间内申明:说明fun01 fun02属于D命名空间
    void fun01();
    void fun02();
}

//命名空间的成员函数 外部实现 必须加作用域
void D::fun01()
{
    cout<<"D中的fun01"<<endl;
}
void D::fun02()
{
    cout<<"D中的fun02"<<endl;
}


void test04()
{
    D::fun01();
    D::fun02();
}

//static int num = 100;只能在当前源文件使用
namespace{
    int num = 100;
}
void test05()
{
    cout<<"num = "<<num<<endl;
    cout<<"num = "<<::num<<endl;
}

namespace veryLongName {
    int a =100;
    int b = 200;
}
//给veryLongName取别名shortName
namespace shortName = veryLongName;
void test06()
{
    cout<<"a = "<<shortName::a<<endl;
    cout<<"b = "<<veryLongName::b<<endl;
}

int main(int argc, char *argv[])
{
    test06();
    return 0;
}
