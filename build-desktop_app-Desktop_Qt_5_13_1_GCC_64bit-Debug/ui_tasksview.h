/********************************************************************************
** Form generated from reading UI file 'tasksview.ui'
**
** Created by: Qt User Interface Compiler version 5.13.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_TASKSVIEW_H
#define UI_TASKSVIEW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QTableWidget>

QT_BEGIN_NAMESPACE

class Ui_tasksview
{
public:
    QTableWidget *tableWidget;

    void setupUi(QDialog *tasksview)
    {
        if (tasksview->objectName().isEmpty())
            tasksview->setObjectName(QString::fromUtf8("tasksview"));
        tasksview->resize(600, 500);
        tableWidget = new QTableWidget(tasksview);
        tableWidget->setObjectName(QString::fromUtf8("tableWidget"));
        tableWidget->setGeometry(QRect(10, 10, 581, 481));

        retranslateUi(tasksview);

        QMetaObject::connectSlotsByName(tasksview);
    } // setupUi

    void retranslateUi(QDialog *tasksview)
    {
        tasksview->setWindowTitle(QCoreApplication::translate("tasksview", "Dialog", nullptr));
    } // retranslateUi

};

namespace Ui {
    class tasksview: public Ui_tasksview {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_TASKSVIEW_H
