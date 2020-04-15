#include "fulldataview.h"
#include "ui_fulldataview.h"

QString parseJson(QJsonObject j, int depth, QString res) {
    QString tabs = "";
    res = "";
    for (int i = 0; i < depth; i++) {
        tabs += "\t";
    }
    QJsonObject::iterator it;
    for (it = j.begin(); it != j.end(); it++) {
        if (it.value().isObject()) {
            res += tabs + it.key() + ":\n";
            res += parseJson(it->toObject(), depth + 1, res);
        }
        else {
            res += tabs + it.key() + ": " +  it.value().toVariant().toString() + "\n";
        }
    }
    return res;
}

FullDataView::FullDataView(QWidget *parent, QJsonDocument d) :
    QDialog(parent),
    ui(new Ui::FullDataView)
{
    ui->setupUi(this);
    data = d;
    viewJson();
}

FullDataView::~FullDataView()
{
    delete ui;
}

void FullDataView::on_exit_clicked()
{
    this->hide();
}

void FullDataView::viewJson() {
    QJsonObject o = data.object();
    QString text = parseJson(o, 0, "");
    ui->dataView->setText(text);
}
