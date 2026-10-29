#include <iostream>
#include <list>
#include <algorithm>
using namespace std;
void printListInt(list<int> &l)
{
    list<int>::iterator it;
    for(it=l.begin(); it!=l.end();it++)
    {
        cout<<*it<<" ";
    }
    cout<<endl;
}

void test01()
{
    list<int> l1;
    l1.push_back(10);
    l1.push_back(20);
    l1.push_back(30);
    l1.push_front(40);
    l1.push_front(50);
    l1.push_front(60);

    printListInt(l1);//60 50 40 10 20 30
    //list容器  是双向迭代器 不支持+2  支持++
    list<int>::iterator it=l1.begin();
    it++;
    it++;
    l1.insert(it, 3, 100);
    printListInt(l1);//60 50 100 100 100 40 10 20 30

    //删除所有100
    l1.remove(100);
    printListInt(l1);//60 50 40 10 20 30

    //对链表排序
    //STL提供的算法 只支持 随机访问迭代器，而list是双向迭代器 所以sort不支持list
//    l1.sort(greater<int>());
    l1.sort();
    printListInt(l1);//10 20 30 40 50 60
}

int main(int argc, char *argv[])
{
    test01();
    return 0;
}
