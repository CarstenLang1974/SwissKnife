"""
Link
Link class
"""
import json
import os
import favicon
import requests
import logging
log = logging.getLogger(__name__)
from PyQt5.QtCore import *
from PyQt5.QtGui import *

CACHE_PATH = "./cache"
iconsize = QSize(32, 32)

linktypes = ["http", "http-ms", "starter", "file", "folder", "DOORS"]
iconPaths = [":/icons/icons/globe.png",
             ":/icons/icons/blue-document-office.png",
             ":/icons/icons/globe.png",
             ":/icons/icons/document-bookmark.png",
             ":/icons/icons/drawer--arrow.png",
             "./icons/doors.png"]

# link properties
L_NAME = "name"
L_DESC = "description"
L_ICON = "icon"
L_TYPE = "type"
L_URL = "url"
L_CALL = "call"
L_ARGS = "arguments"

class Link(object):
    def __init__(self, jsonDict = None):
        """
        Link
        :param jsonDict: representation of the json file content
        """
        super().__init__()
        if jsonDict is None:
            self._setJsonData("")
        else:
            self.jsonData = jsonDict
        self._checkJsonData()

    def __str__(self):
        return "Link {0} of type {1}".format(self.name(), self.type())

    def _setJsonData(self, name, description="", icon = None, linktype="http", url="", arguments=None):
        """
        Fill link dict according to the linktype.
        :param name: name of the link
        :param description: description of the link
        :param icon: icon path (optional)
        :param linktype: type of link
        :param url: URL or path to file/folder to link
        :param arguments: arguments for a command line call (optional)
        :return: dict with all entries for a link in json
        """
        self.jsonData = dict()
        self.jsonData[L_NAME] = name
        self.jsonData[L_DESC] = description
        if icon:
            self.jsonData[L_ICON] = icon

        if linktype in linktypes:
            self.jsonData[L_TYPE] = linktype
        else:
            raise ValueError("invalid link type")
        if self.jsonData[L_TYPE] == "starter":
            self.jsonData[L_CALL] = url
            if arguments:
                self.jsonData["arguments"] = arguments
        else:
            self.jsonData[L_URL] = url

    def _checkJsonData(self):
        """
        logical checks for mandatory properties in the jsonData dictionary
        :return: n/a
        :exception: ValueError if check fails
        """
        l = self.jsonData
        log.debug("checking link: " + str(l))
        if l["name"] is None:
            raise ValueError('link has no name')
        if not l["type"]:
            raise ValueError('link has no type')
        else:
            if l["type"] == "starter":
                if not l["call"]:
                    raise ValueError('starter link has no call defined')
                if l["arguments"] is None:
                    raise ValueError('starter link has no arguments defined')
            if l["type"] == "http":
                if l["url"] is None:
                    raise ValueError('http link has no url')

    def name(self):
        """
        :return: name of this link
        """
        return self.jsonData[L_NAME]

    def setName(self, name):
        """
        :return: set name of this link
        """
        self.jsonData[L_NAME] = name

    def type(self):
        """
        :return: url of this link
        """
        return self.jsonData[L_TYPE]

    def setType(self, link_type):
        """
        :return: set type of this link
        """
        self.jsonData[L_TYPE] = link_type

    def url(self):
        """
        :return: url of this link
        """
        if L_URL in self.jsonData:
            url = self.jsonData[L_URL]
        else:
            url = ""
        return url

    def setUrl(self, url):
        """
        :return: set url of this link
        """
        self.jsonData[L_URL] = url

    def call(self):
        """
        :return: name of this link
        """
        if L_CALL in self.jsonData:
            call = self.jsonData[L_CALL]
        else:
            call = ""
        return call

    def setCall(self, call):
        """
        :return: set call of this link
        """
        self.jsonData[L_CALL] = call

    def arguments(self):
        """
        :return: name of this link
        """
        if L_ARGS in self.jsonData:
            args = self.jsonData[L_ARGS]
        else:
            args = ""
        return args

    def setArguments(self, arguments):
        """
        :return: set arguments of this link
        """
        self.jsonData[L_ARGS] = arguments

    def description(self):
        """
        :return: description of this link
        """
        if L_DESC in self.jsonData:
            description = self.jsonData[L_DESC]
        else:
            description = ""
        return description

    def setDescription(self, description):
        """
        :return: set description of this link
        """
        self.jsonData[L_DESC] = description

    def icon(self):
        """
        :return: icon file path for this project
        """
        if L_ICON in self.jsonData:
            icon = self.jsonData[L_ICON]
        else:
            icon = ""
        return icon

    def setIcon(self, icon):
        """
        :return: set icon of this link
        """
        self.jsonData[L_ICON] = icon

    def isStarter(self):
        return self.type() == "starter"

    def iconPixmap(self):
        iconPath = self.icon()
        if iconPath != "":
            return QPixmap(iconPath).scaled(iconsize, Qt.KeepAspectRatio)
        else:
            return self._getDefaultLinkIcon().pixmap(iconsize).scaled(iconsize, Qt.KeepAspectRatio)

    def _getDefaultLinkIcon(self):
        iconPath = self._getCacheIconPath()
        if iconPath is None:
            # no cached icon, use default for this type
            type_name = self.type()
            i = linktypes.index(type_name)
            iconPath = iconPaths[i]
        return QIcon(iconPath)

    def _getCacheIconPath(self):
        iconPath = None
        try:
            if self.type().startswith("http") and (self.name() != ""):
                #log.debug("check cache for icon for " + self.name())
                # check for existing favicon in cache
                for file in os.listdir(CACHE_PATH):
                    if file.startswith(self.name()):
                        #log.debug("cache file exists: " + str(file))
                        return os.path.join(CACHE_PATH, file)

                # if not existent, try to download
                icons = favicon.get(self.url())
                icon = icons[0]
                response = requests.get(icon.url, stream=True)
                cache_file_path = os.path.join(CACHE_PATH, '{0}.{1}'.format(self.name(), icon.format))
                log.debug("create cache file: " + str(cache_file_path))
                with open(cache_file_path, 'wb') as image:
                    for chunk in response.iter_content(1024):
                        image.write(chunk)
                return cache_file_path
        except Exception as e:
            log.error("exception in Model.cacheIcons: {0}".format(str(e)))
        return iconPath

