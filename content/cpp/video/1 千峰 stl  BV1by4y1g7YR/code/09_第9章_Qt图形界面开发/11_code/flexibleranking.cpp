#include "flexibleranking.h"
#include "ui_flexibleranking.h"

FlexibleRanking::FlexibleRanking(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::FlexibleRanking)
{
    ui->setupUi(this);
}

FlexibleRanking::~FlexibleRanking()
{
    delete ui;
}
