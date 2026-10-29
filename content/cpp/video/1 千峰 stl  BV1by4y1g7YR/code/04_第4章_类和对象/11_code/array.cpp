#include "array.h"
#include<string.h>
#include<iostream>

using namespace std;
int Array::getCapacity() const
{
    return capacity;
}

int Array::getSize() const
{
    return size;
}

void Array::printArray()
{
    int i=0;
    for(i=0;i<size; i++)
    {
        cout<<arr[i]<<" ";
    }
    cout<<endl;
    return;
}

void Array::pushBack(int elem)
{
    //判断容器是否满
    if(size == capacity)
    {
        //申请空间
        int *tmp = new int[2*capacity];
        //将就空间的内容 拷贝到新空间
        memcpy(tmp, arr, capacity*sizeof(int));
        //释放原有的空间
        delete [] arr;
        //更新arr的空间
        arr = tmp;
        //更新容量
        capacity = 2*capacity;
    }

    arr[size]=elem;
    size++;
    return;
}

void Array::popBack()
{
    if(size == 0)
    {
        cout<<"容量为空"<<endl;
    }
    else
    {
        size--;
    }
    return;
}

int& Array::at(int pos)
{
    if(pos<0 || pos >=size)
    {
        cout<<"访问违法内存"<<endl;
        exit(-1);
    }

    return arr[pos];
}

Array::Array()
{
    capacity = 5;
    size = 0;
    arr = new int[capacity];
    //空间清0
    memset(arr, 0, sizeof(int)*capacity);
}

Array::Array(int capacity)
{
    this->capacity = capacity;
    size = 0;
    arr  = new int[capacity];
    //空间清0
    memset(arr, 0, sizeof(int)*capacity);
}

Array::Array(const Array &ob)
{
    capacity = ob.capacity;
    size = ob.size;
    //深拷贝
    arr = new int[capacity];
    memcpy(arr, ob.arr, sizeof(int)*capacity);
}

Array::~Array()
{
    if(arr != NULL)
    {
        delete [] arr;
        arr = NULL;
    }
}
