import sys
from PyQt5.QtCore import QProcess, QTextStream
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.process = QProcess(self)
        self.output = QTextEdit(self)
        self.input = QLineEdit(self)
        self.run_command_button = QPushButton("Run Command", self)

        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.run_command_button)
        layout.addLayout(input_layout)
        layout.addWidget(self.output)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.process.readyReadStandardOutput.connect(self.read_output)
        self.run_command_button.clicked.connect(self.run_command)
        self.process.start("cmd.exe")

    def read_output(self):
        stream = QTextStream(self.process)
        self.output.append(stream.readAll())

    def run_command(self):
        command = self.input.text() + "\n"
        self.process.write(command.encode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())