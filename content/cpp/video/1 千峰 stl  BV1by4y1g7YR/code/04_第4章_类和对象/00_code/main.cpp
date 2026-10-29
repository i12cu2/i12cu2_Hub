#include <iostream>

using namespace std;

//类Data1 是一个类型
class Data1
{
    //类中 默认为私有
private:
    int a;//不要给类中成员 初始化
protected://保护
    int b;
public://公共
    int c;
    //在类的内部 不存在 权限之分
    void showData(void)
    {
        cout<<a<<" "<<b<<" "<<c<<endl;
    }
};
void test01()
{
    //类实例化一个对象
   Data1 ob;
   //类外不能直接访问 类的私有和保护数据
   //cout<<ob.a <<endl;
   //cout<<ob.b <<endl;
   cout<<ob.c <<endl;

   //类中的成员函数 需要对象调用
   ob.showData();
}
#include<string.h>
class Person
{
private:
    char mName[32];
    int mAge;
public:
    //初始化成员
    void init(char *name, int age)
    {
        strcpy(mName, name);
        if(age>=0 && age<=100)
        {
            mAge = age;
        }
        else
        {
            cout<<"年龄无效"<<endl;
        }
        return;
    }
    //设置name
    void setName(char *name)
    {
        strcpy(mName, name);
    }
    //获取name
    char *getName(void)
    {
        return mName;
    }

    //设置age
    void setAge(int age)
    {
        if(age>=0 && age<=100)
        {
            mAge = age;
        }
        else
        {
            cout<<"年龄无效"<<endl;
        }
    }
    //得到age
    int getAge(void)
    {
        return mAge;
    }

    //显示所有数据
    void showPerson(void)
    {
        cout<<mName<<" "<<mAge<<endl;
    }
};

void test02()
{
    Person ob1;

    ob1.init("lucy", 18);
    ob1.showPerson();

    ob1.setName("bob");
    cout<<"年龄:"<<ob1.getAge()<<endl;
    ob1.showPerson();
}

class Cube
{
private:
    int mA;
    int mB;
    int mC;
public:
    void setA(int a)
    {
        mA = a;
    }
    int getA(void)
    {
        return mA;
    }
    void setB(int b)
    {
        mB = b;
    }
    int getB(void)
    {
        return mB;
    }
    void setC(int c)
    {
        mC = c;
    }
    int getC(void)
    {
        return mC;
    }

    //获取面积
    int getS(void)
    {
        return (mA*mB+mB*mC+mC*mA)*2;
    }
    //获取体积
    int getV(void)
    {
        return mA*mB*mC;
    }
    //成员函数实现
    bool compareCube02(Cube &ob)
    {
        if(mA==ob.mA && mB ==ob.mB && mC == ob.mC)
        {
            return true;
        }

        return false;
    }
};

//全局函数 比较两个立方体是否先等
bool compareCube01(Cube &ob1, Cube &ob2)
{
    if(ob1.getA()==ob2.getA() && ob1.getB() ==ob2.getB() && ob1.getC() == ob2.getC())
    {
        return true;
    }

    return false;
}

void test03()
{
    Cube ob1;
    ob1.setA(10);
    ob1.setB(20);
    ob1.setC(30);

    cout<<"面积:"<<ob1.getS()<<endl;
    cout<<"体积:"<<ob1.getV()<<endl;

    Cube ob2;
    ob2.setA(10);
    ob2.setB(20);
    ob2.setC(30);

//    if(compareCube01(ob1, ob2))
    if(ob1.compareCube02(ob2))
    {
        cout<<"相等"<<endl;
    }
    else
    {
        cout<<"不相等"<<endl;
    }
}

class Point
{
private:
    int mX;
    int mY;
public:
    void setX(int x)
    {
        mX = x;
    }
    int getX(void)
    {
        return mX;
    }
    void setY(int y)
    {
        mY = y;
    }
    int getY(void)
    {
        return mY;
    }
};

class Circle
{
private:
    Point p;//对象作为类的成员变量
    int mR;
public:
    void setPoint(int x, int y)
    {
        p.setX(x);
        p.setY(y);
    }
    Point getPoint(void)
    {
        return p;
    }
    void setR(int r)
    {
        mR = r;
    }
    int getR(void)
    {
        return mR;
    }

    //判断点 在圆的位置
    int pointIsOnCircle(Point &ob)
    {
        int len = (ob.getX()-p.getX())*(ob.getX()-p.getX())+\
                (ob.getY()-p.getY())*(ob.getY()-p.getY());
        if(len == mR*mR)
        {
            return 0;
        }
        else if(len > mR*mR)
        {
            return 1;
        }
        else if(len < mR*mR)
        {
            return -1;
        }
    }
};

void test04()
{
    //实例化一个点的对象
    Point p;
    p.setX(5);
    p.setY(5);

    //实例化一个圆的对象
    Circle cir;
    cir.setPoint(2,2);
    cir.setR(5);
    if(cir.pointIsOnCircle(p) == 0)
    {
        cout<<"点在圆上"<<endl;
    }
    else if(cir.pointIsOnCircle(p) > 0)
    {
        cout<<"点在圆外"<<endl;
    }
    else if(cir.pointIsOnCircle(p) < 0)
    {
        cout<<"点在圆内"<<endl;
    }
}


class Data2
{
private:
    int mA;
public:
    void setA(int a);
    int getA(void);
};
void test05()
{
    Data2 ob;
    ob.setA(10);
    cout<<ob.getA()<<endl;
}
int main(int argc, char *argv[])
{
    test05();
    return 0;
}

void Data2::setA(int a)
{
    mA = a;
}

int Data2::getA()
{
    return mA;
}
