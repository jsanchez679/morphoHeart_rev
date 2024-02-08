
from pathlib import Path
from PyQt6 import uic
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QIcon

rev = Path('d:/Documents JSP/Dropbox/Dropbox_Juliana/morphoHeart_rev')#cwd.parent
mH_icon = str(rev /'images/logos_w_icon_2o5mm.png')
mH_top_corner = str(rev /'images/logos_1o75mm.png')

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Yes

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class CustomDialog_mH(QDialog):
    def __init__(self):
        super().__init__()
        self.output = None
        self.setWindowTitle("HELLO!")

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Help", QDialogButtonBox.HelpRole)
        self.buttonBox.addButton("Apply", QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)

        self.buttonBox.accepted.connect(self.apply_func)
        self.buttonBox.rejected.connect(self.cancel_func)
        self.buttonBox.helpRequested.connect(self.no_func)

        # self.dialogButtons = QDialogButtonBox(self)
        # # self.dialogButtons.setGeometry(10, 490, 615, 30)
        # self.dialogButtons.setStandardButtons(QDialogButtonBox.Cancel |
        #                                       QDialogButtonBox.Ok |
        #                                       QDialogButtonBox.Apply )#|
        #                                     #   QDialogButtonBox.Yes |
        #                                     #   QDialogButtonBox.No )


        # self.dialogButtons.rejected.connect(self.reject)
        # self.dialogButtons.accepted.connect(self.accept)
        # self.dialogButtons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_func)
        # self.cancel = self.dialogButtons.button(QDialogButtonBox.Cancel)
        # self.cancel.clicked.connect(self.cancel_func)
        # self.ok = self.dialogButtons.button(QDialogButtonBox.Ok)
        # self.ok.clicked.connect(self.ok_func)
        # self.apply = self.dialogButtons.button(QDialogButtonBox.Apply)
        # self.apply.clicked.connect(self.apply_func)
        # self.yes = self.dialogButtons.button(QDialogButtonBox.Yes)
        # self.yes.clicked.connect(self.yes_func)
        # self.no = self.dialogButtons.button(QDialogButtonBox.No)
        # self.no.clicked.connect(self.no_func)
        
        # QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Retry

        # self.buttonBox = QDialogButtonBox(QBtn)
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        # self.layout.addWidget(self.dialogButtons)
        self.setLayout(self.layout)

    def cancel_func(self): 
        self.output = 'Cancel!'
        print('cancel!')
        self.close()

    def ok_func(self): 
        self.output = 'Ok!'
        print('ok!')
        self.close()

    def apply_func(self):         
        self.output = 'Apply!'
        print('applied!')
        self.close()

    def yes_func(self): 
        self.output = 'Yes!'
        print('yes!')
        self.close()

    def no_func(self): 
        self.output = 'No!'
        print('no!')
        self.close()

class Custom_mH(QDialog):
    def __init__(self, title:str, msg:str, parent=None):
        super().__init__()
        uic_path = rev / 'gui/prompt_user_input.ui'
        print(uic_path)
        uic.loadUi(uic_path, self)
        # uic.loadUi('gui/prompt_user_input.ui', self)
        # self.setFixedSize(400,250)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setText(msg)

        self.setModal(True)
        self.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self):
        print("click")
        title = 'This is the title!'
        msg = 'Message goes here!'
        prompt = Custom_mH(msg, title, parent=self)
        # dlg = CustomDialog_mH()
        # print('Out:',dlg.output)
        # if dlg.exec():
        #     print("Success!")
        # else:
        #     print("Cancel!")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()