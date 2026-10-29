#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <QPushButton>
#include <QMessageBox>
#include <QFileDialog>
#include <QColorDialog>
#include <QFontDialog>
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    connect( ui->msgBtn, &QPushButton::clicked,[&](){
#if 0
        QMessageBox::critical(this,"错误","严重的错误");
#endif
#if 0
        QMessageBox::information(this,"信息","余额不足");
#endif
#if 0
        QMessageBox::StandardButton ret;
        ret = QMessageBox::question(this,"询问","是否保存");
        if(ret == QMessageBox::Yes)
        {
            qDebug()<<"正在下载中"<<endl;
        }
        else if(ret == QMessageBox::No)
        {
            qDebug()<<"取消下载"<<endl;
        }
#endif
#if 1
        QMessageBox::StandardButton ret;
        ret = QMessageBox::question(this,"询问","是否保存",QMessageBox::Save|QMessageBox::Cancel);
        if(ret == QMessageBox::Save)
        {
            qDebug()<<"正在下载中"<<endl;
        }
        else if(ret == QMessageBox::Cancel)
        {
            qDebug()<<"取消下载"<<endl;
        }
#endif
    } );
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_actionNew_triggered()
{
    qDebug()<<"转到槽函数动起来"<<endl;
}


void MainWindow::on_login_clicked()
{
    qDebug()<<"登录"<<endl;
}

void MainWindow::on_next_clicked()
{
    qDebug()<<"下一曲"<<endl;
}

void MainWindow::on_actionOpen_triggered()
{
    QString fileName =  QFileDialog::getOpenFileName(this,"文件","./","*.cpp");
    qDebug()<<fileName<<endl;
}

void MainWindow::on_actioncolor_triggered()
{
    QColor color =  QColorDialog::getColor(Qt::white,this,"颜色");
    qDebug()<<color.red()<<" "<<color.green()<<" "<<color.blue()<<endl;
}

void MainWindow::on_actionfont_triggered()
{
    bool yes=true;
    QFont font =  QFontDialog::getFont(&yes, QFont("宋体"), this, "字体");
    qDebug()<<font.family()<<" "<<font.pointSize()<<endl;
}
