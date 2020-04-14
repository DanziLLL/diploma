#ifndef WORKSPACE_H
#define WORKSPACE_H

#include <QDialog>
#include <QJsonDocument>
#include <QJsonObject>
#include <QMenu>
#include <QLabel>

#include "inventory_api.h"

namespace Ui {
class workspace;
}

class workspace : public QDialog
{
    Q_OBJECT

public:
    QString api_token;
    explicit workspace(QWidget *parent = nullptr, QString api_token = "");
    void viewComputers(QJsonDocument);
    ~workspace();

private slots:
    void on_togglePeripherals_clicked();
    void slotCustomMenuRequested(QPoint);
    void slotGetQR();
    void on_toggleComputer_clicked();

private:
    Ui::workspace *ui;
};

#endif // WORKSPACE_H
