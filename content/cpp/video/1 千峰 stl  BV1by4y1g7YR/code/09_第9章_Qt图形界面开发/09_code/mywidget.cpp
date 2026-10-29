#include "mywidget.h"
#include "ui_mywidget.h"
#include <QSlider>
#include<QSpinBox>
MyWidget::MyWidget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::MyWidget)
{
    ui->setupUi(this);

    //改变spinBox数据 让进度条QSlider发生变化
    void (QSpinBox:: *p1)(int) = &QSpinBox::valueChanged;
    connect(ui->spinBox, p1,ui->horizontalSlider, &QSlider::setValue);

    //拖动进度条QSlider 改变spinBox数据
    connect(ui->horizontalSlider, &QSlider::valueChanged, ui->spinBox, &QSpinBox::setValue);
}

MyWidget::~MyWidget()
{
    delete ui;
}

void MyWidget::mySetValue(int value)
{
    ui->horizontalSlider->setValue(value);
}
