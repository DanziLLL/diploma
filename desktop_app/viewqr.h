#ifndef VIEWQR_H
#define VIEWQR_H

#include <QDialog>
#include <QClipboard>

namespace Ui {
class viewQR;
}

class viewQR : public QDialog
{
    Q_OBJECT

public:
    explicit viewQR(QWidget *parent = nullptr, QByteArray b64 = "");
    ~viewQR();

private slots:
    void on_exit_clicked();

    void on_toClipboard_clicked();

private:
    Ui::viewQR *ui;
};

#endif // VIEWQR_H
