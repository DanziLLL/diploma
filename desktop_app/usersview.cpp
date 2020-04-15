#include "usersview.h"
#include "ui_usersview.h"

usersview::usersview(QWidget *parent, QString token) :
    QDialog(parent),
    ui(new Ui::usersview)
{
    ui->setupUi(this);
    api_token = token;
    viewusers();
}

usersview::~usersview()
{
    delete ui;
}

void usersview::viewusers() {
    QJsonObject o = inventory_api::getUserList(api_token).object();
    QStringList ids = o.keys();
    ui->tableWidget->setColumnCount(3);
    ui->tableWidget->setHorizontalHeaderLabels(QStringList() << "id" << "login" << "access_level");
    ui->tableWidget->horizontalHeader()->setSectionResizeMode(1, QHeaderView::Stretch);
    ui->tableWidget->horizontalHeader()->setSectionResizeMode(2, QHeaderView::Stretch);
    ui->tableWidget->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->tableWidget->setEditTriggers(QAbstractItemView::NoEditTriggers);
    ui->tableWidget->horizontalHeader()->show();
    for (int i = 0; i < ids.length(); i++) {
        QJsonObject entry = o[ids[i]].toObject();
        ui->tableWidget->insertRow(ui->tableWidget->rowCount() );
        QTableWidgetItem *item = new QTableWidgetItem();
        item->setText(ids[i]);
        ui->tableWidget->setItem(i, 0, item);
        QTableWidgetItem *item1 = new QTableWidgetItem();
        item1->setText(entry["login"].toString());
        ui->tableWidget->setItem( i, 1, item1);
        QTableWidgetItem *item2 = new QTableWidgetItem();
        item2->setText(entry["access_level"].toString());
        ui->tableWidget->setItem(i, 2, item2);
    }
}

void usersview::slotCustomMenuRequested(QPoint pos)
{
    QMenu * menu = new QMenu(this);
    QAction* del = new QAction("Delete", this);
    connect(del, SIGNAL(triggered()), this, SLOT(slotDeleteAsset()));
    menu->addAction(del);
    menu->popup(ui->tableWidget->viewport()->mapToGlobal(pos));
}

void usersview::on_btnCreate_clicked()
{

}

void usersview::slotDeleteUser() {
    int id = 0;
    QList<QTableWidgetItem *> list = ui->tableWidget->selectedItems();
    id = list.at(0)->text().toInt();
    inventory_api::deleteUser(api_token, id);
    ui->tableWidget->setRowCount(0);
    viewusers();
}
