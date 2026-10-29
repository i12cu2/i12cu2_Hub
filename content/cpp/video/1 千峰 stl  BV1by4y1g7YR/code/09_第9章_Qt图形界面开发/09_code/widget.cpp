#include "widget.h"
#include "ui_widget.h"
#include "ui_mywidget.h"
#include <QPushButton>
Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);

    connect( ui->pushButton, &QPushButton::clicked,[=](){
        ui->widget->mySetValue(50);
    }  );
}

Widget::~Widget()
{
    delete ui;
}
