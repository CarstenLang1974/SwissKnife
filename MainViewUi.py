# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainViewUi.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QSplitter, QStatusBar, QTabWidget,
    QTreeView, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(532, 592)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(10)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.lineEdit.setFont(font)

        self.verticalLayout.addWidget(self.lineEdit)

        self.treeView = QTreeView(self.layoutWidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setStyleSheet(u"QTreeView::item:active { color: black; }   /*  When widget has focus*/\n"
"QTreeView::item:!active { color: black; } /*  When widget doesn't have focus*/\n"
"QTreeView::item:selected:active{\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);\n"
"}\n"
"\n"
"QTreeView::item:selected:!active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);\n"
"}")

        self.verticalLayout.addWidget(self.treeView)

        self.splitter.addWidget(self.layoutWidget)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(300, 0))
        self.tabProject = QWidget()
        self.tabProject.setObjectName(u"tabProject")
        self.verticalLayout_2 = QVBoxLayout(self.tabProject)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.projectSelectorLayout = QHBoxLayout()
        self.projectSelectorLayout.setObjectName(u"projectSelectorLayout")

        self.verticalLayout_2.addLayout(self.projectSelectorLayout)

        self.projecTabSplitter = QSplitter(self.tabProject)
        self.projecTabSplitter.setObjectName(u"projecTabSplitter")
        self.projecTabSplitter.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout_2.addWidget(self.projecTabSplitter)

        self.tabWidget.addTab(self.tabProject, "")
        self.tabTools = QWidget()
        self.tabTools.setObjectName(u"tabTools")
        self.tabWidget.addTab(self.tabTools, "")
        self.splitter.addWidget(self.tabWidget)

        self.horizontalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 532, 33))
        self.menuApplication = QMenu(self.menubar)
        self.menuApplication.setObjectName(u"menuApplication")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuApplication.menuAction())
        self.menuApplication.addAction(self.actionExit)
        self.menuApplication.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Filter:", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"type to filter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabProject), QCoreApplication.translate("MainWindow", u"Projects", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTools), QCoreApplication.translate("MainWindow", u"Python", None))
        self.menuApplication.setTitle(QCoreApplication.translate("MainWindow", u"Application", None))
    # retranslateUi

