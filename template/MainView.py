from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
import numpy as np
import pyqtgraph as pg
import logging
log = logging.getLogger(__name__)

class MainView(QMainWindow):
    logger = logging.getLogger(__name__)

    def __init__(self, model):
        super().__init__()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # setup window properties and main menu
        self.setWindowTitle("My Python Swiss Knife")
        self.setMinimumSize(1600, 800)
        self.setWindowFlags(QtCore.Qt.Window)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # setup line edit
        self.layout = QVBoxLayout()
        self.layoutLineEdit = QHBoxLayout()
        self.layoutLineEdit.addWidget(QLabel("arguments:"))
        self.lineEdit = QLineEdit()
        self.lineEdit.textChanged.connect(self.on_change)
        self.lineEdit.returnPressed.connect(self.on_return)
        self.layoutLineEdit.addWidget(self.lineEdit)

        # add global button
        style = qApp.style()
        button = QPushButton()
        button.setCheckable(True)
        button.setText("global")
        button.setIcon(QIcon(style.standardIcon(QStyle.SP_ComputerIcon)))
        button.setMaximumWidth(100)
        self.layoutLineEdit.addWidget(button)
        self.layout.addLayout(self.layoutLineEdit)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.layout)

        self.pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
        self.layout.addWidget(self.pw)

        data1 = np.random.normal(size=100) * 1000
        data2= data1 + 100
        curve1 = self.pw.plot(data1)
        curve1.setPen((0,0,0))  ## white pen
        curve2 = self.pw.plot(data2)
        curve2.setPen('r')  ## white pen

        self.pw.setBackground('w')
        pfill = pg.FillBetweenItem(curve1, curve2, brush=(0,0,255,100))

        self.pw.addItem(pfill)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # set/select project 0
        self.setModel(model)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # restore
        #self.restore(self.settings)

    def setModel(self, model):
        self.model = model

    @QtCore.pyqtSlot()
    def on_return(self):
        # attention if you don't catch exception explicit, there is no console output if the slot function has an error
        try:
            identifier = str(self.lineEdit.text())
            log.debug("lineEditText:" + identifier)
        except Exception as e:
            log.exception("exception in MainView.on_return: " + str(e))

    @QtCore.pyqtSlot()
    def on_change(self):
        # attention if you don't catch exception explicit, there is no console output if the slot function has an error
        try:
            identifier = str(self.lineEdit.text())
            log.debug("lineEditText:" + identifier)
        except Exception as e:
            log.exception("exception in MainView.on_change: " + str(e))

    def closeEvent(self, event):
        log.debug("close main view")
        #self.save(self.settings)

    def save(self, settings):
        try:
            log.debug("save UI settings")
            settings.setValue("mainview/geometry", self.saveGeometry())
        except Exception as e:
            log.exception("MainView.save : " + str(e))

    def restore(self, settings):
        try:
            finfo = QtCore.QFileInfo(settings.fileName())
            if finfo.exists() and finfo.isFile():
                log.debug("restore UI settings")
                self.restoreGeometry(self.settings.value("mainview/geometry"))
        except Exception as e:
            log.exception("MainView.restore : " + str(e))
