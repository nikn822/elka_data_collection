from PyQt4 import QtGui, QtCore
from collections import deque
import pyqtgraph as pg
import numpy as np

import ftdi_uart as ftdi
import parse

# Define a top-level widget to hold everything
class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Create some widgets to be placed inside
        self.plt_btn = QtGui.QPushButton('Plot data')
        self.elka_start_btn = QtGui.QPushButton('Start ELKA')
        self.elka_stop_btn = QtGui.QPushButton('Stop ELKA')
        #self.plt_btn.clicked.connect()
        #self.text = QtGui.QLineEdit('Name of data set')
        self.listw = QtGui.QListWidget()
        #self.plot = pg.PlotWidget()
        self.plotw = pg.GraphicsLayoutWidget()

        #TODO add menubar
        '''
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'),
                '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        # Create menu bar
        menubar = QtGui.QMenuBar(self)
        menubar.setNativeMenuBar(True)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        '''

        # Create a grid layout to managet the widgets size and position
        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        # Add widgets to the layout in their proper positions
        layout.addWidget(self.plt_btn, 1, 0) # Button goes in upper left
        # Start ELKA
        # For now, just start ELKA serial
        # TODO start ELKA and specify connection
        layout.addWidget(self.elka_start_btn, 2, 0)
        layout.addWidget(self.elka_stop_btn, 3, 0)
        #layout.addWidget(self.text, 2, 0) # Text edit goes in middle left
        layout.addWidget(self.listw, 4, 0) # List widget goes in bottom left
        layout.addWidget(self.plotw, 1, 1, 4, 1) # Plot goes on right side, spanning 3 rows

        self.threads = {}

        q = deque()
        self.threads["elka"] = ftdi.FtdiUartThread(q=q)
        self.threads["parse"] = parse.Parse(q=q)

        self.connect(self.threads["elka"], QtCore.SIGNAL("finished()"),
                self.stop_elka_thread)
        self.connect(self.threads["elka"], QtCore.SIGNAL("terminated()"),
                self.stop_elka_thread)
        # TODO change this to take arguments maybe
        self.connect(self.elka_start_btn, QtCore.SIGNAL("clicked()"),
                self.start_elka_thread)
        self.connect(self.elka_stop_btn, QtCore.SIGNAL("clicked()"),
                self.stop_elka_thread)
        self.connect(self.threads["parse"], QtCore.SIGNAL("finished()"),
                self.stop_parse_thread)
        self.connect(self.threads["parse"], QtCore.SIGNAL("terminated()"),
                self.stop_parse_thread)
        # TODO change this to take arguments maybe
        self.connect(self.elka_start_btn, QtCore.SIGNAL("clicked()"),
                self.start_parse_thread)
        self.connect(self.elka_stop_btn, QtCore.SIGNAL("clicked()"),
                self.stop_parse_thread)

        # self.plots stores PlotData
        # Keys to are provided names
        self.plots = {} 

        self.add_plot('test')
        self.add_plot_data('test','random',
                'y',np.random.normal(size=(10,1000)))

        # Enable live plotting
        self.make_plot_dynamic('test')
       
    def start_elka_thread(self):
        self.threads["elka"].exiting=False
        self.threads["elka"].start()

    def stop_elka_thread(self):
        self.threads["elka"].exiting = True

    def start_parse_thread(self):
        self.threads["parse"].exiting=False
        self.threads["parse"].start()

    def stop_parse_thread(self):
        self.threads["parse"].exiting = True

    def add_plot(self, name):
        self.plots[name] = PlotData(self.plotw.addPlot(title=name))

    def add_plot_data(self, plot_name, dataset_name, pen, data):
        self.plots[plot_name].add_dataset(dataset_name, pen, data)

    def make_plot_dynamic(self, plot_name):
        self.plots[plot_name].make_plot_dynamic()

    def update(self, plot_name, dataset_name):
        self.plots[plot_name].update(dataset_name)

    def update_all(self):
        for key in self.plots:
            self.plots[key].update_all()



class PlotData(object):
    def __init__(self, plot):
        self.plot_holder = plot 
        # Holds tuple with (curve, data)
        self.datasets = {}

        self.timer = None

        # FIXME Temporary for data update checking
        self.ptr = {}

    def add_dataset(self, name, pen, data):
        self.datasets[name] = (self.plot_holder.plot(pen=pen), data)
        # FIXME Temporary for data update checking
        self.ptr[name] = 0

    def make_plot_dynamic(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(50)

    def update(self, name):
        self.datasets[name][0].setData(self.datasets[name][1]\
                [self.ptr[name]%10])
        if self.ptr[name] == 0:
            # Stop auto-scaling after the first data
            # set is plotted
            self.plot_holder.enableAutoRange('xy', False)
        self.ptr[name] += 1

    def update_all(self):
        for key in self.datasets:
            self.update(key)

