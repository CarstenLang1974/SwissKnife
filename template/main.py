"""
main.py
"""
import argparse
import logging
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
import Controller
import Model

if __name__ == '__main__':
    logging.basicConfig(filename='template.log',
                        filemode='w',
                        format='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
                        level=logging.DEBUG)
    logging.info('start application')
    parser = argparse.ArgumentParser(description='My App')
    parser.add_argument('--settings', dest='settings_file', default='./settings.json',
                        help='set the settings.json file to load on startup')
    args = parser.parse_args()
    logging.debug("setup: '{0}'".format(args.settings_file))

    app = QApplication(sys.argv)

    model = Model.Model(args.settings_file)
    ctr = Controller.Controller(model)
    logging.info("start event loop, also if window is hidden")
    app.exec_()
    logging.info("end event loop / close application")
