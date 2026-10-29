#include "singleanddoublequalifying.h"
#include "ui_singleanddoublequalifying.h"

SingleAndDoubleQualifying::SingleAndDoubleQualifying(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::SingleAndDoubleQualifying)
{
    ui->setupUi(this);
}

SingleAndDoubleQualifying::~SingleAndDoubleQualifying()
{
    delete ui;
}
