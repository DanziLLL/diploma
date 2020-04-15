#ifndef CHANGELOGVIEW_H
#define CHANGELOGVIEW_H

#include <QDialog>
#include <QTextEdit>
#include "inventory_api.h"

namespace Ui {
class changelogview;
}

class changelogview : public QDialog
{
    Q_OBJECT

public:
    QString api_token;
    int id;
    explicit changelogview(QWidget *parent = nullptr, QString token = "", int id = 0);
    void viewchangelog();
    ~changelogview();

private:
    Ui::changelogview *ui;
};

#endif // CHANGELOGVIEW_H
