#ifndef FLEXIBLERANKING_H
#define FLEXIBLERANKING_H

#include <QWidget>

namespace Ui {
class FlexibleRanking;
}

class FlexibleRanking : public QWidget
{
    Q_OBJECT

public:
    explicit FlexibleRanking(QWidget *parent = 0);
    ~FlexibleRanking();

private:
    Ui::FlexibleRanking *ui;
};

#endif // FLEXIBLERANKING_H
