#include "widget.h"
#include "ui_widget.h"
#include <QDebug>
#include <QTimer>
#include <QPushButton>
Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);

    //启动定时器事件 会返回定时器的标示
    t1 = this->startTimer(1000);//1000ms
    t2 = this->startTimer(2000);//1000ms

    //创建一个定时器对象
    QTimer *timer = new QTimer(this);
    //定时器对象  监听 超时信号的 到来
    connect( timer, &QTimer::timeout,[=](){
        static int num = 0;
        ui->label_3->setText(QString::number(num));
        num++;
    } );
    //启动定时
    connect( ui->pushButton, &QPushButton::clicked,[=](){
        timer->start(1000);//1000ms
    } );
    //停止计时
    connect( ui->pushButton_2, &QPushButton::clicked,[=](){
        timer->stop();//停止计时
    } );

    //QTimer的静态函数 只会触发一次  加入延时5秒
    QTimer::singleShot(5000, [=](){
        ui->label_4->setText("哈哈，梁哥来了!!!!!");
    });
}

Widget::~Widget()
{
    delete ui;
}

void Widget::timerEvent(QTimerEvent *event)
{
    if(event->timerId() == t1)
    {
        static int time1 = 0;
        ui->label->setText(QString::number(time1));
        time1++;
    }
    else if(event->timerId() == t2)
    {
        static int time2 = 0;
        ui->label_2->setText(QString::number(time2));
        time2++;
    }

}
