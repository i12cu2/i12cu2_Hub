#include <iostream>

using namespace std;



//类模板
template<class T1, class T2>
class Data
{
     template<typename T3, typename T4>
     friend void myPrintData(Data<T3, T4> &ob);
private:
    T1 a;
    T2 b;
public:
    Data(){}
    Data(T1 a, T2 b);
    void showData();
};

//函数模板
template<typename T3, typename T4> void myPrintData(Data<T3, T4> &ob)
{
    cout<<ob.a<<" "<<ob.b<<endl;
}


void test02()
{
    Data<int, char> ob1(100, 'A');
    myPrintData(ob1);
}

void test01()
{
    //类模板 实例化对象  不能自动类型推导
    //Data ob(10, 20);
    //类模板 实例化对象 必须指明T的类型
    Data<int,int> ob1(10,20);
    ob1.showData();
    Data<int,char> ob2(10,'A');
    ob2.showData();
}

int main(int argc, char *argv[])
{
    test02();
    return 0;
}

template<class T1, class T2>
Data<T1,T2>::Data(T1 a, T2 b)
{
    this->a = a;
    this->b = b;
}

template<class T1, class T2>
void Data<T1,T2>::showData()
{
    cout<<a<<" "<<b<<endl;
}
