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
    qDebug() << ids.length();
    ui->assetsTable->setColumnCount(3);
    ui->assetsTable->setHorizontalHeaderLabels(QStringList() << "id" << "hostname" << "ip");
    ui->assetsTable->horizontalHeader()->setSectionResizeMode(1, QHeaderView::Stretch);
    ui->assetsTable->horizontalHeader()->setSectionResizeMode(2, QHeaderView::Stretch);
    ui->assetsTable->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->assetsTable->setEditTriggers(QAbstractItemView::NoEditTriggers);
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
        ui->assetsTable->setItem(i, 2, item2);
    }
}

void workspace::slotCustomMenuRequested(QPoint pos)
{
    QMenu * menu = new QMenu(this);
    QAction* getQR = new QAction("Get QR Code", this);
    connect(getQR, SIGNAL(triggered()), this, SLOT(slotGetQR()));
    menu->addAction(getQR);
    QAction* getFullData = new QAction("Get full data", this);
    connect(getFullData, SIGNAL(triggered()), this, SLOT(slotGetAssetData()));
    menu->addAction(getFullData);
    QAction* tasks = new QAction("Get linked tasks", this);
    connect(tasks, SIGNAL(triggered()), this, SLOT(slotGetTasks()));
    menu->addAction(tasks);
    QAction* changelog = new QAction("Get changelog", this);
    connect(changelog, SIGNAL(triggered()), this, SLOT(slotGetChangelog()));
    menu->addAction(changelog);
    QAction* del = new QAction("Delete", this);
    connect(del, SIGNAL(triggered()), this, SLOT(slotDeleteAsset()));
    menu->addAction(del);
    menu->popup(ui->assetsTable->viewport()->mapToGlobal(pos));
}

void workspace::createQRView(QByteArray b64) {
    viewQR *v = new viewQR(this, b64);
    v->show();
}

void workspace::slotGetQR()
{
    int id = 0;
    QList<QTableWidgetItem *> list = ui->assetsTable->selectedItems();
    id = list.at(0)->text().toInt();
    QJsonDocument d = inventory_api::getQrCode(api_token, id);
    QByteArray b64 = QByteArray::fromBase64(d["code"].toString().toUtf8());
    createQRView(b64);
}

void workspace::slotDeleteAsset() {
    int id = 0;
    QList<QTableWidgetItem *> list = ui->assetsTable->selectedItems();
    id = list.at(0)->text().toInt();
    inventory_api::deleteAsset(api_token, id);
    refresh();
}

void workspace::slotGetAssetData() {
    int id = 0;
    QList<QTableWidgetItem *> list = ui->assetsTable->selectedItems();
    id = list.at(0)->text().toInt();
    QJsonDocument d = inventory_api::getAssetData(api_token, id);
    qDebug() << d;
    FullDataView *v = new FullDataView(this, d);
    v->show();
}

void workspace::slotGetTasks() {
    int id = 0;
    QList<QTableWidgetItem *> list = ui->assetsTable->selectedItems();
    id = list.at(0)->text().toInt();
    tasksview *v = new tasksview(this, api_token, id);
    v->show();
}

void workspace::slotGetChangelog() {
    int id = 0;
    QList<QTableWidgetItem *> list = ui->assetsTable->selectedItems();
    id = list.at(0)->text().toInt();
    changelogview *v = new changelogview(this, api_token, id);
    v->show();
}

void workspace::refresh() {
    ui->assetsTable->setRowCount(0);
    viewComputers(inventory_api::getAllComputers(api_token));
}

void workspace::on_btnRefresh_clicked()
{
    refresh();
}

void workspace::on_btnAllTasks_clicked()
{
    tasksview *v = new tasksview(this, api_token, 0);
    v->show();
}

void workspace::on_btnUsers_clicked()
{
    usersview *v = new usersview(this, api_token);
    v->show();
}

void workspace::on_btnChangelog_clicked()
{
    changelogview *v = new changelogview(this, api_token, 0);
    v->show();
}
