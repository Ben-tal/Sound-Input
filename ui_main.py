# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainIyHmCN.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QKeySequenceEdit,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(408, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.NoteComboBox = QComboBox(self.frame_2)
        self.NoteComboBox.setObjectName(u"NoteComboBox")

        self.verticalLayout_2.addWidget(self.NoteComboBox)

        self.comboBox = QComboBox(self.frame_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_2.addWidget(self.comboBox)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.keySequence = QKeySequenceEdit(self.frame_3)
        self.keySequence.setObjectName(u"keySequence")

        self.gridLayout.addWidget(self.keySequence, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_6 = QFrame(self.frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.comboBox_2 = QComboBox(self.frame_6)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_3.addWidget(self.comboBox_2)

        self.Slider = QSlider(self.frame_6)
        self.Slider.setObjectName(u"Slider")
        self.Slider.setMaximum(500)
        self.Slider.setOrientation(Qt.Horizontal)
        self.Slider.setTickPosition(QSlider.TicksAbove)

        self.horizontalLayout_3.addWidget(self.Slider)

        self.ValueSlider = QSpinBox(self.frame_6)
        self.ValueSlider.setObjectName(u"ValueSlider")
        self.ValueSlider.setCorrectionMode(QAbstractSpinBox.CorrectToPreviousValue)
        self.ValueSlider.setMaximum(500)
        self.ValueSlider.setDisplayIntegerBase(10)

        self.horizontalLayout_3.addWidget(self.ValueSlider)


        self.verticalLayout.addWidget(self.frame_6)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(200, 200))
        self.label.setMaximumSize(QSize(16777215, 16777215))
        self.label.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"border-width : 1.2px;\n"
"border-style:inset;")
        self.label.setPixmap(QPixmap(u"1.png"))

        self.verticalLayout.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBox_3 = QComboBox(self.frame_5)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gridLayout_2.addWidget(self.comboBox_3, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.frame_5)

        self.Add = QPushButton(self.frame_2)
        self.Add.setObjectName(u"Add")

        self.verticalLayout_2.addWidget(self.Add)

        self.table = QTableWidget(self.frame_2)
        if (self.table.columnCount() < 3):
            self.table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table.setObjectName(u"table")
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setProperty("showSortIndicator", False)
        self.table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_2.addWidget(self.table)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Export = QPushButton(self.frame_4)
        self.Export.setObjectName(u"Export")

        self.horizontalLayout_2.addWidget(self.Export)

        self.Import = QPushButton(self.frame_4)
        self.Import.setObjectName(u"Import")

        self.horizontalLayout_2.addWidget(self.Import)


        self.verticalLayout_2.addWidget(self.frame_4)

        self.Start = QPushButton(self.frame_2)
        self.Start.setObjectName(u"Start")

        self.verticalLayout_2.addWidget(self.Start)


        self.verticalLayout_3.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.NoteComboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Note to enable shortcut", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Mouse Move", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Mouse Click", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Keyboard", None))

        self.comboBox.setPlaceholderText("")
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Up", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Down", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"Left", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow", u"Rigth", None))

        self.label.setText("")
        self.comboBox_3.setItemText(0, QCoreApplication.translate("MainWindow", u"Left Click", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("MainWindow", u"Middle Click", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("MainWindow", u"Right Click", None))

        self.Add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Type", None));
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Key", None));
        ___qtablewidgetitem2 = self.table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        self.Export.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.Import.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.Start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
    # retranslateUi

