#ifndef SINGLEANDDOUBLEQUALIFYING_H
#define SINGLEANDDOUBLEQUALIFYING_H

#include <QWidget>

namespace Ui {
class SingleAndDoubleQualifying;
}

class SingleAndDoubleQualifying : public QWidget
{
    Q_OBJECT

public:
    explicit SingleAndDoubleQualifying(QWidget *parent = 0);
    ~SingleAndDoubleQualifying();

private:
    Ui::SingleAndDoubleQualifying *ui;
};

#endif // SINGLEANDDOUBLEQUALIFYING_H
