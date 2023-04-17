from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton, QWidget


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        x_pos, y_pos = 10, 10
        w_pix, h_pix = 150, 150

        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(w_pix, h_pix)
        container.move(x_pos, y_pos)
        container.setStyleSheet("background-color:salmon;")

        hbox = QHBoxLayout(container)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")

        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)

        self.resize(640, 480)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())