#include "inventory_api.h"

const QString api_url = "http://inventoryapp.example.com:9001/api";

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

QJsonDocument inventory_api::getAssetData(QString token, int id) {
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + QString("/computer?id=%1").arg(id));
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

void inventory_api::deleteAsset(QString token, int id) {
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + QString("/computer?id=%1").arg(id));
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.deleteResource(request);
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        QJsonDocument json_response = QJsonDocument::fromJson(response_data);
    }
}

QJsonDocument inventory_api::getTasks(QString token, int id) {
    QNetworkAccessManager nam;
    QJsonDocument json_response;
    QNetworkRequest request;
    if (id == 0) {
        request.setUrl(api_url + QString("/tasks?all=true"));
    }
    else {
        request.setUrl(api_url + QString("/tasks?computer_id=%1").arg(id));
    }
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.get(request);
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        json_response = QJsonDocument::fromJson(response_data);
    }
    return json_response;
}

void inventory_api::closeTask(QString token, int id) {
    QNetworkAccessManager nam;
    QJsonDocument json_response;
    QNetworkRequest request(api_url + QString("/tasks?id=%1&status=closed").arg(id));
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.sendCustomRequest(request, "PATCH");
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        json_response = QJsonDocument::fromJson(response_data);
    }
}

QString inventory_api::getLoginById(QString token, int id) {
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + QString("/users?id=%1").arg(id));
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.get(request);
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        QJsonDocument json_response = QJsonDocument::fromJson(response_data);
        return json_response.object()["login"].toString();
    }
    else {
        return "";
    }
}

QJsonDocument inventory_api::getUserList(QString token) {
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + QString("/users?all=true"));
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

QString inventory_api::getComputerNameById(QString token, int id) {
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + QString("/computer?id=%1").arg(id));
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.get(request);
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        QJsonDocument json_response = QJsonDocument::fromJson(response_data);
        return json_response["misc"]["hostname"].toString();
    }
    else {
        return "";
    }
}


QString inventory_api::getRegistrationToken(QString token) {
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + QString("/register"));
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.get(request);
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        QJsonDocument json_response = QJsonDocument::fromJson(response_data);
        return json_response["registration_token"].toString();
    }
    else {
        return "";
    }
}

QString inventory_api::registerNewUser(QString login, QString password, QString registration_token) {
    QString api_token = "";
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + "/register");
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject json;
    json.insert("login", login);
    json.insert("password", password);
    json.insert("token", registration_token);
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

void inventory_api::deleteUser(QString token, int id) {
    QNetworkAccessManager nam;
    QNetworkRequest request(api_url + QString("/users?id=%1").arg(id));
    request.setRawHeader("Cookie", QString("api_token=%1").arg(token).toUtf8());
    QNetworkReply *reply = nam.deleteResource(request);
    while (!reply->isFinished())
    {
        qApp->processEvents();
    }
    if (reply->error() == reply->NoError) {
        QByteArray response_data = reply->readAll();
        QJsonDocument json_response = QJsonDocument::fromJson(response_data);
    }
}

QJsonDocument inventory_api::getChangelog(QString token, int id) {
    QNetworkAccessManager nam;
    QNetworkRequest request;
    if (id == 0) {
        request.setUrl(api_url + QString("/computer/changes?all=true"));
    }
    else {
        request.setUrl(api_url + QString("/computer/changes?computer_id=%1").arg(id));
    }
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
