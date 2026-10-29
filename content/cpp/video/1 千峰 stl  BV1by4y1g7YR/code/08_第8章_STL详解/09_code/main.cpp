#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
#if 0

//第二步：公共继承binary_function   参数萃取
class PrintInt:public binary_function<int,int,void>
{
public:
    //第三步：整个函数加const修饰
    void operator()(int value, int tmp) const
    {
        cout<<"value="<<value<<" tmp="<< tmp<<endl;
    }
};



void test01()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);

    //for_each(v1.begin(), v1.end(),  myPrintInt);
    cout<<endl;
}

void myPrintInt(int value, int tmp)
{
    cout<<"value="<<value<<" tmp="<< tmp<<endl;
}
void test02()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);

    //for_each 提取容器的每个元素
    for_each(v1.begin(), v1.end(), bind2nd(ptr_fun(myPrintInt),100) );
    cout<<endl;
}

#endif
class Data
{
public:
    int data;
public:
    Data(){}
    Data(int d){
        data = d;
    }
    void printInt(int tmp)
    {
        cout<<"value="<<data+tmp<<endl;
    }
};

void test03()
{

    vector<Data> v1;
    v1.push_back(Data(10));
    v1.push_back(Data(30));
    v1.push_back(Data(50));
    v1.push_back(Data(70));
    v1.push_back(Data(90));

    //for_each 提取容器的每个元素
    for_each(v1.begin(), v1.end(), bind2nd(mem_fun_ref(&Data::printInt),100) );
    cout<<endl;
}

void test04()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);

    vector<int>::iterator ret;
    ret = find_if(v1.begin(), v1.end(), not1(bind2nd(greater<int>(), 30))  );
    if(ret != v1.end())
    {
        cout<<"找到相关数据:"<<*ret<<endl;
    }
}
void test05()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(40);
    v1.push_back(50);
    v1.push_back(20);
    v1.push_back(30);

    //lambda 表达式 c++11才支持
    //[]里面啥都不写 lambda不能识别 外部数据
    //[=] lambda能对 外部数据 读操作
    //[&] lambda能对 外部数据 读写操作
    for_each(v1.begin(), v1.end(), [&](int val){
        cout<<val<<" ";
    } );
    cout<<endl;

    sort(v1.begin(), v1.end(),not2(greater<int>()));

    for_each(v1.begin(), v1.end(), [&](int val){
        cout<<val<<" ";
    } );
    cout<<endl;
}
int main(int argc, char *argv[])
{
    test05();
    return 0;
}
