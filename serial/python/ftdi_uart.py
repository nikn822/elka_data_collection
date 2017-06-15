import serial
from PyQt4.QtCore import QThread
from collections import deque
from time import sleep

class FtdiUartThread(QThread):
    def __init__(self, dev_type='elka', q=None):
        QThread.__init__(self)
        self.exiting=False

        self.dev_type = dev_type
        self.q = q

    def run(self):
        if not self.exiting:
            try:
                ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
                print(ser.name)
            except serial.SerialException:
                raise

        while not self.exiting:
            #TODO ensure that serial reads in as characters
            s = ser.read(100)
            for i in range(len(s)):
                self.q.append(s[i])

        ser.close()

    def __del__(self):
        self.exiting=True
        self.wait()
