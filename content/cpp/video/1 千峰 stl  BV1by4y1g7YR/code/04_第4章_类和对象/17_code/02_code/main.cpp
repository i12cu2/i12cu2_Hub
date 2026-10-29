#include <iostream>

using namespace std;
class Animal
{
public:
    //虚函数
    virtual void speak(void)
    {
        cout << "动物在说话" << endl;
    }
    //虚析构
    virtual ~Animal()
    {
        cout << "Animal的析构函数" << endl;
    }
};
class Dog :public Animal
{
public:
    //子类重写 父类的虚函数
    void speak(void)
    {
        cout << "狗在汪汪" << endl;
    }
    ~Dog()
    {
        cout << "Dog的析构函数" << endl;
    }
};

void test01()
{
    Animal* p1 = new Dog;
    p1->speak();

    delete p1;

}

int main(int argc, char* argv[])
{
    test01();
    return 0;
}
