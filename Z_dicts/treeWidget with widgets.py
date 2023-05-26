from PyQt5 import QtWidgets 
from PyQt5 import QtCore 
from PyQt5.Qt import Qt 
import sys

class MySlider(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        # keep only the default margin on the left
        layout.setContentsMargins(-1, 0, 0, 0)
        self.label = QtWidgets.QLabel()
        self.label.setText('Spinbox:')
        self.spinBox1 = QtWidgets.QSpinBox()
        # make sure the spin-box doesn't get too small
        self.spinBox1.setMinimumWidth(80)
        layout.addWidget(self.label)
        layout.addWidget(self.spinBox1)
        # don't allow the spin-box to exapnd too much
        layout.addStretch()

import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView
# from MySlider import MySlider

def main():
    _translate = QtCore.QCoreApplication.translate
    app = QtWidgets.QApplication(sys.argv)
    tree = QtWidgets.QTreeWidget()
    tree.setColumnCount(3)
    headerItem = QtWidgets.QTreeWidgetItem()
    headerItem.setText(0, _translate("MainWindow", "md-name"))
    headerItem.setText(1, _translate("MainWindow", "md_value"))
    headerItem.setText(2, _translate("MainWindow", "others"))
    tree.setHeaderItem(headerItem)

    parent = QtWidgets.QTreeWidgetItem(tree)
    parent.setText(0, "Parent 1")
    parent.setText(1, "")
    parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsEditable)

    for x in range(3):
        child = QtWidgets.QTreeWidgetItem(parent)
        child.setFlags(child.flags() | Qt.ItemIsEditable)
        child.setText(0, "Child {}".format(x))
        line_edit = QtWidgets.QLineEdit(tree)

        rs = MySlider(tree)
        tree.setItemWidget(child, 1, line_edit)
        tree.setItemWidget(child, 2, rs)

    tree.setEditTriggers(QAbstractItemView.AllEditTriggers)
    tree.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()