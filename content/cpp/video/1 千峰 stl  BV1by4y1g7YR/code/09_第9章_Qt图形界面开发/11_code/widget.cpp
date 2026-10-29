#include "widget.h"
#include "ui_widget.h"
#include <QPushButton>
Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);

    //设置栈容器的默认页码
    ui->stackedWidget->setCurrentIndex(0);

    //动起来
    connect(ui->pushButton, &QPushButton::clicked,[=](){
        ui->stackedWidget->setCurrentIndex(0);
    } );
    connect(ui->pushButton_2, &QPushButton::clicked,[=](){
        ui->stackedWidget->setCurrentIndex(1);
    } );
    connect(ui->pushButton_3, &QPushButton::clicked,[=](){
        ui->stackedWidget->setCurrentIndex(2);
    } );


}

Widget::~Widget()
{
    delete ui;
}
