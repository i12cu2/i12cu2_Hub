#include "widget.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    //定义一个应用程序 对象a
    QApplication a(argc, argv);

    //定义一个主窗口 w
    Widget w;
    //默认窗口为隐藏 需要调用show显示  hide隐藏
    w.show();

    //exec主事件循环 （等待用户操作界面 并响应）
    return a.exec();
}
