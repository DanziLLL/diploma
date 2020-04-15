#include "changelogview.h"
#include "ui_changelogview.h"

changelogview::changelogview(QWidget *parent, QString token, int i) :
    QDialog(parent),
    ui(new Ui::changelogview)
{
    ui->setupUi(this);
    api_token = token;
    id = i;
    viewchangelog();
}

changelogview::~changelogview()
{
    delete ui;
}

void changelogview::viewchangelog() {
    QJsonObject o = inventory_api::getChangelog(api_token, id).object();
    QStringList ids = o.keys();
    if (id == 0) {
        ui->tableWidget->setColumnCount(4);
        ui->tableWidget->setHorizontalHeaderLabels(QStringList() << "id" << "change_type" << "change" << "linked_to");
    }
    else {
        ui->tableWidget->setColumnCount(3);
        ui->tableWidget->setHorizontalHeaderLabels(QStringList() << "id" << "change_type" << "change");
    }
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
        item1->setText(entry["change"].toString());
        ui->tableWidget->setItem( i, 1, item1);
        QTableWidgetItem *item2 = new QTableWidgetItem();
        QTextEdit *edit = new QTextEdit();
        edit->setText(entry["data"].toString());
        item2->setText(entry["data"].toString());
        //ui->tableWidget->setItem(i, 2, item2);
        ui->tableWidget->setCellWidget(i,2,edit);
        if (id == 0) {
            QTableWidgetItem *item4 = new QTableWidgetItem();
            item4->setText(inventory_api::getComputerNameById(api_token, entry["linked_to"].toString().toInt()));
            ui->tableWidget->setItem(i, 3, item4);
        }
    }
    ui->tableWidget->resizeRowsToContents();
}


