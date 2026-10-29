#include <iostream>
#include <vector>
#include <string>
#include <stdlib.h>
#include <time.h>
#include <map>
using namespace std;
class Person
{
    friend void showDepartmentPerson(multimap<int,Person> &m);
    friend void personJoinDepartment(vector<Person> &v, multimap<int,Person> &m);
private:
    string name;
    int age;
    int money;
    string tel;
public:
    Person(){}
    Person(string name, int age, int money, string tel);
};

void createVectorPerson(vector<Person> &v);
void personJoinDepartment(vector<Person> &v, multimap<int,Person> &m);
void showDepartmentPerson(multimap<int,Person> &m);
int main(int argc, char *argv[])
{
    //创建vector容器 存放 员工
    vector<Person> v;
    createVectorPerson(v);

    //5名员工加入部门
    multimap<int, Person> m;
    personJoinDepartment(v, m);

    //显示部门员工
    showDepartmentPerson(m);

    return 0;
}

Person::Person(string name, int age, int money, string tel)
{
    this->name = name;
    this->age = age;
    this->money = money;
    this->tel = tel;
}

void createVectorPerson(vector<Person> &v)
{
    //设置随机数种子
    srand(time(NULL));
    int i=0;
    for(i=0;i<5; i++)
    {
        string seedName="ABCDE";
        string tmpName = "员工";
        tmpName += seedName[i];
        int age = 20+i;
        int money = 15000+rand()%10*1000;
        string tel = to_string(rand());

        v.push_back(Person(tmpName,age,money,tel));
    }
    return;
}

void personJoinDepartment(vector<Person> &v, multimap<int,Person> &m)
{
    vector<Person>::iterator it;
    for(it=v.begin(); it != v.end(); it++)
    {
        //*it == Person
        cout<<"请输入["<<(*it).name<<"]加入的部门0(销售)、1(研发)、2(财务):";
        int op = 0;
        cin>>op;

        m.insert(make_pair(op, *it));
        //(m[op]) = (*it);
    }
}

void showDepartmentPerson(multimap<int,Person> &m)
{
    cout<<"请选择你要显示的部门0(销售)、1(研发)、2(财务):";
    int op = 0;
    cin>>op;

    switch (op) {
    case 0:
        cout<<"-------销售部门员工如下----------"<<endl;
        break;
    case 1:
        cout<<"-------研发部门员工如下----------"<<endl;
        break;
    case 2:
        cout<<"-------财务部门员工如下----------"<<endl;
        break;
    }

    //0 1 1 1 2
    //寻找op的位置
    multimap<int,Person>::const_iterator ret;
    ret = m.find(op);
    if(ret == m.end())
        return;
    //统计op的个数
    int count = m.count(op);

    //从op的位置 按照个数 逐个遍历
    int i=0;
    for(i=0;i<count; i++, ret++)
    {
        //*ret == pair<int, Person>
        cout<<"\t"<<(*ret).second.name<<" "<<(*ret).second.age<<" "\
           <<(*ret).second.money<<" "<<(*ret).second.tel<<endl;
    }
    return;
}
