#ifndef FULLDATAVIEW_H
#define FULLDATAVIEW_H

#include <QDialog>
#include <QJsonDocument>
#include <QJsonObject>
#include <QDebug>

namespace Ui {
class FullDataView;
}

class FullDataView : public QDialog
{
    Q_OBJECT

public:
    QJsonDocument data;
    explicit FullDataView(QWidget *parent = nullptr, QJsonDocument d = QJsonDocument());
    void viewJson();
    ~FullDataView();

private slots:
    void on_exit_clicked();

private:
    Ui::FullDataView *ui;
};

#endif // FULLDATAVIEW_H
