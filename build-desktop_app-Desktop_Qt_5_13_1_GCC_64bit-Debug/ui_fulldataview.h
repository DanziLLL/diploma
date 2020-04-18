/********************************************************************************
** Form generated from reading UI file 'fulldataview.ui'
**
** Created by: Qt User Interface Compiler version 5.13.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_FULLDATAVIEW_H
#define UI_FULLDATAVIEW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTextBrowser>

QT_BEGIN_NAMESPACE

class Ui_FullDataView
{
public:
    QTextBrowser *dataView;
    QPushButton *exit;

    void setupUi(QDialog *FullDataView)
    {
        if (FullDataView->objectName().isEmpty())
            FullDataView->setObjectName(QString::fromUtf8("FullDataView"));
        FullDataView->resize(500, 500);
        FullDataView->setMinimumSize(QSize(500, 500));
        FullDataView->setMaximumSize(QSize(500, 500));
        dataView = new QTextBrowser(FullDataView);
        dataView->setObjectName(QString::fromUtf8("dataView"));
        dataView->setGeometry(QRect(10, 10, 481, 431));
        exit = new QPushButton(FullDataView);
        exit->setObjectName(QString::fromUtf8("exit"));
        exit->setGeometry(QRect(170, 450, 171, 41));

        retranslateUi(FullDataView);

        QMetaObject::connectSlotsByName(FullDataView);
    } // setupUi

    void retranslateUi(QDialog *FullDataView)
    {
        FullDataView->setWindowTitle(QCoreApplication::translate("FullDataView", "Asset Data", nullptr));
        exit->setText(QCoreApplication::translate("FullDataView", "Exit", nullptr));
    } // retranslateUi

};

namespace Ui {
    class FullDataView: public Ui_FullDataView {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_FULLDATAVIEW_H
