#include "widget.h"
#include "ui_widget.h"
#include <QMovie>
#include <QPushButton>
Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    flag = 0;
    ui->setupUi(this);

    QMovie *m = new QMovie(":/image/mario.gif");
    ui->label_3->setMovie(m);

    connect( ui->playBtn, &QPushButton::clicked,[=](){
        m->start();//播放动画
    } );

    connect( ui->pause, &QPushButton::clicked,[=](){
        m->stop();//暂停动画
    } );
}

Widget::~Widget()
{
    delete ui;
}

void Widget::on_pushButton_clicked()
{
    ui->label->setText("哈哈、你被修改了");
}

void Widget::on_pushButton_2_clicked()
{
    QString imgPath[2]={":/image/down.png", ":/image/up.png"};
    static int x=0;
    QPixmap pix(imgPath[flag]);
    ui->label_2->move( x+=10 ,ui->label_2->pos().y());
    if(x>this->width())
        x=0;
    ui->label_2->setPixmap(pix);

    flag = !flag;
}
