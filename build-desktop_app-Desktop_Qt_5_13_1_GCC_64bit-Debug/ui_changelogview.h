/********************************************************************************
** Form generated from reading UI file 'changelogview.ui'
**
** Created by: Qt User Interface Compiler version 5.13.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_CHANGELOGVIEW_H
#define UI_CHANGELOGVIEW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QTableWidget>

QT_BEGIN_NAMESPACE

class Ui_changelogview
{
public:
    QTableWidget *tableWidget;

    void setupUi(QDialog *changelogview)
    {
        if (changelogview->objectName().isEmpty())
            changelogview->setObjectName(QString::fromUtf8("changelogview"));
        changelogview->resize(500, 400);
        tableWidget = new QTableWidget(changelogview);
        tableWidget->setObjectName(QString::fromUtf8("tableWidget"));
        tableWidget->setGeometry(QRect(10, 10, 481, 381));

        retranslateUi(changelogview);

        QMetaObject::connectSlotsByName(changelogview);
    } // setupUi

    void retranslateUi(QDialog *changelogview)
    {
        changelogview->setWindowTitle(QCoreApplication::translate("changelogview", "Changelog", nullptr));
    } // retranslateUi

};

namespace Ui {
    class changelogview: public Ui_changelogview {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_CHANGELOGVIEW_H
