#include <iostream>
#include"data.hpp"
using namespace std;

int main(int argc, char *argv[])
{
    Data<int,char> ob1(100,'A');
    ob1.showData();
    return 0;
}
