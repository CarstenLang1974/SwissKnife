from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import importlib
import logging
log = logging.getLogger(__name__)

import pythontools.example_dialog
TOOLS_LIST = ["plot_test", "example_dialog"]

class ToolsWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(ToolsWidget, self).__init__(*args, **kwargs)

        self.the_widget = None
        self.main_layout = QHBoxLayout()

        self.listWidget = QListWidget()
        self.listWidget.setMaximumWidth(150)
        for i in TOOLS_LIST:
            self.listWidget.addItem(i)
        self.main_layout.addWidget(self.listWidget)

        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        #self.main_splitter = QSplitter(Qt.Horizontal)

        #self.main_splitter.addWidget(self.listWidget)

        self.loadWidget(TOOLS_LIST[0])
        self.main_layout.addWidget(self.scrollArea)

        #self.main_layout.addWidget(self.main_splitter)
        self.setLayout(self.main_layout)

        self.listWidget.itemSelectionChanged.connect(self.on_tool_change)
        self.show()

    def loadWidget(self, tool_name):
        tool_name = "pythontools." + tool_name
        tool_module = importlib.import_module(tool_name)
        log.debug("load " + str(tool_module))
        new_widget = tool_module.CentralWidget()
        log.debug("new widget is  " + str(new_widget))
        if self.the_widget:
            self.the_widget.deleteLater()
        self.the_widget = new_widget
        self.scrollArea.setWidget(self.the_widget)
        # try:
        #     if self.the_widget:
        #         self.main_layout.replaceWidget(self.the_widget, new_widget)
        #     else:
        #         self.main_layout.addWidget(self.the_widget)
        # except:
        #     log.exception("can't include widget")
        # self.the_widget = new_widget

    def on_tool_change(self):
        items = self.listWidget.selectedItems()
        log.debug("tool item: " + str(items[0].text()))
        self.loadWidget(items[0].text())


if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    app = QApplication(sys.argv)
    app.setApplicationName("Tools Test")
    window = ToolsWidget(None)
    app.exec_()
