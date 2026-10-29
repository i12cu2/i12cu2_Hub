#include <iostream>
#include <vector>
using namespace std;
void test01()
{
    vector<int> v1;
    v1.reserve(1000);//预留空间

    cout<<"容量:"<<v1.capacity()<<" 大小:"<<v1.size()<<endl;
    vector<int>::iterator it;
    int i=0;
    int count = 0;
    for(i=1;i<=1000;i++)
    {
        v1.push_back(1);
        if(it != v1.begin())
        {
            count++;
            cout<<"第"<<count<<"次开辟空间，容量为："<<v1.capacity()<<endl;
            it=v1.begin();
        }
    }
}
void printVectorInt(vector<int> &v)
{
    vector<int>::iterator it;
    for(it=v.begin(); it!=v.end();it++)
    {
        cout<<*it<<" ";
    }
    cout<<endl;
}

void test02()
{
    vector<int> v1(5,100);
    printVectorInt(v1);

    vector<int> v2 = v1;
    printVectorInt(v2);

    vector<int> v3(v1.begin(), v1.end());
    printVectorInt(v3);

    vector<int> v4;
//    v4 = v3;
    v4.assign(10,10);
    printVectorInt(v4);

    //交换
    v3.swap(v4);
    printVectorInt(v3);
    printVectorInt(v4);

    cout<<"大小:"<<v4.size()<<" 容量:"<<v4.capacity()<<endl;
    //容器是否为空
    vector<int> v5;
    if(v5.empty())
    {
        cout<<"空"<<endl;
    }
    else
    {
        cout<<"非空"<<endl;
    }

    vector<int> v6(10, 30);
    cout<<"大小:"<<v6.size()<<" 容量:"<<v6.capacity()<<endl;
    printVectorInt(v6);
    //v6.resize(20);//过大补0
    //v6.resize(20, 50);//过大补50
    v6.resize(32);
    cout<<"大小:"<<v6.size()<<" 容量:"<<v6.capacity()<<endl;
    printVectorInt(v6);
}
void test03()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(20);
    v1.push_back(30);
    v1.push_back(40);
    v1.push_back(50);

    cout<<"头元素:"<<v1.front()<<"   尾元素:"<<v1.back()<<endl;
    //at越界抛出异常  【】越界不会抛出异常
    cout<<v1.at(1)<<" "<<v1[1]<<endl;
    v1.at(1)=200;
    v1[3]=300;
    printVectorInt(v1);//10 200 30 300 50

    v1.pop_back();//尾删
    printVectorInt(v1);//10 200 30 300
    v1.insert( v1.begin()+2, 3, 500 );
    printVectorInt(v1);//10 200 500 500 500 30 300
    v1.erase(v1.begin()+2, v1.begin()+5 );
    printVectorInt(v1);//10 200 30 300
    v1.clear();
    cout<<"大小:"<<v1.size()<<" 容量:"<<v1.capacity()<<endl;
}
void test04()
{
    vector<int> v1;
    v1.reserve(1000);
    v1.assign(5,100);
    cout<<"大小:"<<v1.size()<<" 容量:"<<v1.capacity()<<endl;
    //v1.resize(3);
    vector<int>(v1).swap(v1);
    cout<<"大小:"<<v1.size()<<" 容量:"<<v1.capacity()<<endl;
}
void test05()
{
    vector<int> v1(5,10);
    vector<int> v2(5,100);
    vector<int> v3(5,1000);

    //需求：定义一个容器 存放v1 v2 v3
    vector< vector<int> > v;
    v.push_back(v1);
    v.push_back(v2);
    v.push_back(v3);

    //遍历
    vector< vector<int> >::iterator it;
    for(it=v.begin(); it!=v.end(); it++)
    {
        //*it == vector<int>
        vector<int>::iterator mit;
        for(mit=(*it).begin();mit!=(*it).end();mit++ )
        {
            //*mit == int
            cout<<*mit<<" ";
        }
        cout<<endl;
    }
}
#include<algorithm>//算法头文件
bool myCompare(int value1, int value2)
{
    return value1<value2;
}

void test06()
{
    vector<int> v1;
    v1.push_back(20);
    v1.push_back(60);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(40);
    v1.push_back(10);
    printVectorInt(v1);

    //sort算法排序
    sort(v1.begin(), v1.end());
    //sort(v1.begin(), v1.end(), greater<int>());
    //sort(v1.begin(), v1.end(), myCompare);
    printVectorInt(v1);
}
class Person
{
    friend void printVectorPerson(vector<Person>  &v);
    friend bool myComparePerson(const Person &ob1,  const Person &ob2);
private:
    int num;
    string name;
    float score;
public:
    Person(){}
    Person(int num, string name, float score)
    {
        this->num = num;
        this->name = name;
        this->score = score;
    }
#if 0
    //方法2：重载自定义数据的<运算符
    bool operator<(const Person &ob)
    {
        return this->num < ob.num;
    }
#endif
};
void printVectorPerson(vector<Person>  &v)
{
    vector<Person>::iterator it;
    for(it=v.begin(); it!=v.end(); it++)
    {
        //*it == Person
        cout<<(*it).num<<" "<<(*it).name<<" "<<(*it).score<<endl;
    }
}
//方法1：对于自定义容器排序 必须实现 排序规则
bool myComparePerson(const Person &ob1,  const Person &ob2)
{
    if(ob1.num == ob2.num)
        return ob1.score<ob2.score;
    return ob1.num > ob2.num;
}

void test07()
{
    vector<Person> v;

    v.push_back(Person(100, "lucy", 88.8f));
    v.push_back(Person(103, "bob", 99.8f));
    v.push_back(Person(103, "tom", 77.8f));
    v.push_back(Person(103, "德玛", 88.8f));
    v.push_back(Person(101, "小法", 66.8f));

    printVectorPerson(v);
    //方法1：对于自定义容器排序 必须实现 排序规则
    sort(v.begin(), v.end(), myComparePerson);
    //方法2：重载自定义数据的<运算符
    //sort(v.begin(), v.end());
    cout<<"--------------"<<endl;
    printVectorPerson(v);
}

int main(int argc, char *argv[])
{
    test07();
    return 0;
}
