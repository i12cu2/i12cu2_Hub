#include <iostream>

using namespace std;
class Print
{
public:
    //重载函数调用运算符
    void operator()(char *str)
    {
        cout<<str<<endl;
    }
};
void test01()
{
    //对象和()结合 触发 operator()成员函数调用
    Print ob;
    //像函數調用  ==>  仿函数
    ob("hello world");

    Print()("hello world");
}
class Data
{
public:
    Data()
    {
        cout<<"无参构造"<<endl;
    }
    ~Data()
    {
        cout<<"析构函数"<<endl;
    }
    void func()
    {
        cout<<"func函数"<<endl;
    }
};
class SmartPointer
{
private:
    Data *p;
public:
    SmartPointer(){}
    SmartPointer(Data *p)
    {
        this->p = p;
    }
    ~SmartPointer()
    {
        delete p;
    }
    Data& operator*()
    {
       return *p;
    }
    Data* operator->()
    {
        return p;
    }
};

void test02()
{
    SmartPointer ob(new Data);
    ob.operator *().func();
    (*ob).func();

    ob.operator ->()->func();
    ob->func();
}

int main(int argc, char *argv[])
{
    test02();
    return 0;
}
