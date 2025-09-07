import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PySide6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class CentralWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(CentralWidget, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # Data for plotting
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        sc.axes.plot(t,s)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("This is a sinus"))
        self.lineEdit = QLineEdit()
        layout.addWidget(self.lineEdit)
        layout.addWidget(toolbar)
        layout.addWidget(sc)
        self.setLayout(layout)


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
