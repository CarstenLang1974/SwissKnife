import os
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
import logging
log = logging.getLogger(__name__)

import AboutSwissKnife

class RightClickMenu(QtWidgets.QMenu):
    # switchKeyboardSignal = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        QtWidgets.QMenu.__init__(self, "RightClickMenu", parent=parent)

        # show main window action
        style = QtWidgets.qApp.style()
        icon = QtGui.QIcon(style.standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        self.showAction = QtWidgets.QAction(icon, "&Show Main Window", self)
        self.addAction(self.showAction)

        # # enable/disable shortcut actions action
        # icon = QtGui.QIcon(style.standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        # self.keyboardAction = QtWidgets.QAction(icon, "shortcut actions", self)
        # self.keyboardAction.setCheckable(True)
        # self.keyboardAction.setChecked(True)
        # self.keyboardAction.triggered.connect(self.switchKeyboardUse)
        # self.addAction(self.keyboardAction)

        # about dialog action
        icon = QtGui.QIcon(style.standardIcon(QtWidgets.QStyle.SP_DialogHelpButton))
        self.aboutAction = QtWidgets.QAction(icon, "&About", self)
        self.aboutAction.triggered.connect(self.showAbout)
        self.addAction(self.aboutAction)

        # Create the icon
        icon = QtGui.QIcon(style.standardIcon(QtWidgets.QStyle.SP_BrowserStop))
        exitAct = QtWidgets.QAction(icon, "&Exit", self)
        exitAct.triggered.connect(QtWidgets.qApp.quit)
        self.addAction(exitAct)

    def showAbout(self):
        log.debug("open about dialog")
        AboutSwissKnife.about()

    # def switchKeyboardUse(self):
    #     log.debug("switch keyboard use" + str(self.keyboardAction.isChecked()))
    #     self.switchKeyboardSignal.emit(self.keyboardAction.isChecked())

    def setShowMainWindowAction(self, showMainWindowSlot):
        self.showAction.triggered.connect(showMainWindowSlot)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, showMainWindowSlot, parent=None):
        log.debug("init system tray icon")
        self._hotkey = True
        QtWidgets.QSystemTrayIcon.__init__(self, parent)
        # Create the icon
        style = QtWidgets.qApp.style()
        #icon = QtGui.QIcon(style.standardIcon(QtWidgets.QStyle.SP_TitleBarMenuButton))
        self.iconOn = QtGui.QIcon(os.path.join('icons', 'logo.png'))
        self.iconOff = QtGui.QIcon(os.path.join('icons', 'logo_off.png'))
        self.setIcon(self.iconOn)

        self.right_menu = RightClickMenu()
        self.setContextMenu(self.right_menu)

        self.showMainWindowSlot = showMainWindowSlot
        self.right_menu.setShowMainWindowAction(self.showMainWindowSlot)

        self.activated.connect(self.click_trap)


    def click_trap(self, value):
        if value == self.Trigger:  # left click!
            log.debug("SystemTray icon left clicked")
        #     self._hotkey = not self._hotkey
        #     if self._hotkey:
        #         self.setIcon(self.iconOn)
        #         self.switchKeyboardSignal.emit(True)
        #     else:
        #         self.setIcon(self.iconOff)
        #         self.switchKeyboardSignal.emit(False)
        #     return
        #if value == self.DoubleClick:  # double click!
            self.showMainWindowSlot()
            return


    def show(self):
        self.setVisible(True)
        QtWidgets.QSystemTrayIcon.show(self)


# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#
#     tray = SystemTrayIcon(app)
#     tray.show()
#
#     # set the exec loop going
#     app.exec_()
#     print("exit")
