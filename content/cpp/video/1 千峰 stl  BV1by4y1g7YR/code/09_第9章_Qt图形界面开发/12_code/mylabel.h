#ifndef MYLABEL_H
#define MYLABEL_H

#include <QWidget>
#include <QLabel>

class MyLabel : public QLabel
{
    Q_OBJECT
public:
    explicit MyLabel(QWidget *parent = 0);

    //重写鼠标按下事件
    virtual void mousePressEvent(QMouseEvent *ev);
    //重写鼠标移动事件
    virtual void mouseMoveEvent(QMouseEvent *ev);

    //重写事件分发器
    virtual bool event(QEvent *event);

    //重写事件分发器
    virtual bool eventFilter(QObject *watched, QEvent *event);




signals:

public slots:
};

#endif // MYLABEL_H
