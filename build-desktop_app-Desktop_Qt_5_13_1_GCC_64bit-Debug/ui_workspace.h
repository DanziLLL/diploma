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
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTableWidget>

QT_BEGIN_NAMESPACE

class Ui_workspace
{
public:
    QTableWidget *assetsTable;
    QPushButton *btnRefresh;
    QPushButton *btnAllTasks;
    QPushButton *btnUsers;
    QPushButton *btnChangelog;

    void setupUi(QDialog *workspace)
    {
        if (workspace->objectName().isEmpty())
            workspace->setObjectName(QString::fromUtf8("workspace"));
        workspace->resize(800, 450);
        workspace->setMinimumSize(QSize(800, 450));
        workspace->setMaximumSize(QSize(800, 450));
        assetsTable = new QTableWidget(workspace);
        assetsTable->setObjectName(QString::fromUtf8("assetsTable"));
        assetsTable->setGeometry(QRect(20, 20, 581, 411));
        btnRefresh = new QPushButton(workspace);
        btnRefresh->setObjectName(QString::fromUtf8("btnRefresh"));
        btnRefresh->setGeometry(QRect(620, 390, 161, 41));
        btnAllTasks = new QPushButton(workspace);
        btnAllTasks->setObjectName(QString::fromUtf8("btnAllTasks"));
        btnAllTasks->setGeometry(QRect(620, 340, 161, 41));
        btnUsers = new QPushButton(workspace);
        btnUsers->setObjectName(QString::fromUtf8("btnUsers"));
        btnUsers->setGeometry(QRect(620, 290, 161, 41));
        btnChangelog = new QPushButton(workspace);
        btnChangelog->setObjectName(QString::fromUtf8("btnChangelog"));
        btnChangelog->setGeometry(QRect(620, 240, 161, 41));

        retranslateUi(workspace);

        QMetaObject::connectSlotsByName(workspace);
    } // setupUi

    void retranslateUi(QDialog *workspace)
    {
        workspace->setWindowTitle(QCoreApplication::translate("workspace", "Dialog", nullptr));
        btnRefresh->setText(QCoreApplication::translate("workspace", "Reload computers list", nullptr));
        btnAllTasks->setText(QCoreApplication::translate("workspace", "Show all tasks", nullptr));
        btnUsers->setText(QCoreApplication::translate("workspace", "Users", nullptr));
        btnChangelog->setText(QCoreApplication::translate("workspace", "Full changelog", nullptr));
    } // retranslateUi

};

namespace Ui {
    class workspace: public Ui_workspace {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_WORKSPACE_H
