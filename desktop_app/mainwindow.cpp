#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{

    ui->setupUi(this);
    ui->login->setFocus();
    ui->btn_go->setDefault(true);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_btn_go_clicked()
{
    QString api_token = inventory_api::login(ui->login->text(), ui->password->text());
    QString* login_data = inventory_api::validateToken(api_token);
    if (api_token == "err_no_token") {
        QMessageBox::critical(this, "Error", "Authentication error");
    }
    if (login_data == nullptr) {
        QMessageBox::critical(this, "Error", "Got invalid token");
        return;
    } //looking up for hash in database
    else {
        if (login_data[1] != "admin") {
            QMessageBox::critical(this, "Error", "You are not an admin");
            return;
        }
        else {
            workspace* w = new workspace(this, api_token);
            this->hide();
            w->show();
            return;
        }
    }
}
