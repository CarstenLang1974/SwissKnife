import os
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
import logging
log = logging.getLogger(__name__)


class CentralWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(CentralWidget, self).__init__(*args, **kwargs)
        log.debug("start example dialog with args: {0} / kwargs: {1}".format(args, kwargs))

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("line edit:"))
        self.lineEdit = QLineEdit()
        self.layout.addWidget(self.lineEdit)

        self.layout.addWidget(QLabel("selector:"))
        self.comboBox = QComboBox(self)
        for linktype in ["A","B","C"]:
            self.comboBox.addItem(linktype)
        self.layout.addWidget(self.comboBox)
        self.comboBox.currentTextChanged.connect(self.on_combobox_change)

        self.layoutUrl = QHBoxLayout()
        self.linkUrlEdit = QLineEdit()
        self.linkUrlEdit.setMinimumWidth(400)
        self.layoutUrl.addWidget(self.linkUrlEdit)
        self.linkFileDlgButton = QPushButton(QIcon(os.path.join('icons', 'disk--arrow.png')), None, self)
        self.layoutUrl.addWidget(self.linkFileDlgButton)
        self.layout.addLayout(self.layoutUrl)
        self.linkFileDlgButton.clicked.connect(self.on_open_fileDialog)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def on_open_fileDialog(self):
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

    def on_combobox_change(self):
        index = self.comboBox.currentIndex()
        selection = self.comboBox.itemText(index)
        log.debug("selection: " + str(selection))

    def accept(self):
        log.debug("accepted")

    def reject(self):
        log.debug("rejected")

if __name__ == '__main__':
    class MainWindow(QMainWindow):

        def __init__(self, *args, **kwargs):
            super(MainWindow, self).__init__(*args, **kwargs)

            # Create a central widget (with toolbar and canvas)
            widget = CentralWidget()
            self.setCentralWidget(widget)
            self.show()


    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
