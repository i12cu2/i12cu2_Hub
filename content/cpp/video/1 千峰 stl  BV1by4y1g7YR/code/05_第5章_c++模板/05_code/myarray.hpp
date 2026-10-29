#ifndef MYARRAY_HPP
#define MYARRAY_HPP
#include<iostream>
#include<string.h>
#include<string>
using namespace std;
template<class T>
class MyArray
{
    template<typename T1>
    friend ostream& operator<<(ostream& out, MyArray<T1> ob);
private:
    T *arr;//保存数组首元素地址
    int size;//大小
    int capacity;//容量
public:
    MyArray();
    MyArray(int capacity);
    MyArray(const MyArray &ob);
    ~MyArray();
    MyArray& operator=(MyArray &ob);

    void pushBack(T elem);
    void sortArray();
};

#endif // MYARRAY_HPP

template<class T>
MyArray<T>::MyArray()
{
    capacity = 0;
    size = 0;
    arr = NULL;
}

template<class T>
MyArray<T>::MyArray(int capacity)
{
    this->capacity = capacity;
    size = 0;
    arr = new T[this->capacity];
    memset(arr, 0,sizeof(T)*capacity);
}

template<class T>
MyArray<T>::MyArray(const MyArray &ob)
{
    if(ob.arr == NULL)
    {
        arr = NULL;
        size = 0;
        capacity=0;
    }
    else
    {
        capacity = ob.capacity;
        size = ob.size;
        arr = new T[capacity];
        memcpy(arr, ob.arr, sizeof(T)*capacity);
    }

}

template<class T>
MyArray<T>::~MyArray()
{
    if(arr != NULL)
    {
        delete [] arr;
    }
}

template<class T>
MyArray<T> &MyArray<T>::operator=(MyArray<T> &ob)
{
    //判断this->arr是否存在空间
    if(arr != NULL)
    {
        delete [] arr;
        arr=NULL;
    }

    size = ob.size;
    capacity = ob.capacity;
    arr = new T[capacity];
    memset(arr,0,sizeof(T)*capacity);
    memcpy(arr, ob.arr, sizeof(T)*capacity);
    return *this;
}

template<class T>
void MyArray<T>::pushBack(T elem)
{
    if(size==capacity)//满
    {
        //扩展容量
        capacity = (capacity==0?1:2*capacity) ;
        //申请空间
        T *tmp = new T[capacity];

        if(arr != NULL)
        {
            //将旧空间的内容拷贝到新空间
            memcpy(tmp,arr,sizeof(T)*size);
            //释放旧空间
            delete [] arr;
        }

        arr = tmp;
    }

    arr[size] = elem;
    size++;
    return;
}

template<class T>
void MyArray<T>::sortArray()
{
    if(arr == NULL)
    {
        cout<<"容器为空间"<<endl;
    }
    else
    {
        int i=0,j=0;
        for(i=0;i<size-1;i++)
        {
            for(j=0;j<size-i-1;j++)
            {
                if(arr[j] > arr[j+1])
                {
                    T tmp = arr[j];
                    arr[j] = arr[j+1];
                    arr[j+1] = tmp;
                }
            }
        }
    }
    return;
}
template<typename T1>
ostream& operator<<(ostream& out, MyArray<T1> ob)
{
    int i=0;
    for(i=0;i<ob.size;i++)
    {
        out<<ob.arr[i]<<" ";
    }

    return out;
}

