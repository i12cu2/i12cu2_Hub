#include <iostream>
#include "myarray.hpp"
using namespace std;
class Person
{
    friend ostream& operator<<(ostream& out, Person ob);
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
    bool operator>(const Person &ob)
    {
        return num>ob.num;
    }
};
ostream& operator<<(ostream& out, Person ob)
{
    int i=0;

    out<<ob.num<<" "<<ob.name<<" "<<ob.score<<endl;
    return out;
}

int main(int argc, char *argv[])
{
    MyArray<int> ob1(5);
    ob1.pushBack(10);
    ob1.pushBack(30);
    ob1.pushBack(20);
    ob1.pushBack(50);
    ob1.pushBack(40);

    cout<<ob1<<endl;
    ob1.sortArray();
    cout<<ob1<<endl;

    MyArray<char> ob2(5);
    ob2.pushBack('A');
    ob2.pushBack('C');
    ob2.pushBack('D');
    ob2.pushBack('B');
    ob2.pushBack('F');

    cout<<ob2<<endl;
    ob2.sortArray();
    cout<<ob2<<endl;

    MyArray<Person> ob3;
    ob3.pushBack(Person(100,"lucy", 88.8f));
    ob3.pushBack(Person(103,"bob", 89.9f));
    ob3.pushBack(Person(105,"tom", 98.8f));
    ob3.pushBack(Person(102,"µÂÂê", 99.8f));

    cout<<ob3<<endl;
    ob3.sortArray();
    cout<<ob3<<endl;
    return 0;
}
