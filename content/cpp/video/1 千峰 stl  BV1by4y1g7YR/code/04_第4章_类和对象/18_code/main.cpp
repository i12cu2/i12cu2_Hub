#include<iostream>
#include<string.h>
using namespace std;
class Animal
{
public:
    int data;
};
class Sheep :virtual public Animal{};
class Tuo :virtual public Animal {};
class SheepTuo:public Sheep,public Tuo{};
int main()
{
    SheepTuo ob;
    memset(&ob, 0, sizeof(SheepTuo));

    cout << ob.data << endl;
    //cout << ob.Sheep::data << endl;
    //cout << ob.Tuo::data << endl;
}
