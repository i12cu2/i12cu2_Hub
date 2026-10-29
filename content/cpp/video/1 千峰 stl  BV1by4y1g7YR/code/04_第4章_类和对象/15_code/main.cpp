#include <iostream>

using namespace std;
class Base
{
public:
    int a;
public:
    Base()
    {
        cout<<"父类默认构造"<<endl;
    }
    Base(int a)
    {
        this->a = a;
        cout<<"父类有参构造"<<endl;
    }
    ~Base()
    {
        cout<<"父类析够"<<endl;
    }
};
class Other
{
public:
    int b;
public:
    Other()
    {
        cout<<"Other默认构造"<<endl;
    }
    Other(int b)
    {
        this->b = b;
        cout<<"Other有参构造"<<endl;
    }
    ~Other()
    {
        cout<<"Other析够"<<endl;
    }
};

class Son:public Base
{
public:
    Other ob;
    int c;
public:
    Son()
    {
        cout<<"Son构造"<<endl;
    }
    //父类写类名称   成员对象用对象名
    Son(int a, int b, int c):Base(a), ob(b)
    {
        this->c = c;
        cout<<"Son有参构造"<<endl;
    }
    ~Son()
    {
        cout<<"Son析够"<<endl;
    }
};

void test01()
{
    Son ob(10,20,30);
}

int main(int argc, char *argv[])
{
    test01();
    return 0;
}
