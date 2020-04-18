/********************************************************************************
** Form generated from reading UI file 'viewqr.ui'
**
** Created by: Qt User Interface Compiler version 5.13.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_VIEWQR_H
#define UI_VIEWQR_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>

QT_BEGIN_NAMESPACE

class Ui_viewQR
{
public:
    QLabel *QRView;
    QPushButton *toClipboard;
    QPushButton *exit;

    void setupUi(QDialog *viewQR)
    {
        if (viewQR->objectName().isEmpty())
            viewQR->setObjectName(QString::fromUtf8("viewQR"));
        viewQR->resize(400, 500);
        QRView = new QLabel(viewQR);
        QRView->setObjectName(QString::fromUtf8("QRView"));
        QRView->setGeometry(QRect(20, 20, 360, 360));
        toClipboard = new QPushButton(viewQR);
        toClipboard->setObjectName(QString::fromUtf8("toClipboard"));
        toClipboard->setGeometry(QRect(39, 400, 111, 80));
        exit = new QPushButton(viewQR);
        exit->setObjectName(QString::fromUtf8("exit"));
        exit->setGeometry(QRect(250, 400, 111, 80));

        retranslateUi(viewQR);

        QMetaObject::connectSlotsByName(viewQR);
    } // setupUi

    void retranslateUi(QDialog *viewQR)
    {
        viewQR->setWindowTitle(QCoreApplication::translate("viewQR", "QR Code", nullptr));
        QRView->setText(QString());
        toClipboard->setText(QCoreApplication::translate("viewQR", "To Clipboard", nullptr));
        exit->setText(QCoreApplication::translate("viewQR", "Exit", nullptr));
    } // retranslateUi

};

namespace Ui {
    class viewQR: public Ui_viewQR {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_VIEWQR_H
