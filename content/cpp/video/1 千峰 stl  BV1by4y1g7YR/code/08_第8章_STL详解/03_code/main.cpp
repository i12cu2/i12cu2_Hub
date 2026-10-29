#include <iostream>
#include <stack>
using namespace std;
void test01()
{
    stack<int> s;
    s.push(10);
    s.push(20);
    s.push(30);
    s.push(40);
    s.push(50);

    if(!s.empty())
    {
        cout<<"栈的大小:"<<s.size()<<endl;
        while(!s.empty())
        {
            cout<<s.top()<<" ";
            s.pop();
        }
    }

}
#include<queue>
void test02()
{
    queue<int> q;
    q.push(10);
    q.push(20);
    q.push(30);
    q.push(40);
    q.push(50);

    if(!q.empty())
    {
        cout<<"栈的大小:"<<q.size()<<endl;
        while(!q.empty())
        {
            cout<<q.front()<<" ";
            q.pop();
        }
    }

}
int main(int argc, char *argv[])
{
    test02();
    return 0;
}
