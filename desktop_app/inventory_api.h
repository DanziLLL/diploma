#ifndef INVENTORY_API_H
#define INVENTORY_API_H
#include <QString>
#include <QtNetwork>
#include <QMessageBox>


class inventory_api
{
public:
    inventory_api();
    static QString login(QString, QString);
    static QString* validateToken(QString);
    static QJsonDocument getAllComputers(QString);
    static QJsonDocument getQrCode(QString, int);

};

#endif // INVENTORY_API_H
