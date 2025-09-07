import json
import os
import platform
import logging
log = logging.getLogger(__name__)
from PySide6.QtGui import *
from ProjectModel import ProjectModel

class Model(QStandardItemModel):
    def __init__(self, settings_file):
        """
        init model by loading given settings file and locals file according to current machines name.
        Afterwards iterate over the defined project files to create project objects.
        """
        super().__init__()
        settings_file_path=os.path.abspath(settings_file)
        log.debug("load settings file :{}".format(settings_file_path))
        with open(settings_file) as f:
            self.settings = json.load(f)
            self.globalsFileName = self.settings["globals"]
            projectFiles = self.settings["projects"]
        #log.debug(self.starters)
        if os.path.isdir(self.settings["locals_folder"]):
            locals_filename = "locals_" + platform.uname().node + ".json"
            locals_path = os.path.join(self.settings["locals_folder"], locals_filename)
            log.debug("open local settings file: " + locals_filename)
            with open(locals_path) as f:
                self.settings.update(json.load(f))
        else:
            raise FileNotFoundError
        log.debug(self.settings)
        self.projects = list()
        for filePath in projectFiles:
            self.projects.append(ProjectModel(filePath))
        self.globals = ProjectModel(self.globalsFileName)
        self.setHorizontalHeaderLabels(['my links'])
        self.currentProjectIndex = None
        self.setupTreeModel()

    def setCurrentProjectIndex(self, index):
        """
        set new project by index
        :param index: index for the project
        :return: n/a
        """
        if (index is None) or (index>=len(self.projects)):
            log.debug("no project selected")
            self.currentProjectIndex = None
        else:
            self.currentProjectIndex = index


    def getCurrentProject(self):
        """
        :return: project object for current project
        """
        if self.currentProjectIndex is not None:
            return self.projects[self.currentProjectIndex]
        else:
            return None

    def updateTreeModel(self):
        self.setupTreeModel()
        self.layoutChanged.emit()

    def setupTreeModel(self):
        """
        Generate the tree model for a tree view that includes al projects and the general links
        defined in the settings.
        :return: n/a
        """
        self.clear()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # populate data
        self._projectItems = list()
        self._linkItems = list()
        for p in self.projects:
            parentItem = QStandardItem(p.getName())
            self._projectItems.append(parentItem)
            for l in p.linkList:
                child = QStandardItem(l.name())
                parentItem.appendRow([child])
                self._linkItems.append(child)
            self.appendRow(parentItem)
        for s in self.globals.linkList:
            item = QStandardItem(s.name())
            self.appendRow(item)
            self._linkItems.append(item)

    def getProjectByIndex(self, index):
        return self._projectItems[index]

    # def updateTreeModel(self, filter=""):
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     # populate data
    #     index = self.findItems(filter)
    #     #currentItem.setEnabled(0)

    def getStarterNames(self):
        """
        generate a list of names for all general links/starters
        :return: list of name strings
        """
        names = []
        for i in self.globals.linkList:
            names.append(i.name())
        return names

    def getLinkFromName(self, identifier):
        """
        get the link object by identifier string
        :param identifier: identifier string to search for
        :return: link object (dict)
        """
        try:
            # first check current project for matching link
            if self.getCurrentProject():
                for l in self.getCurrentProject().linkList:
                    if l.name() == identifier:
                        return l
            # second check global starters for matching link
            for i in self.globals.linkList:
                if i.name() == identifier:
                    return i
        except Exception as e:
            log.debug("getLinkFromName nothing found - " + str(e))
            return None

    def getProjects(self):
        """
        Get list of dicts with "name" and "icon" of all projects
        :return: list of all projects
        """
        projectList = list()
        for p in self.projects:
            project = dict()
            project["name"] = p.getName()
            project["icon"] = p.getIcon()
            projectList.append(project)
        return projectList

    def getBrowser(self):
        """
        :return: default browser path
        """
        return self.settings["BrowserDefault"]

    def getBrowserMicrosoft(self):
        """
        :return: browser path for Microsoft pages (Sharepoint etc.)
        """
        return self.settings["BrowserMicrosoft"]

    def getFileExplorer(self):
        """
        :return: FileExplorer
        """
        return self.settings["FileExplorer"]

    def getStarter(self):
        """
        :return: Starter
        """
        return self.settings["Starter"]

    def getDoorsLinkStarter(self):
        """
        :return: DoorsLinkStarter
        """
        return self.settings["DoorsLinkStarter"]

    def getOpenHotkey(self):
        """
        :return: hotkey to show the swissknife window
        """
        return self.settings["open hotkey"]

    def getClipboardHotkey(self):
        """
        :return: hotkey to input the clipboard context (plain)
        """
        return self.settings["clipboard hotkey"]

    def getDateHotkey(self):
        """
        :return: hotkey for current date input
        """
        return self.settings["date hotkey"]

    def getShortcuts(self):
        """
        :return: list of shortcuts (hotkeys)
        """
        return self.settings["shortcuts"]

    def getStyle(self):
        """
        :return: style defined in settings or None if not defined
        """
        if "style" in self.settings:
            return self.settings["style"]
        else:
            return None

    def getFramlessMode(self):
        """
        :return: frameless mode defined in settings or False if not defined
        """
        if "frameless" in self.settings:
            return self.settings["frameless"]
        else:
            return False  # default off

    def getPreviewEnable(self):
        """
        :return: preview mode defined in settings or False if not defined
        """
        if "preview" in self.settings:
            return self.settings["preview"]
        else:
            return False  # default off
