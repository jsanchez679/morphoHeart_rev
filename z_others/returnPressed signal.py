from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtWidgets
import sys

class myWidget(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(myWidget, self).__init__(parent)
        self.lineEdit = QtWidgets.QLineEdit()
        self.textBrowser = QtWidgets.QTextBrowser()
        self.top_btn = QtWidgets.QPushButton("Ask me", )
        self.bottom_btn = QtWidgets.QPushButton("disable")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.textBrowser)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.top_btn)
        layout.addWidget(self.bottom_btn)
        self.setLayout(layout)
        self.lineEdit.setDisabled(True)
        self.top_btn.clicked.connect(self.inputFunc)
        self.lineEdit.returnPressed.connect(self.process)
        #self.bottom_btn.clicked.connect(self.disableLine)
    def inputFunc(self):
        self.lineEdit.setDisabled(False)
        self.textBrowser.setText("Welcome to #1 button. what do you want to do?")
    def process(self):
        userInput = self.lineEdit.text()
        if userInput == "anything":
            self.textBrowser.append("Ok i will leave you alone")
            self.close()
        else:
            self.textBrowser.append("say what?")
        self.lineEdit.clear()

app = QtWidgets.QApplication(sys.argv)
w = myWidget()
w.show()
sys.exit(app.exec())