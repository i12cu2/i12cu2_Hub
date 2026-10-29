#include "widget.h"
#include "ui_widget.h"
#include <QDebug>
#include <QPainter>
#include <QPushButton>
Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);

    //单击按钮切换背景 图片 update调用 就会执行 绘图事件
    connect( ui->pushButton, &QPushButton::clicked, [=](){
        this->update();
    } );
}

Widget::~Widget()
{
    delete ui;
}

//窗口加载、update都会执行绘图事件
void Widget::paintEvent(QPaintEvent *event)
{
    QString img[4]={":/image/Frame.jpg", ":/image/butterfly.png",":/image/LuffyQ.png",":/image/Sunny.jpg"};
    int n = sizeof(img)/sizeof(img[0]);
    static int index = 0;

    //定义一个画家 在主窗口this上 作画
    QPainter *painter = new QPainter(this);

    //开始画
    QPixmap pix;
    //加载图片
    pix.load(img[index]);
    //修改图片大小
    pix.scaled(this->width(), this->height());
    painter->drawPixmap(0,0,this->width(),this->height(), pix);

    index++;
    if(index == 4)
        index=0;
}
