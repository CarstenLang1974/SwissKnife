import platform
from pathlib import Path
import logging
log = logging.getLogger(__name__)
from datetime import date
# if not platform.system() == "Linux":
#     log.debug("load keyboard support")
#     import keyboard
import subprocess
import os
import MainView
import pyperclip
from SystemTray import SystemTrayIcon

class Controller(object):
    def __init__(self, model):
        self._model = model
        identifiers = self._model.getStarterNames()
        self._screen = MainView.MainView(identifiers, self._model)
        self._systemtrayicon = SystemTrayIcon(self.on_hotkey)
        # self._systemtrayicon.right_menu.switchKeyboardSignal.connect(self.on_switchKeyboard)
        self._screen.closeAndComplete.connect(self.on_filterExecute)
        self._screen.linkListView.projectLinkClicked.connect(self.on_projectLinkClicked)
        self._screen.linkListView.projectLinkDoubleClicked.connect(self.on_projectLinkDoubleClicked)
        self._screen.projectChanged.connect(self.on_projectChanged)
        self._screen.openUrlExtern.connect(self.on_openUrlExtern)
        self.setup()

    def on_filterExecute(self, identifier="none"):
        try:
            log.debug("dialog closed with selection of: {}".format(identifier))
            if len(identifier) > 0:
                link = self._model.getLinkFromName(identifier)
                self.executeLink(link)
        except Exception as e:
            log.error("exception in Controller.on_filterExecute", exc_info=True)

    def on_projectLinkClicked(self, row):
        try:
            currentProject = self._model.getCurrentProject()
            if currentProject:
                link = currentProject.getLinkByIndex(row)
            else:
                link = self._model.globals.getLinkByIndex(row)
            log.debug("on_projectLinkClicked: row: {0}, link: {1}".format(row, link))
            if link.type().startswith("http"):
                self._screen.browserWidget.setUrl(link.url())
        except Exception as e:
            log.error("exception in Controller.on_projectLinkClicked", exc_info=True)

    def on_projectLinkDoubleClicked(self, row):
        try:
            currentProject = self._model.getCurrentProject()
            if currentProject:
                link = currentProject.getLinkByIndex(row)
            else:
                link = self._model.globals.getLinkByIndex(row)
            self.executeLink(link)
        except Exception as e:
            log.error("exception in Controller.on_projectLinkDoubleClicked", exc_info=True)

    def executeLink(self, link):
        if link.type() == "starter":
            call = link.call()
            if not os.path.isfile(call) and not os.access(call, os.X_OK):
                log.info("file is not executable: " + str(call))
                self._screen.showMessage("file is not executable: " + str(call))
                return
            args = link.arguments()
            log.info("call: '{} {}'".format(call, args))
            p = subprocess.Popen(call+" "+args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if link.type() == "http":
            self.start_browser(link.url())
        if link.type() == "http-ms":
            self.start_browser_microsoft(link.url())
        if link.type() == "file":
            self.open_file(link.url())
        if link.type() == "folder":
            self.open_folder(link.url())
        if link.type() == "DOORS":
            self.open_doors_link(link.url())
        self._screen.hide()

    def open_file(self, filepath):
        starter = self._model.getStarter()
        if starter == "":
            cmd_line = filepath
        else:
            cmd_line = starter + " " + filepath
        log.debug("file open command: {}".format(cmd_line))
        p = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.debug("file opened")

    def open_doors_link(self, url):
        doors = self._model.getDoorsLinkStarter()
        cmd_line = '{0} "{1}"'.format(doors, url)
        log.debug("DOORS link open command: '{}'".format(cmd_line))
        p = subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def open_folder(self, folderpath):
        fileExplorer = self._model.getFileExplorer()
        path = Path(folderpath)
        log.debug("fileExplorer: {}".format(fileExplorer))
        log.debug("folderpath: {}".format(path))
        p = subprocess.Popen(fileExplorer + " " + str(path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.debug("folder opened")

    def start_browser(self, url):
        browser = self._model.getBrowser()
        log.debug("browser: {}".format(browser))
        log.debug("url: {}".format(url))
        p = subprocess.Popen(browser + " " + url, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.debug("browser started")

    def start_browser_microsoft(self, url):
        browser = self._model.getBrowserMicrosoft()
        log.debug("browser (MS): {}".format(browser))
        log.debug("url: {}".format(url))
        p = subprocess.Popen(browser + " " + url, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.debug("browser started")

    def on_hotkey(self):
        # translate this hotkey call to an Qt Signal to be thread safe and return to the event loop thread
        self._screen.bringToFrontSignal.emit()

    # def on_clipboard_hotkey(self):
    #     clipboard_text = pyperclip.paste()
    #     clipboard_text = clipboard_text.replace('\r', '')
    #     log.debug("clipbord content pasted raw <{}>".format(repr(clipboard_text)))
    #     keyboard.write(clipboard_text, exact="exact")
    #
    # def on_date_hotkey(self):
    #     date_string = date.today().strftime('%d.%m.%Y')
    #     log.debug("date pasted raw <{}>".format(repr(date_string)))
    #     keyboard.write(date_string, exact="exact")

    def setup(self):
        # if not platform.system() == "Linux":
        #     log.debug("register hotkey, press ctrl+shift+q to start")
        #     self.initializeHotkeys()
        log.debug("show system tray icon")
        self._systemtrayicon.show()
        log.debug("show dialog on startup")
        self._screen.bringToFrontSignal.emit()


    def on_projectChanged(self):
        # if not platform.system() == "Linux":
        #     log.debug("project changed to project {0}".format(self._model.currentProjectIndex))
        #     self.initializeHotkeys()
        #     try:
        #         if self._model.currentProjectIndex is not None:
        #             shortcuts = self._model.getCurrentProject()["shortcuts"]
        #             for key in shortcuts:
        #                 log.debug("new shortcut: {0} -> {1}".format(key, shortcuts[key]))
        #                 keyboard.add_abbreviation(key, shortcuts[key])
        #         else:
        #             log.debug("no project selected")
        #     except Exception as e:
        #         log.debug("exception in Controller.on_projectChanged, no shortcuts for this project : " + str(e))
        return

    def on_switchKeyboard(self, keyboardSniffing):
        # if not platform.system() == "Linux":
        #     log.debug("switch keyboard sniffing: " + str(keyboardSniffing))
        #     if keyboardSniffing:
        #         self.initializeHotkeys()
        #     else:
        #         self.disableHotkeys()
        return

    def on_openUrlExtern(self, url):
        try:
            if url:
                self.start_browser(url)
                self._screen.hide()
        except Exception as e:
            log.debug("exception in Controller.on_openUrlExtern : " + str(e))

    # def disableHotkeys(self):
    #     try:
    #         keyboard.clear_all_hotkeys()
    #     except Exception as e:
    #         log.debug("no hotkeys to clear : " + str(e))
    #
    # def initializeHotkeys(self):
    #     self.disableHotkeys()
    #     keyboard.add_hotkey(self._model.getOpenHotkey(), self.on_hotkey, suppress=True)
    #     keyboard.add_hotkey(self._model.getClipboardHotkey(), self.on_clipboard_hotkey, suppress=True)
    #     keyboard.add_hotkey(self._model.getDateHotkey(), self.on_date_hotkey, suppress=True)
    #     try:
    #         shortcuts = self._model.getShortcuts()
    #         for key in shortcuts:
    #             log.debug("new general shortcut: {0} -> {1}".format(key, shortcuts[key]))
    #             keyboard.add_abbreviation(key, shortcuts[key])
    #     except Exception as e:
    #         log.debug("exception in Controller.initializeHotkeys : " + str(e))
