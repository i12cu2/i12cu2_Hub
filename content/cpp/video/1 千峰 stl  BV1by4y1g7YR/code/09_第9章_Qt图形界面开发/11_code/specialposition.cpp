#include "specialposition.h"
#include "ui_specialposition.h"

SpecialPosition::SpecialPosition(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::SpecialPosition)
{
    ui->setupUi(this);
}

SpecialPosition::~SpecialPosition()
{
    delete ui;
}
