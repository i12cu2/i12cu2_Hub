#ifndef STUDENT_H
#define STUDENT_H

#include <QWidget>
#include <QDebug>
class Student : public QWidget
{
    Q_OBJECT
public:
    explicit Student(QWidget *parent = 0);

signals:

public slots:
    //槽函数返回值类型为void 可以有参数（重载） 必须实现函数体
    void treat(void)
    {
        qDebug()<<"请老师吃饭了"<<endl;
    }
    void treat(QString foodName)
    {
        qDebug()<<"请老师吃了"<<foodName<<endl;
    }
};

#endif // STUDENT_H
