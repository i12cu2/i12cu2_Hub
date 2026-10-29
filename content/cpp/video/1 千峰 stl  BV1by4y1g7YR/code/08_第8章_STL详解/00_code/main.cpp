#include <iostream>
#include <string>
using namespace std;

void test01()
{
    string str1("hello world");
    cout<<str1<<endl;
    string str2(5,'A');
    cout<<str2<<endl;
    string str3 = str2;
    cout<<str3<<endl;

    string str4;
    str4 = "hello world";
    cout<<str4<<endl;
    str4 = 'W';
    cout<<str4<<endl;

    str4.assign("hello world", 5);
    cout<<str4<<endl;
    str4.assign(str1, 2, 3);
    cout<<str4<<endl;
}
void test02()
{
    string str1="hello world";
    cout<<str1[1]<<" "<<str1.at(1)<<endl;
    str1[1]='E';
    str1.at(6)='H';
    cout<<str1<<endl;

    //[] 越界不会抛出异常  at越界会抛出异常
    try
    {
        //str1[1000]='A';
        str1.at(1000)='A';
    }
    catch(exception &e)
    {
        cout<<"捕获到异常:"<<e.what()<<endl;
    }
}
void test03()
{
    string str1="hello";
    str1 += "world";
    cout<<str1<<endl;

    string str2="hehe";
    str1 += str2;
    cout<<str1<<endl;

    string str3="hello";
    string str4="world";
    cout<<str3+str4<<endl;

    string str5="hello";
    string str6="world";
    str5.append(str6, 2, 3);
    cout<<str5<<endl;
    str5.append("world", 3);
    cout<<str5<<endl;
}
void test04()
{
    string str1="http://www.sex.777.sex.999.sex.com";
    while(1)
    {
        int ret = str1.find("sex");
        if(ret == -1)
            break;

        str1.replace(ret,3,"***");
    }

    cout<<str1<<endl;
}
void test05()
{
    string str1 ="hehe";
    string str2 = "haha";
    if(str1.compare(str2) > 0 )
    {
        cout<<"大于"<<endl;
    }
    else if(str1.compare(str2) == 0)
    {
        cout<<"等于"<<endl;
    }
    else if(str1.compare(str2) < 0)
    {
        cout<<"小于"<<endl;
    }
}
void test06()
{
   string str1="hehehe:hahaha:xixixi:lalala";
   int pos = 0;
   while(1)
   {
       int ret = str1.find(":", pos);
       if(ret < 0)
       {
           string tmp = str1.substr(pos, str1.size()-pos);
           cout<<tmp<<endl;
           break;
       }

       string tmp = str1.substr(pos, ret-pos);
       cout<<tmp<<endl;

       pos = ret+1;
   }
}
void test07()
{
    string str1="hello";
    str1.insert(2,"###");
    cout<<str1<<endl;
    str1.erase(2, 3);
    cout<<str1<<endl;
    str1.erase(0,str1.size());
    cout<<str1<<endl;
}

void test08()
{
    //char * 转换成 string  （默认支持）
    string str1;
    str1 = (string)("hello");
    cout<<str1<<endl;

    //string 转成  char *  必须使用 成员函数c_str
    string str2="hello world";
//    char *p = const_cast<char *>(str2.c_str());
    char *p = (char *)str2.c_str();
    cout<<p<<endl;
}

int main(int argc, char *argv[])
{
    test08();
    return 0;
}
