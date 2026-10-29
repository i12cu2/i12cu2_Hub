#include "widget.h"
#include <QString>
#include <QPushButton>
Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    //修改窗口的标题
    this->setWindowTitle("第一个窗口");
    //设置窗口的大小
    this->resize(800,600);
    //固定窗口大小
    //this->setFixedSize(QSize(800,600));
    this->setFixedSize(800,600);

    //创建一个按钮控件
    QPushButton *btn1 = new QPushButton;
    //给按钮设置文本
    btn1->setText("第一个按钮");
    //设置按钮的父对象（在哪个窗口显示按钮  按钮就认哪个窗口为父对象）
    btn1->setParent(this);

    //创建一个按钮控件
    QPushButton *btn2 = new QPushButton("第二个按钮",this);
    //移动按钮
    btn2->move( 30 ,30);
    btn2->move( this->width()/2-btn2->width()/2,this->height()/2-btn2->height()/2 );
}

Widget::~Widget()
{

}
