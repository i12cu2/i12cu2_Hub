#ifndef ARRAY_H
#define ARRAY_H


class Array
{
private:
    int *arr;//存放首元素地址
    int capacity;//容量
    int size;//大小
public:
    Array();
    Array(int capacity);
    Array(const Array &ob);
    ~Array();

    int getCapacity() const;
    int getSize() const;

    void printArray(void);

    //插入尾部元素
    void pushBack(int elem);
    //删除尾部元素
    void popBack(void);
    int &at(int pos);
};

#endif // ARRAY_H
