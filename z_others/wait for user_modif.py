from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import QtWidgets
import time

# Step 1: Create a worker class
class MyWorker(QObject):

    wait_for_input = pyqtSignal()
    done = pyqtSignal()

    @pyqtSlot()
    def firstWork(self):
        print('Waiting for user input')
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

    def initUi(self):
        layout = QtWidgets.QVBoxLayout()
        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.setEnabled(True)
        layout.addWidget(self.start_button)
        self.textBrowser = QtWidgets.QTextBrowser()
        layout.addWidget(self.textBrowser)
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setEnabled(False)
        layout.addWidget(self.lineEdit)
        self.button = QtWidgets.QPushButton('Set')
        self.button.setEnabled(False)
        layout.addWidget(self.button)
        self.label = QtWidgets.QLabel()
        self.label.setGeometry(QRect(20, 20, 211, 16))
        self.label.setText('Loop No:')
        layout.addWidget(self.label)
        self.loop_label = QtWidgets.QLabel()
        self.loop_label.setGeometry(QRect(20, 20, 211, 16))
        self.label.setText('0')
        layout.addWidget(self.loop_label)
        
        self.setLayout(layout)
        self.show()

        self.start_button.clicked.connect(lambda: self.get_user_input())

    @pyqtSlot()
    def enable_user_input(self):
        self.lineEdit.setEnabled(True)
        self.button.setEnabled(True)

    @pyqtSlot()    
    def done(self):
        self.textBrowser.append("DONE")

    def get_user_input(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = MyWorker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        self.textBrowser.append("Provide a list of numbers from 10 to 100 separated by commas:")
        # Step 5: Connect signals and slots
        # - Start the thread
        self.thread.started.connect(self.worker.firstWork)

        # - Thread waiting for user input
        self.worker.wait_for_input.connect(self.enable_user_input)
        # - User has provided input
        self.button.clicked.connect(self.user_input_provided)

        # - End the thread
        #   > Print DONE
        self.worker.done.connect(self.done)
        #   > Quit the thread
        self.worker.done.connect(self.thread.quit)
        #   > Delete the worker
        self.worker.done.connect(self.worker.deleteLater)
        #   > Delete the Thread
        self.thread.finished.connect(self.thread.deleteLater)

        # Step 6: Start the thread
        self.thread.start()    
    
    def user_input_provided(self):
        user_input = self.lineEdit.text()
        print('user_input:', user_input)
        self.textBrowser.append(user_input)
        self.lineEdit.clear()
        self.lineEdit.setEnabled(False)
        self.button.setEnabled(False)
        self.worker.secondWork()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = Window()
    app.exec()