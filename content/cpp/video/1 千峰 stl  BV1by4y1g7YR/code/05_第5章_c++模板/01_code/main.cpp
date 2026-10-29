#include <iostream>

using namespace std;
#if 0
class Data
{
    friend ostream& operator<<(ostream& out, Data ob);
private:
    int data;
public:
    Data(){}
    Data(int data)
    {
        this->data = data;
    }
};
ostream& operator<<(ostream& out, Data ob)
{
    out<<ob.data;
    return out;
}
#endif
template<typename T>
void myPrintAll(T a)
{
    cout<<a<<endl;
    cout<<"函数模板"<<endl;
}

class Data
{
    friend void myPrintAll<Data>(Data a);
private:
    int data;
public:
    Data(){}
    Data(int data)
    {
        this->data = data;
    }
};

//函数模板具体化
template<> void myPrintAll<Data>(Data a)
{
    cout<<a.data<<endl;
    cout<<"函数模板"<<endl;
}
int main(int argc, char *argv[])
{
    myPrintAll(10);
    myPrintAll('a');

    Data ob1(100);
    myPrintAll(ob1);

    return 0;
}
