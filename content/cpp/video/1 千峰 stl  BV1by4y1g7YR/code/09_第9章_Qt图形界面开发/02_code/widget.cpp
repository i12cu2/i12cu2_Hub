#include "widget.h"
#include "teacher.h"
#include "student.h"
#include <QPushButton>
Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    this->resize(400,300);
    //实例化老师的控件
    Teacher *tea = new Teacher(this);
    //实例化学生的控件
    Student *stu = new Student(this);

    //建立老师和学生的关系
#if 0
   connect( tea, SIGNAL(hungury()),stu,SLOT(treat()) );
#else
    connect( tea, SIGNAL(hungury(QString)),stu,SLOT(treat(QString)) );
#endif
    //创建一个按钮
    QPushButton *btn = new QPushButton("下课", this);
    connect(btn, &QPushButton::clicked, tea, &Teacher::classOver );
}

Widget::~Widget()
{

}
