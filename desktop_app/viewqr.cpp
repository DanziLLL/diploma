#include "viewqr.h"
#include "ui_viewqr.h"

viewQR::viewQR(QWidget *parent, QByteArray b64) :
    QDialog(parent),
    ui(new Ui::viewQR)
{
    ui->setupUi(this);
    QImage img;
    img.loadFromData(b64, "PNG");
    img = img.scaled(350, 350, Qt::KeepAspectRatio);
    QPixmap p = QPixmap::fromImage(img);
    ui->QRView->setPixmap(p);
}

viewQR::~viewQR()
{
    delete ui;
}

void viewQR::on_exit_clicked()
{
    this->hide();
}

void viewQR::on_toClipboard_clicked()
{
    QApplication::clipboard()->setImage(ui->QRView->pixmap()->toImage(), QClipboard::Clipboard);
}
