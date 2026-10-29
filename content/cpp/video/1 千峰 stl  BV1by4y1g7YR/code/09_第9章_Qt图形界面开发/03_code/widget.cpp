#include "widget.h"
#include <QPushButton>
#include <QDebug>
Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    this->resize(400,300);
    QPushButton *btn = new QPushButton("按钮", this);

    //lambda 表达式
    connect(btn, &QPushButton::clicked,[&](){
        qDebug()<<"lambda 按钮被按下了"<<endl;
    } );

    connect(btn, &QPushButton::clicked, this , &Widget::printMsg );
}
void Widget::printMsg()
{
    qDebug()<<"槽函数 按钮被按下了"<<endl;
}
Widget::~Widget()
{

}


