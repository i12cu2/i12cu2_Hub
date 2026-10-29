#include <iostream>

using namespace std;
void test01()
{
    int *p = NULL;

    //申请int空间 并初始化为100
    p = new int(100);//堆区空间
    cout<<"*p = "<<*p<<endl;

    delete p;
}
void test02()
{
    int *arr = NULL;

    //申请数组 5个int元素
    //arr = new int[5];//堆区空间
    arr = new int[5]{10,20,30,40,50};
    int i=0;
    for(i=0;i<5;i++)
    {
        cout<<arr[i]<<" ";
    }
    cout<<endl;

    //如果new有[]  delete就必须有[]
    delete [] arr;
}
#include<stdlib.h>
class A
{
public:
    int mA;
public:
    A()
    {
        cout<<"无参构造"<<endl;
    }
    A(int a)
    {
        mA = a;
        cout<<"有参构造 mA="<<mA<<endl;
    }
    ~A()
    {
        cout<<"析构函数 mA="<<mA<<endl;
    }
};
void test03()
{
#if 0  //malloc free
    A *p = (A *)malloc(sizeof(A));

    p->mA = 100;
    cout<<p->mA<<endl;

    free(p);

#endif

#if 1
    A *p = new A(100);

    //p->mA = 100;
    cout<<p->mA<<endl;

    delete p;
#endif
}
void test04()
{
    //每个元素 默认调用无参构造
    //A *arr = new A[5];

    A *arr = new A[5]{A(10), A(20),A(30),A(40),A(50)};

    delete  [] arr;
}

int main(int argc, char *argv[])
{
    test04();
    return 0;
}
