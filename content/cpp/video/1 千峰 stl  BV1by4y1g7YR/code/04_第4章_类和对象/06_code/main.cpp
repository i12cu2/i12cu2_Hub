#include <iostream>

using namespace std;

class Data
{
public:
    int a;//普通成员数据
    //类中定义
    static int b;//静态成员数据
};
//类外初始化
int Data::b=100;

void test01()
{
    //静态成员数据 通过类名称直接访问（属于类）
    cout<<Data::b<<endl;

    //静态成员数据 通过对象访问(共享)
    Data ob1;
    cout<<ob1.b<<endl;

    ob1.b = 200;
    Data ob2;
    ob2.b = 300;
    cout<<Data::b<<endl;//300
}

class Data2
{
public:
    int mA;
    static int count;
public:
    Data2()
    {
        count++;
    }
    Data2(int a)
    {
        mA = a;
        count++;
    }

    Data2(const Data2 &ob)
    {
        count++;
    }
    ~Data2()
    {
       count--;
    }
};
int Data2::count=0;
void test02()
{
    Data2 ob1;
    Data2 ob2(10);
    Data2 ob3 = ob2;
    cout<<"对象个数:"<<Data2::count<<endl;//3
    {
        Data2 ob4;
        Data2 ob5;
        cout<<"对象个数:"<<Data2::count<<endl;//5
    }
    cout<<"对象个数:"<<Data2::count<<endl;//3
}

class Data3
{
private:
    int data;
    static int a;
public:
    static int getA()
    {
        data = 10;//err 静态成员函数 只能操作 静态成员数据 而data为普通成员数据
        return a;
    }
};
int Data3::a = 100;
void test03()
{
    cout<<Data3::getA()<<endl;
}

int main(int argc, char *argv[])
{
    test03();
    return 0;
}
