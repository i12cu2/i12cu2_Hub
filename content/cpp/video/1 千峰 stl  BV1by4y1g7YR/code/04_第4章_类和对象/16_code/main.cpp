#include <iostream>

using namespace std;
class Base1
{
public:
    int a;
    Base1(int a):a(a){}
};
class Base2
{
public:
    int a;
    Base2(int a):a(a){}
};


class Son:public Base1, public Base2
{
public:
    //int a;
    Son(int a, int b):Base1(a),Base2(b){}
};

void test01()
{
    Son ob(10,20);
    //cout<<ob.a<<endl;//×ÓÀàa
    cout<<ob. Base1::a<<endl;//Base1 a
    cout<<ob.Base2::a<<endl;//Base2 a
}

int main(int argc, char *argv[])
{
    test01();
    return 0;
}
