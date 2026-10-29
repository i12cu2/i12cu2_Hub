#include <iostream>

using namespace std;

namespace A {
    int a = 10;
    int b = 20;
    int c = 30;
}

void test01()
{
    //只能说明A::a可以直接使用变量名a访问
    using A::a;//会和普通变量产生名字冲突
    //int a = 100;

    cout<<"a = "<<a<<endl;
}

namespace B {
    void fun01(void)
    {
        cout<<"B中的fun01 void"<<endl;
    }
    void fun01(int a)
    {
        cout<<"B中的fun01 int"<<endl;
    }
    void fun01(int a, int b)
    {
        cout<<"B中的fun01 int int"<<endl;
    }
}
void test02()
{
    //函数重载  命名空间的所有同名函数 都被申明 可用
    using B::fun01;

    fun01();
    fun01(10);
    fun01(10,20);
}

namespace C{
    int a = 10;
    int b = 20;
    int c = 30;
}
int a = 200;
void test03()
{
    //using namespace C;
    int a = 100;

    //std::cout<<"命名空间中的a = "<<C::a<<std::endl;
    cout<<"全部变量a = "<<::a<<endl;
    cout<<"局部变量a = "<<a<<endl;
}

struct stu
{
    int num;
    char name[32];

    //c++允许函数 作为结构体的成员
    void fun()
    {
        cout<<"stu 中的fun"<<endl;
    }
};

struct STU
{
    int num;
    char name[32];
};
//#include<string.h>
#include<cstring>
void test04()
{
    const STU lucy={100,"lucy"};
    STU *p = (STU *)&lucy;
    p->num = 200;
    strcpy(p->name, "bob");

    cout<<p->num<<" "<<p->name<<endl;
    cout<<lucy.num<<" "<<lucy.name<<endl;
}

namespace A {
//    #define N 10 不能 作为命名空间、结构体、类的成员
    const int N=10;//可以 作为命名空间、结构体、类的成员
}
void test05()
{
  cout<<A::N<<endl;
}

int main(int argc, char *argv[])
{
    test05();
    return 0;
}
