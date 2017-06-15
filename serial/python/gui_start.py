import sys
import numpy as np
import pyqtgraph as pg
from PyQt4 import QtGui, QtCore

if __name__ == "__main__":
    # Start by initializing Qt
    app = QtGui.QApplication(sys.argv)

    from gui import MainWindow

    window = MainWindow()
    window.resize(1000,600)
    window.setWindowTitle('Elka Control')

    window.show()
    sys.exit(app.exec_())

