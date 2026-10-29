#include <iostream>

using namespace std;
class Base{};
class Son:public Base{};
class Other{};

void test01()
{
    //基本类型：
    int num = static_cast<int>(3.14);
    //上行转换：
    Base *p1 = static_cast<Base *>(new Son);
    //下行转换：
    Son *p2 = static_cast<Son *>(new Base);
    //不相关类型转换：
    //Base *p3 = static_cast<Base *>(new Other);
}
void test02()
{
    //基本类型：
    //int num = dynamic_cast<int>(3.14);
    //上行转换：
    Base *p1 = dynamic_cast<Base *>(new Son);
    //下行转换：
    //Son *p2 = dynamic_cast<Son *>(new Base);
    //不相关类型转换：
    //Base *p3 = dynamic_cast<Base *>(new Other);
}
void test03()
{
    const int *p1;
    int *p2 = const_cast<int *>(p1);

    const int &ob = 10;
    int &ob1 = const_cast<int &>(ob);

    int *p3;
    const *p4 = const_cast<int *>(p3);

    int data = 10;
    const int &ob2 = const_cast<const int &>(data);
}
void test04()
{
    //基本类型：不支持
    int num = reinterpret_cast<int>(3.14f);
    //基本类型指针：支持
    float *q;
    int *p = reinterpret_cast<int *>(q);
    //上行转换：支持
    Base *p1 = reinterpret_cast<Base *>(new Son);
    //下行转换：支持
    Son *p2 = reinterpret_cast<Son *>(new Base);
    //不相关类型转换：支持
    Base *p3 = reinterpret_cast<Base *>(new Other);
}
int main(int argc, char *argv[])
{
    test04();
    return 0;
}
