#include <iostream>

using namespace std;
class Data1
{
public:
    Data1& myPrintf(char *str)
    {
        cout<<str<<" ";
        return *this;//返回调用该成员函数的对象
    }
};
void test01()
{
    Data1().myPrintf("hehe").myPrintf("haha").myPrintf("xixix");
}
class Data2
{
public:
    int a;
    int b;
    mutable int c;
public:
    Data2(int a, int b,int c)
    {
        this->a = a;
        this->b = b;
        this->c = c;
    }
    //const 修饰成员函数为只读（该成员函数不允许对 成员数据 赋值） mutable修饰的成员除外
    void showData(void) const
    {
        //a = 100;//err
        c=100;
        cout<<a<<" "<<b<<" "<<c<<endl;
    }
};
void test02()
{
    Data2 ob1(10,20,30);
    ob1.showData();
}

int main(int argc, char *argv[])
{
    test02();
    return 0;
}
