#include <iostream>
#include "array.h"
using namespace std;

int main(int argc, char *argv[])
{
    Array ob;
    cout<<ob.getCapacity()<<" "<<ob.getSize()<<endl;

    ob.pushBack(10);
    ob.pushBack(20);
    ob.pushBack(30);
    ob.pushBack(40);
    ob.printArray();
    cout<<ob.getCapacity()<<" "<<ob.getSize()<<endl;
    ob.pushBack(50);
    ob.pushBack(60);
    ob.printArray();
    cout<<ob.getCapacity()<<" "<<ob.getSize()<<endl;
    ob.popBack();
    ob.popBack();
    ob.printArray();
    cout<<ob.getCapacity()<<" "<<ob.getSize()<<endl;

    cout<<"arr[2] = "<<ob.at(2)<<endl;
    ob.at(2) = 100;
    ob.printArray();
    return 0;
}
