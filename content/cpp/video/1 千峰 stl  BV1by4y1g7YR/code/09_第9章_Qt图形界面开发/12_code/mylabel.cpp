#include "mylabel.h"
#include <QDebug>
#include <QMouseEvent>
MyLabel::MyLabel(QWidget *parent) : QLabel(parent)
{
    //设置鼠标的追踪模式
    this->setMouseTracking(true);

    //安装事件过滤器
    this->installEventFilter(this);
}

//形参QMouseEvent *ev中ev保存了鼠标的信息（左键、右键、滚轮、位置）
void MyLabel::mousePressEvent(QMouseEvent *ev)
{
    if(ev->button() == Qt::LeftButton)
    {
        qDebug()<<"左键按下了("<<ev->x()<<","<<ev->y()<<")"<<endl;
    }
    else if(ev->button() == Qt::RightButton)
    {
        qDebug()<<"右键按下了("<<ev->x()<<","<<ev->y()<<")"<<endl;
    }
}

void MyLabel::mouseMoveEvent(QMouseEvent *ev)
{
    qDebug()<<"移动了("<<ev->x()<<","<<ev->y()<<")"<<endl;
}

bool MyLabel::event(QEvent *event)
{
    //处理关心的事件（鼠标按下事件）
    if( event->type() == QEvent::MouseButtonPress )
    {
        QMouseEvent *ev = (QMouseEvent *)event;
        qDebug()<<"事件分发器中 鼠标按下了("<<ev->x()<<","<<ev->y()<<")"<<endl;
        return true;//表示处理完毕 不继续分发
    }

    //不关心的事件 统一由父类的event分发器处理
    return QLabel::event(event);
}

bool MyLabel::eventFilter(QObject *watched, QEvent *event)
{
    //对当前控件this 感兴趣
    if(watched == this)
    {
        //感兴趣的是鼠标按下事件
        if( event->type() == QEvent::MouseButtonPress )
        {
            QMouseEvent *ev = (QMouseEvent *)event;
            qDebug()<<"事件过滤器中 鼠标按下了("<<ev->x()<<","<<ev->y()<<")"<<endl;
            return true;//表示处理完毕 不继续分发
        }
    }

    //其他过滤事件 交给父类
    return QLabel::eventFilter(watched, event);
}
