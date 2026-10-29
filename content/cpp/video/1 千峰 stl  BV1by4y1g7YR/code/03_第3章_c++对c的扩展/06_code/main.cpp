#include <iostream>

using namespace std;


//函數声明的时候 不要使用inline
int my_add(int x, int y);
void test01()
{
    cout<<my_add(100,200)<<endl;
}
//内联函数 在定义的时候使用inline
inline int my_add(int x, int y)
{
    return x+y;
}

void printFun(int a)
{
    cout<<"int"<<endl;
}
void printFun(int a, char b)
{
    cout<<"int char"<<endl;
}
void printFun(char a, int b)
{
    cout<<"char int"<<endl;
}
void printFun(char a)
{
    cout<<"char"<<endl;
}

void test02()
{
    printFun(10);
    printFun(10, 'a');
    printFun('a', 10);
    printFun('a');
}


//建议 在函数声明处 给出缺省值
int my_sub(int x, int y=20);
void test03()
{
    cout<<my_sub(200, 50)<<endl;
    cout<<my_sub(200)<<endl;

}
int my_sub(int x, int y)
{
    return x-y;
}

void myFun(int x)
{
    cout<<"A:int x="<<x<<endl;
}

void myFun(int x, int y=10)
{
    cout<<"B:int x="<<x<<" y="<<y<<endl;
}
void test04()
{
    myFun(10);
    myFun(10, 20);
}

int main(int argc, char *argv[])
{
    test04();
    return 0;
}
