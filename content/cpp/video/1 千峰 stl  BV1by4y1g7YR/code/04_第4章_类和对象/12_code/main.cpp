#include <iostream>
#include <string>
using namespace std;
class Person
{
    friend ostream & operator<<(ostream &out, Person ob);
    friend istream &operator>>(istream &in, Person &ob);
private:
    int num;
    string name;
    float score;
public:
    Person(){}
    Person(int num, string name, float score):num(num),name(name),score(score){}
    //成员函数重载+
    Person operator+(Person ob)
    {
        Person tmp;
        tmp.num = this->num + ob.num;
        tmp.name = this->name + ob.name;
        tmp.score = this->score + ob.score;
        return tmp;
    }
    //成员函数重载==
    bool operator==(Person &ob)
    {
        if(num == ob.num && name==ob.name && score==ob.score)
            return true;
        return false;
    }
    //重载后置++ operator++(a,int)
    Person operator++(int)
    {
        //先保存 旧的值
        Person old = *this;//*this == lucy

        //lucy++ ==> lucy = lucy+1
        this->num = this->num +1;
        this->name = this->name+this->name;//（自定义操作）
        this->score = this->score+1;

        return old;//返回旧值
    }
    //重载前置++ operator++(a)
    Person operator++()
    {
        //先++
        this->num = this->num +1;
        this->name = this->name+this->name;//（自定义操作）
        this->score = this->score+1;

        //后使用
        return *this;
    }

};
ostream & operator<<(ostream &out, Person ob)
{
    out<<ob.num<<" "<<ob.name<<" "<<ob.score<<endl;
    return out;
}
istream &operator>>(istream &in, Person &ob)
{
    in>>ob.num>>ob.name>>ob.score;
    return in;
}

int main(int argc, char *argv[])
{
    Person lucy(100,"lucy", 88.8f);
    Person bob;
    //先++  后使用
    bob = ++lucy;//
    cout<<bob<<endl;
    cout<<lucy<<endl;
    return 0;
}
