from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import QtWidgets
import time

class MyWorker(QObject):

    wait_for_input = pyqtSignal()
    done = pyqtSignal()


    @pyqtSlot()
    def firstWork(self):
        print('doing first work')
        time.sleep(2)
        print('first work done')
        self.wait_for_input.emit()

    @pyqtSlot()
    def secondWork(self):
        print('doing second work')
        time.sleep(2)
        print('second work done')
        self.done.emit()


class Window(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(Window, self).__init__()

        self.initUi()
        self.setupThread()

    def initUi(self):
        layout = QtWidgets.QVBoxLayout()
        self.button = QtWidgets.QPushButton('User input')
        self.button.setEnabled(False)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()

    @pyqtSlot()
    def enableButton(self):
        self.button.setEnabled(True)

    @pyqtSlot()    
    def done(self):
        self.button.setEnabled(False)

    def setupThread(self):
        self.thread = QThread()
        self.worker = MyWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.firstWork)
        self.button.clicked.connect(self.worker.secondWork)
        self.worker.wait_for_input.connect(self.enableButton)
        self.worker.done.connect(self.done)

        # Start thread
        self.thread.start()    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = Window()
    app.exec()