#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
void printVectorInt(vector<int> &v)
{
    vector<int>::iterator it;
    for(it=v.begin(); it!=v.end(); it++)
    {
        cout<<*it<<" ";
    }
    cout<<endl;
}
int myTransInt01(int val)
{
    return val;
}

void test01()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(70);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(90);


    vector<int> v2;
    v2.resize(v1.size());
    transform(v1.begin(), v1.end(), v2.begin(), myTransInt01);
    printVectorInt(v2);
}

void test02()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(70);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(90);

    vector<int>::iterator ret;
    ret = find(v1.begin(), v1.end(), 30);
    if(ret != v1.end())
    {
        cout<<"查找的数据:"<<*ret<<endl;
    }
}

#include<string>
class Person
{
    friend void test03();
private:
    int num;
    string name;
public:
    Person(){}
    Person(int num, string name){
        this->num = num;
        this->name = name;
    }
    bool operator==(const Person &ob)
    {
        return ((this->num == ob.num) && (this->name == ob.name));
    }
};

void test03()
{
    vector<Person> v1;
    v1.push_back(Person(100,"lucy"));
    v1.push_back(Person(101,"bob"));
    v1.push_back(Person(102,"tom"));

    vector<Person>::iterator ret;
    //find 查找自定义数据类型  需要重载==
    ret = find(v1.begin(), v1.end(), Person(101,"bob"));
    if(ret != v1.end())
    {
        cout<<"查找的数据:"<<(*ret).num<<" "<<(*ret).name<<endl;
    }
}

void test04()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(70);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(90);

    vector<int>::iterator ret;
    ret = find_if(v1.begin(), v1.end(),  bind2nd(greater<int>(),30)  );
    if(ret != v1.end())
    {
        cout<<"查找的数据:"<<*ret<<endl;
    }
}
void test05()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(20);
    v1.push_back(20);
    v1.push_back(30);
    v1.push_back(30);
    vector<int>::iterator ret;

    ret = adjacent_find(v1.begin(),v1.end());
    if(ret != v1.end())
    {
        cout<<"第一个相邻重复的元素:"<<*ret<<endl;
    }
}
void test06()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(70);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(90);
    sort(v1.begin(), v1.end());

    bool ret;
    ret = binary_search(v1.begin(), v1.end(),  30);
    if(ret)
    {
        cout<<"存在该数据"<<endl;
    }
}

void test07()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(70);
    v1.push_back(30);
    v1.push_back(90);

    cout<<count(v1.begin(), v1.end(), 30)<<endl;
}
void test08()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(70);
    v1.push_back(30);
    v1.push_back(90);

    cout<<count_if(v1.begin(), v1.end(), bind2nd(greater<int>(), 10) )<<endl;
}
void test09()
{
    int i=8;
    printf("%d %d %d\n", ++i, --i, i++);
}
void test10()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);

    vector<int> v2;
    v2.push_back(20);
    v2.push_back(40);
    v2.push_back(60);
    v2.push_back(70);
    v2.push_back(80);

    vector<int> v3;
    v3.resize(v1.size() + v2.size());
    merge(v1.begin(), v1.end(), v2.begin(), v2.end(), v3.begin());
    printVectorInt(v3);
}
#include<stdlib.h>
#include<time.h>
void test11()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);
    printVectorInt(v1);
    //设置随机数种子
    srand(time(NULL));
    //洗牌
    random_shuffle(v1.begin(), v1.end());
    printVectorInt(v1);
}
void test12()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);
    printVectorInt(v1);
    //洗牌
    reverse(v1.begin(), v1.end());
    printVectorInt(v1);
}

void test13()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);
    vector<int> v2;
    v2.resize(v1.size());

    copy(v1.begin(), v1.end(), v2.begin());
    printVectorInt(v2);
}
#include<iterator>
void test14()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);

    copy(v1.begin(), v1.end(), ostream_iterator<int>(cout, " ") );
    cout<<endl;
}
void test15()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);

    copy(v1.begin(), v1.end(), ostream_iterator<int>(cout, " ") );
    cout<<endl;

    replace(v1.begin(), v1.end(), 30, 3000);

    copy(v1.begin(), v1.end(), ostream_iterator<int>(cout, " ") );
    cout<<endl;
}
class GreaterThan30
{
public:
    bool operator()(int value)
    {
        return value>30;
    }
};

void test16()
{
    vector<int> v1;
    v1.push_back(10);
    v1.push_back(30);
    v1.push_back(50);
    v1.push_back(70);
    v1.push_back(90);

    copy(v1.begin(), v1.end(), ostream_iterator<int>(cout, " ") );
    cout<<endl;

    replace_if(v1.begin(), v1.end(), GreaterThan30() , 3000);

    copy(v1.begin(), v1.end(), ostream_iterator<int>(cout, " ") );
    cout<<endl;
}
void test17()
{
   vector<int> v1;
   v1.resize(5);

   fill(v1.begin(), v1.end(), 10);

   copy(v1.begin(), v1.end(), ostream_iterator<int>(cout, " ") );
   cout<<endl;
}

void test18()
{
    vector<int> v1;
    v1.push_back(1);
    v1.push_back(3);
    v1.push_back(5);
    v1.push_back(7);
    v1.push_back(9);

    vector<int> v2;
    v2.push_back(7);
    v2.push_back(9);
    v2.push_back(11);
    v2.push_back(13);
    v2.push_back(15);

    vector<int> v3;
    v3.resize( v1.size());

    vector<int>::iterator ret;
    ret = set_difference(v1.begin(), v1.end(), v2.begin(),v2.end(), v3.begin());
    copy(v3.begin(), ret, ostream_iterator<int>(cout, " ") );
    cout<<endl;
}

int main(int argc, char *argv[])
{
    test18();
    return 0;
}
