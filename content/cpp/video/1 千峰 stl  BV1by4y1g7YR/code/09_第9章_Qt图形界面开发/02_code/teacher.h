#ifndef TEACHER_H
#define TEACHER_H

#include <QWidget>
#include <QDebug>
class Teacher : public QWidget
{
    Q_OBJECT
public:
    explicit Teacher(QWidget *parent = 0);

signals:
    //信号的返回值类型为void 可以有参（重载），不能实现函数体
    void hungury(void);
    void hungury(QString foodName);

public slots:
    //下课的槽函数
    void classOver(void)
    {
        qDebug()<<"下课了"<<endl;
        //emit 发出老师饿了的信号

       //emit this->hungury();

       emit this->hungury("锅包肉");

    }
};

#endif // TEACHER_H
