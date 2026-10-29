#include <iostream>

using namespace std;

class SingleTon//单例模式
{
    //构造私有化 防止实例化其他对象
private:
    SingleTon(){
        count=0;
        cout<<"构造"<<endl;
    }
    SingleTon(const SingleTon &ob){
        count=0;
    }
    ~SingleTon()
    {
        cout<<"析够"<<endl;
    }
private:
    //const防止p 在类内部 被修改指向
    static SingleTon * const p;//保存唯一的实例地址
    int count;//统计任务执行次数
public:
    static SingleTon * getSingleTon(void)//获取唯一的实例地址
    {
        return p;
    }


    //用户自定义 任务函数
    void printString(char *str)
    {
        count++;
        cout<<"当前第"<<count<<"次任务打印:"<<str<<endl;
    }

};
SingleTon *const SingleTon::p = new SingleTon;//创建唯一的实例

int main(int argc, char *argv[])
{
    //获取单例的地址
    SingleTon *p1 =SingleTon::getSingleTon();
    p1->printString("离职证明1");
    p1->printString("学历证明1");
    p1->printString("学位证明1");
    p1->printString("身份证明1");

    SingleTon *p2 =SingleTon::getSingleTon();
    p2->printString("离职证明2");
    p2->printString("学历证明2");
    p2->printString("学位证明2");
    p2->printString("身份证明2");
    return 0;
}
