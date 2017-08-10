
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class DrawCircles(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(550, 550, 600, 600)
        self.setWindowTitle('Draw circles')
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        # for circle make the ellipse radii match
        radxOne = 150
        radyOne = 150
        # draw red circles
        paint.setPen(Qt.blue)
        centerOne = QPoint(300,630)
        paint.setBrush(Qt.blue)
        paint.drawEllipse(centerOne, radxOne, radyOne)

	radx2 = 35
        rady2 = 35
        paint.setPen(Qt.blue)
        center2 = QPoint(180,400)
        paint.setBrush(Qt.green)
        paint.drawEllipse(center2, radx2, rady2)
	
	radx3 = 35
        rady3 = 35
        paint.setPen(Qt.blue)
        center3 = QPoint(420,400)
        paint.setBrush(Qt.green)
        paint.drawEllipse(center3, radx3, rady3)

	radx4 = 35
        rady4 = 35
        paint.setPen(Qt.blue)
        center4 = QPoint(80,250)
        paint.setBrush(Qt.green)
        paint.drawEllipse(center4, radx4, rady4)
	
	radx5 = 35
        rady5 = 35
        paint.setPen(Qt.blue)
        center5 = QPoint(200,100)
        paint.setBrush(Qt.green)
        paint.drawEllipse(center5, radx5, rady5)
	
	radx6 = 35
        rady6 = 35
        paint.setPen(Qt.blue)
        center6 = QPoint(400,100)
        paint.setBrush(Qt.green)
        paint.drawEllipse(center6, radx6, rady6)

	radx7 = 35
        rady7 = 35
        paint.setPen(Qt.blue)
        center7 = QPoint(520,250)
        paint.setBrush(Qt.green)
        paint.drawEllipse(center7, radx7, rady7)
        
	paint.end()

if __name__ == '__main__':
    app = QApplication([])
    circles = DrawCircles()
    circles.show()
    sys.exit(app.exec_())

