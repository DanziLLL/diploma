#ifndef INVENTORY_API_H
#define INVENTORY_API_H
#include <QString>
#include <QtNetwork>


class inventory_api
{
public:
    inventory_api();
    static QString login(QString, QString);
    static QString* validateToken(QString);
    static QJsonDocument getAllComputers(QString);
    static QJsonDocument getQrCode(QString, int);
    static QJsonDocument getAssetData(QString, int);
    static QJsonDocument getTasks(QString, int);
    static void deleteAsset(QString, int);
    static void closeTask(QString, int);
    static QString getLoginById(QString, int);
    static QJsonDocument getUserList(QString);
    static QString getComputerNameById(QString, int);
    static QString getRegistrationToken(QString);
    static QString registerNewUser(QString, QString, QString);


};

#endif // INVENTORY_API_H
