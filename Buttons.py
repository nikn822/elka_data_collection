# coding=utf-8
from PyQt4 import QtGui, QtCore

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

from Tkinter import *

class PlotData(object):
    def __init__(self, plot):
        self.plot_holder = plot 
        
        self.datasets = {}

        self.timer = None

       
        self.ptr = {}

    def add_dataset(self, name, pen, data):
        self.datasets[name] = (self.plot_holder.plot(pen=pen), data)
       
        self.ptr[name] = 0

    def make_plot_dynamic(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(50)

    def update(self, name):
        self.datasets[name][0].setData(self.datasets[name][1]\
                [self.ptr[name]%10])
        if self.ptr[name] == 0:
            
            self.plot_holder.enableAutoRange('xy', False)
        self.ptr[name] += 1

    def update_all(self):
        for key in self.datasets:
            self.update(key)


class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
    	self.setGeometry(550, 550, 600, 600)
        self.setWindowTitle('Draw circles')
        button1 = QtGui.QPushButton('', self)
        button1.clicked.connect(self.handleButton)
        button1.setIcon(QtGui.QIcon('groundCTRL.gif'))
        button1.setIconSize(QtCore.QSize(150,150))
        button1.setStyleSheet("background-color: rgb(0, 164, 255);\n"
                                        "border:1px solid rgb(255, 255, 255);")
        button1.move(300, 430)

        button2 = QtGui.QPushButton('', self)
        button2.clicked.connect(self.handleButton)
        button2.setIcon(QtGui.QIcon('disconnected Elka.gif'))
        button2.setIconSize(QtCore.QSize(150,150))
        button2.setStyleSheet("background-color: rgb(0, 164, 255);\n"
                                        "border:1px solid rgb(255, 255, 255);")
        button2.move(0, 275)

        button3 = QtGui.QPushButton('', self)
        button3.clicked.connect(self.handleButton)
        button3.setIcon(QtGui.QIcon('connectedelka.gif'))
        button3.setIconSize(QtCore.QSize(150,150))
        button3.setStyleSheet("background-color: rgb(0, 164, 255);\n"
                                        "border:1px solid rgb(255, 255, 255);")
        button3.move(600, 275)
        


        self.windows = {}
        self.plots = {} 
    

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



    #def handleButton(self, name):
    def handleButton(self):


    	if 'device1' not in self.windows.keys(): 	
    	    self.windows['device1'] = QtGui.QWidget()
            self.plots['test'] = pg.GraphicsLayoutWidget()
            self.windows['device1'].show()

            self.plotw = pg.GraphicsLayoutWidget()

            layout = QtGui.QGridLayout()
            self.windows['device1'].setLayout(layout)

            layout.addWidget(self.plotw, 1, 1, 4, 1)


            self.add_plot('test')
            self.add_plot_data('test','random',
                    'y',np.random.normal(size=(10,1000)))

            # Enable live plotting
            self.make_plot_dynamic('test')

        else:
            self.windows['device1'].show()


    





if __name__ == '__main__':
    app = QtGui.QApplication([])
    wid = Window()
    wid.resize(750, 600)
    #wid.setWindowTitle('Simple')
    wid.show()
    sys.exit(app.exec_())










