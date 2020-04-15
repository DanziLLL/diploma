#ifndef WORKSPACE_H
#define WORKSPACE_H

#include <QDialog>
#include <QJsonDocument>
#include <QJsonObject>
#include <QMenu>
#include <QLabel>

#include "inventory_api.h"
#include "viewqr.h"
#include "fulldataview.h"
#include "tasksview.h"

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
    void createQRView(QByteArray);
    void refresh();
    ~workspace();

private slots:
    void slotGetQR();
    void slotDeleteAsset();
    void slotGetAssetData();
    void slotGetTasks();
    void on_btnRefresh_clicked();
    void on_btnAllTasks_clicked();
    void slotCustomMenuRequested(QPoint);
    void on_btnUsers_clicked();

private:
    Ui::workspace *ui;
};

#endif // WORKSPACE_H
