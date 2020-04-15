#ifndef TASKSVIEW_H
#define TASKSVIEW_H

#include <QDialog>
#include <QJsonDocument>
#include <QJsonObject>
#include "inventory_api.h"

namespace Ui {
class tasksview;
}

class tasksview : public QDialog
{
    Q_OBJECT

public:
    int id;
    QString api_token;
    void cellDoubleClicked();
    void viewTasks();
    explicit tasksview(QWidget *parent = nullptr, QString token = "", int i = 0);
    ~tasksview();

private:
    Ui::tasksview *ui;
};

#endif // TASKSVIEW_H
