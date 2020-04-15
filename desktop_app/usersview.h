#ifndef USERSVIEW_H
#define USERSVIEW_H

#include <QDialog>
#include "inventory_api.h"

namespace Ui {
class usersview;
}

class usersview : public QDialog
{
    Q_OBJECT

public:
    QString api_token;
    void viewusers();
    explicit usersview(QWidget *parent = nullptr, QString token = "");
    ~usersview();

private slots:
    void on_btnCreate_clicked();
    void slotCustomMenuRequested(QPoint);

private:
    Ui::usersview *ui;


};

#endif // USERSVIEW_H
