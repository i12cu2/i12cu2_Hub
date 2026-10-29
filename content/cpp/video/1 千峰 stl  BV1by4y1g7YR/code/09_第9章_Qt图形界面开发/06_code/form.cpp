#include "form.h"
#include "ui_form.h"
#include <QPushButton>
Form::Form(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Form)
{
    ui->setupUi(this);
    //给主窗口发送回退信号
#if 0
    connect( ui->backBtn, &QPushButton::clicked,[&](){
        emit this->myBack();
    } );
#else
    connect( ui->backBtn, &QPushButton::clicked, this, &Form::myBack  );
#endif
}

Form::~Form()
{
    delete ui;
}
