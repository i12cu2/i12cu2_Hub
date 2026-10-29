#include <iostream>

using namespace std;

//T只能对当前函数有效  typename可以换成class
template<typename T>
void swapAll(T &a, T &b)
{
    T tmp = a;
    a = b;
    b=tmp;
    cout<<"函数模板"<<endl;
    return;
}

void swapAll(int &a, int &b)
{
    int tmp = a;
    a = b;
    b=tmp;
    cout<<"普通函数"<<endl;
    return;
}
void test01()
{
    int a = 10, b = 20;
    //强制使用函数模板
    swapAll(a, b);
    cout<<a<<" "<<b<<endl;

}
#if 1
template<typename T>
void myPrintAll(T a)
{
    cout<<a<<endl;
    cout<<"函数模板"<<endl;
}

template<typename T>
void myPrintAll(T a, T b)
{
    cout<<a<<" "<<b<<endl;
    cout<<"函数模板"<<endl;
}
#endif
void myPrintAll(int a, int b)
{
   cout<<a<<" "<<b<<endl;
    cout<<"普通函数"<<endl;
}

void test02()
{
    myPrintAll(10, 20);//普通函数
    myPrintAll('a','b');//函数模板
    myPrintAll(10,'b');//普通函数
    //支持自动类型转换
    myPrintAll<int>(10,'b');
}

int main(int argc, char *argv[])
{
    test02();
    return 0;
}
