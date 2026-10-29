#include "widget.h"
#include "ui_widget.h"
#include <QPushButton>
#include <QLineEdit>
#include <QDebug>
#include <QMessageBox>
#include "form.h"
Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);

    //创建一个新页面
    this->newWidget = new Form();

    connect( ui->loginBtn, &QPushButton::clicked,[&](){
        //获取用户名以及密码
        QString usr =  ui->lineEditUser->text();
        QString pwd = ui->lineEditPwd->text();
        if(usr == "root" && pwd=="123456")
        {
            qDebug()<<"登录成功"<<endl;
            //页面跳转
            //旧页面隐藏
            this->hide();
            //新页面显示
            newWidget->show();
        }
        else
        {
            QMessageBox::critical(this,"错误","用户名或密码错误");
            //将输入框中的用户名及密码清空
            ui->lineEditUser->setText("");
            ui->lineEditPwd->setText("");
        }
    } );

    //监听新窗口的 myBack信号
    connect(newWidget, &Form::myBack,[&](){
        //新窗口隐藏
        newWidget->hide();
        //主窗口显示
        this->show();
    } );
}

Widget::~Widget()
{
    delete ui;
}
