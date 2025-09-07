"""
main.py
"""
import argparse
import logging
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import QFile, QTextStream
from PySide6.QtGui import QIcon
import Controller
import Model

if __name__ == '__main__':
    logging.basicConfig(filename='swissknife.log',
                        filemode='w',
                        format='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
                        level=logging.DEBUG)
    logging.info('start swiss knife application')
    parser = argparse.ArgumentParser(description='My Python Swiss Knife')
    parser.add_argument('--settings', dest='settings_file', default='./settingsTest/settings.json',
                        help='set the settings.json file to load on startup')
    args = parser.parse_args()
    logging.debug("setup: '{0}'".format(args.settings_file))

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icons/logo.png'))

    model = Model.Model(args.settings_file)

    if model.getStyle():
        # set stylesheet
        file = QFile(model.getStyle())     # supported: ":/light.qss" and "":/dark.qss""
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())
    else:
        app.setStyle("Fusion")

    app.setQuitOnLastWindowClosed(False)
    ctr = Controller.Controller(model)
    logging.info("start event loop, also if window is hidden")
    app.exec()
    logging.info("end event loop / close application")
