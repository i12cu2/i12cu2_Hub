#include "mainwindow.h"
#include <QMenuBar>
#include <QMenu>
#include <QAction>
#include <QDebug>
#include <QToolBar>
#include <QStatusBar>
#include <QLabel>
#include <QTextEdit>
#include <QDockWidget>
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    this->resize(800,600);

    //创建 菜单栏
    QMenuBar *menuBar = new QMenuBar(this);
    //将菜单栏 添加到主窗口的特殊位置
    this->setMenuBar(menuBar);

    //创建菜单
    QMenu *file = new QMenu("文件", this);
    QMenu *edit = new QMenu("编辑", this);
    //将菜单 放入 菜单栏中
    menuBar->addMenu(file);
    menuBar->addMenu(edit);

    //创建菜单项
    QAction *New = new QAction("新建", this);
    QAction *Open = new QAction("打开", this);
    //将菜单项 添加到菜单中
    file->addAction(New);
    //添加一个分隔符
    file->addSeparator();
    file->addAction(Open);

    edit->addActions(QList<QAction *>()<<New<<Open);

    //让菜单项动起来
    connect(New, &QAction::triggered,[&](){
        qDebug()<<"新建文件了"<<endl;
    }  );
    connect(Open, &QAction::triggered,[&](){
        qDebug()<<"打开文件了"<<endl;
    }  );

    //设置菜单项的快捷方式
    New->setShortcut(QKeySequence(Qt::CTRL+Qt::Key_N));
    Open->setShortcut(tr("Ctrl+o"));

    //创建工具栏QToolBar
    QToolBar *toolBar = new QToolBar(this);
    //将工具栏 放入主窗口的特定位置
    this->addToolBar(toolBar);
    //将菜单项 放入工具栏中
    toolBar->addAction(New);
    toolBar->addAction(Open);
    //工具栏默认可以浮动、可以停靠四周
    //不允许工具栏浮动false
    toolBar->setFloatable(false);
    //只允许工具栏停靠左右
    toolBar->setAllowedAreas(Qt::LeftToolBarArea|Qt::RightToolBarArea);

    //创建状态栏
    QStatusBar *statusBar = new QStatusBar(this);
    //将状态栏 添加到 主窗口中
    this->setStatusBar(statusBar);
    //在状态栏上 添加左侧信息
    QLabel *label1= new QLabel("左侧提示信息", this);
    statusBar->addWidget(label1);
    //在状态栏上 添加右侧信息
    QLabel *label2= new QLabel("右侧提示信息", this);
    statusBar->addPermanentWidget(label2);

    //创建中心部件
    //将文本框作为中心部件
    QTextEdit *textEdit = new QTextEdit("这是中心部件", this);
    this->setCentralWidget(textEdit);

    //创建铆接部件
    QDockWidget *dock = new QDockWidget("我是铆接部件",this);
    //将铆接部件 添加到主窗口中
    this->addDockWidget(Qt::AllDockWidgetAreas, dock);

    //给菜单项添加图标 :代表的是资源文件
    New->setIcon(QIcon(":/image/New.png"));
    Open->setIcon(QIcon(":/image/Edit.png"));

}

MainWindow::~MainWindow()
{

}
