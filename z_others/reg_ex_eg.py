from PyQt6 import QtWidgets
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QLineEdit

import sys

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.le_input = QLineEdit(self)

        # reg_ex = QRegularExpression(r"[+]?((\d+(\.\d*)?)|(\.\d+))([^a-d,f-z,A-D,F-Z][+-]?\d+)?")
        reg_ex = QRegularExpression("[a-z-A-Z_ 0-9,.+-:/]+")
        input_validator = QRegularExpressionValidator(reg_ex, self.le_input)
        self.le_input.setValidator(input_validator)

if __name__ == '__main__':
    a = QtWidgets.QApplication(sys.argv)

    w = MyWidget()
    w.show()

    a.exec()