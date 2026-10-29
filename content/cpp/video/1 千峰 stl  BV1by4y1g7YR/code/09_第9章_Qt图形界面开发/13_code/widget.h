#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = 0);
    ~Widget();
    //重写定时器 事件
    virtual void timerEvent(QTimerEvent *event);

private:
    Ui::Widget *ui;
    //定义两个定时器 标示
    int t1;
    int t2;
};

#endif // WIDGET_H
