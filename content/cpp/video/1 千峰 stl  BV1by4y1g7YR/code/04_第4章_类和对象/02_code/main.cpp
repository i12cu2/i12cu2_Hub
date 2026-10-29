#include <iostream>

using namespace std;
class Data1
{
public:
    int mA;
public:
    //无参构造函数
    Data1()
    {
        mA=0;
        cout<<"无参构造函数"<<endl;
    }


    //有参构造函数
    Data1(int a)
    {
        mA=a;
        cout<<"有参构造函数 mA="<<mA<<endl;
    }

    //析构函数
    ~Data1()
    {
        cout<<"析构函数 mA="<<mA<<endl;
    }
};
void test01()
{
    //隐式调用无参构造函数（推荐）
    Data1 ob1;
    cout<<ob1.mA<<endl;
    //显示调用无参构造函数
    Data1 ob2 = Data1();

    //隐式调用有参构造函数（推荐）
    Data1 ob3(10);

    //显示调用有参构造函数
    Data1 ob4 = Data1(10);

    //匿名对象(无参)
    Data1();
    Data1(20);

    //构造函数隐式转换（类中只有一个数据成员）
    Data1 ob5 = 100;
}
//Data1 ob1(10);
void test02()
{
    Data1 ob2(20);
    {
        Data1(200);
        Data1 ob3(30);
    }
    Data1 ob4(40);
}

#include<stdlib.h>
#include<string.h>
class Data2
{
public:
    char *name;//指针成员
public:
    Data2()
    {
        name=NULL;
    }

    Data2(char *str)
    {
        name = (char *)calloc(1, strlen(str)+1);
        strcpy(name, str);
        cout<<"有参构造 name="<<name<<endl;
    }
    ~Data2()
    {
        cout<<"析构函数name = "<<name<<endl;
        if(name != NULL)
        {
            free(name);
            name=NULL;
        }
    }
};
void test03()
{
    Data2 ob1("hello world");
}

class Data4
{
public:
    int mA;
public:
#if 1
    Data4()
    {
        mA = 0;
        cout<<"无参构造 mA = "<<mA<<endl;
    }
#endif
#if 1
    Data4(int a)
    {
        mA = a;
        cout<<"有参构造 mA = "<<mA<<endl;
    }
#endif
#if 1
    Data4(const Data4 &ob)//ob就是旧对象的别名
    {
        //一旦实现 了拷贝构造 必须完成赋值动作
        mA = ob.mA;
        cout<<"拷贝构造函数"<<endl;
    }
#endif
    ~Data4()
    {
        cout<<"析构函数 mA = "<<mA<<endl;
    }
};
Data4 getObject(void)
{
    Data4 ob1(10);
    cout << "A:" << &ob1 << endl;
    return ob1;
}

void test04()
{
    Data4 ob2 = getObject();
    cout << "B:" << &ob2 << endl;
}
class Data5
{
public:
    char *name;
public:
    Data5()
    {
        name=NULL;
    }
    Data5(char *str)
    {
        name = (char *)calloc(1, strlen(str)+1);
        strcpy(name, str);
        cout<<"有参构造 name="<<name<<endl;
    }
    ~Data5()
    {
        cout<<"析构函数name = "<<name<<endl;
        if(name != NULL)
        {
            free(name);
            name=NULL;
        }
    }
};
void test05()
{
    Data5 ob1("hello world\n");
    Data5 ob2 = ob1;
}

int main(int argc, char *argv[])
{
    test05();
    return 0;
}
