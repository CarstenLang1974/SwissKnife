from PySide6.QtWidgets import *
from PySide6 import QtCore
from PySide6.QtGui import QIcon
import EditLinkDialog
import logging
import os
import logging
log = logging.getLogger(__name__)

class LinkListView(QWidget):
    logger = logging.getLogger(__name__)
    closeAndComplete = QtCore.Signal(str)
    bringToFrontSignal = QtCore.Signal()
    projectLinkDoubleClicked = QtCore.Signal(int)
    projectLinkClicked = QtCore.Signal(int)
    projectLinkListChanged = QtCore.Signal()
    openUrlExtern = QtCore.Signal(str)
    settings = QtCore.QSettings("swissknife_ui.ini", QtCore.QSettings.IniFormat)

    def __init__(self, model, *args, **kwargs):
        super(LinkListView, self).__init__(*args, **kwargs)
        self.model = None
        log.debug("__init__ LinkListView")
        self.tableView = QTableView(self)
        self.setModel(model)
        main_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.tableView)
        self.setLayout(main_layout)

        #self.newLinkButton = QPushButton(QIcon(os.path.join('icons', 'arrow-180.png')), None, self)
        self.newLinkButton = QPushButton("new link", self)
        self.newLinkButton.setStatusTip("new link")
        self.newLinkButton.pressed.connect(self.on_newLink)
        buttons_layout.addWidget(self.newLinkButton)

        # self.editLinkButton = QPushButton(QIcon(os.path.join('icons', 'arrow-180.png')), None, self)
        self.editLinkButton = QPushButton("edit link", self)
        self.editLinkButton.setStatusTip("edit link")
        self.editLinkButton.pressed.connect(self.on_editLink)
        buttons_layout.addWidget(self.editLinkButton)

        # self.removeLinkButton = QPushButton(QIcon(os.path.join('icons', 'arrow-180.png')), None, self)
        self.removeLinkButton = QPushButton("remove link", self)
        self.removeLinkButton.setStatusTip("remove link")
        self.removeLinkButton.pressed.connect(self.on_deleteLink)
        buttons_layout.addWidget(self.removeLinkButton)

        self.moveLinkUpButton = QPushButton(QIcon(os.path.join('icons', 'arrow-090.png')), None, self)
        self.moveLinkUpButton.setStatusTip("move link up")
        self.moveLinkUpButton.pressed.connect(self.on_moveLinkUp)
        buttons_layout.addWidget(self.moveLinkUpButton)

        self.moveLinkDownButton = QPushButton(QIcon(os.path.join('icons', 'arrow-270.png')), None, self)
        self.moveLinkDownButton.setStatusTip("move link down")
        self.moveLinkDownButton.pressed.connect(self.on_moveLinkDown)
        buttons_layout.addWidget(self.moveLinkDownButton)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # setup table view and browser widget
        #self.tableView.clicked.connect(self.on_linkClick)
        #self.tableView.doubleClicked.connect(self.on_linkDoubleClick)
        self.tableView.clicked.connect(self.on_linkClick)
        self.tableView.doubleClicked.connect(self.on_linkDoubleClick)

    def setModel(self, model):
        self.model = model
        self.tableView.setModel(model)
        self.tableView.resizeRowsToContents()
        #self.tableView.resizeColumnsToContents()

    def saveGeometry(self):
        geometry = self.tableView.saveGeometry()
        #log.debug("save LinkListView geometry " + str(geometry))
        return geometry

    def restoreGeometry(self, Union, QByteArray=None, bytes=None, bytearray=None):
        result = self.tableView.restoreGeometry(Union)
        #log.debug("restore LinkListView geometry " + str(Union) + " : " + str(result))
        return result

    def saveHeader(self):
        header = self.tableView.horizontalHeader()
        headerState = header.saveState()
        #log.debug("save LinkListView headerState " + str(headerState))
        log.debug("save header section sizes: {0}, {1}, {2} ".format(header.sectionSize(0),
                                                 header.sectionSize(1),
                                                 header.sectionSize(2)))
        return headerState

    def restoreHeader(self, state):
        header = self.tableView.horizontalHeader()
        result = header.restoreState(state)
        #log.debug("restore header state " + str(state) + " : " + str(result))
        log.debug("restored header section sizes: {0}, {1}, {2} ".format(header.sectionSize(0),
                                                 header.sectionSize(1),
                                                 header.sectionSize(2)))
        return result

    def on_newLink(self):
        try:
            log.debug("on_newLink")
            dlg = EditLinkDialog.EditLinkDialog(None, self)
            if dlg.exec_():
                link = dlg.getLink()
                self.model.addLinkEntry(link)
                self.projectLinkListChanged.emit()
            else:
                log.debug("on_newLink Cancel EditLinkDialog")
        except Exception as e:
            log.error("exception in on_newLink", exc_info=True)

    def on_editLink(self):
        try:
            row = self.tableView.currentIndex().row()

            #index = self.tableView.model().createIndex(row, 0)
            #name = self.tableView.model().data(index,role=QtCore.Qt.DisplayRole)
            #index = self.tableView.model().createIndex(row, 1)
            #description = self.tableView.model().data(index, role=QtCore.Qt.DisplayRole)

            link=self.tableView.model().linkList[row]
            dlg = EditLinkDialog.EditLinkDialog(link, self)
            if dlg.exec_():
                newLink = dlg.getLink()
                self.tableView.model().replaceLinkEntry(row, newLink)
                self.projectLinkListChanged.emit()
            else:
                log.debug("on_editLink EditLinkDialog Cancel")
        except Exception as e:
            log.error("exception in on_editLink", exc_info=True)

    def on_deleteLink(self):
        try:
            row_number = self.tableView.selectionModel().selectedIndexes()[0].row()
            self.model.deleteLinkEntry(row_number)
            self.projectLinkListChanged.emit()
        except Exception as e:
            log.exception("exception in MainView.on_deleteLink: " + str(e))

    def on_moveLinkUp(self):
        try:
            row = self.tableView.currentIndex().row()
            linkList=self.tableView.model().linkList
            if row>0:
                replacedLink = linkList[row-1]
                linkList[row-1] = linkList[row]
                linkList[row] = replacedLink
                oldIndex = self.tableView.currentIndex()
                newIndex = self.tableView.model().createIndex(row-1, oldIndex.column())
                self.tableView.setCurrentIndex(newIndex)
                self.tableView.model().saveProject()
        except Exception as e:
            log.error("exception in on_moveLinkUp", exc_info=True)

    def on_moveLinkDown(self):
        try:
            row = self.tableView.currentIndex().row()
            linkList=self.tableView.model().linkList
            if row<(len(linkList)-1):
                replacedLink = linkList[row+1]
                linkList[row+1] = linkList[row]
                linkList[row] = replacedLink
                oldIndex = self.tableView.currentIndex()
                newIndex = self.tableView.model().createIndex(row+1, oldIndex.column())
                self.tableView.setCurrentIndex(newIndex)
                self.tableView.model().saveProject()
        except Exception as e:
            log.error("exception in on_moveLinkUp", exc_info=True)

    @QtCore.Slot()
    def on_linkClick(self):
        try:
            row_number = self.tableView.selectionModel().selectedIndexes()[0].row()
            #print("index is {}".format(row_number))
            self.projectLinkClicked.emit(row_number)
        except Exception as e:
            log.exception("exception in MainView.on_linkClick: " + str(e))

    @QtCore.Slot()
    def on_linkDoubleClick(self):
        try:
            row_number = self.tableView.selectionModel().selectedIndexes()[0].row()
            #print("index is {}".format(row_number))
            self.projectLinkDoubleClicked.emit(row_number)
        except Exception as e:
            log.exception("exception in MainView.on_linkDoubleClick: " + str(e))

