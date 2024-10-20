import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import logging
log = logging.getLogger(__name__)
import ProjectModel
import Link

class EditLinkDialog(QDialog):

    def __init__(self, link, *args, **kwargs):
        super(EditLinkDialog, self).__init__(*args, **kwargs)
        log.debug("start EditLinkDialog with args: {0} / kwargs: {1}".format(args, kwargs))
        if link is None:
            self.link = Link.Link()
        else:
            self.link = link

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.layout = QVBoxLayout()

        self.linkIcon = QLabel()
        self.linkIcon.setMinimumSize(64,64)
        self.layout.addWidget(self.linkIcon)

        self.layout.addWidget(QLabel("name:"))
        self.linkNameEdit = QLineEdit()
        self.layout.addWidget(self.linkNameEdit)

        self.layout.addWidget(QLabel("description:"))
        self.linkDescriptionEdit = QLineEdit()
        self.layout.addWidget(self.linkDescriptionEdit)

        self.layout.addWidget(QLabel("icon:"))
        self.layoutIcon = QHBoxLayout()
        self.linkIconEdit = QLineEdit()
        self.linkIconEdit.setMinimumWidth(400)
        self.layoutIcon.addWidget(self.linkIconEdit)
        self.linkIconFileDlgButton = QPushButton(QIcon(os.path.join('icons', 'disk--arrow.png')), None, self)
        self.layoutIcon.addWidget(self.linkIconFileDlgButton)
        self.layout.addLayout(self.layoutIcon)
        self.linkIconFileDlgButton.clicked.connect(self.on_open_icon_fileDialog)
        self.linkIconEdit.textChanged.connect(self.on_icon_change)

        self.layout.addWidget(QLabel("type:"))
        self.linkTypeSelect = QComboBox(self)
        for linktype in Link.linktypes:
            self.linkTypeSelect.addItem(linktype)
        self.layout.addWidget(self.linkTypeSelect)
        self.linkTypeSelect.currentTextChanged.connect(self.on_linktype_change)

        self.layoutUrl = QHBoxLayout()
        self.linkUrlEdit = QLineEdit()
        self.linkUrlEdit.setMinimumWidth(400)
        self.layoutUrl.addWidget(self.linkUrlEdit)
        self.linkFileDlgButton = QPushButton(QIcon(os.path.join('icons', 'disk--arrow.png')), None, self)
        self.layoutUrl.addWidget(self.linkFileDlgButton)
        self.layout.addLayout(self.layoutUrl)
        self.linkFileDlgButton.clicked.connect(self.on_open_fileDialog)

        self.layout.addWidget(QLabel("arguments:"))
        self.callArguments = QLineEdit()
        self.layout.addWidget(self.callArguments)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

        if link is not None:
            log.debug("link to edit: " + str(link))
            self.setWindowTitle("Edit Link")
            self.linkNameEdit.setText(link.name())
            self.linkDescriptionEdit.setText(link.description())
            self.linkTypeSelect.setCurrentText(link.type())
            if link.icon():
                self.linkIconEdit.setText(link.icon())
            if link.type() == "starter":
                self.linkUrlEdit.setText(link.call())
                self.callArguments.setText(link.arguments())
            else:
                self.linkUrlEdit.setText(link.url())
        else:
            self.setWindowTitle("New Link")
        self._setIcon()
        self.on_linktype_change()

    def _setIcon(self):
        pixmap = self.link.iconPixmap()
        self.linkIcon.setPixmap(pixmap)

    def on_open_fileDialog(self):
        index = self.linkTypeSelect.currentIndex()
        linktype = self.linkTypeSelect.itemText(index)
        if linktype == "folder":
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            folder = QFileDialog.getExistingDirectory(self,
                                                      "select folder",
                                                      "",
                                                      options)
            if folder:
                log.debug("selected: " + folder)
                self.linkUrlEdit.setText(folder)
                if self.linkNameEdit.text() == "":
                    head, tail = os.path.split(folder)
                    self.linkNameEdit.setText(tail)
        else:
            options = QFileDialog.Options()
            #options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,
                                                      "select file",
                                                      "",
                                                      "All Files (*);;Python Files (*.py)",
                                                      options=options)
            if fileName:
                log.debug("selected file: {0}".format(fileName))
                self.linkUrlEdit.setText(fileName)
                if self.linkNameEdit.text() == "":
                    head, tail = os.path.split(fileName)
                    self.linkNameEdit.setText(tail)

    def on_open_icon_fileDialog(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        dir = os.path.join(os.path.dirname(__file__), "icons")
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "select icon file",
                                                  dir,
                                                  "All Files (*);;PNG Files (*.png)",
                                                  options=options)
        if fileName:
            log.debug("selected icon file: {0}".format(fileName))
            self.linkIconEdit.setText(fileName)

    def on_linktype_change(self):
        index = self.linkTypeSelect.currentIndex()
        linktype = self.linkTypeSelect.itemText(index)
        self.link.setType(linktype)
        log.debug("link type changed to: {0}".format(linktype))
        if linktype == "starter":
            self.callArguments.setEnabled(True)
        else:
            self.callArguments.setEnabled(False)
        iconPath = self.linkIconEdit.text()
        if iconPath == "":
            self._setIcon()
        #self.linkIconButton.setIcon(self.getDefaultLinkIcon(linktype))

    def on_icon_change(self):
        iconPath = self.linkIconEdit.text()
        log.debug("new icon path: " + str(iconPath))
        self.link.setIcon(iconPath)
        self._setIcon()

    def getLink(self):
        index = self.linkTypeSelect.currentIndex()
        linktype = self.linkTypeSelect.itemText(index)
        self.link.setName(self.linkNameEdit.text())
        self.link.setDescription(self.linkDescriptionEdit.text())
        self.link.setType(linktype)
        if linktype == "starter":
            self.link.setCall(self.linkUrlEdit.text())
            self.link.setArguments(self.callArguments.text())
        else:
            self.link.setUrl(self.linkUrlEdit.text())
        return self.link

