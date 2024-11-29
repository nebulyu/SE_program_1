#include "mainwindow.h"
#include "ui_mainwindow.h"

using namespace std;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow() {
    delete ui;
}

vector<ITEM> ar;  // 存储 ITEM 的容器



// 创建新的 ITEM，添加到 ar 中
void create_new_ITEM(string type, string note, string text) {
    ITEM cur;
    cur.TYPE = type;
    cur.NOTE = note;
    cur.TEXT = text;
    ar.push_back(cur);
}


// 当 CREATE button 被点击时调用
void MainWindow::on_CREATEbutton_clicked() {
    QString qtype = ui->TYPEbox->currentText();
    QString qnote = ui->NOTEbox->toPlainText();
    QString qtext = ui->TEXTbox->toPlainText();

    // 将输入框内容转换为 std::string
    string type = qtype.toStdString();
    string note = qnote.toStdString();
    string text = qtext.toStdString();

    // 创建新 ITEM 并加入到 ar 中
    create_new_ITEM(type, note, text);

    // 清空输入框
    ui->NOTEbox->clear();
    ui->TEXTbox->clear();


    ui->DisplayTable->setRowCount(ar.size());
    int cnt = 0;
    for (auto cur : ar) {
        string type =cur.TYPE;
        QString qtype = QString::fromStdString(type);
        QTableWidgetItem *itm=new QTableWidgetItem();//创建一个Item
        itm->setText(qtype);
        ui->DisplayTable->setItem(cnt,0,itm);//把这个Item加到第一行第二列中
        ++cnt;
        // qDebug() << type <<"\n";
    }
}

void MainWindow::on_DELETEbutton_clicked()
{
    if(ar.empty()) return ;
    ar.pop_back();
    ui->DisplayTable->setRowCount(ar.size());
    for (auto cur : ar) {
        string type =cur.TYPE;
        qDebug() << type <<"\n";
    }
}

