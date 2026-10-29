#include <iostream>//标准输入输出流

//使用std命名空间
using namespace std;

int main(int argc, char *argv[])
{
    //cout输出设备 （终端）  endl 换行符
    cout << "Hello World!" << endl;

    //
    int num = 0;
    //cin输入设备（键盘）
    cin >> num;
    cout<<"num = "<< num<<endl;
    //cin>>num1>>num2;

    return 0;//返回值 以及 结束函数
}
