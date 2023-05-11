# Form implementation generated from reading ui file 'C:\Users\Noel\Desktop\welcome_screen.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 591)
        self.bgwidget = QtWidgets.QWidget(parent=Dialog)
        self.bgwidget.setGeometry(QtCore.QRect(0, 0, 600, 590))
        self.bgwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.bgwidget.setObjectName("bgwidget")
        self.welcome_to_msg = QtWidgets.QLabel(parent=self.bgwidget)
        self.welcome_to_msg.setGeometry(QtCore.QRect(0, 30, 601, 71))
        self.welcome_to_msg.setStyleSheet("font: 25 38pt \"Calibri Light\"; color: rgb(95, 95, 95)\n"
"")
        self.welcome_to_msg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.welcome_to_msg.setObjectName("welcome_to_msg")
        self.label_instructions = QtWidgets.QLabel(parent=self.bgwidget)
        self.label_instructions.setGeometry(QtCore.QRect(0, 285, 601, 51))
        self.label_instructions.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_instructions.setStyleSheet("font: 25 14pt \"Calibri Light\"; color: rgb(116, 116, 116)")
        self.label_instructions.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_instructions.setObjectName("label_instructions")
        self.mH_logo_XL = QtWidgets.QLabel(parent=self.bgwidget)
        self.mH_logo_XL.setGeometry(QtCore.QRect(0, 120, 601, 111))
        self.mH_logo_XL.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.mH_logo_XL.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mH_logo_XL.setObjectName("mH_logo_XL")
        self.label_instructions_2 = QtWidgets.QLabel(parent=self.bgwidget)
        self.label_instructions_2.setGeometry(QtCore.QRect(275, 220, 326, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.label_instructions_2.setFont(font)
        self.label_instructions_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_instructions_2.setStyleSheet("font: 25 12pt \"Calibri Light\"; color: rgb(116, 116, 116)")
        self.label_instructions_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_instructions_2.setObjectName("label_instructions_2")
        self.label_instructions_3 = QtWidgets.QLabel(parent=self.bgwidget)
        self.label_instructions_3.setGeometry(QtCore.QRect(0, 420, 601, 61))
        self.label_instructions_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_instructions_3.setStyleSheet("font: 25 12pt \"Calibri Light\"; color: rgb(116, 116, 116)")
        self.label_instructions_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_instructions_3.setObjectName("label_instructions_3")
        self.cB_theme = QtWidgets.QComboBox(parent=self.bgwidget)
        self.cB_theme.setGeometry(QtCore.QRect(490, 555, 100, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cB_theme.sizePolicy().hasHeightForWidth())
        self.cB_theme.setSizePolicy(sizePolicy)
        self.cB_theme.setMinimumSize(QtCore.QSize(100, 0))
        self.cB_theme.setMaximumSize(QtCore.QSize(100, 16777215))
        self.cB_theme.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.cB_theme.setAutoFillBackground(False)
        self.cB_theme.setStyleSheet("border-color: rgb(173, 173, 173);\n"
"font: 25 10pt \"Calibri Light\";")
        self.cB_theme.setFrame(True)
        self.cB_theme.setObjectName("cB_theme")
        self.cB_theme.addItem("")
        self.cB_theme.addItem("")
        self.label_instructions_4 = QtWidgets.QLabel(parent=self.bgwidget)
        self.label_instructions_4.setGeometry(QtCore.QRect(420, 555, 71, 25))
        self.label_instructions_4.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_instructions_4.setStyleSheet("font: 25 10pt \"Calibri Light\"; color: rgb(116, 116, 116)")
        self.label_instructions_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_instructions_4.setObjectName("label_instructions_4")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.bgwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 495, 601, 36))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mH_logo_XL_2 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.mH_logo_XL_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.mH_logo_XL_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mH_logo_XL_2.setObjectName("mH_logo_XL_2")
        self.horizontalLayout.addWidget(self.mH_logo_XL_2)
        self.btn_link2paper = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.btn_link2paper.setStyleSheet("QPushButton{ border: none;\n"
"color:rgb(136, 136, 136);\n"
"font: 12pt \"Calibri\";}\n"
"\n"
"QPushButton:hover{\n"
"    color: rgb(255, 60, 128)}\n"
"")
        self.btn_link2paper.setObjectName("btn_link2paper")
        self.horizontalLayout.addWidget(self.btn_link2paper)
        self.btn_link2docs = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.btn_link2docs.setStyleSheet("QPushButton{ border: none;\n"
"color:rgb(136, 136, 136);\n"
"font: 12pt \"Calibri\";}\n"
"\n"
"QPushButton:hover{\n"
"    color: rgb(255, 60, 128)}\n"
"")
        self.btn_link2docs.setObjectName("btn_link2docs")
        self.horizontalLayout.addWidget(self.btn_link2docs)
        self.btn_link2github = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.btn_link2github.setStyleSheet("QPushButton{ border: none;\n"
"color:rgb(136, 136, 136);\n"
"font: 12pt \"Calibri\";}\n"
"\n"
"QPushButton:hover{\n"
"    color: rgb(255, 60, 128)}\n"
"")
        self.btn_link2github.setObjectName("btn_link2github")
        self.horizontalLayout.addWidget(self.btn_link2github)
        self.mH_logo_XL_3 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.mH_logo_XL_3.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.mH_logo_XL_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mH_logo_XL_3.setObjectName("mH_logo_XL_3")
        self.horizontalLayout.addWidget(self.mH_logo_XL_3)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.bgwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 345, 601, 46))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mH_logo_XL_4 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_2)
        self.mH_logo_XL_4.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.mH_logo_XL_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mH_logo_XL_4.setObjectName("mH_logo_XL_4")
        self.horizontalLayout_2.addWidget(self.mH_logo_XL_4)
        self.button_new_proj = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_new_proj.sizePolicy().hasHeightForWidth())
        self.button_new_proj.setSizePolicy(sizePolicy)
        self.button_new_proj.setMinimumSize(QtCore.QSize(100, 30))
        self.button_new_proj.setMaximumSize(QtCore.QSize(100, 30))
        self.button_new_proj.setStyleSheet("QPushButton{border-radius:10px;\n"
"border-width: 1px;\n"
"border-style: outset;\n"
"border-color: rgb(66, 66, 66);\n"
"background-color: rgb(134, 134, 134); \n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"Calibri\";}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgba(162, 0, 122,180);\n"
"    border-color: rgba(162, 0, 122,180);\n"
"    border-width: 2px}\n"
"")
        self.button_new_proj.setObjectName("button_new_proj")
        self.horizontalLayout_2.addWidget(self.button_new_proj)
        self.button_new_proj_from_template = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_new_proj_from_template.sizePolicy().hasHeightForWidth())
        self.button_new_proj_from_template.setSizePolicy(sizePolicy)
        self.button_new_proj_from_template.setMinimumSize(QtCore.QSize(200, 30))
        self.button_new_proj_from_template.setMaximumSize(QtCore.QSize(200, 30))
        self.button_new_proj_from_template.setStyleSheet("QPushButton{border-radius:10px;\n"
"border-width: 1px;\n"
"border-style: outset;\n"
"border-color: rgb(66, 66, 66);\n"
"background-color: rgb(134, 134, 134); \n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"Calibri\";}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgba(162, 0, 122,180);\n"
"    border-color: rgba(162, 0, 122,180);\n"
"    border-width: 2px}\n"
"")
        self.button_new_proj_from_template.setObjectName("button_new_proj_from_template")
        self.horizontalLayout_2.addWidget(self.button_new_proj_from_template)
        self.button_load_proj = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_load_proj.sizePolicy().hasHeightForWidth())
        self.button_load_proj.setSizePolicy(sizePolicy)
        self.button_load_proj.setMinimumSize(QtCore.QSize(100, 30))
        self.button_load_proj.setMaximumSize(QtCore.QSize(100, 30))
        self.button_load_proj.setStyleSheet("QPushButton{border-radius:10px;\n"
"border-width: 1px;\n"
"border-style: outset;\n"
"border-color: rgb(66, 66, 66);\n"
"background-color: rgb(134, 134, 134); \n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"Calibri\";}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgba(162, 0, 122,180);\n"
"    border-color: rgba(162, 0, 122,180);\n"
"    border-width: 2px}")
        self.button_load_proj.setObjectName("button_load_proj")
        self.horizontalLayout_2.addWidget(self.button_load_proj)
        self.mH_logo_XL_5 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_2)
        self.mH_logo_XL_5.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.mH_logo_XL_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mH_logo_XL_5.setObjectName("mH_logo_XL_5")
        self.horizontalLayout_2.addWidget(self.mH_logo_XL_5)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(parent=self.bgwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 555, 201, 26))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.hL_toggle_on_off = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.hL_toggle_on_off.setContentsMargins(0, 0, 0, 0)
        self.hL_toggle_on_off.setObjectName("hL_toggle_on_off")
        self.label_instructions_5 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_instructions_5.sizePolicy().hasHeightForWidth())
        self.label_instructions_5.setSizePolicy(sizePolicy)
        self.label_instructions_5.setMinimumSize(QtCore.QSize(50, 24))
        self.label_instructions_5.setMaximumSize(QtCore.QSize(50, 24))
        self.label_instructions_5.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_instructions_5.setStyleSheet("font: 25 10pt \"Calibri Light\"; color: rgb(116, 116, 116)")
        self.label_instructions_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_instructions_5.setObjectName("label_instructions_5")
        self.hL_toggle_on_off.addWidget(self.label_instructions_5)
        self.lab_on = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lab_on.sizePolicy().hasHeightForWidth())
        self.lab_on.setSizePolicy(sizePolicy)
        self.lab_on.setMinimumSize(QtCore.QSize(40, 24))
        self.lab_on.setMaximumSize(QtCore.QSize(40, 24))
        self.lab_on.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.lab_on.setStyleSheet("font: 25 10pt \"Calibri Light\"; color: rgb(116, 116, 116)")
        self.lab_on.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lab_on.setObjectName("lab_on")
        self.hL_toggle_on_off.addWidget(self.lab_on)
        self.label_off = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_off.sizePolicy().hasHeightForWidth())
        self.label_off.setSizePolicy(sizePolicy)
        self.label_off.setMinimumSize(QtCore.QSize(40, 24))
        self.label_off.setMaximumSize(QtCore.QSize(40, 24))
        self.label_off.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_off.setStyleSheet("font: 25 10pt \"Calibri Light\"; color: rgb(116, 116, 116)")
        self.label_off.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_off.setObjectName("label_off")
        self.hL_toggle_on_off.addWidget(self.label_off)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.welcome_to_msg.setText(_translate("Dialog", "Welcome to"))
        self.label_instructions.setText(_translate("Dialog", "Create a new project or load one that was already created"))
        self.mH_logo_XL.setText(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.label_instructions_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">v2.0.1</span></p></body></html>"))
        self.label_instructions_3.setText(_translate("Dialog", "Don\'t forget to cite the lastest morphoHeart paper when \n"
"you publish your results using the software!"))
        self.cB_theme.setItemText(0, _translate("Dialog", "Bright"))
        self.cB_theme.setItemText(1, _translate("Dialog", "Dark"))
        self.label_instructions_4.setText(_translate("Dialog", "Theme: "))
        self.mH_logo_XL_2.setText(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.btn_link2paper.setText(_translate("Dialog", "Paper"))
        self.btn_link2docs.setText(_translate("Dialog", "Docs"))
        self.btn_link2github.setText(_translate("Dialog", "GitHub"))
        self.mH_logo_XL_3.setText(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.mH_logo_XL_4.setText(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.button_new_proj.setText(_translate("Dialog", "New Project"))
        self.button_new_proj_from_template.setText(_translate("Dialog", "New Project from Template"))
        self.button_load_proj.setText(_translate("Dialog", "Load Project"))
        self.mH_logo_XL_5.setText(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.label_instructions_5.setText(_translate("Dialog", "Sounds:"))
        self.lab_on.setText(_translate("Dialog", "ON"))
        self.label_off.setText(_translate("Dialog", "OFF"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())