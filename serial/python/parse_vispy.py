from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

#p1 = win.addPlot(title="Updating plot")
#curve = p1.plot(pen='y')
#data = np.random.normal(size=(10,1000))
#ptr = 0

class DataPlotter(object):
    def __init__(self):
    	self.p1 = win.addPlot(title="Updating plot")
    	self.curve = self.p1.plot(pen='y')
    	self.data = np.random.normal(size=(10,1000))
	self.ptr = 0
    def update(self):
	#global curve, data, ptr, p1
	self.curve.setData(self.data[self.ptr%10])
	if self.ptr == 0:
	    self.p1.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
	self.ptr += 1

dp = DataPlotter()

timer = QtCore.QTimer()
timer.timeout.connect(dp.update)
timer.start(50)

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
	QtGui.QApplication.instance().exec_()

