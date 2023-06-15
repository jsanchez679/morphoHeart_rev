import sys

from PyQt6.QtWidgets import (QApplication, QGridLayout, QPushButton, QStyle,
                             QWidget)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        icons = sorted([attr for attr in dir(QStyle.StandardPixmap) if attr.startswith("SP_")])
        layout = QGridLayout()

        for n, name in enumerate(icons):
            print(name)
            btn = QPushButton(name)

            pixmapi = getattr(QStyle.StandardPixmap, name)
            icon = self.style().standardIcon(pixmapi)
            btn.setIcon(icon)
            stylesheet1 = 'QPushButton{border-radius:10px; border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); background-color: rgb(211, 211, 211); color: rgb(39, 39, 39);font: 10pt "Calibri Light";}'
            stylesheet2 = ' QPushButton:hover{ background-color: #eb6fbd; border-color: #672146}'
            btn.setStyleSheet(stylesheet1+stylesheet2)
            layout.addWidget(btn, int(n/4), int(n%4))


        self.setLayout(layout)


app = QApplication(sys.argv)

w = Window()
w.show()

app.exec()