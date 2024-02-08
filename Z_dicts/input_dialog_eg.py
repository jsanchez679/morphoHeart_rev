#https://www.youtube.com/watch?v=RI646fqeFDQ

from pathlib import Path
from PyQt6 import uic
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QInputDialog, QDialog, QMessageBox, QMainWindow)
from PyQt6.QtGui import QPixmap, QIcon
cwd = Path.cwd()
rev = Path('d:/Documents JSP/Dropbox/Dropbox_Juliana/morphoHeart_rev')#cwd.parent
mH_icon = str(rev /'images/logos_w_icon_2o5mm.png')
mH_top_corner = str(rev /'images/logos_1o75mm.png')
print(mH_icon)
class PromptWindow(QDialog):

    def __init__(self, msg:str, title:str, info:str, parent=None):
        super().__init__()
        uic.loadUi('gui/prompt_user_input.ui', self)
        # self.setFixedSize(400,250)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setText(msg)
        
        if title == 'Custom Orientation':
            self.custom_or = None
            reg_ex = QRegularExpression("[a-z-A-Z_ 0-9,]+")
            self.button_ok.clicked.connect(lambda: self.validate_custom_or(parent, info))

        elif title == 'Custom Strain' or title == 'Custom Stage' or title == 'Custom Genotype' or title == 'Custom Manipulation': 
            reg_ex = QRegularExpression("[a-z-A-Z_ 0-9(),.:;/+-]+")
            self.button_ok.clicked.connect(lambda: self.validate_organ_data(parent, info))
        
        else: 
            reg_ex = QRegularExpression('.*')

        input_validator = QRegularExpressionValidator(reg_ex, self.lineEdit)
        self.lineEdit.setValidator(input_validator)
        self.setModal(True)
        self.show()

    def validate_custom_or(self, parent, info):
        user_input = split_str(self.lineEdit.text())
        if len(set(user_input)) != 3:
            error_txt = '*Three different names need to be given for each orientation'
            self.tE_validate.setText(error_txt)
            return
        else: 
            self.custom_or = user_input
            added_or = ','.join(self.custom_or)
            user_or = getattr(parent, 'cB_'+info+'_orient')
            user_or.addItem(added_or)
            user_or.setCurrentText(added_or)
            self.close()
    
    def validate_organ_data(self, parent, name):
        user_input = self.lineEdit.text()
        if len(user_input) <= 1: 
            error_txt = "*The organ's "+name+" needs to have at least two (2) characters."
            self.tE_validate.setText(error_txt)
            return
        else: 
            setattr(self, 'custom_'+name, user_input)
            cB_data = getattr(parent, 'cB_'+name)
            cB_data.addItem(user_input)
            cB_data.setCurrentText(user_input)
            self.close()

        # print('self.custom_',name,':',getattr(self,'custom_'+name))
        
class Prompt_ok_cancel(QDialog):
    def __init__(self, title:str, msg:str, parent=None):
        super().__init__(parent)
        uic.loadUi('gui/prompt_ok_cancel.ui', self)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setText(msg)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setModal(True)
        self.show()

class Prompt_ok_cancel_comboBox(QDialog):
    def __init__(self, title:str, msg:str, items:list, parent=None):
        super().__init__(parent)
        uic.loadUi('gui/prompt_ok_cancel_comboBox.ui', self)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setText(msg)
        self.comboBox.addItems(items)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.show()

class Prompt_options_input(QDialog):
    def __init__(self, title:str, msg:str, res:dict, parent=None):
        super().__init__(parent)
        uic.loadUi('gui/prompt_options_input.ui', self)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit_msg.setText(msg)

        #Set options list 
        res_txt = ''
        for num, item in res.items():
            res_txt += '#'+str(num)+': '+ item+'\n'
        self.textEdit_options.setText(res_txt)
        print(res_txt)

        reg_ex = QRegularExpression("(\d+(?:-\d+)?)((?:(?:,)(\d+(?:-\d+)?))*)")
        input_validator = QRegularExpressionValidator(reg_ex, self.user_input)
        self.user_input.setValidator(input_validator)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.show()

class Prompt_yes_no(QDialog): 
    def __init__(self, title:str, msg:str, parent=None):
        super().__init__(parent)
        uic.loadUi('gui/prompt_yes_no.ui', self)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setText(msg)
        self.msg = QMessageBox(parent)
        # self.buttonBox = QtWidgets.QDialogButtonBox()
        # self.buttonBox.setStyleSheet("QDialogButtonBox QPushButton{\n"
        #                             "color: rgb(39, 39, 39);\n"
        #                             "font: 11pt \"Calibri Light\";\n"
        #                             "height:20;\n"
        #                             "padding:0px;\n"
        #                             "width:120;\n"
        #                             "background-color: rgb(211, 211, 211);\n"
        #                             "border-radius: 10px;\n"
        #                             "border-width: 1px;\n"
        #                             "border-style: outset;\n"
        #                             "border-color: rgb(66, 66, 66);\n"
        #                             "}\n"
        #                             "\n"
        #                             "QDialogButtonBox QPushButton:hover{\n"
        #                             "background-color: #eb6fbd;\n"
        #                             "border-color: #672146\n"
        #                             "}\n"
        #                             "\n"
        #                             "")
        
        # self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        # self.buttonBox.QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        # self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        # self.buttonBox.setCenterButtons(True)
        # self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.msg)
        # self.verticalLayout.addWidget(self.buttonBox)
        self.msg.buttonClicked.connect(self.yes_no_clicked)
    
    def yes_no_clicked(self, button_clicked):
        print(button_clicked.text())

    # def msgbtn(self, i):
    #     print( "Button pressed is:",i.text() )
    #     self.output = i.text()
    #     self.close()

    # class MainWindow(QMainWindow):
    #     def __init__(self):
    #         super().__init__()

    #         self.setWindowTitle("My App")

    #         button = QPushButton("Press me for a dialog!")
    #         button.clicked.connect(self.button_clicked)
    #         self.setCentralWidget(button)

    #     def button_clicked(self, s):
    #         print("click", s)

    #         dlg = CustomDialog()
    #         if dlg.exec():
    #             print("Success!")
    #         else:
    #             print("Cancel!")


class Input_ok_cancel(QMessageBox):
    def __init__(self, title:str, msg:str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(msg)
        # self.setWindowIcon(QIcon(mH_icon))
        # self.setIcon(QIcon(mH_icon))
        self.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        clicked_button  = self.exec()

        if clicked_button == QMessageBox.StandardButton.Ok: 
            print('OK!')
            self.output = True
        else:
            print('Cancel!')
            self.output = False

class Input_ok_cancel_mH(QDialog): 
    def __init__(self, title:str, msg:str, parent=None):
        super().__init__(parent)
        path_uic = str(rev /'gui/prompt_options_select.ui')
        uic.loadUi(path_uic, self)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(mH_icon))
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.textEdit.setText(msg)
        
        # self.msg = QMessageBox(parent)
        # self.msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        # clicked_button  = self.exec()

        # if clicked_button == QMessageBox.StandardButton.Ok: 
        #     print('OK!')
        #     self.output = True
        # else:
        #     print('Cancel!')
        #     self.output = False

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Show Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Input Dialog')        
        self.show()

    def showDialog(self):
        title = 'This is the title'
        msg = 'Message goes here'
        # dialog = Input_ok_cancel(title, msg)
        # print(dialog.output)
        dialog = Input_ok_cancel_mH(title, msg)
        # print(dialog.output)
        # text, ok = QInputDialog.getText(self, 'input dialog', 'Is this ok?')
        # if ok:
        #     self.le.setText(str(text))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())