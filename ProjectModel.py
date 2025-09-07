"""
ProjectModel
Model for the project*.json files defined in settings.json
"""
import json
import os
import favicon
import requests
import logging
import Link
log = logging.getLogger(__name__)
from PySide6.QtCore import *
from PySide6.QtGui import *


headers = ["Name", "Description", "Link"]

class ProjectModel(QAbstractTableModel):
    def __init__(self, projectFile=None):
        """
        ProjectModel as TableModel for the Links and all other Project properties defined in project*.json
        :param projectFile: file path of the project*.json file
        """
        super().__init__()
        self.jsonData = None
        self.linkList = list()
        self.projectFile = projectFile
        self.loadProject()

    def loadProject(self):
        """
        load project form self.projectFile
        :return: n/a
        """
        with open(self.projectFile) as f:
            self.jsonData = json.load(f)
        self.checkProjectData()
        for l in self.jsonData["links"]:
            self.linkList.append(Link.Link(l))

    def saveProject(self):
        """
        save project to self.projectFile
        :return: n/a
        """
        newLinkList = list()
        for l in self.linkList:
            newLinkList.append(l.jsonData)
        self.jsonData["links"] = newLinkList
        with open(self.projectFile, 'w') as outfile:
            json.dump(self.jsonData, outfile)
        self.layoutChanged.emit()

    def checkProjectData(self):
        """
        logical checks for mandatory properties in the project json file data
        :return: n/a
        :exception: ValueError if check fails
        """
        p = self.jsonData
        log.debug("checking: " + str(p))
        if not p["name"]:
            raise ValueError('project has no name')
        if not p["description"]:
            raise ValueError('project has no description')
        if not p["links"]:
            raise ValueError('project has no defined links')

    def rowCount(self, parent):
        """
        part of the QAbstractTableModel interface
        provide number of rows for link table
        :param parent: not used
        :return: number of link entries for this project
        """
        return len(self.jsonData["links"])

    def columnCount(self, parent):
        """
        part of the QAbstractTableModel interface
        provide number of columns for link table
        :param parent: not used
        :return: number of columns for link table
        """
        return len(headers)

    def getLinkByIndex(self, row):
        return self.linkList[row]

    def getLinkInfoByIndex(self, row):
        e = self.linkList[row]
        if e.isStarter():
            return [e.name(), e.description(), e.call()]
        else:
            return [e.name(), e.description(), e.url()]

    def data(self, index, role):
        """
        part of the QAbstractTableModel interface
        provide data for this index in link table
        :param index: QIndex for this table entry
        :param role: this function provides data for Qt.DisplayRole, DecorationRole and SizeHintRole
        :return: QVariant with the information for this role
        """
        try:
            #log.debug("role: {0}, row: {1}, column: {2}".format(role, index.row(), index.column()))
            if role == Qt.DisplayRole:
                return self.getLinkInfoByIndex(index.row())[index.column()]
            elif role == Qt.DecorationRole:
                if index.column()==0:
                    link = self.linkList[index.row()]
                    return link.iconPixmap()
            elif role == Qt.SizeHintRole:
                #print('Model.data(role == Qt.SizeHintRole) row: %s; column %s' % (index.row(), index.column()))
                return Link.iconsize
        except Exception as e:
            log.error("exception in Model.data: {0} with role {1}".format(str(e), role))
        return None

    def headerData(self, section, orientation, role):
        """
        part of the QAbstractTableModel interface
        provide header data in link table
        :param section: number of column
        :param orientation: only Qt.Horizontal supported
        :param role: only Qt.DisplayRole supported
        :return: header strings
        """
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        return headers[section]

    def addLinkEntry(self, newEntry, index=None):
        """
        add link to current project object
        :param newEntry: new link entry (dict)
        :param index: position of the new created link in the link list
        :return: n/a
        """
        log.debug("add new entry: {0}, {1}".format(newEntry.name(), newEntry.description()))
        if index is None:
            self.linkList.append(newEntry)
        else:
            self.linkList.insert(index, newEntry)
        self.saveProject()

    def deleteLinkEntry(self, index):
        del self.linkList[index]
        self.saveProject()

    def replaceLinkEntry(self, row, newLink):
        self.linkList.pop(row)
        self.linkList.insert(row, newLink)
        self.saveProject()

    def getName(self):
        """
        :return: name of this project
        """
        return self.jsonData["name"]

    def getProjectNameAndDescription(self):
        return self.jsonData["name"], self.jsonData["description"]

    def getProjectUrl(self):
        """
        :return: URL for projects description or None if not available
        """
        if "url" in self.jsonData:
            return self.jsonData["url"]
        else:
            return None

    def getIcon(self):
        """
        :return: icon file path for this project
        """
        return self.jsonData["icon"]
