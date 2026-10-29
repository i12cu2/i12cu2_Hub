#include <iostream>
#include "mystring.h"
using namespace std;

int main(int argc, char *argv[])
{
    MyString str1="hello";
    MyString str2="world";
    //if(str1 > str2)
    if(str1 > "world")
    {
        cout<<"大于"<<endl;
    }
    else
    {
        cout<<"不大于"<<endl;
    }
    return 0;
}
