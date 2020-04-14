/********************************************************************************
** Form generated from reading UI file 'workspace.ui'
**
** Created by: Qt User Interface Compiler version 5.13.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_WORKSPACE_H
#define UI_WORKSPACE_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QTableWidget>

QT_BEGIN_NAMESPACE

class Ui_workspace
{
public:
    QTableWidget *assetsTable;
    QRadioButton *toggleComputer;
    QRadioButton *togglePeripherals;

    void setupUi(QDialog *workspace)
    {
        if (workspace->objectName().isEmpty())
            workspace->setObjectName(QString::fromUtf8("workspace"));
        workspace->resize(800, 450);
        workspace->setMinimumSize(QSize(800, 450));
        workspace->setMaximumSize(QSize(800, 450));
        assetsTable = new QTableWidget(workspace);
        assetsTable->setObjectName(QString::fromUtf8("assetsTable"));
        assetsTable->setGeometry(QRect(20, 30, 581, 401));
        toggleComputer = new QRadioButton(workspace);
        toggleComputer->setObjectName(QString::fromUtf8("toggleComputer"));
        toggleComputer->setGeometry(QRect(620, 30, 100, 21));
        toggleComputer->setChecked(true);
        togglePeripherals = new QRadioButton(workspace);
        togglePeripherals->setObjectName(QString::fromUtf8("togglePeripherals"));
        togglePeripherals->setGeometry(QRect(620, 60, 100, 21));

        retranslateUi(workspace);

        QMetaObject::connectSlotsByName(workspace);
    } // setupUi

    void retranslateUi(QDialog *workspace)
    {
        workspace->setWindowTitle(QCoreApplication::translate("workspace", "Dialog", nullptr));
        toggleComputer->setText(QCoreApplication::translate("workspace", "Computers", nullptr));
        togglePeripherals->setText(QCoreApplication::translate("workspace", "Peripherals", nullptr));
    } // retranslateUi

};

namespace Ui {
    class workspace: public Ui_workspace {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_WORKSPACE_H
