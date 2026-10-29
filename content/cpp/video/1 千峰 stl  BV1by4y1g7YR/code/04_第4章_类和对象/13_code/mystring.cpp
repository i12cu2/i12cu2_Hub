#include "mystring.h"
#include <string.h>

int MyString::getSize() const
{
    return size;
}

char& MyString::operator[](int pos)
{
    if(pos<0 || pos>=size)
    {
        cout<<"元素位置不合法"<<endl;
        exit(-1);
    }

    return str[pos];
}

MyString MyString::operator+(MyString ob)
{
    MyString tmp;
    tmp.size = size+ob.size;
    tmp.str = new char[tmp.size+1];
    memset(tmp.str, 0, tmp.size+1);

    strcpy(tmp.str, str);
    strcat(tmp.str, ob.str);

    return tmp;
}

MyString MyString::operator+(char *str)
{
    MyString tmp;
    tmp.size = size+strlen(str);
    tmp.str = new char[tmp.size+1];
    memset(tmp.str, 0, tmp.size+1);

    strcpy(tmp.str, this->str);
    strcat(tmp.str, str);

    return tmp;
}

MyString &MyString::operator=(MyString ob)
{
    //str2 = str1;
    if(this->str != NULL)
    {
        delete [] this->str;
        this->str = NULL;
    }

    this->size = ob.size;
    this->str = new char[this->size+1];
    memset(this->str, 0, this->size+1);
    strcpy(this->str, ob.str);

    return *this;
}

MyString &MyString::operator=(char *str)
{
    //str2 = str1;
    if(this->str != NULL)
    {
        delete [] this->str;
        this->str = NULL;
    }

    this->size = strlen(str);
    this->str = new char[this->size+1];
    memset(this->str, 0, this->size+1);
    strcpy(this->str, str);

    return *this;
}

bool MyString::operator>(MyString ob)
{
    if(str==NULL || ob.str == NULL)
    {
        exit(-1);
    }
    if(strcmp(this->str, ob.str) > 0)
    {
        return true;
    }
    return false;
}

bool MyString::operator>(char *str)
{
    if(this->str==NULL || str == NULL)
    {
        exit(-1);
    }
    if(strcmp(this->str, str) > 0)
    {
        return true;
    }
    return false;
}

MyString::MyString()
{
    str=NULL;
    size=0;
}

MyString::MyString(char *str)
{
    size = strlen(str);
    this->str = new char[size+1];
    memset(this->str, 0, size+1);

    strcpy(this->str, str);
}

MyString::MyString(const MyString &ob)
{
    size = ob.size;
    str = new char[size+1];
    memset(str, 0, size+1);
    strcpy(str, ob.str);
}

MyString::~MyString()
{
    if(str != NULL)
    {
        delete [] str;
        str=NULL;
    }
}

//全局函数实现 <<重载
ostream& operator<<(ostream &out, MyString ob)
{
    out<<ob.str;
    return out;
}
//全局函数实现 >>重载
istream& operator>>(istream &in, MyString &ob)
{
    char buf[1024]="";
    cin>>buf;

    if(ob.str != NULL)//ob已经有字符串
    {
        delete [] ob.str;
        ob.str = NULL;
    }

    ob.size = strlen(buf);
    ob.str = new char[ob.size+1];
    memset(ob.str, 0,ob.size+1);
    strcpy(ob.str, buf);

    return in;
}
