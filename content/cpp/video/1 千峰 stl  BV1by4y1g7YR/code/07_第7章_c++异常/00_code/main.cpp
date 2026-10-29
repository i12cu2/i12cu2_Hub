#include <iostream>

using namespace std;

//函数默认 可以抛出任何类型的异常（推荐）
void fun01()
{
    //throw 1;
    //throw '1';
    throw "hello";

}
//只能抛出int,char异常
void fun02() throw(int,char)
{
    //throw 1;
    //throw '1';
    throw "hello";//抛出 不能捕获
}

//不能抛出 任何异常
void fun03() throw()
{
    throw 1;
    //throw '1';
    //throw "hello";//抛出 不能捕获
}

void test01()
{
    int ret = 0;
    try
    {
        fun03();
    }
    catch(int)//捕获
    {
        cout<<"int异常值为:"<<endl;
    }
    catch(char)//捕获
    {
        cout<<"char异常值为:"<<endl;
    }
    catch(const char *)//捕获
    {
        cout<<"const char *异常值为:"<<endl;
    }

    catch(...)//捕获
    {
        cout<<"其他异常值为:"<<endl;
    }
}

class MyException
{
public:
    MyException(){
        cout << "异常变量构造" << endl;
    };
    MyException(const MyException & e)
    {
        cout << "拷贝构造" << endl;
    }
    ~MyException()
    {
        cout << "异常变量析构" << endl;
    }
};

void test02()
{
    try
    {
        throw MyException();
    }
    catch(MyException &e)
    {
        cout<<"普通对象接异常"<<endl;
    }
}

//异常基类
class BaseException{
public:
    virtual void printError(){};
};

//空指针异常
class NullPointerException : public BaseException{
public:
    virtual void printError(){
        cout << "空指针异常!" << endl;
    }
};
//越界异常
class OutOfRangeException : public BaseException{
public:
    virtual void printError(){
        cout << "越界异常!" << endl;
    }
};

void doWork(){

    //throw NullPointerException();
    throw OutOfRangeException();
}

void test03()
{
    try{
        doWork();
    }
    catch (BaseException& ex){
        ex.printError();
    }
}


void test04()
{
    try
    {
        throw out_of_range("哈哈，我越界了");
        //throw bad_alloc();
    }
    catch(exception &e)
    {
        //what()存放的是异常信息（char *方式存在）
        cout<<e.what()<<endl;
    }
}

//#include<string>

class NewException:public exception
{
private:
    string msg;
public:
    NewException(){}
    NewException(string msg)
    {
        this->msg = msg;
    }
    //重写父类的what
    virtual const char* what()const throw()//防止父类在子类前抛出标准异常
    {
        //将string类转换成char *
        return this->msg.c_str();
    }
    ~NewException(){}
};

void test05()
{
    try
    {
        throw NewException("哈哈，自己的异常");

    }
    catch(exception &e)
    {
        cout<<e.what()<<endl;
    }
}

int main(int argc, char *argv[])
{
    test05();
    return 0;
}
