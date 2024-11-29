#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QApplication>
#include <QLabel>
#include <QVBoxLayout>
#include <QWidget>
#include <vector>
#include <string>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_CREATEbutton_clicked();

    void on_DELETEbutton_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H

class ITEM{
public:
    std::string TYPE;
    std::string NOTE;
    std::string TEXT;
};
