#ifndef SPECIALPOSITION_H
#define SPECIALPOSITION_H

#include <QWidget>

namespace Ui {
class SpecialPosition;
}

class SpecialPosition : public QWidget
{
    Q_OBJECT

public:
    explicit SpecialPosition(QWidget *parent = 0);
    ~SpecialPosition();

private:
    Ui::SpecialPosition *ui;
};

#endif // SPECIALPOSITION_H
