#include <iostream>

using namespace std;
class Print
{
public:
    void operator()(char *str)
    {
        cout<<str<<endl;
    }
};
void test01()
{
    Print ob;
    ob("hello world");
    Print()("hello wprld");
}

#include<vector>
#include<algorithm>
bool greaterThan30(int value)
{
    return value>30;
}
class GreaterThan30
{
public:
    bool operator()(int value)
    {
        return value>30;
    }
};

void test02()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);

    //find_if条件查找
    vector<int>::iterator ret;
    //普通函数提供策略  函数名
    //ret = find_if(v1.begin(), v1.end(), greaterThan30);
    //仿函数提供策略 类名称+（）
    ret = find_if(v1.begin(), v1.end(), GreaterThan30());
    if(ret != v1.end())
    {
        cout<<"寻找的结果:"<<*ret<<endl;
    }
}
void printVectorAll(vector<int> &v)
{
    vector<int>::iterator it;
    for(it=v.begin(); it!=v.end(); it++)
    {
        cout<<*it<<" ";
    }
    cout<<endl;
}

bool myGreaterInt(int v1, int v2)
{
    return v1>v2;
}
class MyGreaterInt
{
public:
    bool operator()(int v1, int v2)
    {
        return v1>v2;
    }
};
void test03()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(50);
    v1.push_back(30);
    v1.push_back(90);
    v1.push_back(70);

    printVectorAll(v1);

    sort(v1.begin(), v1.end(), greater<int>() );

    printVectorAll(v1);
}

void test04()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);

    //find_if条件查找
    vector<int>::iterator ret;

    ret = find_if(v1.begin(), v1.end(), bind2nd(greater<int>(), 30)  );
    if(ret != v1.end())
    {
        cout<<"寻找的结果:"<<*ret<<endl;
    }
}
int main(int argc, char *argv[])
{
    test04();
    return 0;
}
