#include <iostream>

using namespace std;
void test01()
{
    int a = 10;
    //需求：给变量a 取个别名叫b
    //在定义的时候 &修饰变量为引用   b就是a的别名
    //系统不会为引用 开辟独立空间
    int &b = a;//引用必须初始化

    cout<<"a = "<<a<<endl;
    cout<<"b = "<<b<<endl;

    b = 100;
    cout<<"a = "<<a<<endl;
    cout<<"b = "<<b<<endl;

    cout<<"&a = "<<&a<<endl;
    cout<<"&b = "<<&b<<endl;
}
void test02()
{
    int arr[5]={10,20,30,40,50};
    int n = sizeof(arr)/sizeof(arr[0]);

    int (&myArr)[5] = arr;
    int i=0;
    for(i=0;i<n;i++)
    {
        cout<<myArr[i]<<" ";
    }
    cout<<endl;
}
void test03()
{
    int num = 10;
    int *p = &num;

    int* &my_p = p;
    cout<<"*p = "<<*p<<endl;
    cout<<"*my_p = "<<*my_p<<endl;
}

void fun01(void)
{
    cout<<"fun01"<<endl;
}

void test04()
{
    void (&my_fun)(void) = fun01;
    my_fun();
}

void test05()
{
    int a = 10;
    int b = 20;

    //a的别名为num
    int &num = a;

    //将b的值赋值给num 也就是a的空间
    num = b;
    cout<<"a = "<<a<<endl;
    cout<<"num = "<<num<<endl;
}

void swap01(int *p1, int *p2)
{
    int tmp = *p1;
    *p1 = *p2;
    *p2 = tmp;
}
void swap02(int &x, int &y)//int &x=a; int &y=b;
{
    int tmp = x;
    x = y;
    y=tmp;
}

void test06()
{
    int a = 10;
    int b = 20;
    cout<<"a = "<<a<<" "<<", b = "<<b<<endl;
    //swap01(&a, &b);
    swap02(a, b);
    cout<<"a = "<<a<<" "<<", b = "<<b<<endl;
}

struct STU
{
    int num;
    char name[32];
};
void printStu01(STU tmp)//tmp占 空间
{
    cout<<tmp.num<<" "<<tmp.name<<endl;
}
void printStu02(STU &tmp)//tmp不占 空间
{
    cout<<tmp.num<<" "<<tmp.name<<endl;
}
void test07()
{
   STU lucy={100, "lucy"};
   printStu02(lucy);
}

int& getData(void)
{
    static int num = 100;

    //不要返回局部变量的引用
    return num;//返回num 外界就是给num取别名
}

void test08()
{
    //b是num的别名
   int &b = getData();
   cout<<"b = "<<b<<endl;
}

struct stu
{
    stu& printStu(stu &ob, int value)
    {
        cout<<value<<" ";
        return ob;
    }
};

void test09()
{
    stu ob1;
    ob1.printStu(ob1, 100).printStu(ob1, 200).printStu(ob1, 300);
}

void test10()
{
    //int &a = 10;//err
    const int &a = 10;//a就是10的别名
//    a = 100;//err
}

void printInt(const int &a)
{
    //a = 200;//err
    cout<<"a = "<<a<<endl;
}

void test11()
{
   int num = 100;
   printInt(num);
}

int main(int argc, char *argv[])
{
    test11();
    return 0;
}
