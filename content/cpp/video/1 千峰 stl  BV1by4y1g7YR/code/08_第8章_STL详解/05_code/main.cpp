#include <iostream>
#include<set>
using namespace std;
class MyCompare
{
public:
    bool operator()(int v1, int v2)
    {
        return v1>v2;
    }
};
void printSetInt(set<int> &s)
{
    set<int>::iterator it;
    for(it=s.begin(); it!=s.end();it++)
    {
        cout<<*it<<" ";
    }
    cout<<endl;
}

void printSetInt(set<int,MyCompare> &s)
{
    set<int,MyCompare>::iterator it;
    for(it=s.begin(); it!=s.end();it++)
    {
        cout<<*it<<" ";
    }
    cout<<endl;
}


void test01()
{
    set<int,MyCompare> s1;
    s1.insert(30);
    s1.insert(10);
    s1.insert(20);
    s1.insert(20);
    s1.insert(40);
    printSetInt(s1);
}

class Person
{
    friend class MyComparePerson;
    friend ostream& operator<<(ostream &out, Person ob);
private:
    int num;
    string name;
    float score;
public:
    Person(){}
    Person(int num,string name, float score)
    {
        this->num = num;
        this->name = name;
        this->score = score;
    }
};
ostream& operator<<(ostream &out, Person ob)
{
    out<<ob.num<<" "<<ob.name<<" "<<ob.score<<endl;
    return out;
}

class MyComparePerson
{
public:
    bool operator()(Person ob1, Person ob2)
    {
        return ob1.num < ob2.num;
    }
};
void printSetInt(set<Person,MyComparePerson>  &s)
{
    set<Person,MyComparePerson> ::iterator it;
    for(it=s.begin(); it!=s.end();it++)
    {
        cout<<(*it);
    }
    cout<<endl;
}
void test02()
{
    set<Person,MyComparePerson>  s1;
    s1.insert(Person(100,"lucy", 88.8f));
    s1.insert(Person(104,"bob", 99.8f));
    s1.insert(Person(103,"tom", 77.8f));
    s1.insert(Person(101,"德玛", 66.8f));
    s1.insert(Person(105,"寒冰", 55.8f));
    printSetInt(s1);
}
void test03()
{
    set<int> s1;
    s1.insert(10);
    s1.insert(30);
    s1.insert(50);
    s1.insert(70);
    s1.insert(90);
    printSetInt(s1);

    set<int>::const_iterator ret;
    ret = s1.find(50);
    if(ret != s1.end())
    {
        cout<<"找到的结果:"<<*ret<<endl;
    }

    //count(key);//查找键key的元素个数  set容器的结果只能是0或1
    cout<<s1.count(50)<<endl;
}
void test04()
{
    set<int> s1;
    s1.insert(10);
    s1.insert(30);
    s1.insert(50);
    s1.insert(70);
    s1.insert(90);
    printSetInt(s1);

    set<int>::const_iterator ret;
    //lower_bound(keyElem);//返回第一个key>=keyElem元素的迭代器。(下限)
    ret = s1.lower_bound(50);
    if(ret !=s1.end())
    {
        cout<<"下限为:"<<*ret<<endl;
    }
    //upper_bound(keyElem);//返回第一个key>keyElem元素的迭代器（上限）
    ret = s1.upper_bound(50);
    if(ret !=s1.end())
    {
        cout<<"上限为:"<<*ret<<endl;
    }
    //equal_range(keyElem);//返回容器中key与keyElem相等的上下限的两个迭代器
    //返回值类型为pair 对组
    pair< set<int>::const_iterator, set<int>::const_iterator> p;
    p = s1.equal_range(50);
    if(p.first  != s1.end())
    {
        cout<<"下限为:"<<*(p.first)<<endl;
    }
    if(p.second != s1.end())
    {
        cout<<"上限为:"<<*(p.second)<<endl;
    }
}
void test05()
{
    set<int> s1;
    pair<set<int>::const_iterator, bool> ret;
    ret = s1.insert(10);
    if(ret.second == true)
    {
        cout<<"第一次插入成功"<<endl;
    }
    else
    {
        cout<<"第一次插入失败"<<endl;
    }

    ret = s1.insert(10);
    if(ret.second == true)
    {
        cout<<"第二次插入成功"<<endl;
    }
    else
    {
        cout<<"第二次插入失败"<<endl;
    }
}

void printSetInt(multiset<int>  &s)
{
    multiset<int>::iterator it;
    for(it=s.begin(); it!=s.end();it++)
    {
        cout<<(*it)<<" ";
    }
    cout<<endl;
}
void test06()
{
    multiset<int> s1;
    s1.insert(10);
    s1.insert(30);
    s1.insert(10);
    s1.insert(70);
    s1.insert(10);
    printSetInt(s1);

    cout<<s1.count(10)<<endl;
}
void test07()
{
    //方式1
    pair<int, string> p1(10086,"移动");
    pair<int, string> p2(10010,"联通");
    pair<int, string> p3(10000,"电信");

    //方式2：（推荐）
    pair<int, string> p4=make_pair(9527,"星爷");

    cout<<p4.first<<" "<<p4.second<<endl;
}

int main(int argc, char *argv[])
{
    test07();
    return 0;
}
