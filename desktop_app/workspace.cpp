#include "workspace.h"
#include "ui_workspace.h"
#include <QDebug>

workspace::workspace(QWidget *parent, QString api_token) :
    QDialog(parent),
    ui(new Ui::workspace)
{
    this->api_token = api_token;
    ui->setupUi(this);
    viewComputers(inventory_api::getAllComputers(api_token));
    ui->assetsTable->setContextMenuPolicy(Qt::CustomContextMenu);

    // Connect SLOT to context menu
    connect(ui->assetsTable, SIGNAL(customContextMenuRequested(QPoint)), this, SLOT(slotCustomMenuRequested(QPoint)));
}

workspace::~workspace()
{
    delete ui;
}

void workspace::viewComputers(QJsonDocument d) {
    QJsonObject o = d.object();
    QStringList ids = o.keys();
//    ui->assetsTable->setRowCount(o.keys().length());
    ui->assetsTable->setColumnCount(3);
    ui->assetsTable->setHorizontalHeaderLabels(QStringList() << "id" << "hostname" << "ip");
    ui->assetsTable->horizontalHeader()->setSectionResizeMode(1, QHeaderView::Stretch);
    ui->assetsTable->horizontalHeader()->setSectionResizeMode(2, QHeaderView::Stretch);
    ui->assetsTable->horizontalHeader()->show();
    for (int i = 0; i < ids.length(); i++) {
        QJsonDocument entry = QJsonDocument(d[ids[i]].toObject());
        ui->assetsTable->insertRow(ui->assetsTable->rowCount() );
        QTableWidgetItem *item = new QTableWidgetItem();
        item->setText(ids[i]);
        ui->assetsTable->setItem(i, 0, item);
        QJsonDocument test = QJsonDocument::fromJson(d[ids[i]].toString().toUtf8());
        QTableWidgetItem *item1 = new QTableWidgetItem();
        item1->setText(entry["misc"]["hostname"].toString());
        ui->assetsTable->setItem( i, 1, item1);
        QTableWidgetItem *item2 = new QTableWidgetItem();
        QStringList interfaces = entry["network"].toObject().keys();
        item2->setText(entry["network"][interfaces[interfaces.length()-1]]["ip"].toString());
        ui->assetsTable->setItem( i, 2, item2);
    }
}

void workspace::on_toggleComputer_clicked()
{
    if (ui->toggleComputer->isChecked()) {
        ui->togglePeripherals->setChecked(false);
    }
    else {
        ui->togglePeripherals->setChecked(true);
    }
}

void workspace::on_togglePeripherals_clicked()
{
    if (ui->togglePeripherals->isChecked()) {
        ui->toggleComputer->setChecked(false);
    }
    else {
        ui->toggleComputer->setChecked(true);
    }
}

void workspace::slotCustomMenuRequested(QPoint pos)
{
    /* Create an object context menu */
    QMenu * menu = new QMenu(this);
    /* Create actions to the context menu */
    QAction * getQR = new QAction(trUtf8("Get QR Code"), this);
    //QAction * deleteDevice = new QAction(trUtf8("Удалить"), this);
    /* Connect slot handlers for Action pop-up menu */
    connect(getQR, SIGNAL(triggered()), this, SLOT(slotGetQR()));     // Call Handler dialog editing
    //connect(deleteDevice, SIGNAL(triggered()), this, SLOT(slotRemoveRecord())); // Handler delete records
    /* Set the actions to the menu */
    menu->addAction(getQR);
    //menu->addAction(deleteDevice);
    /* Call the context menu */
    menu->popup(ui->assetsTable->viewport()->mapToGlobal(pos));
}

void workspace::slotGetQR() // TODO : FIX IT FOR FUCKS SAKE
{
    int id = ui->assetsTable->takeItem(ui->assetsTable->selectionModel()->currentIndex().row(), 0)->text().toInt();
    QJsonDocument d = inventory_api::getQrCode(api_token, id);
    QJsonObject o = d.object();
    QByteArray b64 = d["code"].toString().trimmed().toUtf8();
    QByteArray imageData = QByteArray::fromBase64( "iVBORw0KGgoAAAANSUhEUgAAASIAAAEiAQAAAAB1xeIbAAABgklEQVR4nO2aS47bMBBEX4cCZkkBcwAfhb5ybkAdxQcIIC4H4KCyIJV4PItko4+t5kIf4gEstKhWdUMm/j2mH/8BgVNOOeWUU0enrI8BKGZ2LcvMdVddp6CSJGkGposEBEmSvlLb63ppaujnMkL6CZZuQxUFDELdTdc5qVix66YrOtXHNG694mmpJedEAQVIuc/cF11HVf/cVI/9ZAAEoLxX4NP21XUGqsX+bo9Pl0p/DfbUdR5qMfQDynxaM/nN7u+q67Upmo/XDBDrcqu2+dWMfz6q+uem7oOdZvqh11bLo/DYr0K16JLmIOVYAYKUYy9pPfYrUsPfS0u3fmdEgDhjzXIeVf1zU39yTh+kGZQJUiZ4vl+T4r5lxpfE4/l+ZWrJ983sBJFUUY4V3/dbUWXp1U8jkG4DJH3YA7W9rnNR5U1MY5Bdy5uUD6Pr9ajh20z8ZaT5HU1j2E/XGajHPqYAMV0+zPuYa1OPPqdVWZrpH1z3OetR5v9GOeWUU06dgvoNpRDuTm0MMmQAAAAASUVORK5CYII=");
    QImage img;
    if (img.loadFromData(b64)) {
        // show this label somewhere.
        QLabel *label;
        label->setPixmap(QPixmap::fromImage(img));
        label->show();
    }
}
