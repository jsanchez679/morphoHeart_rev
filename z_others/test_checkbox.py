import sys
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *

class Window(QWidget):
    def __init__(self, rows, columns):
        super().__init__()
        
        self.table = QTableWidget(rows, columns, self)
        
        for row in range(rows):
            widget   = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            layoutH = QHBoxLayout(widget)
            layoutH.addWidget(checkbox)
            layoutH.setAlignment(Qt.AlignCenter)
            layoutH.setContentsMargins(0, 0, 0, 0)
            
            self.table.setCellWidget(row, 0, widget)                  # <----
            self.table.setItem(row, 1, QTableWidgetItem(str(row)))
            
        self.button = QPushButton("Control selected QCheckBox")
        self.button.clicked.connect(self.ButtonClicked)
        
        layoutV     = QVBoxLayout(self)
        layoutV.addWidget(self.table)
        layoutV.addWidget(self.button)


    def ButtonClicked(self):
        checked_list = []
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                checked_list.append(self.table.item(i, 1).text())
        print(checked_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window(3, 3)
    window.resize(350, 300)
    window.show()
    sys.exit(app.exec_())