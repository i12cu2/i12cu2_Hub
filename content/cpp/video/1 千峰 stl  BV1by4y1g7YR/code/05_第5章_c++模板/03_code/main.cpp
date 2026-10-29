#include <iostream>

using namespace std;
//类模板
template<class T1, class T2>
class Base
{
private:
    T1 a;
    T2 b;
public:
    Base(){}
    Base(T1 a, T2 b);
    void showData();
};
template<class T1, class T2>
Base<T1,T2>::Base(T1 a, T2 b)
{
    this->a = a;
    this->b = b;
}

template<class T1, class T2>
void Base<T1,T2>::showData()
{
    cout<<a<<" "<<b<<endl;
}

//类模板派生处类模板
template<class T1, class T2, class T3>
class Son1:public Base<T1,T2>
{
public:
    T3 c;
public:
    Son1(T1 a, T2 b, T3 c):Base<T1,T2>(a, b){
        this->c = c;
    }
};
int main(int argc, char *argv[])
{
    Son1<int,char, int> ob1(100, 'A', 200);
    ob1.showData();
    cout<<ob1.c<<endl;
    return 0;
}
