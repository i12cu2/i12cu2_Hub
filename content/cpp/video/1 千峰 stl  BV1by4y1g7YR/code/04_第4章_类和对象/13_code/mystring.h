#ifndef MYSTRING_H
#define MYSTRING_H
#include <iostream>
using namespace std;

class MyString
{
    friend ostream& operator<<(ostream &out, MyString ob);
    friend istream& operator>>(istream &in, MyString &ob);
private:
    char *str;
    int size;
public:
    MyString();
    MyString(char *str);
    MyString(const MyString &ob);
    ~MyString();
    int getSize() const;
    //成员函数重载[]
    char& operator[](int pos);
    MyString operator+(MyString ob);
    MyString operator+(char *str);

    MyString& operator=(MyString ob);
    MyString& operator=(char *str);

    bool operator>(MyString ob);
    bool operator>(char *str);

//    bool operator<(MyString ob);
//    bool operator<(char *str);
//    bool operator==(MyString ob);
//    bool operator==(char *str);
//    bool operator!=(MyString ob);
//    bool operator!=(char *str);
};

#endif // MYSTRING_H
