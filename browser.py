from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtPrintSupport import *

import os
import sys
import logging
log = logging.getLogger(__name__)

class BrowserWidget(QWidget):
    def __init__(self, openUrlExternSignal, *args, **kwargs):
        super(BrowserWidget, self).__init__(*args, **kwargs)
        self.homeUrl = "http://google.com"
        self.browser = QWebEngineView()
        self.openUrlExternSignal = openUrlExternSignal
        #self.browser.setUrl(QUrl("http://google.com"))

        self.browser.urlChanged.connect(self.update_urlbar)
        main_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.browser)
        self.setLayout(main_layout)

        back_btn = QPushButton(QIcon(os.path.join('icons', 'arrow-180.png')), None, self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.pressed.connect(self.browser.back)
        buttons_layout.addWidget(back_btn)

        next_btn = QPushButton(QIcon(os.path.join('icons', 'arrow-000.png')), None, self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.pressed.connect(self.browser.forward)
        buttons_layout.addWidget(next_btn)

        reload_btn = QPushButton(QIcon(os.path.join('icons', 'arrow-circle-315.png')), None, self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.pressed.connect(self.browser.reload)
        buttons_layout.addWidget(reload_btn)

        home_btn = QPushButton(QIcon(os.path.join('icons', 'home.png')), None, self)
        home_btn.setStatusTip("Go home")
        home_btn.pressed.connect(self.navigate_home)
        buttons_layout.addWidget(home_btn)

        openext_btn = QPushButton(QIcon(os.path.join('icons', 'double-arrow.png')), None, self)
        openext_btn.setStatusTip("open url external")
        openext_btn.pressed.connect(self.open_extern)
        buttons_layout.addWidget(openext_btn)

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'lock-nossl.png')))
        buttons_layout.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        buttons_layout.addWidget(self.urlbar)

        stop_btn = QPushButton(QIcon(os.path.join('icons', 'cross-circle.png')), None, self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.pressed.connect(self.browser.stop)
        buttons_layout.addWidget(stop_btn)
        self.show()

    def setUrl(self, url):
        self.browser.setUrl(QUrl(url))

    def setHome(self, url = None, content = None):
        if url:
            self.homeUrl = url
            self.browser.setUrl(QUrl(url))
        else:
            self.homeContent = content
            self.browser.setHtml(content)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):
        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'lock-ssl.png')))

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def open_extern(self):
        if self.openUrlExternSignal:
            log.debug("open current URL extern")
            url = str(self.browser.url().toString())
            log.debug("emit {0} with url {1}".format(self.openUrlExternSignal, url))
            self.openUrlExternSignal.emit(url)
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Browser Test")
    window = BrowserWidget(None)
    app.exec_()
