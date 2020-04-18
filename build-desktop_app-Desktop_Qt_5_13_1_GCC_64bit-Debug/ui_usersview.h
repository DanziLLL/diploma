/********************************************************************************
** Form generated from reading UI file 'usersview.ui'
**
** Created by: Qt User Interface Compiler version 5.13.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_USERSVIEW_H
#define UI_USERSVIEW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTableWidget>

QT_BEGIN_NAMESPACE

class Ui_usersview
{
public:
    QTableWidget *tableWidget;
    QLineEdit *loginEdit;
    QLineEdit *passEdit;
    QLineEdit *confirmEdit;
    QPushButton *btnCreate;
    QLabel *label;

    void setupUi(QDialog *usersview)
    {
        if (usersview->objectName().isEmpty())
            usersview->setObjectName(QString::fromUtf8("usersview"));
        usersview->resize(600, 400);
        tableWidget = new QTableWidget(usersview);
        tableWidget->setObjectName(QString::fromUtf8("tableWidget"));
        tableWidget->setGeometry(QRect(10, 10, 391, 381));
        loginEdit = new QLineEdit(usersview);
        loginEdit->setObjectName(QString::fromUtf8("loginEdit"));
        loginEdit->setGeometry(QRect(440, 110, 113, 25));
        passEdit = new QLineEdit(usersview);
        passEdit->setObjectName(QString::fromUtf8("passEdit"));
        passEdit->setGeometry(QRect(440, 170, 113, 25));
        passEdit->setEchoMode(QLineEdit::PasswordEchoOnEdit);
        confirmEdit = new QLineEdit(usersview);
        confirmEdit->setObjectName(QString::fromUtf8("confirmEdit"));
        confirmEdit->setGeometry(QRect(440, 230, 113, 25));
        confirmEdit->setEchoMode(QLineEdit::PasswordEchoOnEdit);
        btnCreate = new QPushButton(usersview);
        btnCreate->setObjectName(QString::fromUtf8("btnCreate"));
        btnCreate->setGeometry(QRect(442, 280, 111, 31));
        label = new QLabel(usersview);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(440, 70, 101, 20));

        retranslateUi(usersview);

        QMetaObject::connectSlotsByName(usersview);
    } // setupUi

    void retranslateUi(QDialog *usersview)
    {
        usersview->setWindowTitle(QCoreApplication::translate("usersview", "Users", nullptr));
        loginEdit->setText(QString());
        loginEdit->setPlaceholderText(QCoreApplication::translate("usersview", "Login", nullptr));
        passEdit->setPlaceholderText(QCoreApplication::translate("usersview", "Password", nullptr));
        confirmEdit->setText(QString());
        confirmEdit->setPlaceholderText(QCoreApplication::translate("usersview", "Confirm password", nullptr));
        btnCreate->setText(QCoreApplication::translate("usersview", "Create user", nullptr));
        label->setText(QCoreApplication::translate("usersview", "Add new user", nullptr));
    } // retranslateUi

};

namespace Ui {
    class usersview: public Ui_usersview {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_USERSVIEW_H
