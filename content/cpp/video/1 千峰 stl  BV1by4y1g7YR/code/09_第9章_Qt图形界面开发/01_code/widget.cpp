#include "widget.h"
#include <QPushButton>
Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    //设置主窗口大小
    this->resize(400,300);
    //创建一个按钮
    QPushButton *btn = new QPushButton("关闭", this);
#if 1
    // 建立信号和槽的关系(Qt5的方式)
    connect( btn, &QPushButton::clicked  ,this, &Widget::close );
#else
    // 建立信号和槽的关系(Qt4的方式) SIGNAL将（）里面当成字符串看待 不会判断信号是否存在
    connect( btn, SIGNAL(clicked())  ,this, SLOT(close()) );
#endif
}

Widget::~Widget()
{

}
