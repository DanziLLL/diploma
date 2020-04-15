#include "tasksview.h"
#include "ui_tasksview.h"

tasksview::tasksview(QWidget *parent, QString token, int i) :
    QDialog(parent),
    ui(new Ui::tasksview)
{
    ui->setupUi(this);
    api_token = token;
    id = i;
    viewTasks();
    connect(ui->tableWidget, &QTableWidget::cellDoubleClicked, this, &tasksview::cellDoubleClicked);

}

tasksview::~tasksview()
{
    delete ui;
}

void tasksview::viewTasks() {
    QJsonObject o = inventory_api::getTasks(api_token, id).object();
    QStringList ids = o.keys();
    if (id == 0) {
        ui->tableWidget->setColumnCount(5);
        ui->tableWidget->setHorizontalHeaderLabels(QStringList() << "id" << "summary" << "body" << "created by" << "linked_to");
    }
    else {
        ui->tableWidget->setColumnCount(4);
        ui->tableWidget->setHorizontalHeaderLabels(QStringList() << "id" << "summary" << "body" << "created by");
    }
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
        item1->setText(entry["summary"].toString());
        ui->tableWidget->setItem( i, 1, item1);
        QTableWidgetItem *item2 = new QTableWidgetItem();
        item2->setText(entry["body"].toString());
        ui->tableWidget->setItem(i, 2, item2);
        QTableWidgetItem *item3 = new QTableWidgetItem();
        item3->setText(inventory_api::getLoginById(api_token, entry["created_by"].toInt()));
        ui->tableWidget->setItem(i, 3, item3);
        if (id == 0) {
            QTableWidgetItem *item4 = new QTableWidgetItem();
            item4->setText(inventory_api::getComputerNameById(api_token, entry["linked_to"].toString().toInt()));
            ui->tableWidget->setItem(i, 4, item4);
        }
    }
}

void tasksview::cellDoubleClicked()
{
    QList<QTableWidgetItem *> list = ui->tableWidget->selectedItems();
    int id = list.at(0)->text().toInt();
    inventory_api::closeTask(api_token, id);
    ui->tableWidget->setRowCount(0);
    viewTasks();
}
