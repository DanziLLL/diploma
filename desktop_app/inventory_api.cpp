#include "inventory_api.h"

const QString api_url = "http://inventoryapp.example.com:9000/api";

inventory_api::inventory_api()
{

}

QString inventory_api::login(QString login, QString password) {
    QString api_token = "";
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + "/auth");
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject json;
    json.insert("login", login);
    json.insert("password", password);
    QNetworkReply *reply = nam.post(request, QJsonDocument(json).toJson());
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    QByteArray response_data = reply->readAll();
    QJsonDocument json_response = QJsonDocument::fromJson(response_data);
    if (json_response["status"] == "ok") {
        QVariant cookieVar = reply->header(QNetworkRequest::SetCookieHeader);
        if (cookieVar.isValid()) {
            QList<QNetworkCookie> cookies = cookieVar.value<QList<QNetworkCookie> >();
            foreach (QNetworkCookie cookie, cookies) {
                if (cookie.name() == "api_token") {
                    api_token = cookie.value();
                }
            }
        }
    }
    else {
        api_token = "err_no_token";
    }
    return api_token;
}

QString* inventory_api::validateToken(QString token) {
    QString* data = new QString[2];

    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + "/validate_token");
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.get(request);
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        QJsonDocument json_response = QJsonDocument::fromJson(response_data);
        data[0] = json_response["user_id"].toString();
        data[1] = json_response["access_level"].toString();
        return data;
    }
    else {
        return nullptr;
    }
}


QJsonDocument inventory_api::getAllComputers(QString token) {
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + "/computer?all=true");
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.get(request);
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        QJsonDocument json_response = QJsonDocument::fromJson(response_data);
        return json_response;
    }
    else {
        return QJsonDocument();
    }
}

QJsonDocument inventory_api::getQrCode(QString token, int id) {
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + QString("/computer/qrcode?id=%1").arg(id));
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.get(request);
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        QJsonDocument json_response = QJsonDocument::fromJson(response_data);
        return json_response;
    }
    else {
        return QJsonDocument();
    }
}
