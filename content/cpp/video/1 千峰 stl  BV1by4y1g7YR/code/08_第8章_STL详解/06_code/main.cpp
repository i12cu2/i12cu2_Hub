#include <iostream>
#include <map>
using namespace std;
class Person
{
    friend void test01();
    friend void printMapAll(map<int, Person> &m);
private:
    int num;
    string name;
    float score;
public:
    Person(){}
    Person(int num,string name, float score);
};
void printMapAll(map<int, Person> &m)
{
    map<int, Person>::const_iterator it;
    for(it=m.begin(); it!=m.end();it++)
    {
        //(*it) ==pair<int, Person>
        cout<<"学号:"<<(*it).first<<" 姓名:"<<(*it).second.name<<" \
分数:"<<(*it).second.score<<endl;
    }
}

void test01()
{
    map<int, Person> m;
    //方式1：
    m.insert(pair<int,Person>(103, Person(103,"lucy", 88.8f)));
    //方式2：推荐
    m.insert(make_pair(101,Person(101,"bob", 77.7f)));
    //方式3：
    m.insert( map<int, Person>::value_type( 102 , Person(102,"tom", 66.6f)));
    //方式4:
    m[104] = Person(104,"德玛", 99.9f);

    printMapAll(m);

    //假如key值存在  m[key]代表对应的实值
    cout<< m[107].num<<" "<<m[107].name<<" "<<m[107].score<<endl;

    cout<<"----------"<<endl;
    printMapAll(m);

    m.erase(104);
    cout<<"----------"<<endl;
    printMapAll(m);

    //查找key为103的数据
    map<int, Person>::const_iterator ret;
    ret = m.find(103);
    if(ret != m.end())
    {
        //*ret == pair<int,Person>
        cout<<(*ret).first<<" "<<(*ret).second.name<<" "<<(*ret).second.score<<endl;
    }
}

int main(int argc, char *argv[])
{
    test01();
    return 0;
}

Person::Person(int num, string name, float score)
{
    this->num = num;
    this->name = name;
    this->score = score;
}
