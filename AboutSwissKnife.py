from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os
import sys

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Swiss Knife")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('icons', 'logo.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 1.0"))
        layout.addWidget(QLabel("Copyright 2020 Carsten Lang"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

def about():
    dlg = AboutDialog()
    #dlg.show()
    #dlg.raise_()
    #dlg.activateWindow()
    dlg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.exec_()
    about()