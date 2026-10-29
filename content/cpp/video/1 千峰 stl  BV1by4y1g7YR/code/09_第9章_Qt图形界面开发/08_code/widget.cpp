#include "widget.h"
#include "ui_widget.h"
#include <QRadioButton>
#include <QCheckBox>
#include<QDebug>
#include <QComboBox>
#include <QListWidget>
#include <QTreeWidget>
#include <QTableWidget>
#include <QToolBox>
Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
#if 0
    //让单选框动起来
    connect(ui->radioButton, &QRadioButton::clicked,[=](){
        qDebug()<<ui->radioButton->text()<<endl;
    }  );

    static QStringList strList;

    connect( ui->checkBox, &QCheckBox::stateChanged, [=](int state){
         //state 2选中  0w未选中
        if(state == 2)
            strList.append(ui->checkBox->text());         ;
    } );
    connect( ui->checkBox_2, &QCheckBox::stateChanged, [=](int state){
         //state 2选中  0w未选中
        if(state == 2)
            strList.append(ui->checkBox_2->text());
    } );
    connect( ui->checkBox_3, &QCheckBox::stateChanged, [=](int state){
         //state 2选中  0w未选中
        if(state == 2)
            strList.append(ui->checkBox_3->text());
    } );
    connect( ui->checkBox_4, &QCheckBox::stateChanged, [=](int state){
         //state 2选中  0w未选中
        if(state == 2)
            strList.append(ui->checkBox_4->text());
    } );

    connect( ui->pushButton, &QPushButton::clicked,[=](){
        qDebug()<<"选中的菜单："<<strList<<endl;
    } );

     void (QComboBox:: *p)(const QString &) =&QComboBox::currentIndexChanged;
     connect( ui->comboBox, p,[=](const QString &text){
         qDebug()<<"选中的车型为:"<<text<<endl;
     } );


     //添加一项数据
     ui->listWidget->addItem("德玛西亚");
     //添加 多项数据
     QStringList list;
     list<<"小法"<<"盲僧"<<"提莫";
     ui->listWidget->addItems(list);

     connect( ui->listWidget, &QListWidget::itemDoubleClicked,[=](QListWidgetItem *item){
          qDebug()<<"选中的英雄为:"<<item->text()<<endl;
     } );
     //设置背景透明
    ui->listWidget->setStyleSheet("background-color:transparent");


    connect( ui->treeWidget, &QTreeWidget::itemClicked,[=](QTreeWidgetItem *item, int column){
        qDebug()<<item->text(column)<<endl;
    } );

    connect( ui->tableWidget, &QTableWidget::cellClicked, [=](int row, int col){
       qDebug()<< ui->tableWidget->item(row,col)->text()<<endl;
    } );
#endif
}

Widget::~Widget()
{
    delete ui;
}
