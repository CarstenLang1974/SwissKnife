from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from MainViewUi import Ui_MainWindow
import browser
import AboutSwissKnife
import LinkListView
import ToolsWidget
import logging
log = logging.getLogger(__name__)

class MainView(QMainWindow, Ui_MainWindow):
    logger = logging.getLogger(__name__)
    closeAndComplete = QtCore.pyqtSignal(str)
    bringToFrontSignal = QtCore.pyqtSignal()
    projectChanged = QtCore.pyqtSignal()
    openUrlExtern = QtCore.pyqtSignal(str)
    settings = QtCore.QSettings("swissknife_ui.ini", QtCore.QSettings.IniFormat)

    def __init__(self, identifiers, model):
        super().__init__()
        self.setupUi(self)
        self.currentMatches = list()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # setup window properties and main menu
        self.setWindowTitle("My Python Swiss Knife")
        self.setMinimumSize(1600, 800)
        self.setWindowIcon(QIcon('icons/logo.png'))
        if model.getFramlessMode():
            self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(QtCore.Qt.Window)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.actionExit.triggered.connect(qApp.quit)
        self.actionAbout.triggered.connect(self.on_about)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # setup line edit
        completer = QCompleter(identifiers)
        self.lineEdit.setCompleter(completer)
        self.lineEdit.textChanged.connect(self.on_filter_change)
        self.lineEdit.returnPressed.connect(self.on_return)
        self.bringToFrontSignal.connect(self.bringToFront)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # setup tree view
        self.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setHeaderHidden(True)
        #self.treeView.selectionModel().selectionChanged.connect(self.on_treeviewClicked)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # setup project selection buttons
        self.projectSelector = QButtonGroup()
        self.projectSelector.buttonClicked[int].connect(self.on_projectSelector_clicked)

        # add global button
        style = qApp.style()
        button_id=0
        projects = model.getProjects()

        # add project buttons
        for p in projects:
            button = QPushButton()
            button.setCheckable(True)
            button.setText(p["name"])
            button.setIcon(QIcon(p["icon"]))
            button.setIconSize(QtCore.QSize(64, 64))
            self.projectSelector.addButton(button, button_id)
            self.projectSelectorLayout.addWidget(button)
            button_id += 1
        # add global button
        style = qApp.style()
        button = QPushButton()
        button.setCheckable(True)
        button.setText("global")
        button.setIcon(QIcon(style.standardIcon(QStyle.SP_ComputerIcon)))
        button.setIconSize(QtCore.QSize(64, 64))
        button.setMaximumWidth(100)
        self.projectSelector.addButton(button, button_id)
        self.projectSelectorLayout.addWidget(button)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # setup table view and browser widget
        self.linkListView = LinkListView.LinkListView(model.getCurrentProject())
        self.projecTabSplitter.addWidget(self.linkListView)
        self.browserWidget = browser.BrowserWidget(self.openUrlExtern)
        self.projecTabSplitter.addWidget(self.browserWidget)
        #self.horizontalLayoutProjectViews.addWidget(self.browserWidget)
        self.installEventFilter(self)
        self.linkListView.projectLinkListChanged.connect(self.on_projectLinkListChanged)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # init Tools
        self.tools = ToolsWidget.ToolsWidget()
        self.toolsLayout = QHBoxLayout()
        self.toolsLayout.addWidget(self.tools)
        self.tabTools.setLayout(self.toolsLayout)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # set/select project 0
        self.setModel(model)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # restore
        self.restore(self.settings)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:  # Catch the TouchBegin event.
            if event.key() == QtCore.Qt.Key_Escape:
                self.logger.info("ESCAPE pressed")
                self.hide()
                return True
        return super().eventFilter(obj, event)

    def setModel(self, model):
        self.model = model
        self.treeView.setModel(self.model)
        self.model.setCurrentProjectIndex(0)
        self.linkListView.setModel(self.model.getCurrentProject())

    def setProjectHtml(self):
        project = self.model.getCurrentProject()
        if project:
            url = project.getProjectUrl()
            if url:
                self.browserWidget.setHome(url=url)
            else:
                name, descr = project.getProjectNameAndDescription()
                html = "<h1>"+name+"</h1>"
                html+= "<p>"+descr+"</p>"
                self.browserWidget.setHome(content=html)
        else:
            html = "<h1>"+"no project selected"+"</h1>"
            self.browserWidget.setHome(content=html)

    def on_projectSelector_clicked(self, id):
        try:
            count = 0
            for button in self.projectSelector.buttons():
                if button is self.projectSelector.button(id):
                    log.debug("selected {0} - id {1}".format(button.text(), count))
                    self.setProjectIndex(count)
                    self.projectChanged.emit()
                count += 1
        except Exception as e:
            log.error("exception in MainView.on_projectSelector_clicked: " + str(e))

    def on_projectLinkListChanged(self):
        self.model.updateTreeModel()

    def on_treeviewClicked(self, currentIndex, previousIndex):
        log.debug("tree view: current index: {0}".format(currentIndex))

    def setProjectIndex(self, indexValue):
        if indexValue is None:
            index = len(self.model.getProjects())
        else:
            index = int(indexValue)
        self.model.setCurrentProjectIndex(index)
        self.projectSelector.button(index).setChecked(True)
        if self.model.currentProjectIndex is not None:
            self.linkListView.setModel(self.model.getCurrentProject())
        else:
            self.linkListView.setModel(self.model.globals)
        self.setProjectHtml()
        self.setTreeForProject()
        self.setTreeSelection(self.lineEdit.text())

    def setTreeForProject(self):
        if self.model.currentProjectIndex is not None:
            projectItem = self.model.getProjectByIndex(self.model.currentProjectIndex)
            modelIndex = self.model.indexFromItem(projectItem)
            self.treeView.collapseAll()
            self.treeView.expand(modelIndex)
        else:
            self.treeView.collapseAll()

    def setTreeSelection(self, filter):
        log.debug("setTreeSelection for " + str(filter))
        selection_model = self.treeView.selectionModel()
        selection_model.clear()
        matches = list()
        if filter != "":
            items = self.model.findItems(filter, flags=QtCore.Qt.MatchStartsWith | QtCore.Qt.MatchRecursive)
            currentProjectName = self.model.getCurrentProject().getName()
            for i in items:
                if not i.hasChildren() and (i.parent() is None or i.parent().text() == currentProjectName):
                    # no project items and only global items or in current project
                    index = self.model.indexFromItem(i)
                    selection_model.select(index, QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows)
                    matches.append(i.text())
        return matches

    @QtCore.pyqtSlot()
    def on_return(self):
        # attention if you don't catch exception explicit, there is no console output if the slot function has an error
        try:
            identifier = str(self.lineEdit.text())
            if len(self.currentMatches) > 0:
                # auto complete, if there is currently exactly one match
                identifier = self.currentMatches[0]
            #print("hide mainview and emit signal {0} with value {1}".format(self.closeAndComplete, identifier))
            self.closeAndComplete.emit(identifier)
            self.hide()
        except Exception as e:
            log.exception("exception in MainView.on_return: " + str(e))

    @QtCore.pyqtSlot()
    def on_filter_change(self):
        try:
            self.currentMatches = self.setTreeSelection(self.lineEdit.text())
        except Exception as e:
            log.exception("exception in MainView.on_filter_change: " + str(e))

    @QtCore.pyqtSlot()
    def on_about(self):
        try:
            AboutSwissKnife.about()
        except Exception as e:
            log.exception("exception in MainView.on_about: " + str(e))

    @QtCore.pyqtSlot()
    def bringToFront(self):
        #self.lineedit.setFocus()
        # the following will remove minimized status
        # and restore window with keeping maximized/normal state
        try:
            self.show()
            log.debug("show main view")
            self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
            self.raise_()
            self.activateWindow()
            self.lineEdit.clear()
            self.lineEdit.setFocus()
        except Exception as e:
            log.exception("exception in MainView.bringToFront: " + str(e))

    def hideEvent(self, event):
        log.debug("hide main view")
        #self.save(self.settings)

    def closeEvent(self, event):
        log.debug("close main view")
        self.save(self.settings)

    def save(self, settings):
        try:
            log.debug("save UI settings")
            settings.setValue("mainview/geometry", self.saveGeometry())
            settings.setValue("tabwidget/selection", self.tabWidget.currentIndex())
            settings.setValue("splitter/geometry", self.splitter.saveGeometry())
            settings.setValue("splitter/state", self.splitter.saveState())
            settings.setValue("projecTabSplitter/geometry", self.projecTabSplitter.saveGeometry())
            settings.setValue("projecTabSplitter/state", self.projecTabSplitter.saveState())
            settings.setValue("tableViewProject/geometry", self.linkListView.saveGeometry())
            settings.setValue("tableViewProject/headerstate", self.linkListView.saveHeader())
            settings.setValue("mainview/projectIndex", self.model.currentProjectIndex)
        except Exception as e:
            log.exception("MainView.save : " + str(e))

    def restore(self, settings):
        try:
            finfo = QtCore.QFileInfo(settings.fileName())
            if finfo.exists() and finfo.isFile():
                log.debug("restore UI settings")
                self.restoreGeometry(self.settings.value("mainview/geometry"))
                self.tabWidget.setCurrentIndex(int(self.settings.value("tabwidget/selection")))
                self.splitter.restoreGeometry(self.settings.value("splitter/geometry"))
                self.splitter.restoreState(settings.value("splitter/state"))
                self.linkListView.restoreGeometry(settings.value("tableViewProject/geometry"))
                self.linkListView.restoreHeader(settings.value("tableViewProject/headerstate"))
                self.projecTabSplitter.restoreGeometry(self.settings.value("projecTabSplitter/geometry"))
                self.projecTabSplitter.restoreState(settings.value("projecTabSplitter/state"))
                self.setProjectIndex(settings.value("mainview/projectIndex"))
        except Exception as e:
            log.exception("MainView.restore : " + str(e))

    def showMessage(self, message, window_title="Information"):
       log.debug('show message box' + str(message))
       msgBox = QMessageBox()
       msgBox.setIcon(QMessageBox.Information)
       msgBox.setText(message)
       msgBox.setWindowTitle(window_title)
       #msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
       msgBox.setStandardButtons(QMessageBox.Ok)
       #msgBox.buttonClicked.connect(msgButtonClick)

       returnValue = msgBox.exec()
       if returnValue == QMessageBox.Ok:
          log.debug('OK clicked')
