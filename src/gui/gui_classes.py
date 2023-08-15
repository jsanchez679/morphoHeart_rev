
'''
morphoHeart_GUI_classes

Version: Apr 26, 2023
@author: Juliana Sanchez-Posada

'''
#%% Imports - ########################################################
# import sys
from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSlot, QDate, Qt, QRegularExpression, QRect, QSize, QAbstractTableModel
from PyQt6.QtWidgets import (QDialog, QApplication, QMainWindow, QWidget, QFileDialog, QTabWidget,
                              QGridLayout, QVBoxLayout, QHBoxLayout, QLayout, QLabel, QPushButton, QLineEdit,
                              QColorDialog, QTableWidgetItem, QCheckBox, QTreeWidgetItem, QSpacerItem, QSizePolicy, 
                              QDialogButtonBox, QMessageBox, QHeaderView, QStyle)
from PyQt6.QtGui import QPixmap, QIcon, QFont, QRegularExpressionValidator, QColor, QPainter, QPen, QBrush
from qtwidgets import Toggle, AnimatedToggle
import qtawesome as qta
from pathlib import Path
import flatdict
# import os
from itertools import count
import webbrowser
from skimage import measure, io
import copy
import seaborn as sns
from functools import reduce  
import operator
from typing import Union
import vedo 
import numpy as np
import pandas as pd

#%% morphoHeart Imports - ##################################################
# from .src.modules.mH_funcBasics import get_by_path
# from .src.modules.mH_funcMeshes import * 
from ..modules.mH_funcBasics import get_by_path, compare_dicts, update_gui_set, alert
from ..modules.mH_funcContours import checkWfCloseCont, ImChannel
from ..modules.mH_funcMeshes import plot_grid, s3_to_mesh
from ..modules.mH_classes_new import Project, Organ
from .config import mH_config

path_mHImages = mH_config.path_mHImages

#%% Set default fonts and sizes for plots
txt_font = mH_config.txt_font
leg_font = mH_config.leg_font
leg_width = mH_config.leg_width
leg_height = mH_config.leg_height
txt_size = mH_config.txt_size
txt_color = mH_config.txt_color
txt_slider_size = mH_config.txt_slider_size

#https://wpamelia.com/loading-bar/

#%% Classes - ########################################################
class WelcomeScreen(QDialog):

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('src/gui/ui/welcome_screen.ui', self)
        # self.setFixedSize(600,680)
        self.setWindowTitle('Welcome to morphoHeart...')
        self.mH_logo_XL.setPixmap(QPixmap(mH_big))
        self.setWindowIcon(QIcon(mH_icon))
        self.label_version.setText('v'+mH_config.version)
        self.label_version.setStyleSheet('color: rgb(116, 116, 116); font: bold 15pt "Calibri Light";')
        

        # self.btn_link2paper
        # self.btn_link2paper.clicked.connect(lambda: self.get_file())#webbrowser.open('https://github.com/jsanchez679/morphoHeart'))
        # self.btn_link2docs
        # self.btn_link2docs.clicked.connect(lambda: webbrowser.open('https://github.com/jsanchez679/morphoHeart'))
        # self.btn_link2github.setIcon(qta.icon("fa5b.github"))
        self.btn_link2github.clicked.connect(lambda: webbrowser.open('https://github.com/jsanchez679/morphoHeart'))

        # Sound Buttons
        layout = self.hL_sound_on_off 
        add_sound_bar(self, layout)
        sound_toggled(win=self)

        # Theme 
        mH_config.theme = self.cB_theme.currentText()
        self.on_cB_theme_currentIndexChanged(mH_config.theme)

    @pyqtSlot(int)
    def on_cB_theme_currentIndexChanged(self, theme):
        print('mH_config.theme:',mH_config.theme)
        if theme == 'Light' or theme == 0: 
            file = 'src/gui/themes/Light.qss'
        else: 
            file = 'src/gui/themes/Dark.qss'
        #Open the file
        with open(file, 'r') as f: 
            style_str = f.read()
            print('Selected theme: ', theme)
        #Set the theme
        self.setStyleSheet(style_str)
        mH_config.theme = theme

class Prompt_ok_cancel(QDialog):
    def __init__(self, title:str, msg:str, parent=None):
        super().__init__(parent)
        uic.loadUi('src/gui/ui/prompt_ok_cancel.ui', self)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setHtml(html_txt[0]+html_txt[1]+msg+html_txt[2])
        # self.textEdit.setText(msg)
        self.output = None

        self.buttonBox.accepted.connect(lambda: self.accepted())
        self.buttonBox.rejected.connect(lambda: self.rejected())
        self.setModal(True)
        self.show()

    def accepted(self): 
        print('Entered func!')
        self.output = True
        self.close()

    def rejected(self): 
        print('Rejected!')
        self.output = False
        self.close()

class Prompt_ok_cancel_Big(QDialog):
    def __init__(self, title:str, msg:list, parent=None):
        super().__init__(parent)
        uic.loadUi('src/gui/ui/prompt_ok_cancel_big.ui', self)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        for nn in range(0,7,1): 
            text = getattr(self, 'textEdit'+str(nn+1))
            if nn == 0:
                text.setHtml(html_txt[0]+html_txt[1]+msg[nn]+html_txt[2])
            elif nn < len(msg): 
                text.setText(msg[nn])
            else: 
                text.setText('')

        self.output = None

        self.buttonBox.accepted.connect(lambda: self.accepted())
        self.buttonBox.rejected.connect(lambda: self.rejected())
        self.setModal(True)
        self.show()

    def accepted(self): 
        print('Entered func!')
        self.output = True
        self.close()

    def rejected(self): 
        print('Rejected!')
        self.output = False
        self.close()

class Prompt_ok_cancel_radio(QDialog):
    def __init__(self, title:str, msg:str, items:dict, parent=None):
        super().__init__(parent)
        uic.loadUi('src/gui/ui/prompt_ok_cancel_radio.ui', self)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setHtml(html_txt[0]+html_txt[1]+msg+html_txt[2])
        self.output = None

        #Set radio buttons
        nn = 0
        self.rButtons = []
        for key in items: 
            if nn < 2: 
                rB = getattr(self, 'radioButton'+str(nn))
                lE = getattr(self, 'lineEdit'+str(nn))
                hL = getattr(self, 'hL'+str(nn))
                # sp = getattr(self, 'spacer'+str(nn))
            else: 
                hL = QtWidgets.QHBoxLayout()
                hL.setObjectName("hL"+str(nn))
                rB = QtWidgets.QRadioButton(parent=self.widget)
                rB.setMinimumSize(QtCore.QSize(0, 20))
                rB.setMaximumSize(QtCore.QSize(16777215, 20))
                rB.setStyleSheet("font: 25 11pt \"Calibri Light\";")
                rB.setObjectName("radioButton"+str(nn))
                hL.addWidget(rB)
                sp = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
                hL.addItem(sp)
                lE = QtWidgets.QLineEdit(parent=self.widget)
                lE.setMinimumSize(QtCore.QSize(0, 20))
                lE.setMaximumSize(QtCore.QSize(16777215, 20))
                lE.setObjectName("lineEdit"+str(nn))
                hL.addWidget(lE)
                self.verticalLayout.addLayout(hL)
                setattr(self, 'spacer'+str(nn), sp)

            #Assign values
            rB.setText(items[key]['opt'])
            if 'lineEdit' in items[key].keys(): 
                if items[key]['lineEdit']: 
                    lE.setVisible(True)
                    if items[key]['regEx'] == 'int3d': 
                        reg_ex = QRegularExpression("\d{1,3}")
                    else:
                        reg_ex = QRegularExpression('.*')
                    input_validator = QRegularExpressionValidator(reg_ex, lE)
                    lE.setValidator(input_validator)
                else: 
                    lE.setVisible(False)
            else: 
                lE.setVisible(False)
            self.rButtons.append(rB)

            setattr(self, 'hL'+str(nn), hL)
            setattr(self, 'radioButton'+str(nn), rB)
            setattr(self, 'lineEdit'+str(nn), lE)
            nn += 1

        self.buttonBox.clicked.connect(lambda: self.accepted(items))
        self.buttonBox.rejected.connect(lambda: self.rejected())
        self.setModal(True)
        self.show()

    def accepted(self, items):
        print('Entered func!')
        for rB in self.rButtons:
            if rB.isChecked():
                rB_checked = rB.text()
                break
        
        #Find the opt that was selected
        for key in items: 
            if items[key]['opt'] == rB_checked: 
                keyf = key
                break
        
        #Check the lineEdit if it was true and get value
        if 'lineEdit' in items[keyf].keys(): 
            if items[keyf]['lineEdit']: 
                lineEdit_txt = getattr(self, 'lineEdit'+str(keyf)).text()
                print(lineEdit_txt, len(lineEdit_txt))
                if len(lineEdit_txt) == 0: 
                    self.tE_validate.setText('Please provide an input for the selected option!')
                    return
                else: 
                    self.output = [keyf, rB_checked, lineEdit_txt]
                    self.close()
            else: 
                self.output = [keyf, rB_checked, None]
                self.close()
        else: 
            self.output = [keyf, rB_checked, None]
            self.close()
    
    def rejected(self):
        print('Rejected!')
        self.output = None
        self.close()

class Prompt_ok_cancel_checkbox(QDialog):
    def __init__(self, title:str, msg:str, items:dict, parent=None):
        super().__init__(parent)
        uic.loadUi('src/gui/ui/prompt_ok_cancel_checkbox.ui', self)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setHtml(html_txt[0]+html_txt[1]+msg+html_txt[2])
        self.output = None

        #Set radio buttons
        nn = 0
        self.cButtons = []
        for key in items: 
            if nn < 2: 
                cB = getattr(self, 'checkBox'+str(nn))
                lE = getattr(self, 'lineEdit'+str(nn))
                hL = getattr(self, 'hL'+str(nn))
                # sp = getattr(self, 'spacer'+str(nn))
            else: 
                hL = QtWidgets.QHBoxLayout()
                hL.setObjectName("hL"+str(nn))
                cB = QtWidgets.QCheckBox(parent=self.widget)
                cB.setMinimumSize(QtCore.QSize(0, 20))
                cB.setMaximumSize(QtCore.QSize(16777215, 20))
                cB.setStyleSheet("font: 25 11pt \"Calibri Light\";")
                cB.setObjectName("checkBox"+str(nn))
                hL.addWidget(cB)
                sp = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
                hL.addItem(sp)
                lE = QtWidgets.QLineEdit(parent=self.widget)
                lE.setMinimumSize(QtCore.QSize(0, 20))
                lE.setMaximumSize(QtCore.QSize(16777215, 20))
                lE.setObjectName("lineEdit"+str(nn))
                hL.addWidget(lE)
                self.verticalLayout.addLayout(hL)
                setattr(self, 'spacer'+str(nn), sp)

            #Assign values
            cB.setText(items[key]['opt'])
            if 'lineEdit' in items[key].keys(): 
                if items[key]['lineEdit']: 
                    lE.setVisible(True)
                    reg_ex = QRegularExpression(reg_exps[items[key]['regEx']])
                    input_validator = QRegularExpressionValidator(reg_ex, lE)
                    lE.setValidator(input_validator)
                else: 
                    lE.setVisible(False)
            else: 
                lE.setVisible(False)
            self.cButtons.append(cB)

            setattr(self, 'hL'+str(nn), hL)
            setattr(self, 'checkBox'+str(nn), cB)
            setattr(self, 'lineEdit'+str(nn), lE)
            nn += 1

        self.buttonBox.clicked.connect(lambda: self.accepted(items))
        self.buttonBox.rejected.connect(lambda: self.rejected())
        self.setModal(True)
        self.show()

    def accepted(self, items):
        checked = {}
        for cB in self.cButtons:
            #Find the key that leads to that text
            for key in items: 
                if items[key]['opt'] == cB.text(): 
                    keyf = key
                    break
            checked[keyf] = cB.isChecked()
        self.output = checked
        self.close()

    def rejected(self):
        print('Rejected!')
        self.output = None
        self.close()

class Prompt_user_input(QDialog):
    def __init__(self, msg:str, title:str, info:Union[str, tuple], parent=None):
        super().__init__()
        uic.loadUi('src/gui/ui/prompt_user_input.ui', self)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setHtml(html_txt[0]+html_txt[1]+msg+html_txt[2])
        self.output = None

        if title == 'Custom Orientation':
            self.custom_or = None
            reg_ex = QRegularExpression("[a-z-A-Z_ 0-9,]+")
            self.buttonBox.clicked.connect(lambda: self.validate_custom_or(parent, info))

        elif title == 'Custom Strain' or title == 'Custom Stage' or title == 'Custom Genotype' or title == 'Custom Manipulation': 
            reg_ex = QRegularExpression("[a-z-A-Z_ 0-9(),.:;/+-]+")
            self.buttonBox.clicked.connect(lambda: self.validate_organ_data(parent, info))

        elif title == 'Centreline point number to initialise Disc':
            reg_ex = QRegularExpression("\d{1,3}")
            self.buttonBox.clicked.connect(lambda: self.validate_number(parent, info))

        else: 
            reg_ex = QRegularExpression('.*')

        self.buttonBox.rejected.connect(lambda: self.rejected())

        input_validator = QRegularExpressionValidator(reg_ex, self.lineEdit)
        self.lineEdit.setValidator(input_validator)
        self.setModal(True)
        self.show()

    def rejected(self):
        print('Rejected!')
        self.output = None
        self.close()

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
            self.output = added_or
            self.close()
    
    def validate_organ_data(self, parent, name):
        user_input = self.lineEdit.text()
        if len(user_input) <= 0: 
            error_txt = "*The organ's "+name+" needs to have at least two (2) characters."
            self.tE_validate.setText(error_txt)
            return
        else: 
            setattr(self, 'custom_'+name, user_input)
            cB_data = getattr(parent, 'cB_'+name)
            cB_data.addItem(user_input)
            cB_data.setCurrentText(user_input)
            self.output = user_input
            self.close()
    
    def validate_number(self, parent, info): 
        user_input = self.lineEdit.text()
        if len(user_input) == 0: 
            error_txt = "*Please provide a valid number."
            self.tE_validate.setText(error_txt)
            return
        elif int(user_input) < info[0] or int(user_input) > info[1]: 
            error_txt = "*Please provide a valid number between "+str(info)+"."
            self.tE_validate.setText(error_txt)
            return
        else: 
            self.output = int(user_input)
            self.close()

class Prompt_save_all(QDialog): 
    def __init__(self, msg:list, info:list, parent=None):
        super().__init__()
        uic.loadUi('src/gui/ui/prompt_saveall_discard_cancel.ui', self)
        self.setWindowTitle('Save all?')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        html_all = html_txt[0]
        for ms in msg: 
            html_all = html_all+html_txt[1]+ms+html_txt[2]
        self.textEdit.setHtml(html_all)
        self.info = info
        self.parent = parent
        self.output = None

        #Add Button Box
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setStyleSheet("QDialogButtonBox QPushButton{ color: rgb(39, 39, 39); font: 11pt \"Calibri Light\"; height:20;\n"
                                        "padding:0px; width:90; background-color: rgb(211, 211, 211); border-radius: 10px;\n"
                                        "border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66);}\n"
                                    "QDialogButtonBox QPushButton:hover{background-color: #eb6fbd; border-color: #672146}")

        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.SaveAll|QtWidgets.QDialogButtonBox.StandardButton.Discard|QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        self.tE_validate = QtWidgets.QLineEdit()
        self.tE_validate.setMinimumSize(QtCore.QSize(0, 25))
        self.tE_validate.setMaximumSize(QtCore.QSize(16777215, 25))
        self.tE_validate.setStyleSheet("font: 25 9pt \"Calibri Light\"; color: rgb(170, 0, 127); background-color: rgb(250, 250, 250);")
        self.tE_validate.setFrame(False)
        self.tE_validate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tE_validate.setReadOnly(True)
        self.tE_validate.setObjectName("tE_validate")
        self.verticalLayout.addWidget(self.tE_validate)

        self.buttonBox.clicked.connect(self.action_button)
        self.setModal(True)
        self.show()

    def action_button(self, button): 
        self.output = button.text()
        self.close()

class CreateNewProj(QDialog):

    def __init__(self, parent=None):
        super().__init__()
        self.proj_name = ''
        self.proj_dir_parent = ''
        uic.loadUi('src/gui/ui/new_project_screen.ui', self)
        self.setWindowTitle('Create New Project...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))

        self.mH_user_params = None
        self.mC_user_params = None

        #Initialise variables
        self.reg_ex = QRegularExpression("[a-z-A-Z_ 0-9(),]+")
        self.reg_ex_spaces = QRegularExpression("[a-z-A-Z_ 0-9]+")
        self.reg_ex_no_spaces = QRegularExpression("[a-z-A-Z_0-9]+")
        self.reg_ex_comma = QRegularExpression("[a-z-A-Z_ 0-9,]+")

        #Initialise window sections
        self.init_gral_proj_set()
        #Initialise Tabs for morphoHeart Analysis and morphoCell
        self.init_analysis_tabs()
        #- morphoHeart
        self.init_mHeart_tab()
        self.init_orient_group()
        self.init_chNS_group()
        self.init_segments_group()
        self.init_sections_group()
        self.init_segm_sect_group()
        #- morphoCell
        self.init_mCell_tab()

        #Project template
        self.cB_proj_as_template.stateChanged.connect(lambda: self.save_as_template())
        self.lineEdit_template_name.setValidator(QRegularExpressionValidator(self.reg_ex, self.lineEdit_template_name))

    def win_msg(self, msg, btn=None): 
        if self.button_create_initial_proj.isEnabled(): 
            tE = self.tE_validate
        else: 
            tE = self.tE_validate2

        if msg[0] == '*':
            tE.setStyleSheet(error_style)
            msg = 'Error: '+msg
            alert('error_beep')
        elif msg[0] == '!':
            tE.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            tE.setStyleSheet(msg_style)
        tE.setText(msg)

        if btn != None: 
            btn.setChecked(False)

    def init_gral_proj_set(self):
        now = QDate.currentDate()
        self.dateEdit.setDate(now)

        self.checked_analysis = {'morphoHeart': self.checkBox_mH.isChecked(), 
                                'morphoCell': self.checkBox_mC.isChecked(), 
                                'morphoPlot': self.checkBox_mP.isChecked()}
        #Set validator
        self.lineEdit_proj_name.setValidator(QRegularExpressionValidator(self.reg_ex, self.lineEdit_proj_name))

        # Create a new project
        self.win_msg("Create a new project by providing a project's name, directory and analysis pipeline.")

        #Get project directory
        self.button_select_proj_dir.clicked.connect(lambda: self.get_proj_dir())
        #Validate and Create Initial Project (proj_name, analysis_pipeline, proj_dir)
        self.button_create_initial_proj.clicked.connect(lambda: self.validate_new_proj())

    def init_analysis_tabs(self): 
        #Set Tab Widgets
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.tabWidget.setTabText(0,'Morphological [morphoHeart]')
        self.tabWidget.setTabText(1,'Cellular [morphoCell]')
        self.tabWidget.setEnabled(False)

    def init_mHeart_tab(self):
        #Initial set-up objects
        # -- Channels
        #Ch1
        self.fillcolor_ch1_int_btn.clicked.connect(lambda: self.color_picker('ch1_int'))
        self.fillcolor_ch1_tiss_btn.clicked.connect(lambda: self.color_picker('ch1_tiss'))
        self.fillcolor_ch1_ext_btn.clicked.connect(lambda: self.color_picker('ch1_ext'))
        #Ch2
        self.tick_ch2.stateChanged.connect(lambda: self.add_channel('ch2'))
        self.fillcolor_ch2_int_btn.clicked.connect(lambda: self.color_picker('ch2_int'))
        self.fillcolor_ch2_tiss_btn.clicked.connect(lambda: self.color_picker('ch2_tiss'))
        self.fillcolor_ch2_ext_btn.clicked.connect(lambda: self.color_picker('ch2_ext'))
        #Ch3
        self.tick_ch3.stateChanged.connect(lambda: self.add_channel('ch3'))
        self.fillcolor_ch3_int_btn.clicked.connect(lambda: self.color_picker('ch3_int'))
        self.fillcolor_ch3_tiss_btn.clicked.connect(lambda: self.color_picker('ch3_tiss'))
        self.fillcolor_ch3_ext_btn.clicked.connect(lambda: self.color_picker('ch3_ext'))
        #Ch4
        self.tick_ch4.stateChanged.connect(lambda: self.add_channel('ch4'))
        self.fillcolor_ch4_int_btn.clicked.connect(lambda: self.color_picker('ch4_int'))
        self.fillcolor_ch4_tiss_btn.clicked.connect(lambda: self.color_picker('ch4_tiss'))
        self.fillcolor_ch4_ext_btn.clicked.connect(lambda: self.color_picker('ch4_ext'))

        #Default colors (Channels)
        self.ck_def_colors.stateChanged.connect(lambda: self.default_colors('ch'))

        #Set validator
        self.ch1_username.setValidator(QRegularExpressionValidator(self.reg_ex_spaces, self.ch1_username))
        self.ch2_username.setValidator(QRegularExpressionValidator(self.reg_ex_spaces, self.ch2_username))
        self.ch3_username.setValidator(QRegularExpressionValidator(self.reg_ex_spaces, self.ch3_username))
        self.ch4_username.setValidator(QRegularExpressionValidator(self.reg_ex_spaces, self.ch4_username))

        #Validate initial settings
        self.button_set_initial_set.clicked.connect(lambda: self.validate_initial_settings())

        #Set processes
        self.set_processes.setEnabled(False)
        self.button_set_processes.clicked.connect(lambda: self.set_selected_processes())

    def init_orient_group(self): 
        self.cB_stack_orient.currentIndexChanged.connect(lambda: self.custom_orient('stack'))
        self.cB_roi_orient.currentIndexChanged.connect(lambda: self.custom_orient('roi'))
        self.button_set_orient.clicked.connect(lambda: self.set_orientation_settings())

    def init_chNS_group(self):
        # -- Channel NS
        self.set_chNS.setDisabled(True)
        self.set_chNS.setVisible(False)
        self.fillcolor_chNS_int_btn.clicked.connect(lambda: self.color_picker('chNS_int'))
        self.fillcolor_chNS_tiss_btn.clicked.connect(lambda: self.color_picker('chNS_tiss'))
        self.fillcolor_chNS_ext_btn.clicked.connect(lambda: self.color_picker('chNS_ext'))

        #Buttons
        # -Set ChNS
        self.button_set_chNS.clicked.connect(lambda: self.validate_chNS_settings())

        #Set Validator
        self.chNS_username.setValidator(QRegularExpressionValidator(self.reg_ex_spaces, self.chNS_username))
        
        #Default colors (ChannelNS)
        self.ck_def_colorsNS.stateChanged.connect(lambda: self.default_colors('chNS'))

        #Operations
        self.chNS_operation.addItems(['----', 'XOR'])

    def init_segments_group(self):
        # -- Segments
        self.set_segm.setDisabled(True)
        self.set_segm.setVisible(False)
        #Segm 1
        self.tick_segm1.setEnabled(True)
        self.tick_segm1.setChecked(True)
        self.sB_no_segm1.setEnabled(True)
        self.cB_obj_segm1.setEnabled(True)
        self.sB_segm_noObj1.setEnabled(True)
        self.names_segm1.setEnabled(True)
        #Segm 2
        self.tick_segm2.setEnabled(True)
        self.tick_segm2.setChecked(False)
        self.sB_no_segm2.setEnabled(False)
        self.cB_obj_segm2.setEnabled(False)
        self.sB_segm_noObj2.setEnabled(False)
        self.names_segm2.setEnabled(False)
        self.tick_segm2.stateChanged.connect(lambda: self.add_segm_sect('segm'))
        list_obj_segm = ['Disc']#, 'Plane']
        for cB in [self.cB_obj_segm1, self.cB_obj_segm2]:
            for obj in list_obj_segm: 
                cB.addItem(obj)
        for sB in [self.sB_no_segm1, self.sB_no_segm2, self.sB_segm_noObj1, self.sB_segm_noObj2]:
            sB.setMinimum(1)
            sB.setMaximum(5)

        #Set validator
        self.names_segm1.setValidator(QRegularExpressionValidator(self.reg_ex_comma, self.names_segm1))
        self.names_segm2.setValidator(QRegularExpressionValidator(self.reg_ex_comma, self.names_segm2))

        #Buttons
        # self.apply_segm.clicked.connect(lambda: )
        self.button_set_segm.clicked.connect(lambda: self.validate_segments())

        self.tick_segm1.stateChanged.connect(lambda: always_checked(self.tick_segm1))

    def init_sections_group(self):
        # -- Sections
        self.set_sect.setDisabled(True)
        self.set_sect.setVisible(False)
        #Sect1
        self.tick_sect1.setEnabled(True)
        self.tick_sect1.setChecked(True)
        self.cB_obj_sect1.setEnabled(True)
        self.names_sect1.setEnabled(True)
        #Sect2
        self.tick_sect2.setEnabled(True)
        self.tick_sect2.setChecked(False)
        self.cB_obj_sect2.setEnabled(False)
        self.names_sect2.setEnabled(False)
        self.tick_sect2.stateChanged.connect(lambda: self.add_segm_sect('sect'))
        list_obj_sect = ['Centreline']#, 'Plane']
        for cB in [self.cB_obj_sect1, self.cB_obj_sect2]:
            for obj in list_obj_sect: 
                cB.addItem(obj)

        #Set validator
        self.names_sect1.setValidator(QRegularExpressionValidator(self.reg_ex_comma, self.names_sect1))
        self.names_sect2.setValidator(QRegularExpressionValidator(self.reg_ex_comma, self.names_sect2))

        #Buttons
        # self.apply_sect.clicked.connect(lambda: )
        self.button_set_sect.clicked.connect(lambda: self.validate_sections())

        self.tick_sect1.stateChanged.connect(lambda: always_checked(self.tick_sect1))

    def init_segm_sect_group(self): 
        # -- Segments/Sections
        self.set_segm_sect.setDisabled(True)
        self.set_segm_sect.setVisible(False)
        self.widget_segm_sect.setVisible(False)
        self.tick_segm_sect_2.setEnabled(False)

        self.tick_segm_sect_2.stateChanged.connect(lambda: self.open_sect_segm())
        #Buttons
        self.button_set_segm_sect.clicked.connect(lambda: self.validate_segm_sect())

    def init_mCell_tab(self):
        pass

    #Functions for General Project Settings   
    def get_proj_dir(self):
        self.button_create_initial_proj.setChecked(False)
        self.button_select_proj_dir.setChecked(True)
        response = QFileDialog.getExistingDirectory(self, caption='Select a Directory to save New Project Files')
        self.proj_dir_parent = Path(response)
        self.lab_filled_proj_dir.setText(str(self.proj_dir_parent))

    def validate_new_proj(self): 
        valid = []; error_txt = ''
        #Get project name
        if len(self.lineEdit_proj_name.text())<5:
            error_txt = '*Project name needs to have at least five (5) characters'
            self.win_msg(error_txt, self.button_create_initial_proj)
            return
        elif validate_txt(self.lineEdit_proj_name.text()) != None:
            error_txt = "Please avoid using invalid characters in the project's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt, self.button_create_initial_proj)
            return
        else: 
            self.proj_name = self.lineEdit_proj_name.text()
            valid.append(True)
        
        #Get Analysis Pipeline
        self.checked_analysis = {'morphoHeart': self.checkBox_mH.isChecked(), 
                                    'morphoCell': self.checkBox_mC.isChecked(), 
                                    'morphoPlot': self.checkBox_mP.isChecked()}
        checked = [self.checked_analysis[key] for key in self.checked_analysis if 'Plot' not in key]

        if not(any(checked)):
            error_txt = '*Please select an Analysis Pipeline for the new project'
            self.win_msg(error_txt, self.button_create_initial_proj)
            return
        else: 
            valid.append(True)
        
        #Get Directory
        if isinstance(self.proj_dir_parent, str): 
            error_txt = '*Please select a project directory where the new project will be saved.'
            self.win_msg(error_txt, self.button_create_initial_proj)
            return
        else:  
            if self.proj_dir_parent.is_dir() and len(str(self.proj_dir_parent))>1:
                valid.append(True)
            else: 
                self.button_select_proj_dir.setChecked(False)
                error_txt = '*The selected project directory is invalid. Please select another directory.'
                self.win_msg(error_txt, self.button_create_initial_proj)
                return

        #Check and if all valid create new project
        if len(valid)== 3 and all(valid):
            proj_folder = 'R_'+self.proj_name#.replace(' ','_')
            self.proj_dir = self.proj_dir_parent / proj_folder
            if self.proj_dir.is_dir():
                self.win_msg('*There is already a project named "'+self.proj_name+'" in the selected directory. Please select a different name for the new project.', 
                             self.button_create_initial_proj)
                return 
            else: 
                self.lab_filled_proj_dir.setText(str(self.proj_dir))
                self.button_create_initial_proj.setChecked(True)
                self.win_msg('All good. Continue setting up new project!')   
                self.create_new_proj()  
        else: 
            self.button_create_initial_proj.setChecked(False)
            self.win_msg(error_txt, self.button_create_initial_proj)
            return 

    def create_new_proj(self):
        self.tabWidget.setEnabled(True)
        self.tab_mHeart.setEnabled(self.checked_analysis['morphoHeart'])
        self.tab_mCell.setEnabled(self.checked_analysis['morphoCell'])
        self.tab_mHeart.setVisible(self.checked_analysis['morphoHeart'])
        self.tab_mCell.setVisible(self.checked_analysis['morphoCell'])
        if self.checked_analysis['morphoHeart']:
            self.mH_settings = {'no_chs': 0,
                                'name_chs': 0,
                                'chs_relation': 0,
                                'color_chs': 0,
                                'orientation': 0,
                                'rotateZ_90': True}
        else: 
            self.mH_settings = None
            self.mH_user_params = None
            self.mH_methods = None
            
        if self.checked_analysis['morphoCell']:
            self.mC_settings = {}
        else: 
            self.mC_settings = None
            self.mC_user_params = None
            self.mC_methods = None
    
        #Disable all fields from Gral Project Settings
        self.win_msg('New project  "'+self.proj_name+'" has been created! Continue by setting the channel information.')
        self.gral_proj_settings.setDisabled(True)
        if self.checked_analysis['morphoHeart']:
            self.tabWidget.setCurrentIndex(0)
        else: 
            self.tabWidget.setCurrentIndex(1)

    #Functions for Initial Set-up 
    # -- Functions for orientation
    def custom_orient(self, ortype): 
        user_or = getattr(self,'cB_'+ortype+'_orient').currentText()
        if user_or == 'custom':
            msg = "Give the name of the three different custom orientations for the  '"+ortype.upper()+"'  separated by a comma:"
            title = 'Custom Orientation'
            self.prompt = Prompt_user_input(msg = msg, title = title, info = ortype, parent = self)
        else: 
            pass 

    def set_orientation_settings(self):
        valid = []; error_txt = ''
        stack_or = self.cB_stack_orient.currentText()
        if stack_or == '--select--': 
            error_txt = '*Please select axis labels for the stack'
            self.win_msg(error_txt, self.button_set_orient)
            return
        else: 
            valid.append(True)

        roi_or = self.cB_roi_orient.currentText()
        if roi_or == '--select--': 
            error_txt = '*Please select axis labels for the Organ/ROI'
            self.win_msg(error_txt, self.button_set_orient)
            return
        else: 
            valid.append(True)

        if len(valid) == 2 and all(valid):
            # print(self.cB_stack_orient.currentText())
            self.mH_settings['orientation'] = {'stack': self.cB_stack_orient.currentText(),
                                                'roi': self.cB_roi_orient.currentText()}
            self.win_msg('Great! Continue setting up the new project!')
            self.button_set_orient.setChecked(True)
            # print('self.mH_settings (set_orientation_settings):', self.mH_settings)
            return True
        else: 
            self.button_set_orient.setChecked(False)
            return False

    # -- Functions for channels
    def add_channel(self, name):
        tick = getattr(self, 'tick_'+name)

        user_name = getattr(self, name+'_username')
        fill_int = getattr(self, 'fillcolor_'+name+'_int')
        btn_int = getattr(self, 'fillcolor_'+name+'_int_btn')
        fill_tiss = getattr(self, 'fillcolor_'+name+'_tiss')
        btn_tiss = getattr(self, 'fillcolor_'+name+'_tiss_btn')
        fill_ext = getattr(self, 'fillcolor_'+name+'_ext')
        btn_ext = getattr(self, 'fillcolor_'+name+'_ext_btn')
        ck_mask = getattr(self, name+'_mask')
        cB_dist = getattr(self, 'cB_'+name)
        
        if tick.isChecked():
            #Activate all widgets
            user_name.setEnabled(True)
            fill_int.setEnabled(True)
            btn_int.setEnabled(True)
            fill_tiss.setEnabled(True)
            btn_tiss.setEnabled(True)
            fill_ext.setEnabled(True)
            btn_ext.setEnabled(True)
            ck_mask.setEnabled(True)
            cB_dist.setEnabled(True)
            if self.ck_def_colors.isChecked():
                self.default_colors('ch')
        else: 
            #Deactivate all widgets
            user_name.setEnabled(False)
            fill_int.setEnabled(False)
            btn_int.setEnabled(False)
            fill_tiss.setEnabled(False)
            btn_tiss.setEnabled(False)
            fill_ext.setEnabled(False)
            btn_ext.setEnabled(False)
            ck_mask.setEnabled(False)
            cB_dist.setEnabled(False)
            # color_txt = "background-color: rgb(255, 255, 255); color: rgb(255, 255, 255); font: 25 2pt 'Calibri Light'"
            for cont in ['int', 'tiss', 'ext']:
                fill = getattr(self, 'fillcolor_'+name+'_'+cont)
                color_btn(btn = fill, color = 'rgb(255, 255, 255)')
                # fill.setStyleSheet(color_txt)
                fill.setText('rgb(255, 255, 255)')

    def color_picker(self, name):
        color = QColorDialog.getColor()
        if color.isValid():
            # print('The selected color is: ', color.name())
            fill = getattr(self, 'fillcolor_'+name)
            red, green, blue, _ = color.getRgb() #[red, green, blue]
            color_btn(btn = fill, color = color.name())
            # fill.setStyleSheet("background-color: "+color.name()+"; color: "+color.name()+"; font: 25 2pt 'Calibri Light'")#+"; border: 1px solid "+color.name())
            fill.setText(str([red, green, blue]))
            print('Color:', fill.text())
        getattr(self, 'fillcolor_'+name+'_btn').setChecked(False)
            
    def default_colors(self, name):
        if self.ck_def_colors.isChecked():
            if name == 'ch': 
                df_colors = {'ch1': {'int': 'gold', 'tiss': 'lightseagreen', 'ext':'crimson'},
                            'ch2': {'int': 'deepskyblue', 'tiss': 'darkmagenta', 'ext':'deeppink'},
                            'ch3': {'int': 'cyan', 'tiss': 'indigo', 'ext':'hotpink'},
                            'ch4': {'int': 'chocolate', 'tiss': 'seagreen', 'ext':'salmon'}}
            elif name == 'chNS':
                df_colors = {'chNS': {'int': 'greenyellow', 'tiss': 'darkorange', 'ext':'powderblue'}}
                             
            for ch in df_colors:
                if getattr(self, 'tick_'+ch).isChecked():
                    for cont in df_colors[ch]:
                        color = df_colors[ch][cont]
                        fill = getattr(self, 'fillcolor_'+ch+'_'+cont)
                        color_btn(btn = fill, color = color)
                        # fill.setStyleSheet("background-color: "+color+"; color: "+color+"; font: 25 2pt 'Calibri Light'")#+"; border: 1px solid "+color.name())
                        fill.setText(color)

    def checked(self, stype):
        ck_type = getattr(self, 'tick_'+stype)
        s_set = getattr(self, 'set_'+stype)
        if ck_type.isChecked():
            if stype == 'chNS': 
                self.ch_selected.append('chNS')
            if stype in list(self.mH_settings.keys()):
                s_set.setVisible(True)
                s_set.setEnabled(True)
                return True
            else: 
                s_set.setVisible(True)
                s_set.setEnabled(True)
                self.mH_settings[stype] = {}
                return True
        else: 
            if stype == 'chNS': 
                if 'chNS' in self.ch_selected: 
                    self.ch_selected.remove('chNS')
            s_set.setVisible(False)
            s_set.setEnabled(False)
            self.mH_settings[stype] = False
            return False
    
    def validate_initial_settings(self):
        valid = []; error_txt = ''
        self.tick_ch1.setChecked(True)
        # Get ticked channels:
        ch_ticked = [self.tick_ch1.isChecked(), self.tick_ch2.isChecked(), 
                     self.tick_ch3.isChecked(), self.tick_ch4.isChecked()]
        if not any(ch_ticked):
            error_txt = '*Please select at least one channel.'
            self.win_msg(error_txt, self.button_set_initial_set)
            return
        else: 
            valid.append(True)

        #Check names
        names_valid = []
        names = []
        for ch in ['ch1', 'ch2', 'ch3', 'ch4']:
            tick = getattr(self, 'tick_'+ch)
            if tick.isChecked(): 
                ch_name = getattr(self, ch+'_username').text()
                if len(ch_name) < 3:
                    error_txt = '*Active channels must have a name with at least three (3) characters.'
                    self.win_msg(error_txt, self.button_set_initial_set)
                    return
                elif validate_txt(ch_name) != None:
                    error_txt = "*Please avoid using invalid characters in the channel's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
                    self.win_msg(error_txt, self.button_set_initial_set)
                    return
                else: 
                    names.append(ch_name)
                    names_valid.append(True)

        if all(names_valid):
            valid.append(True)

        #Check names are different
        if len(names) > len(set(names)):
            error_txt = '*The names given to the selected channels need to be unique.'
            self.win_msg(error_txt, self.button_set_initial_set)
            return
        else: 
            valid.append(True)

        # Check colors
        all_colors = []
        for ch in ['ch1', 'ch2', 'ch3', 'ch4']:
            tick = getattr(self, 'tick_'+ch)
            if tick.isChecked(): 
                for cont in ['int', 'tiss', 'ext']:
                    all_colors.append(getattr(self, 'fillcolor_'+ch+'_'+cont).text() != '')
        # print(all_colors)
        if not all(all_colors):
            error_txt = '*Make sure you have selected colors for all the active channel contours.'
            self.win_msg(error_txt, self.button_set_initial_set)
            return
        else: 
            valid.append(True)
        
        #Check relation
        ch_relation = []
        for ch in ['ch1', 'ch2', 'ch3', 'ch4']:
            tick = getattr(self, 'tick_'+ch)
            if tick.isChecked():
                ch_relation.append(getattr(self, 'cB_'+ch).currentText())
        print('ch_relation:', ch_relation)

        internal_count = ch_relation.count('internal layer')
        external_count = ch_relation.count('external layer') 
        indep_count = ch_relation.count('independent layer') 
        blank_count = ch_relation.count('--select--')
        print('blank_count:',blank_count)

        if self.ck_chs_contained.isChecked() or self.ck_chs_allcontained.isChecked():
            if sum(ch_ticked) == 1: 
                if external_count != 1: 
                    error_txt = '*Please define the active channel as external.'
                    self.win_msg(error_txt, self.button_set_initial_set)
                    return
                else: 
                    valid.append(True)
            elif sum(ch_ticked) == 2: 
                if internal_count != 1 or external_count != 1:
                    error_txt = '*One channel needs to be selected as the internal layer and other as the external.'
                    self.win_msg(error_txt, self.button_set_initial_set)
                    return
                elif internal_count == 1 and external_count == 1:
                    valid.append(True)

            elif sum(ch_ticked) > 2: 
                if internal_count != 1 or external_count != 1:
                    error_txt = '*One channel needs to be selected as the internal layer, other as the external and the other(s) as middle/independent.'
                    self.win_msg(error_txt, self.button_set_initial_set)
                    return
                elif internal_count == 1 and external_count == 1:
                    valid.append(True)
        else: 
            if sum(ch_ticked) == 1: 
                if indep_count != 1: 
                    error_txt = '*Please define the active channel as independent layer.'
                    self.win_msg(error_txt, self.button_set_initial_set)
                    return
                else: 
                    valid.append(True)
            elif blank_count != 0: 
                error_txt = '*Please define the channel organisation for all channels.'
                self.win_msg(error_txt, self.button_set_initial_set)
                return
            else: 
                valid.append(True)

        if sum(ch_ticked) == 1 and self.tick_chNS.isChecked() and (self.ck_chs_contained.isChecked() or self.ck_chs_allcontained.isChecked()):
            error_txt = '*At least an external channel and an internal channel need to be selected to create a tissue from the negative space.'
            self.win_msg(error_txt, self.button_set_initial_set)
        else: 
            valid.append(True)

        if all(valid):
            self.win_msg('All done!... Press -Set Initial Settings- to continue.')
            self.set_initial_settings()
        else: 
            return False

    def set_initial_settings(self):
        self.set_processes.setEnabled(True)
        self.button_set_initial_set.setChecked(True)
        self.tick_ch1.setChecked(True)

        #Get data from initial settings
        # Get data form ticked channels:
        ch_ticked = [self.tick_ch1.isChecked(), self.tick_ch2.isChecked(), 
                    self.tick_ch3.isChecked(), self.tick_ch4.isChecked()]
        
        self.mH_settings['no_chs'] = sum(ch_ticked)
        user_name = {}
        color_chs = {}
        ch_relation = {}
        mask_ch = {}
        ch_selected = []
        for ch in ['ch1', 'ch2', 'ch3', 'ch4']:
            tick = getattr(self, 'tick_'+ch)
            if tick.isChecked(): 
                ch_selected.append(ch)
                user_name[ch] = getattr(self, ch+'_username').text()
                ch_relation[ch] = getattr(self, 'cB_'+ch).currentText().split(' ')[0]
                mask_ch[ch] = getattr(self, ch+'_mask').isChecked()
                color_chs[ch] = {}
                for cont in ['int', 'tiss', 'ext']:
                    color_chs[ch][cont] = getattr(self, 'fillcolor_'+ch+'_'+cont).text()

        self.mH_settings['name_chs'] = user_name
        self.mH_settings['chs_relation'] = ch_relation
        self.mH_settings['color_chs'] = color_chs
        self.mH_settings['mask_ch'] = mask_ch
        self.mH_settings['all_contained'] = self.ck_chs_allcontained.isChecked()
        self.mH_settings['one_contained'] = self.ck_chs_contained.isChecked()

        self.ch_selected = ch_selected

        #Set the comboBoxes for chNS
        print(ch_relation)
        ch_rel = [item for key, item in ch_relation.items()]
        if self.mH_settings['no_chs'] > 1 and any('external' in flag for flag in ch_rel) and any('internal' in flag for flag in ch_rel):
            self.ext_chNS.clear(); self.int_chNS.clear()
            self.ext_chNS.addItems(['----']+self.ch_selected)
            self.int_chNS.addItems(['----']+self.ch_selected)
            self.tick_chNS.setEnabled(True)
        else: 
            self.tick_chNS.setEnabled(False)
        
        self.win_msg("Great! Now select the processes you would like to include in the workflow and setup their details.")

        return True
    
    def set_selected_processes(self): 
        #Get info from checked boxes
        __ = self.checked('chNS')
        #---- Segments
        segm_bool = self.checked('segm')   
        #---- Sections
        sect_bool = self.checked('sect')

        #Set Table for Segments and Sections
        for ch in ['ch1', 'ch2', 'ch3', 'ch4', 'chNS']:
            for cont in ['int', 'tiss', 'ext']:
                for stype in ['segm', 'sect']:
                    for cut in ['Cut1', 'Cut2']:
                        if ch in self.ch_selected:
                            getattr(self, 'label_'+stype+'_'+ch).setEnabled(True)
                            getattr(self, 'label_'+stype+'_'+ch+'_'+cont).setEnabled(True)
                            if cut == 'Cut1':
                                getattr(self, 'cB_'+stype+'_'+cut+'_'+ch+'_'+cont).setEnabled(True) 
                            else: 
                                getattr(self, 'cB_'+stype+'_'+cut+'_'+ch+'_'+cont).setEnabled(False) 
                        else: 
                            getattr(self, 'label_'+stype+'_'+ch).setVisible(False)
                            getattr(self, 'label_'+stype+'_'+ch+'_'+cont).setVisible(False)
                            getattr(self, 'cB_'+stype+'_'+cut+'_'+ch+'_'+cont).setVisible(False)

        if segm_bool and sect_bool: 
            self.set_segm_sect.setEnabled(True)
            self.set_segm_sect.setVisible(True)

            for ch in ['ch1', 'ch2', 'ch3', 'ch4', 'chNS']:
                for cont in ['int', 'tiss', 'ext']:
                    for cut_segm in ['sCut1', 'sCut2']: # segments
                        for cut_sect in ['Cut1', 'Cut2']: #sections
                            if ch in self.ch_selected:
                                getattr(self, 'label_'+cut_segm+'_'+ch).setEnabled(True)
                                getattr(self, 'label_'+cut_segm+'_'+ch+'_'+cont).setEnabled(True)
                                getattr(self, 'cB_'+cut_segm+'_'+cut_sect+'_'+ch+'_'+cont).setEnabled(True) #cB_sCut1_Cut1_ch1_int
                            else: 
                                getattr(self, 'label_'+cut_segm+'_'+ch).setVisible(False)
                                getattr(self, 'label_'+cut_segm+'_'+ch+'_'+cont).setVisible(False)
                                getattr(self, 'cB_'+cut_segm+'_'+cut_sect+'_'+ch+'_'+cont).setVisible(False)


        self.button_set_processes.setChecked(True)

        #Enable measurement parameters now to know whether regions was selected
        self.set_meas_param_all.setEnabled(True)

    # -- Functions for ChannelNS
    def validate_chNS_settings(self): 
        valid = []; error_txt = ''
        #Check name
        name_chNS = self.chNS_username.text()
        names_ch = [self.mH_settings['name_chs'][key] for key in self.mH_settings['name_chs'].keys()]
        # print('names_ch:',names_ch)
        if len(name_chNS)< 3: 
            error_txt = '*Channel from the negative space must have a name with at least three (3) characters.'
            self.win_msg(error_txt, self.button_set_chNS)
            return
        elif validate_txt(name_chNS) != None:
            error_txt = "*Please avoid using invalid characters in the chNS's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt, self.button_set_chNS)
            return
        else: 
            if name_chNS not in names_ch:
                valid.append(True)
            else:
                error_txt = '*The name given to the channel obtained from the negative space needs to be different to that of the other channels.'
                self.win_msg(error_txt, self.button_set_chNS)
                return
            
        #Check colors
        all_colors = []
        for cont in ['int', 'tiss', 'ext']:
            all_colors.append(getattr(self, 'fillcolor_chNS_'+cont).text() != '')
        
        if not all(all_colors):
            error_txt = '*Make sure you have selected colors for the channel obtained from the negative space.'
            self.win_msg(error_txt, self.button_set_chNS)
            return
        else: 
            valid.append(True)
        
        #Check int and ext channel and cont selection
        ch_ext = self.ext_chNS.currentText()
        ext_cont = self.ext_contNS.currentText()
        ch_int = self.int_chNS.currentText()
        int_cont = self.int_contNS.currentText()

        # print(ch_ext, ext_cont, ch_int, int_cont)
        blank = '----'
        if ch_ext != blank and ext_cont != blank and ch_int != blank and int_cont != blank: 
            if ch_ext == ch_int: 
                error_txt = '*To extract a channel from the negative space, the external and internal channels need to be different. Please check.'
                self.win_msg(error_txt, self.button_set_chNS)
                return
            else: 
                valid.append(True)
        else: 
            error_txt = '*Please select the internal and external channels and contours that need to be used to extract the channel from the negative space.'
            self.win_msg(error_txt, self.button_set_chNS)
            return
        
        #Check operation
        chNS_operation = self.chNS_operation.currentText()
        if chNS_operation != '----': 
            valid.append(True)
        else: 
            error_txt = '*Please select an operation to extract the channel from the negative space.'
            self.win_msg(error_txt, self.button_set_chNS)
            return
            
        if all(valid): # and len(valid)== 4 
            self.win_msg('All done setting ChannelNS!...')
            self.button_set_chNS.setChecked(True)
            self.set_chNS_settings()
            return True
        else: 
            self.button_set_chNS.setChecked(False)
            return False

    def set_chNS_settings(self):
        ch_ext = self.ext_chNS.currentText()
        ext_cont = self.ext_contNS.currentText()
        ch_int = self.int_chNS.currentText()
        int_cont = self.int_contNS.currentText()
        chNS_operation = self.chNS_operation.currentText()

        color_chNS = {}
        for cont in ['int', 'tiss', 'ext']:
            color_chNS[cont] = getattr(self, 'fillcolor_chNS_'+cont).text()

        chNS_settings = {'layer_btw_chs': self.tick_chNS.isChecked(),
                            'ch_ext': (ch_ext.lower(), ext_cont[0:3]),
                            'ch_int': (ch_int.lower(), int_cont[0:3]),
                            'operation' : chNS_operation,
                            'user_nsChName': self.chNS_username.text(),
                            'color_chns': color_chNS, 
                            'keep_largest': {},
                            'alpha': {}}
        
        self.mH_settings['chNS'] = chNS_settings

    # -- Functions for segments and sections
    def add_segm_sect(self, stype):
        tick = getattr(self, 'tick_'+stype+'2')
        obj_type = getattr(self, 'cB_obj_'+stype+'2')
        name_stype = getattr(self, 'names_'+stype+'2')

        if tick.isChecked(): 
            obj_type.setEnabled(True)
            name_stype.setEnabled(True)
            if stype == 'segm': 
                self.sB_no_segm2.setEnabled(True)
                self.sB_segm_noObj2.setEnabled(True)
            for ch in self.ch_selected:
                for cont in ['int', 'tiss', 'ext']:
                    getattr(self, 'cB_'+stype+'_Cut2_'+ch+'_'+cont).setEnabled(True) 
        else: 
            obj_type.setEnabled(False)
            name_stype.setEnabled(False)
            if stype == 'segm': 
                self.sB_no_segm2.setEnabled(False)
                self.sB_segm_noObj2.setEnabled(False)
            for ch in self.ch_selected:
                for cont in ['int', 'tiss', 'ext']:
                    getattr(self, 'cB_'+stype+'_Cut2_'+ch+'_'+cont).setDisabled(True) 
    
    def check_checkBoxes(self, ch_selected, stype):
        dict_stype = {}
        #Get Cuts selected
        cuts_sel = {'Cut1': getattr(self, 'tick_'+stype+'1').isChecked(), 'Cut2':getattr(self, 'tick_'+stype+'2').isChecked()}
        for cut in cuts_sel.keys(): 
            valid = []; error_txt = ''
            if cuts_sel[cut]:
                for ch in ch_selected: 
                    for cont in ['int', 'tiss', 'ext']: 
                        btn_name = 'cB_'+stype+'_'+cut+'_'+ch+'_'+cont
                        # print(btn_name, getattr(self, btn_name).isChecked())
                        dict_stype[btn_name] = getattr(self, btn_name).isChecked()

        setattr(self, 'dict_'+stype, dict_stype)
        # print(getattr(self, 'dict_'+stype))
        # print(dict_stype.items())

    def validate_segments(self): 
        valid_all = []
        stype = 'segm'
        cuts_sel = {'Cut1': getattr(self, 'tick_'+stype+'1').isChecked(), 'Cut2':getattr(self, 'tick_'+stype+'2').isChecked()}
        for cut in cuts_sel.keys(): 
            valid = []; error_txt = ''
            if cuts_sel[cut]:
                cut_no = cut[-1]
                #Get values
                no_segm = getattr(self, 'sB_no_segm'+cut_no).value()
                names_segm = getattr(self, 'names_segm'+cut_no).text()
                names_segm = names_segm.split(',')
                for xx, nam in enumerate(names_segm):
                    if nam == '':
                        names_segm.remove('')

                #Check values
                # print(names_segm, len(names_segm), no_segm)
                if len(names_segm) != int(no_segm):
                    error_txt = "*"+cut+": The number of segments need to match the number of segment names given."
                    self.win_msg(error_txt, self.button_set_segm)
                    return
                elif len(set(names_segm)) != int(no_segm):
                    error_txt = '*'+cut+": Segment names need to be different."
                    self.win_msg(error_txt, self.button_set_segm)
                    return
                else: 
                    valid.append(True)

                #Get checkboxes
                self.check_checkBoxes(self.ch_selected, 'segm')
                bool_cB = [val for (key,val) in self.dict_segm.items() if cut in key]
                if any(bool_cB): 
                    valid.append(True)
                else: 
                    error_txt = '*'+cut+": At least one channel contour needs to be selected for each segment cut."
                    self.win_msg(error_txt, self.button_set_segm)
                    return

                #Check measurement parameters to measure
                meas_vol = getattr(self, 'cB_volume_'+stype).isChecked()
                meas_area = getattr(self, 'cB_area_'+stype).isChecked()
                meas_ellip = getattr(self, 'cB_ellip_'+stype).isChecked()
                meas_angles = getattr(self, 'cB_angles_'+stype).isChecked()
                if any([meas_vol, meas_area, meas_ellip, meas_angles]):
                    valid.append(True)
                else: 
                    error_txt = "*Please select the measurement parameter(s) (e.g. volume, surface area) you want to extract from the segments"
                    self.win_msg(error_txt, self.button_set_segm)
                    return

            if len(valid) == 3 and all(valid): 
                valid_all.append(True)
        
        if all(valid_all): 
            self.win_msg('All good! Segments have been set (1).')
            self.set_segm_settings()
        else: 
            print('Aja? - segments')

    def validate_sections(self): 
        valid_all = []
        stype = 'sect'
        cuts_sel = {'Cut1': getattr(self, 'tick_'+stype+'1').isChecked(), 'Cut2':getattr(self, 'tick_'+stype+'2').isChecked()}
        for cut in cuts_sel.keys(): 
            valid = []; error_txt = ''
            if cuts_sel[cut]:
                cut_no = cut[-1]
                #Get values
                names_sect = getattr(self, 'names_sect'+cut_no).text()
                names_sect = names_sect.split(',')
                for xx, nam in enumerate(names_sect):
                    if nam == '':
                        names_sect.remove('')

                #Check values
                if len(names_sect) != 2:
                    error_txt = "*"+cut+":  Sections cut only produce two objects. Please provide two section names."
                    self.win_msg(error_txt, self.button_set_sect)
                    return
                elif len(set(names_sect)) != 2:
                    error_txt = '*'+cut+": Section names need to be different."
                    self.win_msg(error_txt, self.button_set_sect)
                    return
                else: 
                    valid.append(True)

                #Get checkboxes
                self.check_checkBoxes(self.ch_selected, 'sect')
                bool_cB = [val for (key,val) in self.dict_sect.items() if cut in key]
                if any(bool_cB): 
                    valid.append(True)
                else: 
                    error_txt = '*'+cut+": At least one channel contour needs to be selected for this section cut."
                    self.win_msg(error_txt, self.button_set_sect)
                    return
                
                #Check measurement parameters to measure
                meas_vol = getattr(self, 'cB_volume_'+stype).isChecked()
                meas_area = getattr(self, 'cB_area_'+stype).isChecked()
                if any([meas_vol, meas_area]):
                    valid.append(True)
                else: 
                    error_txt = "*Please select the measurement parameter(s) (e.g. volume, surface area) you want to extract from the sections"
                    self.win_msg(error_txt, self.button_set_sect)
                    return
                
            if len(valid) == 3 and all(valid): 
                valid_all.append(True)
        
        if all(valid_all): 
            self.win_msg('All good! Regions have been set (1).')
            self.set_sect_settings()
        else: 
            print('Aja? - sections')

    def validate_segm_sect(self): 
        valid = []
        #Get checkboxes
        at_least_one = False
        for cB_item in self.list_segm_sect: 
            if getattr(self, cB_item).isChecked(): 
                at_least_one = True
                break
        
        if at_least_one: 
            valid.append(True)
        else: 
            error_txt = "*At least one channel contour needs to be selected for the segment-region intersection cuts."
            self.win_msg(error_txt, self.button_set_segm_sect)
            return
        
        #Check measurement parameters to measure
        meas_vol = getattr(self, 'cB_volume_segm_sect').isChecked()
        meas_area = getattr(self, 'cB_area_segm_sect').isChecked()
        if any([meas_vol, meas_area]):
            valid.append(True)
        else: 
            error_txt = "*Please select the measurement parameter(s) (e.g. volume, surface area) you want to extract from the segment-region intersection cuts"
            self.win_msg(error_txt, self.button_set_segm_sect)
            return

        if all(valid): 
            self.win_msg('All good! Segment-Region Intersections have been set.')
            self.set_segm_sect_settings()
        else: 
            print('Aja? - Segment-Region')

    def set_segm_settings(self): 
        valid_all = []
        segm_settings = {'cutLayersIn2Segments': True}
        stype = 'segm'
        cuts_sel = {'Cut1': getattr(self, 'tick_'+stype+'1').isChecked(), 'Cut2':getattr(self, 'tick_'+stype+'2').isChecked()}
        for cut in cuts_sel.keys(): 
            if cuts_sel[cut]:
                cut_no = cut[-1]
                #Get values
                no_segm = getattr(self, 'sB_no_segm'+cut_no).value()
                obj_type = getattr(self, 'cB_obj_segm'+cut_no).currentText()
                no_obj = getattr(self, 'sB_segm_noObj'+cut_no).value()
                names_segm = getattr(self, 'names_segm'+cut_no).text()
                names_segm = split_str(names_segm)
                #Measure
                meas_vol = getattr(self, 'cB_volume_'+stype).isChecked()
                meas_area = getattr(self, 'cB_area_'+stype).isChecked()
                meas_ellip = getattr(self, 'cB_ellip_'+stype).isChecked()
                meas_angles = getattr(self, 'cB_angles_'+stype).isChecked()

                #Get names
                names_segmF = {}
                for dd in range(int(no_segm)): 
                    segm_no = 'segm'+str(dd+1)
                    names_segmF[segm_no] = names_segm[dd]
                
                #Get selected contours
                self.check_checkBoxes(self.ch_selected, 'segm')
                tiss_cut = []
                for btn in self.dict_segm.keys():
                    if 'Cut'+cut_no in btn:
                        if self.dict_segm[btn]: 
                            _,_,_,ch_s,cont_s = btn.split('_')
                            tiss_cut.append((ch_s,cont_s))
                
                ch_segments = {}
                chs_all = set([ch for (ch,_) in tiss_cut])
                for ch_a in chs_all:
                    list_ch = []
                    for ccc in tiss_cut:
                        if ch_a in ccc:
                            list_ch.append(ccc[1])
                    # print(list_ch)
                    ch_segments[ch_a] = list_ch

                dict_cut = {'no_segments': no_segm,
                            'obj_segm': obj_type,
                            'no_cuts_4segments': no_obj,
                            'name_segments': names_segmF,
                            'ch_segments': ch_segments}
                            
                segm_settings[cut] = dict_cut
                valid_all.append(True)

        # print('valid_all:', valid_all)
        segm_settings['measure'] = {'Vol': meas_vol, 'SA': meas_area, 'Ellip': meas_ellip, 'Angles': meas_angles}
        
        #Add parameters to segments
        selected_params = self.mH_user_params 
        if selected_params == None: 
            selected_params = {}
        #Add measure params from segments
        cuts = [key for key in segm_settings if 'Cut' in key]
        params_segm = [param for param in segm_settings['measure'].keys() if segm_settings['measure'][param]]
        for param_a in params_segm: 
            selected_params[param_a+'(segm)'] = {}
            for cut_a in cuts: 
                cut_semg = segm_settings[cut_a]['ch_segments']
                no_segm = segm_settings[cut_a]['no_segments']
                for ch_a in cut_semg: 
                    for cont_a in cut_semg[ch_a]:
                        for segm in range(1,no_segm+1,1):
                            selected_params[param_a+'(segm)'][cut_a+'_'+ch_a+'_'+cont_a+'_segm'+str(segm)] = True

        self.mH_user_params = selected_params
        self.mH_settings['segm'] = segm_settings
        if all(valid_all):
            self.button_set_segm.setChecked(True)
            self.win_msg('All good! Segments have been set.')
        else: 
            self.button_set_segm.setChecked(False)

        if self.set_segm_sect.isVisible(): 
            if self.button_set_segm.isChecked() and self.button_set_sect.isChecked():
                self.fill_segm_sect()
                self.tick_segm_sect_2.setEnabled(True)

    def set_sect_settings(self): 
        valid_all = []
        sect_settings = {'cutLayersIn2Sections': True}
        stype = 'sect'
        cuts_sel = {'Cut1': getattr(self, 'tick_'+stype+'1').isChecked(), 'Cut2':getattr(self, 'tick_'+stype+'2').isChecked()}
        for cut in cuts_sel.keys(): 
            if cuts_sel[cut]:
                cut_no = cut[-1]
                #Get values
                obj_type = getattr(self, 'cB_obj_sect'+cut_no).currentText()
                names_sect = getattr(self, 'names_sect'+cut_no).text()
                names_sect = split_str(names_sect)
                #Measure
                meas_vol = getattr(self, 'cB_volume_'+stype).isChecked()
                meas_area = getattr(self, 'cB_area_'+stype).isChecked()

                #Get names
                names_sectF = {}
                for dd in range(2): 
                    sect_no = 'sect'+str(dd+1)
                    names_sectF[sect_no] = names_sect[dd]
                
                #Get selected contours
                self.check_checkBoxes(self.ch_selected, 'sect')
                tiss_cut = []
                for btn in self.dict_sect.keys():
                    if 'Cut'+cut_no in btn:
                        if self.dict_sect[btn]: 
                            _,_,_,ch_s,cont_s = btn.split('_')
                            tiss_cut.append((ch_s,cont_s))
                
                ch_sections = {}
                chs_all = set([ch for (ch,_) in tiss_cut])
                for ch_a in chs_all:
                    list_ch = []
                    for ccc in tiss_cut:
                        if ch_a in ccc:
                            list_ch.append(ccc[1])
                    # print(list_ch)
                    ch_sections[ch_a] = list_ch

                dict_cut = {'no_sections': 2,
                            'obj_sect': obj_type,
                            'name_sections': names_sectF,
                            'ch_sections': ch_sections}
                            
                sect_settings[cut] = dict_cut
                valid_all.append(True)

        sect_settings['measure'] = {'Vol': meas_vol, 'SA': meas_area}

        #Add parameters to segments
        selected_params = self.mH_user_params 
        if selected_params == None: 
            selected_params = {}
        #Add measure params from sections
        cuts = [key for key in sect_settings if 'Cut' in key]
        params_sect = [param for param in sect_settings['measure'].keys() if sect_settings['measure'][param]]
        for param_b in params_sect: 
            selected_params[param_b+'(sect)'] = {}
            for cut_b in cuts: 
                cut_sect = sect_settings[cut_b]['ch_sections']
                no_sect = sect_settings[cut_b]['no_sections']
                for ch_b in cut_sect: 
                    for cont_b in cut_sect[ch_b]:    
                        for sect in range(1,no_sect+1,1):
                            selected_params[param_b+'(sect)'][cut_b+'_'+ch_b+'_'+cont_b+'_sect'+str(sect)] = True

        self.mH_user_params = selected_params
        self.mH_settings['sect'] = sect_settings
        # print('self.mH_settings (set_sect_settings):',self.mH_settings)
        if all(valid_all):
            self.button_set_sect.setChecked(True)
            self.win_msg('All good! Regions have been set.')
        else: 
            self.button_set_sect.setChecked(False)

        if self.set_segm_sect.isVisible(): 
            if self.button_set_segm.isChecked() and self.button_set_sect.isChecked():
                self.fill_segm_sect()
                self.tick_segm_sect_2.setEnabled(True)

    def set_segm_sect_settings(self): 
        valid_all = []
        segm_sect_settings = {'cutLayersIn2SegmSect': True}

        #Get selected contours
        for scut in ['sCut1', 'sCut2']:
            scut_list = [item for item in self.list_segm_sect if scut in item]
            if len(scut_list)> 0:
                segm_sect_settings[scut] = {}
                for rcut in ['_Cut1', '_Cut2']: 
                    rcut_list = [item for item in scut_list if rcut in item]
                    if len(rcut_list)> 0: 
                        segm_sect_settings[scut][rcut[1:]] = {'ch_segm_sect': []}
                        for cB_item in rcut_list: 
                            if getattr(self, cB_item).isChecked(): 
                                segm_sect_settings[scut][rcut[1:]]['ch_segm_sect'].append(cB_item[14:])
                    
        #Measure
        meas_vol = getattr(self, 'cB_volume_segm_sect').isChecked()
        meas_area = getattr(self, 'cB_area_segm_sect').isChecked()
        segm_sect_settings['measure'] = {'Vol': meas_vol, 'SA': meas_area}

        #Get segments and section settings
        segm_settings = self.mH_settings['segm']
        sect_settings = self.mH_settings['sect']

        #Add parameters to segments
        selected_params = self.mH_user_params 
        if selected_params == None: 
            selected_params = {}
        #Add measure params from sections
        cuts = [key for key in segm_sect_settings if 'sCut' in key]
        params_segm_sect = [param for param in segm_sect_settings['measure'].keys() if segm_sect_settings['measure'][param]]
        for param_c in params_segm_sect: 
            selected_params[param_c+'(segm-sect)'] = {}
            for cut_c in cuts: 
                no_segm = segm_settings[cut_c[1:]]['no_segments']
                for cut_r in segm_sect_settings[cut_c].keys():
                    no_sect = sect_settings[cut_r]['no_sections']
                    cut_segm_sect = segm_sect_settings[cut_c][cut_r]['ch_segm_sect']
                    print('cut_segm_sect:', cut_segm_sect)
                    for cut_ch_cont in cut_segm_sect: 
                        for segm in range(1,no_segm+1,1):
                            for sect in range(1,no_sect+1,1):
                                selected_params[param_c+'(segm-sect)'][cut_c+'_'+cut_r+'_'+cut_ch_cont+'_segm'+str(segm)+'_sect'+str(sect)] = True

        self.mH_user_params = selected_params
        self.mH_settings['segm-sect'] = segm_sect_settings
        print('self.mH_settings (segm_sect_settings):', self.mH_settings['segm-sect'])
    
        self.button_set_segm_sect.setChecked(True)
        self.win_msg('All good! Segment-Region Intersections have been set.')

    def open_sect_segm(self): 
        if self.tick_segm_sect_2.isChecked(): 
            self.widget_segm_sect.setVisible(True)
            self.mH_settings['segm-sect'] = True
        else: 
            self.mH_settings['segm-sect'] = False

    def fill_segm_sect(self): 
        if not self.tick_segm2.isChecked(): 
            bool_segm = False
        else: 
            bool_segm = True

        getattr(self, 'lab_segm2').setEnabled(bool_segm)
        for ch in ['ch1', 'ch2', 'ch3', 'ch4', 'chNS']:
            for cont in ['int', 'tiss', 'ext']:
                getattr(self, 'label_'+'sCut2'+'_'+ch).setEnabled(bool_segm)
                getattr(self, 'label_'+'sCut2'+'_'+ch+'_'+cont).setEnabled(bool_segm)
                for cut_sect in ['Cut1', 'Cut2']: #sections
                    getattr(self, 'cB_'+'sCut1'+'_'+cut_sect+'_'+ch+'_'+cont).setEnabled(False)
                    getattr(self, 'cB_'+'sCut2'+'_'+cut_sect+'_'+ch+'_'+cont).setEnabled(False)

        if not self.tick_sect2.isChecked():
            bool_sect = False
        else: 
            bool_sect = True

        for ch in ['ch1', 'ch2', 'ch3', 'ch4', 'chNS']:
            for cont in ['int', 'tiss', 'ext']:
                getattr(self, 'lab_sect2').setEnabled(bool_sect)

        list_segm = [key.split('cB_segm_')[1] for key in self.dict_segm.keys() if self.dict_segm[key]]
        list_sect = [key.split('cB_sect_')[1] for key in self.dict_sect.keys() if self.dict_sect[key]]

        self.list_segm_sect = []
        for scut in ['Cut1', 'Cut2']:
            list_segm_noCut = sorted(list(set([ch_cont[5:] for ch_cont in list_segm if scut in ch_cont])))
            print(scut,'- segm:', list_segm_noCut)
            for rcut in ['Cut1', 'Cut2']: 
                list_sect_noCut = sorted(list(set([ch_cont[5:] for ch_cont in list_sect if rcut in ch_cont])))
                print(rcut,'- sect:', list_sect_noCut)
                set_segm = set(list_segm_noCut)
                intersect = set_segm.intersection(set(list_sect_noCut))
                print('intersect:',intersect)
                for item in intersect: 
                    getattr(self, 'cB_s'+scut+'_'+rcut+'_'+item).setEnabled(True)
                    self.list_segm_sect.append('cB_s'+scut+'_'+rcut+'_'+item)

        print('self.list_segm_sect:',self.list_segm_sect)

    def validate_set_all(self): 
        print('\n\nValidating Project!')
        valid = []
        if self.mH_user_params != None and self.set_meas_param_all.isChecked():
            valid.append(True)
        else: 
            error_txt = '*You need to set the parameters you want to extract from the segmented tissues before creating the new project.'
            self.win_msg(error_txt, self.button_new_proj)
            return

        if self.checked('segm'): 
            if self.button_set_segm.isChecked():
                valid.append(True)
            else: 
                error_txt = '*You need to set segments settings before creating the new project.'
                self.win_msg(error_txt, self.button_new_proj)
                return
            
        if self.checked('sect'): 
            CL_meas = self.mH_user_params['CL']
            dict_CL = [CL_meas[key] for key in CL_meas.keys()]
            if all(not x for x in dict_CL):
                error_txt = '*To create region divisions, at least one centreline needs to be created. Go back to  -Set Measurement Parameters-  and select at least one centreline.'
                self.win_msg(error_txt, self.button_new_proj)
                return
            elif self.button_set_sect.isChecked():
                valid.append(True)
            else: 
                error_txt = '*You need to set sections settings before creating the new project.'
                self.win_msg(error_txt, self.button_new_proj)
                return
        
        if self.button_set_segm_sect.isChecked(): 
            valid.append(True)
        else: 
            error_txt = '*You need to set segment-region intersection settings before creating the new project.'
            self.win_msg(error_txt, self.button_new_proj)
            return

        if all(valid): 
            return True
        else: 
            print('Something wrong; validate_set_all')
            return False

    # -- Functions Set Measurement Parameters
    def check_to_set_params(self): 
        # print('self.mH_settings (check_to_set_params):',self.mH_settings)
        valid = []
        if self.button_set_orient.isChecked(): 
            valid.append(True)
        else: 
            error_txt = '*You need to set orientation settings first to set measurement parameters.'
            self.win_msg(error_txt, self.set_meas_param_all)
            return
        if self.button_set_initial_set.isChecked(): 
            valid.append(True)
        else: 
            error_txt = '*You need to set initial settings first to set measurement parameters.'
            self.win_msg(error_txt, self.set_meas_param_all)
            return
        if self.checked('chNS'): 
            if self.button_set_chNS.isChecked():
                valid.append(True)
            else: 
                error_txt = '*You need to set Channel NS settings first to set measurement parameters.'
                self.win_msg(error_txt, self.set_meas_param_all)
                return
            
        if all(valid): 
            return True
        
    # -- Tab general functions
    def tabChanged(self):
        print('Tab was changed to ', self.tabWidget.currentIndex())

    def check_template(self): 
        temp_dir = None
        if self.cB_proj_as_template.isChecked():
            line_temp = self.lineEdit_template_name.text()
            line_temp = line_temp.replace(' ', '_')
            temp_name = 'mH_'+line_temp+'_project.json'
            cwd = Path().absolute()
            dir_temp = cwd / 'db' / 'templates' / temp_name 
            if dir_temp.is_file():
                self.win_msg('*There is already a template with the selected name. Please give this template a new name.')
                return
            else: 
                print('New project template: ', dir_temp)
                temp_dir = dir_temp
        
        return temp_dir
    
    def save_as_template(self):
        if self.cB_proj_as_template.isChecked(): 
            self.lab_temp.setEnabled(True)
            self.lineEdit_template_name.setEnabled(True)

class SetMeasParam(QDialog):

    def __init__(self, mH_settings:dict, parent=None):
        super().__init__(parent)
        uic.loadUi('src/gui/ui/set_meas_screen.ui', self)
        self.setWindowTitle('Set Parameters to Measure...')
        self.setWindowTitle('Select the parameters to measure from the segmented channels...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.mH_settings = mH_settings
        self.parent = parent

        self.params = {0: {'s': 'SA', 'l':'Surface Area'},
                        1: {'s': 'Vol', 'l':'Volume'},
                        2: {'s': 'CL', 'l':'Centreline'},
                        3: {'s': 'th_i2e', 'l':'Thickness Heatmap (int>ext*)'},
                        4: {'s': 'th_e2i','l':'Thickness Heatmap (ext>int*)'}, 
                        5: {'s': 'ball','l':'Centreline>Tissue (Ballooning)'}}
        self.ball_param = 5
                
        ch_all = mH_settings['name_chs']
        if isinstance(mH_settings['chNS'], dict) and len(list(mH_settings['chNS'].keys()))>0:
            if mH_settings['chNS']['layer_btw_chs']:
                ch_all['chNS'] = mH_settings['chNS']['user_nsChName']
        self.ch_all = ch_all

        #Disable params
        self.disable_pars = {2: {'ch1': ['tiss'], 'ch2': ['tiss'], 'ch3': ['tiss'], 'ch4': ['tiss'], 'chNS': ['tiss']},#centreline
                             3: {'ch1': ['int', 'ext'],'ch2': ['int', 'ext'],'ch3': ['int', 'ext'],'ch4': ['int', 'ext'],'chNS': ['int', 'ext']}, #th_i2e
                             4: {'ch1': ['int', 'ext'],'ch2': ['int', 'ext'],'ch3': ['int', 'ext'],'ch4': ['int', 'ext'],'chNS': ['int', 'ext']}, #th_e2i
                             5: {'ch1': ['tiss'], 'ch2': ['tiss'], 'ch3': ['tiss'], 'ch4': ['tiss'], 'chNS': ['int','tiss','ext']}} #ball
        
        #Change names of unused params
        aa = 1
        for num in range(10): 
            if num >= len(self.params):
                getattr(self, 'lab_param'+str(num)).setText('User-Specific Param'+str(aa))
                aa+=1

        #Create table 
        self.set_meas_param_table()

        #Set radiobuttons options
        self.rB_continuous.toggled.connect(lambda: self.radio_button(opt ='continuous'))
        self.rB_continuous.opt = 'continuous'
        self.rB_categorical.toggled.connect(lambda: self.radio_button(opt ='categorical'))
        self.rB_categorical.opt = 'categorical'
        self.rB_descriptive.toggled.connect(lambda: self.radio_button(opt ='descriptive'))
        self.rB_descriptive.opt = 'descriptive'

        #Set validators
        self.reg_ex = QRegularExpression("[a-z-A-Z_ 0-9,]+")
        self.lineEdit_param_name.setValidator(QRegularExpressionValidator(self.reg_ex, self.lineEdit_param_name))
        self.reg_ex_no_spaces = QRegularExpression("[a-z-A-Z_0-9]+")
        self.lineEdit_param_abbr.setValidator(QRegularExpressionValidator(self.reg_ex_no_spaces, self.lineEdit_param_abbr))
        self.reg_ex_most = QRegularExpression("[a-z-A-Z_ 0-9,.:/+-]+")
        self.lineEdit_param_classes.setValidator(QRegularExpressionValidator(self.reg_ex_most, self.lineEdit_param_classes))

        #Buttons
        self.button_add_param.clicked.connect(lambda: self.add_user_param())

        #Parameters all
        self.lab_param0.clicked.connect(lambda: self.tick_all_param(0))
        self.lab_param1.clicked.connect(lambda: self.tick_all_param(1))
        self.lab_param2.clicked.connect(lambda: self.tick_all_param(2))
        self.lab_param3.clicked.connect(lambda: self.tick_all_param(3))
        self.lab_param4.clicked.connect(lambda: self.tick_all_param(4))
        self.lab_param5.clicked.connect(lambda: self.tick_all_param(5))
        self.lab_param6.clicked.connect(lambda: self.tick_all_param(6))
        self.lab_param7.clicked.connect(lambda: self.tick_all_param(7))
        self.lab_param8.clicked.connect(lambda: self.tick_all_param(8))
        self.lab_param9.clicked.connect(lambda: self.tick_all_param(9))

        #Param ballooning
        self.cB_ch1_int_param5.clicked.connect(lambda: self.settings_ballooning('ch1_int'))
        self.cB_ch1_ext_param5.clicked.connect(lambda: self.settings_ballooning('ch1_ext'))
        self.cB_ch2_int_param5.clicked.connect(lambda: self.settings_ballooning('ch2_int'))
        self.cB_ch2_ext_param5.clicked.connect(lambda: self.settings_ballooning('ch2_ext'))
        self.cB_ch3_int_param5.clicked.connect(lambda: self.settings_ballooning('ch3_int'))
        self.cB_ch3_ext_param5.clicked.connect(lambda: self.settings_ballooning('ch3_ext'))
        self.cB_ch4_int_param5.clicked.connect(lambda: self.settings_ballooning('ch4_int'))
        self.cB_ch4_ext_param5.clicked.connect(lambda: self.settings_ballooning('ch4_ext'))

        self.ballooning_to = ['--select--']
        self.set_ballooning_opt()
        self.setModal(True)

        #Heatmap 3d to 2d
        poss_chs = [ch for ch in self.ch_all.keys() if ch != 'chNS']
        hm_ch = getattr(self, 'hm_cB_ch')
        hm_ch.addItems(['--select--']+poss_chs)

        self.cB_hm3d2d.clicked.connect(lambda: self.heatmap3d2d())

    def win_msg(self, msg, btn=None): 
        if msg[0] == '*':
            self.tE_validate.setStyleSheet(error_style)
            msg = 'Error: '+msg
            alert('error_beep')
        elif msg[0] == '!':
            self.tE_validate.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            self.tE_validate.setStyleSheet(msg_style)
        self.tE_validate.setText(msg)

        if btn != None: 
            btn.setChecked(False)

    def radio_button(self, opt): 
        if getattr(self, 'rB_'+opt).isChecked(): 
            if opt == 'categorical': 
                self.lab_categories.setEnabled(True)
                self.lineEdit_param_classes.setEnabled(True)
            else: 
                self.lab_categories.setEnabled(False)
                self.lineEdit_param_classes.setEnabled(False)
                self.lineEdit_param_classes.clear()
        else: 
            pass

    def tick_all_param(self, num:int): 
        tick_o = getattr(self, 'lab_param'+str(num))
        if tick_o.isChecked(): 
            for ch_s in self.ch_all:
                for cont in ['int', 'tiss', 'ext']: 
                    cB = getattr(self, 'cB_'+ch_s+'_'+cont+'_param'+str(num))
                    if cB.isEnabled(): 
                        cB.setChecked(True)
                        if num == 5: 
                            self.settings_ballooning(name = ch_s+'_'+cont)
                cB_roi = getattr(self, 'cB_roi_param'+str(num))
                if num > 5: 
                    cB_roi.setChecked(True)
                    # else: 
                    #     print('Checkbox -'+'cB_'+ch_s+'_'+cont+'_param'+str(num)+ '- is disabled!')
        else: 
            for ch_s in self.ch_all:
                for cont in ['int', 'tiss', 'ext']: 
                    cB = getattr(self, 'cB_'+ch_s+'_'+cont+'_param'+str(num))
                    if cB.isEnabled(): 
                        cB.setChecked(False)
                        if num == 5: 
                            self.settings_ballooning(name = ch_s+'_'+cont)
                cB_roi = getattr(self, 'cB_roi_param'+str(num))
                if num > 5: 
                    cB_roi.setChecked(False)
                    # else: 
                    #     print('Checkbox -'+'cB_'+ch_s+'_'+cont+'_param'+str(num)+ '- is disabled!')

    def check_checkBoxes(self):
        if hasattr(self, 'dict_meas'):
            delattr(self, 'dict_meas')

        dict_meas = {}
        for ch in self.ch_all: 
            for cont in ['int', 'tiss', 'ext']: 
                for num in range(10): 
                    if num < len(self.params):
                        btn_name = 'cB_'+ch+'_'+cont+'_param'+str(num)
                        # print(btn_name, getattr(self, btn_name).isChecked())
                        dict_meas[btn_name] = getattr(self, btn_name).isChecked()

        for num in range(6,10,1):
            if num < len(self.params):
                btn_name = 'cB_roi_param'+str(num)
                # print(btn_name, getattr(self, btn_name).isChecked())
                dict_meas[btn_name] = getattr(self, btn_name).isChecked()

        setattr(self, 'dict_meas', dict_meas)
        # print('self.dict_meas:',self.dict_meas)

    def set_meas_param_table(self): 
        #Set Measurement Parameters
        for key in self.params.keys():
            getattr(self, 'lab_param'+str(key)).setEnabled(True)
            getattr(self, 'lab_param'+str(key)).setText(self.params[key]['l'])
        
        # print(len(self.params),'---', self.params)
        for ch in ['ch1', 'ch2', 'ch3', 'ch4', 'chNS']: 
            if ch in self.ch_all: 
                getattr(self, 'label_'+ch).setText(self.ch_all[ch])
                for num in range(10): 
                    if num < len(self.params):
                        for cont in ['int', 'tiss', 'ext']:
                            getattr(self, 'cB_'+ch+'_'+cont+'_param'+str(num)).setEnabled(True)
                    else: 
                        getattr(self, 'lab_param'+str(num)).setEnabled(False)
                        for cont in ['int', 'tiss', 'ext']:
                            getattr(self, 'cB_'+ch+'_'+cont+'_param'+str(num)).setEnabled(False)
            else:
                getattr(self, 'label_'+ch).setVisible(False)   
                getattr(self, 'label_'+ch+'_2').setVisible(False)    
                for cont in ['int', 'tiss', 'ext']:
                    getattr(self, 'label_'+ch+'_'+cont).setVisible(False)
                for num in range(10): 
                    for cont in ['int', 'tiss', 'ext']:
                        getattr(self, 'cB_'+ch+'_'+cont+'_param'+str(num)).setVisible(False)

        for num in range(6,10,1):
            if num < len(self.params):
                getattr(self, 'cB_roi_param'+str(num)).setEnabled(True)
            else: 
                getattr(self, 'cB_roi_param'+str(num)).setEnabled(False)

        #Disable parameters
        for pars in self.disable_pars:
            for chn in self.disable_pars[pars]: 
                for cont in self.disable_pars[pars][chn]:
                    cB_name = 'cB_'+chn+'_'+cont+'_param'+str(pars)
                    cB = getattr(self, cB_name)
                    cB.setDisabled(True)

        self.check_checkBoxes()
        # print(getattr(self, 'dict_meas'))

    def add_user_param(self):
        valid = []; error_txt = ''
        param_name = self.lineEdit_param_name.text()
        param_abbr = self.lineEdit_param_abbr.text()
        param_desc = self.textEdit_param_desc.toPlainText()
        param_type = [getattr(self, 'rB_'+opt).opt for opt in ['descriptive', 'continuous', 'categorical'] if getattr(self, 'rB_'+opt).isChecked()]
        param_categ = self.lineEdit_param_classes.text()

        if len(param_name)<5: 
            error_txt = "*Parameter's name needs have at least five (5) characters."
            self.win_msg(error_txt, self.button_add_param)
            return
        elif validate_txt(param_name) != None:
            error_txt = "*Please avoid using invalid characters in the parameter's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt, self.button_add_param)
            return
        else: 
            valid.append(True)
        
        if len(param_abbr)<3: 
            error_txt = "*Parameter's abbreviation needs to have between 3 and 12 characters."
            self.win_msg(error_txt, self.button_add_param)
            return
        elif validate_txt(param_abbr) != None:
            error_txt = "*Please avoid using invalid characters in the parameter's abbreviation e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt, self.button_add_param)
            return
        else: 
            valid.append(True)
            param_abbr_line = param_abbr.replace(' ', '_')
        
        if self.rB_categorical.isChecked(): 
            try: 
                param_categs = split_str(param_categ)
                valid.append(True)
            except: 
                error_txt = "*Please check the values introduced in Parameter Classes."
                self.win_msg(error_txt, self.button_add_param)
                return
        else: 
            param_categs = []
            valid.append(True)
        
        if all(valid):
            param_num = len(self.params)
            self.params[param_num]={'s': param_abbr_line, 'l': param_name, 
                                        'description': param_desc, 'type': param_type[0], 'categories': param_categs}
            # print(self.params)
            self.set_meas_param_table()
            self.win_msg("New parameter '"+param_name+"' has been added! Now select the tissues from which you would like to measure this new parameter.")
            param_name = self.lineEdit_param_name.clear()
            param_abbr = self.lineEdit_param_abbr.clear()
            param_desc = self.textEdit_param_desc.clear()
            param_categ = self.lineEdit_param_classes.clear()
        
    def set_ballooning_opt(self):
        for opt in range(1,5,1):
            label_bal = getattr(self, 'label_bal'+str(opt))
            name_bal = getattr(self, 'cB_balto'+str(opt))
            ch_bal = getattr(self, 'cB_ch_bal'+str(opt))
            cont_bal = getattr(self, 'cB_cont_bal'+str(opt))

            label_bal.setEnabled(True)
            name_bal.setEnabled(True)
            name_bal.addItems(self.ballooning_to)
            poss_chs = [ch for ch in self.ch_all.keys() if ch != 'chNS']
            ch_bal.setEnabled(True)
            ch_bal.addItems(['--select--']+poss_chs)
            cont_bal.setEnabled(True)

    def settings_ballooning(self, name): 
        # print('settings_ballooning:'+name)
        ch_to, cont_to = name.split('_') 
        label_name = self.ch_all[ch_to]+' ('+ch_to+')'+'-'+cont_to
        if getattr(self, 'cB_'+name+'_param5').isChecked(): 
            self.ballooning_to.append(label_name)
        else: 
            if label_name in self.ballooning_to:
                self.ballooning_to.remove(label_name)
            else:
                pass

        for but in ['cB_balto1', 'cB_balto2', 'cB_balto3', 'cB_balto4']:
            self.ballooning_to = list(set(self.ballooning_to))
            cB_but = getattr(self, but)
            cB_but.clear()
            cB_but.addItems(self.ballooning_to)
            cB_but.setCurrentText('--select--')
                
    def heatmap3d2d(self): 
        if self.cB_hm3d2d.isChecked():
            value = True
        else: 
            value = False

        self.hm_text.setEnabled(value)
        self.hm_lab_ch.setEnabled(value)
        self.hm_lab_cont.setEnabled(value)
        self.hm_cB_ch.setEnabled(value)
        self.hm_cB_cont.setEnabled(value)

    def validate_params(self): 
        valid = []
        #First validate the ballooning options
        #-- Get checkboxes info
        cB_checked = {}
        for cha in self.ch_all:
            for conta in ['int', 'ext']: 
                chcb = getattr(self, 'cB_'+cha+'_'+conta+'_param5')
                if chcb.isEnabled() and chcb.isChecked():
                    cB_checked[cha+'_'+conta] = True

        #-- Get settings
        names = {}; 
        for opt in range(1,5,1):
            name_bal = getattr(self, 'cB_balto'+str(opt)).currentText()
            ch_bal = getattr(self, 'cB_ch_bal'+str(opt)).currentText() != '--select--'
            cont_bal = getattr(self, 'cB_cont_bal'+str(opt)).currentText() != '--select--'
            if name_bal != '--select--': 
                aaa = name_bal.split('(')[1]
                bbb = aaa.split('-')
                ch_s = bbb[0].split(')')[0]
                cont_s = bbb[1]
                names[ch_s+'_'+cont_s] = {'ch': ch_bal, 
                                          'cont': cont_bal}
        
        #Now double check them 
        if set(list(cB_checked.keys())) != set(list(names.keys())):
            diff = set(list(cB_checked.keys())) - set(list(names.keys()))
            error_txt = "*You have not selected the centreline to use for "+str(diff)
            self.win_msg(error_txt, self.button_set_params)
            return 
        else: 
            for name in names: 
                if not names[name]['ch']: 
                    error_txt = "*You have not selected the channel centreline to use for "+name
                    self.win_msg(error_txt, self.button_set_params)
                    return 
                elif not names[name]['cont']: 
                    error_txt = "*You have not selected the contour type centreline to use for "+name
                    self.win_msg(error_txt, self.button_set_params)
                    return 
                else: 
                    valid.append(True)

        for opt in range(1,5,1):
            name_bal = getattr(self, 'cB_balto'+str(opt)).currentText()
            if name_bal != '--select--': 
                cl_ch = getattr(self, 'cB_ch_bal'+str(opt)).currentText()
                cl_cont = getattr(self, 'cB_cont_bal'+str(opt)).currentText()
                
                cB_name = 'cB_'+cl_ch+'_'+cl_cont[0:3]+'_param2'
                cB_cl = getattr(self, cB_name)
                if cB_cl.isChecked():
                    pass
                else: 
                    cB_cl.setChecked(True)
        
        #Validate centreline to do hm 3D to 2D
        if self.cB_hm3d2d.isChecked():
            hm_ch = getattr(self, 'hm_cB_ch').currentText()
            hm_cont = getattr(self, 'hm_cB_cont').currentText()
            if hm_ch == '--select--':
                error_txt = "*You have not selected the channel centreline to use to unloop and unfold the 3D heatmaps into 2D"
                self.win_msg(error_txt, self.button_set_params)
                return 
            elif hm_cont == '--select--':
                error_txt = "*You have not selected the contour type centreline to use to unloop and unfold the 3D heatmaps into 2D"
                self.win_msg(error_txt, self.button_set_params)
                return
            else: 
                 #Check the selected centreline
                cB_hm = getattr(self, 'cB_'+hm_ch+'_'+hm_cont[0:3]+'_param2')
                if cB_hm.isChecked():
                    pass
                else: 
                    cB_hm.setChecked(True)
                valid.append(True)
        else: 
            valid.append(True)
        
        #Check all checkboxes
        self.check_checkBoxes()
        bool_cB = [val for (_,val) in self.dict_meas.items()]
        if any(bool_cB): 
            valid.append(True)
        else: 
            print('Looopppp!')
            valid.append(self.check_meas_param())

        if all(valid): 
            self.win_msg('All done setting measurement parameters!')
            self.get_parameters()
            return True
        else: 
            return False
        
    def check_meas_param(self): #to finish!
        title = 'No measurement parameter selected!'
        msg = "You have not selected any measurement parameters to obtain from the segmented channels. If you want to go back and select some measurement parameters, press 'Cancel', else if you are happy with this decision press 'OK'."
        self.prompt = Prompt_ok_cancel(title, msg, parent=self.parent)
        self.prompt.exec()
        print('output:',self.prompt.output, '\n')

        if self.prompt.output == True: 
            return True
        else: 
            error_txt = "Select measurement parameters for the channel-contours."
            self.win_msg(error_txt, self.button_set_params)
            return False
    
    def get_parameters(self): 
        ballooning = {}
        for opt in range(1,5,1):
            name_bal = getattr(self, 'cB_balto'+str(opt)).currentText()
            if name_bal != '--select--': 
                aaa = name_bal.split('(')[1]; bbb = aaa.split('-')
                ch_to = bbb[0].split(')')[0]
                cont_to = bbb[1]

                cl_ch = getattr(self, 'cB_ch_bal'+str(opt)).currentText()
                cl_cont = getattr(self, 'cB_cont_bal'+str(opt)).currentText()
                # print('Opt'+str(opt)+':'+name_bal, cl_ch, cl_cont)

                ballooning[opt] = {'to_mesh': ch_to, 
                                    'to_mesh_type': cont_to, 
                                    'from_cl': cl_ch,
                                    'from_cl_type': cl_cont[0:3]}

        hm3d2d = {}
        if self.cB_hm3d2d.isChecked():
            hm3d2d['ch'] = getattr(self, 'hm_cB_ch').currentText()
            hm3d2d['cont'] = getattr(self, 'hm_cB_cont').currentText()

                
        centreline = {'looped_length': getattr(self, 'cB_cl_LoopLen').isChecked(),
                        'linear_length': getattr(self, 'cB_cl_LinLen').isChecked()}
        
        self.final_params = {'ballooning': ballooning, 
                             'centreline': centreline, 
                             'hm3d2d': hm3d2d}
        # print('self.final_params:',self.final_params)

class NewOrgan(QDialog):

    def __init__(self, proj, parent=None):
        super().__init__()
        uic.loadUi('src/gui/ui/create_organ_screen.ui', self)
        self.setWindowTitle('Create New Organ...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))

        now = QDate.currentDate()
        self.dateEdit.setDate(now)
        #Initialise variables 
        self.img_dirs = {}
        self.set_project_info(proj)

        self.cB_strain.currentIndexChanged.connect(lambda: self.custom_data(name='strain', gui_name='Strain'))
        self.cB_stage.currentIndexChanged.connect(lambda: self.custom_data(name='stage', gui_name='Stage'))
        self.cB_genotype.currentIndexChanged.connect(lambda: self.custom_data(name='genotype', gui_name = 'Genotype'))
        self.cB_manipulation.currentIndexChanged.connect(lambda: self.custom_data(name='manipulation', gui_name = 'Manipulation'))
        self.cB_stack_orient.currentIndexChanged.connect(lambda: self.custom_data(name='stack_orient', gui_name = 'Imaging Orientation'))

        #Set validators for the scaling values
        reg_ex = QRegularExpression(r"[+]?((\d+(\.\d*)?)|(\.\d+))([^a-d,f-z,A-D,F-Z][+-]?\d+)?")
        scaling_validator_x = QRegularExpressionValidator(reg_ex, self.scaling_x)
        self.scaling_x.setValidator(scaling_validator_x)
        scaling_validator_y = QRegularExpressionValidator(reg_ex, self.scaling_y)
        self.scaling_y.setValidator(scaling_validator_y)
        scaling_validator_z = QRegularExpressionValidator(reg_ex, self.scaling_z)
        self.scaling_z.setValidator(scaling_validator_z)
        # Custom angle
        reg_ex_angle = QRegularExpression( r"[+-]?((\d+(\.\d*)?)|(\.\d+))?")
        cust_angle_validator = QRegularExpressionValidator(reg_ex_angle, self.cust_angle)
        self.cust_angle.setValidator(cust_angle_validator)

        #Select files
        self.browse_ch1.clicked.connect(lambda: self.get_file('ch1'))
        self.browse_ch2.clicked.connect(lambda: self.get_file('ch2'))
        self.browse_ch3.clicked.connect(lambda: self.get_file('ch3'))
        self.browse_ch4.clicked.connect(lambda: self.get_file('ch4'))

        self.browse_mask_ch1.clicked.connect(lambda: self.get_file_mask('ch1'))
        self.browse_mask_ch2.clicked.connect(lambda: self.get_file_mask('ch2'))
        self.browse_mask_ch3.clicked.connect(lambda: self.get_file_mask('ch3'))
        self.browse_mask_ch4.clicked.connect(lambda: self.get_file_mask('ch4'))

    def win_msg(self, msg, btn=None): 
        if msg[0] == '*':
            self.tE_validate.setStyleSheet(error_style)
            msg = 'Error: '+msg
            alert('error_beep')
        elif msg[0] == '!':
            self.tE_validate.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            self.tE_validate.setStyleSheet(msg_style)
        self.tE_validate.setText(msg)

        if btn != None: 
            btn.setChecked(False)

    def set_project_info(self, proj):

        if proj.analysis['morphoHeart']: 
            self.tab_mHeart.setEnabled(True)
            self.tab_mHeart.setVisible(True)
        else: 
            self.tab_mHeart.setEnabled(False)
            self.tab_mHeart.setVisible(False)

        if proj.analysis['morphoCell']: 
            self.tab_mCell.setEnabled(True)
            self.tab_mCell.setVisible(True)
        else: 
            self.tab_mCell.setEnabled(False)  
            self.tab_mCell.setVisible(False)

        self.lab_filled_proj_name.setText(proj.info['user_projName'])
        self.lab_filled_ref_notes.setText(proj.info['user_projNotes'])
        self.lab_filled_proj_dir.setText(str(proj.dir_proj))

        self.cB_strain.clear()
        strain_it = list(['--select--']+proj.gui_custom_data['strain']+['add'])
        self.cB_strain.addItems(strain_it)
        self.cB_stage.clear()
        stage_it = list(['--select--']+proj.gui_custom_data['stage']+['add'])
        self.cB_stage.addItems(stage_it)
        self.cB_genotype.clear()
        genot_it = list(['--select--']+proj.gui_custom_data['genotype']+['add'])
        self.cB_genotype.addItems(genot_it)
        self.cB_manipulation.clear()
        manip_it = list(['--select--', 'None']+proj.gui_custom_data['manipulation']+['add'])
        self.cB_manipulation.addItems(manip_it)
        self.cB_stack_orient.clear()
        imOr_it = list(['--select--']+proj.gui_custom_data['im_orientation']+['add'])
        self.cB_stack_orient.addItems(imOr_it)
        self.cB_units.clear()
        units_it = list(['--select--']+proj.gui_custom_data['im_res_units']+['add'])
        self.cB_units.addItems(units_it)

        #Change channels
        mH_channels = proj.mH_channels
        for ch in ['ch1', 'ch2', 'ch3', 'ch4']: 
            label = getattr(self, 'lab_'+ch) 
            name = getattr(self, 'lab_filled_name_'+ch)
            brw_ch = getattr(self, 'browse_'+ch)
            dir_ch = getattr(self, 'lab_filled_dir_'+ch)
            check_ch = getattr(self, 'check_'+ch)
            brw_mk = getattr(self, 'browse_mask_'+ch)
            dir_mk = getattr(self, 'lab_filled_dir_mask_'+ch)
            check_mk = getattr(self, 'check_mask_'+ch)
            if ch not in mH_channels.keys():
                label.setVisible(False)
                name.setVisible(False)
                brw_ch.setVisible(False)
                dir_ch.setVisible(False)
                check_ch.setVisible(False)
                brw_mk.setVisible(False)
                dir_mk.setVisible(False)
                check_mk.setVisible(False)
            else: 
                name.setText(proj.mH_channels[ch])
                if not proj.mH_settings['setup']['mask_ch'][ch]:
                    brw_mk.setEnabled(False)
                    dir_mk.setEnabled(False)
                    check_mk.setEnabled(False)
                self.img_dirs[ch] = {}
    
    def custom_data(self, name:str, gui_name:str):
        user_data = getattr(self,'cB_'+name).currentText()
        if name == 'stack_orient': 
            self.lab_custom_angle.setEnabled(True)
            self.cust_angle.setEnabled(True)
        else: 
            pass

        if user_data == 'add':
            if name == 'stack_orient': 
                self.lab_custom_angle.setEnabled(True)
                self.cust_angle.setEnabled(True)

            msg = "Provide the '"+gui_name.upper()+"' of the organ being created."
            title = 'Custom '+gui_name.title()
            self.prompt = Prompt_user_input(msg = msg, title = title, info = name, parent = self)
        else: 
            pass 

    def validate_organ(self, proj):
        valid = []; error_txt = ''
        #Check the name is unique within the project
        organ_folder = self.lineEdit_organ_name.text()
        organ_dir = Path(proj.dir_proj) / organ_folder 
        if organ_dir.is_dir(): 
            error_txt = '*There is already an organ within this project with the same name. Please give this organ a new name to continue.'
            self.win_msg(error_txt, self.button_create_new_organ)
            return
        else: 
            valid.append(True)

        #Get organ name
        if len(self.lineEdit_organ_name.text())<5:
            error_txt = '*Organ name needs to be longer than five (5) characters'
            self.win_msg(error_txt, self.button_create_new_organ)
            return
        elif validate_txt(self.lineEdit_organ_name.text()) != None:
            error_txt = "*Please avoid using invalid characters in the project's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt, self.button_create_new_organ)
            return
        else: 
            self.organ_name = self.lineEdit_organ_name.text()
            valid.append(True)
        
        #Get Strain, stage and genotype
        for name in ['strain', 'stage', 'genotype', 'manipulation','stack_orient', 'units']:
            cB_data = getattr(self, 'cB_'+name).currentText()
            if cB_data == '--select--':
                error_txt = "*Please select the organ's "+name.upper()+"."
                self.win_msg(error_txt, self.button_create_new_organ)
                return
            else: 
                setattr(self, name, cB_data)
                valid.append(True)

        if self.cB_stack_orient.currentText() == 'custom':
            if len(self.cust_angle.text()) == 0: 
                error_txt = "*Please input custom angle for imaging orientation."
                self.win_msg(error_txt, self.button_create_new_organ)
                return
            else: 
                valid.append(True)
        else: 
            valid.append(True)

        #Get scaling
        valid_axis = []
        for axis in ['x', 'y', 'z']:
            scaling = getattr(self, 'scaling_'+axis)
            if scaling == '': 
                error_txt = "*Please enter the scaling value for "+axis+"."
                self.win_msg(error_txt, self.button_create_new_organ)
                return
            else: 
                valid_axis.append(True)

        if all(valid_axis): 
            self.set_resolution()
            valid.append(True)
        
        if all(valid):
            self.win_msg('All good. Continue setting up new organ.') 
            return True   
        else: 
            return False
        
    def set_resolution(self): 
        resolution = {}
        units = getattr(self, 'cB_units').currentText()
        for axis in ['x', 'y', 'z']:
            res = getattr(self, 'scaling_'+axis).text()
            resolution[axis] = {'scaling': float(res), 'units': units}
        self.resolution = resolution
        # print('resolution: ', self.resolution)

    def get_file(self, ch):
        self.win_msg('Loading '+ch+'... Wait for the indicator to turn green, then continue.')
        btn_file = getattr(self, 'browse_'+ch)
        title = 'Import images for '+ch
        if hasattr(self, 'user_dir'):
            cwd = self.user_dir
        else: 
            cwd = Path().absolute()
        file_name, _ = QFileDialog.getOpenFileName(self, title, str(cwd), "Image Files (*.tif)")
        if Path(file_name).is_file(): 
            label = getattr(self, 'lab_filled_dir_'+ch)
            label.setText(str(file_name))
            check = getattr(self, 'check_'+ch)
            check.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(0, 255, 0); color: rgb(0, 255, 0); font: 25 2pt 'Calibri Light'")
            check.setText('Done')
            images_o = io.imread(str(file_name))
            #Save files img_dirs
            self.img_dirs[ch]['image'] = {}
            self.img_dirs[ch]['image']['dir'] = Path(file_name)
            self.img_dirs[ch]['image']['shape'] = images_o.shape
            self.user_dir = Path(file_name).parent
            getattr(self, 'browse_'+ch).setChecked(True)
        else: 
            error_txt = '*Something went wrong importing the images for '+ch+'. Please try again.'
            self.win_msg(error_txt, getattr(self, 'browse_'+ch))
            return

        btn_file.setChecked(True)

    def get_file_mask(self, ch):
        self.win_msg('Loading mask for '+ch+'... Wait for the indicator to turn green, then continue.')
        btn_file = getattr(self, 'browse_mask_'+ch)
        if 'image' not in self.img_dirs[ch].keys(): 
            error_txt = '*Please select first the images for '+ch+', then select their corresponding mask.'
            self.win_msg(error_txt, getattr(self, 'browse_mask_'+ch))
            return
        else: 
            title = 'Import mask images for '+ch
            if hasattr(self, 'user_dir'):
                cwd = self.user_dir
            else: 
                cwd = Path().absolute()
            file_name, _ = QFileDialog.getOpenFileName(self, title, str(cwd), 'Image Files (*.tif)')
            if Path(file_name).is_file(): 
                label = getattr(self, 'lab_filled_dir_mask_'+ch)
                label.setText(str(file_name))
                check = getattr(self, 'check_mask_'+ch)
                mask_o = io.imread(str(file_name))
                if mask_o.shape != self.img_dirs[ch]['image']['shape']:
                    error_txt = '*The mask selected does not match the shape of the selected images (image shape: '+self.img_dirs[ch]['image']['shape']+', mask shape: '+mask_o.shape+'). Check and try again.'
                    self.win_msg(error_txt, getattr(self, 'browse_mask_'+ch))
                    return
                else: 
                    self.img_dirs[ch]['mask'] = {}
                    self.img_dirs[ch]['mask']['dir'] = Path(file_name)
                    self.img_dirs[ch]['mask']['shape'] = mask_o.shape
                    check.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(0, 255, 0); color: rgb(0, 255, 0); font: 25 2pt 'Calibri Light'")
                    check.setText('Done')
                    getattr(self, 'browse_mask_'+ch).setChecked(True)
            else: 
                error_txt = '*Something went wrong importing the mask images for '+ch+'. Please try again.'
                self.win_msg(error_txt, getattr(self, 'browse_mask_'+ch))
                return
                
        btn_file.setChecked(True)

    def check_selection(self, proj): 
        paths_chs = []
        paths = []
        for ch in proj.mH_channels.keys():
            if ch != 'chNS': 
                paths_chs.append(self.img_dirs[ch]['image']['dir'])
                paths.append(self.img_dirs[ch]['image']['dir'])
                if proj.mH_settings['setup']['mask_ch'][ch]: 
                    paths.append(self.img_dirs[ch]['mask']['dir'])
            else: 
                pass
        valid = [val.is_file() for val in paths]
        set_paths_chs = set(paths_chs)
        # print('Valid checking channel selection: ', valid)
        if not all(valid): 
            error_txt = "*Please load the images (and masks) for all the organ's channels."
            self.win_msg(error_txt, self.button_create_new_organ)
            return
        elif len(set_paths_chs) != len(paths_chs):
            error_txt = "*The image files loaded for each channel needs to be different. Please check and retry."
            self.win_msg(error_txt, self.button_create_new_organ)
            for ch in proj.mH_channels.keys():
                getattr(self, 'browse_'+ch).setChecked(False)
                getattr(self, 'lab_filled_dir_'+ch).clear()
                check_ch = getattr(self, 'check_'+ch)
                check_ch.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); color: rgb(0, 255, 0); font: 25 2pt 'Calibri Light'")
                check_ch.setText('')
            return
        else: 
            return True

    def check_shapes(self, proj): 
        shapes = []
        for ch in self.img_dirs:
            for im in ['image','mask']: 
                if im in self.img_dirs[ch].keys():
                    shapes.append(self.img_dirs[ch][im]['shape'])

        if len(set(shapes)) == 1: 
            print('All files have same shape!')
            #Remove shapes keys from the img_dict
            flat_im_dirs = flatdict.FlatDict(self.img_dirs)
            for key in flat_im_dirs:
                if 'shape' in key: 
                    flat_im_dirs.pop(key, None)
            self.img_dirs = flat_im_dirs.as_dict()
            print('img_dirs:', self.img_dirs)
            return True
        else:
            error_txt = '*The shape of all the selected images do not match. Check and try again.'
            self.win_msg(error_txt, self.button_create_new_organ)
            for ch in proj.mH_channels: 
                if ch != 'chNS':
                    bws_ch = getattr(self,'browse_'+ch)
                    bws_ch.setChecked(False)
                    label = getattr(self, 'lab_filled_dir_'+ch)
                    label.clear()
                    check_ch = getattr(self, 'check_'+ch)
                    check_ch.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
                    check_ch.clear()
                    bws_mk = getattr(self, 'browse_mask_'+ch) 
                    bws_mk.setChecked(False)
                    label_mk = getattr(self,'lab_filled_dir_mask_'+ch)
                    label_mk.clear()
                    check_mk = getattr(self,'check_mask_'+ch)
                    check_mk.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
                    check_mk.clear()
            return False

class LoadProj(QDialog):

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('src/gui/ui/load_project_screen.ui', self)
        self.setWindowTitle('Load Existing Project...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.proj = None
        self.organ_selected = None
        self.organ_checkboxes = None

        #Buttons
        self.button_load_organs.clicked.connect(lambda: self.load_proj_organs(proj = self.proj))

        #Blind analysis
        self.cB_blind.stateChanged.connect(lambda: self.reload_table())

    def win_msg(self, msg, btn=None): 
        if msg[0] == '*':
            self.tE_validate.setStyleSheet(error_style)
            msg = 'Error: '+msg
            alert('error_beep')
        elif msg[0] == '!':
            self.tE_validate.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            self.tE_validate.setStyleSheet(msg_style)
        self.tE_validate.setText(msg)

        if btn != None: 
            btn.setChecked(False)

    
    def fill_proj_info(self, proj):

        self.lineEdit_proj_name.setText(proj.info['user_projName'])
        self.textEdit_ref_notes.setText(proj.info['user_projNotes'])
        self.lab_filled_proj_dir.setText(str(proj.dir_proj))

        if proj.analysis['morphoHeart']:
            self.checkBox_mH.setChecked(True)
        if proj.analysis['morphoCell']:
            self.checkBox_mC.setChecked(True)
        if proj.analysis['morphoPlot']:
            self.checkBox_mP.setChecked(True)

        date = proj.info['date_created']
        date_qt = QDate.fromString(date, "yyyy-MM-dd")
        self.dateEdit.setDate(date_qt)
        self.win_msg('Project "'+proj.info['user_projName']+'" was successfully loaded!')
        self.button_browse_proj.setChecked(True)
    
    def get_proj_wf(self, proj): 
        flat_wf = flatdict.FlatDict(copy.deepcopy(proj.workflow))
        keep_keys = [key for key in flat_wf.keys() if len(key.split(':'))== 4 and 'Status' in key]
        # print('flat_wf.keys():', flat_wf.keys())
        for key in flat_wf.keys(): 
            if key not in keep_keys: 
                flat_wf.pop(key, None)
        out_dict = flat_wf.as_dict()
        for keyi in out_dict: 
            if isinstance(out_dict[keyi], flatdict.FlatDict):
                out_dict[keyi] = out_dict[keyi].as_dict()

        return flatdict.FlatDict(out_dict)
    
    def load_proj_organs(self, proj):
        #https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/
        #https://www.pythonguis.com/faq/qtablewidget-for-list-of-dict/
        if self.button_browse_proj.isChecked(): 
            if len(proj.organs) > 0: 
                cBs = []
                self.tabW_select_organ.clear()
                wf_flat = self.get_proj_wf(proj)
                blind = self.cB_blind.isChecked()
                self.tabW_select_organ.setRowCount(len(proj.organs)+2)
                keys = {'-':['select'],'Name': ['user_organName'], 'Notes': ['user_organNotes'], 'Strain': ['strain'], 'Stage': ['stage'], 
                        'Genotype':['genotype'], 'Manipulation': ['manipulation']}
                if blind:
                    keys.pop('Genotype', None); keys.pop('Manipulation', None) 
                name_keys = list(range(len(keys)))

                keys_wf = {}
                for wf_key in wf_flat.keys():
                    nn,proc,sp,_ = wf_key.split(':')
                    keys_wf[sp] = ['workflow']+wf_key.split(':')
                
                # Workflow
                # - Get morphoHeart Labels
                mH_keys = [num+len(name_keys) for num, key in enumerate(list(keys_wf.keys())) if 'morphoHeart' in keys_wf[key]]
                # - Get morphoCell Labels
                mC_keys = [num+len(name_keys)+len(mH_keys) for num, key in enumerate(list(keys_wf.keys())) if 'morphoCell' in keys_wf[key]]

                #Changing big and small labels: 
                big_labels = ['General Info']
                index_big = [0]
                len_ind_big = [len(keys)]
                if len(mH_keys)>0:
                    index_big.append(mH_keys[0]); big_labels.append('morphoHeart'); len_ind_big.append(len(mH_keys))
                if len(mC_keys)>0:
                    index_big.append(mC_keys[0]); big_labels.append('morphoCell'); len_ind_big.append(len(mC_keys))       

                self.tabW_select_organ.setColumnCount(len(name_keys)+len(mH_keys)+len(mC_keys))
                all_labels = keys |  keys_wf
                aa = 0
                for col in range(len(name_keys)+len(mH_keys)+len(mC_keys)):
                    if col in index_big:
                        self.tabW_select_organ.setSpan(0,col,1,len_ind_big[aa])
                        item = QTableWidgetItem(big_labels[aa])
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
                        self.tabW_select_organ.setItem(0,col, item)
                        aa+= 1
                    itemf = QTableWidgetItem(list(all_labels.keys())[col])
                    itemf.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
                    self.tabW_select_organ.setItem(1,col, itemf)

                #Adding organs to table
                row = 2
                for organ in proj.organs:
                    col = 0        
                    for nn, key in all_labels.items(): 
                        if len(key) == 1 and nn == '-': 
                            widget   = QWidget()
                            checkbox = QCheckBox()
                            checkbox.setChecked(False)
                            checkbox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
                            checkbox.setMinimumSize(QtCore.QSize(15, 20))
                            checkbox.setMaximumSize(QtCore.QSize(15, 20))
                            layoutH = QHBoxLayout(widget)
                            layoutH.addWidget(checkbox)
                            layoutH.setContentsMargins(0, 0, 0, 0)
                            self.tabW_select_organ.setCellWidget(row, 0, widget)
                            cB_name = 'cB_'+proj.organs[organ]['user_organName']
                            setattr(self, cB_name, checkbox)
                            cBs.append(cB_name)
                        elif 'workflow' not in key: 
                            item = QTableWidgetItem(get_by_path(proj.organs[organ],key))
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
                            self.tabW_select_organ.setItem(row,col, item)
                        else: 
                            widget   = QWidget()
                            layoutH = QHBoxLayout(widget)
                            color_status = QLineEdit()
                            color_status.setEnabled(True)
                            color_status.setMinimumSize(QtCore.QSize(15, 15))
                            color_status.setMaximumSize(QtCore.QSize(15, 15))
                            color_status.setStyleSheet("border-color: rgb(0, 0, 0);")
                            color_status.setReadOnly(True)
                            layoutH.addWidget(color_status)
                            layoutH.setContentsMargins(0, 0, 0, 0)
                            update_status(proj.organs[organ], key, color_status)
                            self.tabW_select_organ.setCellWidget(row, col, widget)
                        col+=1
                    row +=1
                # self.tabW_select_organ.setHorizontalHeaderLabels([key for key in keys])
                self.tabW_select_organ.verticalHeader().setVisible(False)
                self.tabW_select_organ.horizontalHeader().setVisible(False)

                headerc = self.tabW_select_organ.horizontalHeader()  
                for col in range(len(all_labels.keys())):   
                    headerc.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

                self.tabW_select_organ.resizeColumnsToContents()
                self.tabW_select_organ.resizeRowsToContents()

            else: 
                error_txt = "!The project selected does not contain organs. Add a new organ to this project by selecting 'Create New Organ'."
                self.win_msg(error_txt, self.button_load_organs)
                self.button_load_organs.setChecked(True)
                self.organ_checkboxes = None
                return

            self.organ_checkboxes = cBs
            self.button_load_organs.setChecked(True)
        else: 
            self.button_load_organs.setChecked(False)
            error_txt = '*You need to first load a project to load all the organs comprising it.'
            self.win_msg(error_txt, self.button_load_organs)
    
    def reload_table(self): 
        if self.button_load_organs.isChecked(): 
            self.load_proj_organs(proj = self.proj)
        else: 
            pass

    def check_unique_organ_selected(self, proj): 
        print('self.organ_checkboxes:',self.organ_checkboxes)
        if self.organ_checkboxes != None: 
            checked = []
            for organ_cB in self.organ_checkboxes:
                cb = getattr(self, organ_cB).isChecked()
                checked.append(cb)
            
            if sum(checked) <= 0: 
                self.organ_selected = None
            elif sum(checked) > 1:
                error_txt = '*Please select only one organ to analyse.'
                self.win_msg(error_txt, self.go_to_main_window)
            else: 
                print('checked:', checked)
                if len(checked) > 1:
                    index = [i for i, x in enumerate(checked) if x][0]
                    print('len>1:',index)
                    print('organ_cB:',organ_cB)
                    self.organ_selected = self.organ_checkboxes[index].split('cB_')[1]
                else: 
                    print('len=1:',organ_cB)
                    self.organ_selected = organ_cB.split('cB_')[1]
            print(self.organ_selected)
        else: 
            error_txt = '*Please select one organ to analyse.'
            self.win_msg(error_txt, self.go_to_main_window)

class Load_S3s(QDialog): 
    
    def __init__(self, proj, organ, parent_win):
        super().__init__()
        uic.loadUi('src/gui/ui/load_closed_channels_screen.ui', self)
        self.setWindowTitle('Loading Stacks with Closed Contours...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))

        self.channels = [key for key in proj.mH_channels.keys() if 'NS' not in key]

        #Select files
        self.browse_ch1_int.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch1_int', parent_win=parent_win))
        self.browse_ch1_tiss.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch1_tiss', parent_win=parent_win))
        self.browse_ch1_ext.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch1_ext', parent_win=parent_win))

        self.browse_ch2_int.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch2_int', parent_win=parent_win))
        self.browse_ch2_tiss.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch2_tiss', parent_win=parent_win))
        self.browse_ch2_ext.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch2_ext', parent_win=parent_win))

        self.browse_ch3_int.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch3_int', parent_win=parent_win))
        self.browse_ch3_tiss.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch3_tiss', parent_win=parent_win))
        self.browse_ch3_ext.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch3_ext', parent_win=parent_win))

        self.browse_ch4_int.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch4_int', parent_win=parent_win))
        self.browse_ch4_tiss.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch4_tiss', parent_win=parent_win))
        self.browse_ch4_ext.clicked.connect(lambda: self.get_file(organ=organ, ch_cont='ch4_ext', parent_win=parent_win))

        self.setModal(True)
        parent_win.all_closed.setChecked(True)

        #Buttons
        self.create_imChannels(organ=organ)
        self.button_add_channels.clicked.connect(lambda: self.add_channels_to_organ(proj=proj, organ=organ, parent_win=parent_win))

        #Set channel info
        self.set_channel_info(proj)
        self.show()

        print('organ.__dict__:', organ.__dict__)
        
    def set_channel_info(self, proj): 
        #Change channels
        for ch in ['ch1', 'ch2', 'ch3', 'ch4']: 
            label = getattr(self, 'lab_'+ch) 
            name = getattr(self, 'lab_filled_name_'+ch)

            if ch not in self.channels:
                label.setVisible(False)
                name.setVisible(False)
            else: 
                name.setText(proj.mH_channels[ch])
        
            for cont in ['int', 'tiss', 'ext']:
                brw_ch_cont = getattr(self, 'browse_'+ch+'_'+cont)
                dir_ch_cont = getattr(self, 'lab_filled_dir_'+ch+'_'+cont)
                check_ch_cont = getattr(self, 'check_'+ch+'_'+cont)
                if ch not in self.channels:
                    brw_ch_cont.setVisible(False)
                    dir_ch_cont.setVisible(False)
                    check_ch_cont.setVisible(False)

    def create_imChannels(self, organ):
        self.win_msg('Creating Organ Channels... Please wait...')
        names = []
        for ch_name in self.channels:
            names.append(organ.mH_settings['setup']['name_chs'][ch_name])
            self.win_msg('Creating Channel '+str(ch_name[-1]))
            im_ch = organ.create_ch(ch_name=ch_name)
            for cont in ['int', 'tiss', 'ext']: 
                getattr(self, 'browse_'+ch_name+'_'+cont).setEnabled(True)
    
        str_names = ', '.join(names)
        self.win_msg('Organ channels  -'+str_names+'-  have been successfully created! Please continue by loading the closed contour stacks...')

    def get_file(self, organ, ch_cont, parent_win):
        self.win_msg('Loading '+ch_cont+'... Wait for the indicator to turn green, then continue.')
        btn_file = getattr(self, 'browse_'+ch_cont)
        ch_name, cont_name = ch_cont.split('_')
        ch_num = int(ch_name[-1])
        if cont_name == 'tiss':
            cont_namef = 'all'
        else: 
            cont_namef = cont_name
        title = 'Import closed stacks for '+ch_cont+ ' (previous version name: s3_ch'+str(ch_num-1)+'_'+cont_namef+'.npy)'

        if hasattr(self, 'user_dir'):
            cwd = self.user_dir
        else: 
            cwd = Path().absolute()

        file_name, aaa = QFileDialog.getOpenFileName(self, title, str(cwd), "Numpy Arrays (*.npy)")
        if Path(file_name).is_file(): 
            label = getattr(self, 'lab_filled_dir_'+ch_cont)
            label.setText(str(file_name))
            check = getattr(self, 'check_'+ch_cont)
            
            #Load npy array
            npy_stack = np.load(file_name)
            if isinstance(npy_stack, np.ndarray):
                setattr(self, 'npy_'+ch_name+'_'+cont_name, file_name)
                self.user_dir = Path(file_name).parent
                check.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(0, 255, 0); color: rgb(0, 255, 0); font: 25 2pt 'Calibri Light'")
                check.setText('Done')
            else: 
                self.win_msg('*The selected file is not a numpy array. Please select a valid file.', getattr(self, 'browse_'+ch_cont))

    def add_channels_to_organ(self, proj, organ, parent_win): 

        all_done = []
        nn = 1; total_n = len(self.channels)*3
        for ch in self.channels: 
            process_up =  ['ImProc', ch, 'Status']
            self.win_msg("Adding channels' contours to organ ("+str(nn)+"/"+str(total_n)+")")
            for cont in ['int', 'tiss', 'ext']: 
                text = getattr(self, 'check_'+ch+'_'+cont).text()
                if text != 'Done':
                    self.win_msg('*Please select the stack with closed contours for '+ch+'_'+cont+'!')
                    self.button_add_channels.setChecked(False)
                    return
                else: 
                    im_ch = organ.obj_imChannels[ch]
                    file_name = getattr(self, 'npy_'+ch+'_'+cont)
                    npy_stack = np.load(file_name)
                    im_ch.create_chS3s(layerDict=npy_stack, win=self, cont_list=[cont])
                    process = ['ImProc', ch, 'C-SelectCont','Status']
                    
                    #Update organ workflow
                    organ.update_mHworkflow(process, update = 'DONE')
                    all_done.append(True)
                    nn += 1

            #Update organ workflow
            organ.update_mHworkflow(process_up, update = 'DONE')

            #Update other processes to DONE-Other way
            processes = ['A-Autom','B-Manual','C-CloseInOut']
            for proc in processes: 
                process_x = ['ImProc', ch, 'B-CloseCont', 'Steps', proc, 'Status']
                #Update organ workflow
                organ.update_mHworkflow(process_x, update = 'DONE-Loaded')

        if all(all_done):
            parent_win.update_ch_progress()
            organ.save_organ()
            proj.add_organ(organ)
            proj.save_project()
            print('organ.__dict__:', organ.__dict__)
            self.win_msg('Project  -'+ proj.user_projName + 'and Organ  -'+ organ.user_organName +'-  were saved succesfully!')
            self.close()
            parent_win.win_msg('All closed channels have been successfully imported in this organ!')

    def win_msg(self, msg, btn=None): 
        if msg[0] == '*':
            self.tE_validate.setStyleSheet(error_style)
            msg = 'Error: '+msg
            alert('error_beep')
        elif msg[0] == '!':
            self.tE_validate.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            self.tE_validate.setStyleSheet(msg_style)
        self.tE_validate.setText(msg)

        if btn != None: 
            btn.setChecked(False)

class MainWindow(QMainWindow):

    def __init__(self, proj, organ):
        super().__init__()
        uic.loadUi('src/gui/ui/main_window_screen.ui', self)
        self.setWindowTitle('morphoHeart')
        mH_logoXS = QPixmap('images/logos_1o75mm.png')
        self.mH_logo_XS.setPixmap(mH_logoXS)
        self.setWindowIcon(QIcon(mH_icon))
        self.setStyleSheet("background-color:  rgb(255, 255, 255);")
        self.label_version.setText('v'+mH_config.version+'  ')
        self.label_version.setStyleSheet('color: rgb(116, 116, 116); font: bold 9pt "Calibri Light";')
        
        self.proj = proj
        self.organ = organ

        #Menu options
        self.actionSave_Project_and_Organ.triggered.connect(self.save_project_and_organ_pressed)
        self.actionClose.triggered.connect(self.close_morphoHeart_pressed)

        #Blind analysis
        self.cB_blind.stateChanged.connect(lambda: self.blind_analysis())

        #Sounds
        layout = self.hL_sound_on_off 
        add_sound_bar(self, layout)
        sound_toggled(win=self)
        self.fill_proj_organ_info(self.proj, self.organ)

        #Progress bar
        self.prog_bar_reset()

        #Setting up tabs
        self.init_segment_tab()
        self.init_pandq_tab()
        # self.init_morphoCell_tab()
        # self.init_plot_tab()
        self.win_msg('Organ "'+organ.info['user_organName']+'" was successfully loaded!')

        #Activate first tab
        if self.organ.analysis['morphoHeart']:
            self.tabWidget.setCurrentIndex(0)
        else: 
            if self.organ.analysis['morphoCell']:
                self.tabWidget.setCurrentIndex(2)
            else: 
                self.tabWidget.setCurrentIndex(3)

        # Theme 
        self.theme = self.cB_theme.currentText()
        self.on_cB_theme_currentIndexChanged(0)

        self.pushButton.clicked.connect(lambda: self.update_proj_organ())
        self.btn_settings.clicked.connect(lambda: self.show_mH_settings())
        self.btn_measurements.clicked.connect(lambda: self.show_measurements())
        self.btn_workflow.clicked.connect(lambda: self.show_workflow())
        self.btn_wf_info.clicked.connect(lambda: self.show_wf_info())

        if not mH_config.dev: 
            self.pushButton.setVisible(False)
            self.btn_settings.setVisible(False)
            self.btn_measurements.setVisible(False)
            self.btn_workflow.setVisible(False)
            self.btn_wf_info.setVisible(False)

    def update_proj_organ(self):
        self.proj.mH_settings['measure']['hm3Dto2D'] = {'ch1_int': True}
        self.organ.mH_settings['measure']['hm3Dto2D'] = {'ch1_int': True}
        print(self.proj.mH_settings['measure'])
        print(self.organ.mH_settings['measure'])

        workflow_proj = self.proj.workflow['morphoHeart']['MeshesProc']['C-Centreline']
        workflow_organ = self.organ.workflow['morphoHeart']['MeshesProc']['C-Centreline']
        item_centreline = [tuple(item.split('_')) for item in self.organ.mH_settings['measure']['CL'].keys()]
        for workflow in [workflow_proj, workflow_organ]:
            for item in item_centreline:
                ch, cont, _ = item
                print(ch,cont)
                if ch not in workflow['SimplifyMesh'].keys(): 
                    workflow['SimplifyMesh'][ch] = {}
                    workflow['vmtk_CL'][ch] = {}
                    workflow['buildCL'][ch] = {}
                workflow['SimplifyMesh'][ch][cont] = {'Status': 'NI'}
                workflow['vmtk_CL'][ch][cont] = {'Status': 'NI'}
                workflow['buildCL'][ch][cont] = {'Status': 'NI'}
        
        print(self.proj.workflow['morphoHeart'])
        print(self.organ.workflow['morphoHeart'])

        # pass

    def show_mH_settings(self):
        print('------- MH_SETTINGS -------\n',self.organ.mH_settings)
    
    def show_measurements(self):
        print('------- MEASUREMENTS -------\n',self.organ.mH_settings['measure'])

    def show_workflow(self):
        print('------- WORKFLOW -------\n',self.organ.workflow)

    def show_wf_info(self):
        print('------- WF_INFO -------\n',self.organ.mH_settings['wf_info'])

    @pyqtSlot(int)
    def on_cB_theme_currentIndexChanged(self, theme):
        print('mH_config.theme:',mH_config.theme)
        if theme == 'Light' or theme == 0: 
            file = 'src/gui/themes/Light.qss'
        else: 
            file = 'src/gui/themes/Dark.qss'
        #Open the file
        with open(file, 'r') as f: 
            style_str = f.read()
            print('Selected theme: ', theme)
        #Set the theme
        self.setStyleSheet(style_str)
        mH_config.theme = theme

    #Progress Bar Related functions
    def prog_bar_range(self, r1, r2):
        self.prog_bar.setRange(r1, r2)
        self.prog_bar_reset()

    def prog_bar_update(self, value):
        self.prog_bar.setValue(value)
 
    def prog_bar_reset(self):
        value = 0
        self.prog_bar.setValue(value)

    #Window message
    def win_msg(self, msg, btn=None): 
        if msg[0] == '*':
            self.tE_validate.setStyleSheet(error_style)
            msg = 'Error: '+msg
            alert('error_beep')
        elif msg[0] == '!':
            self.tE_validate.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            self.tE_validate.setStyleSheet(msg_style)
        self.tE_validate.setText(msg)

        if btn != None: 
            btn.setChecked(False)
        
    # Init functions
    #- General Init
    def fill_proj_organ_info(self, proj, organ):
        self.lineEdit_proj_name.setText(proj.info['user_projName'])
        organ_data = ['user_organName','strain','stage','genotype','manipulation','im_orientation','user_organNotes']
        for data in organ_data: 
            lineEdit = getattr(self, 'lineEdit_'+data)
            if data in ['genotype', 'manipulation']:
                if not self.cB_blind.isChecked(): 
                    lineEdit.setText(organ.info[data])
                else: 
                    pass
            else: 
                lineEdit.setText(organ.info[data])
        
        date = organ.info['date_created']
        date_qt = QDate.fromString(date, "yyyy-MM-dd")
        self.dateEdit.setDate(date_qt)

        if proj.analysis['morphoHeart']:
            self.tab_segm.setEnabled(True)
            self.tab_PandQ.setEnabled(True)
        else: 
            self.tab_segm.setVisible(False)
            self.tab_PandQ.setVisible(False)

        if proj.analysis['morphoCell']:
            self.tab_segm.setEnabled(True)
        else: 
            self.tab_segm.setVisible(False)
        if proj.analysis['morphoPlot']:
            self.tab_plot.setEnabled(True)
        else: 
            self.tab_plot.setVisible(False)

    def blind_analysis(self):
        if not self.cB_blind.isChecked(): 
            self.lineEdit_genotype.setText(self.organ.info['genotype'])
            self.lineEdit_manipulation.setText(self.organ.info['manipulation'])
        else: 
            self.lineEdit_genotype.clear()
            self.lineEdit_manipulation.clear()
    
    #- Init SEGMENTATION Tab
    def init_segment_tab(self): 
        print('Setting up Segmentation Tab')
        self.channels = self.organ.mH_settings['setup']['name_chs'] # {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}
        num = 0
        for ch in ['ch1', 'ch2', 'ch3', 'ch4']:
            ch_tab = getattr(self, 'tab_chs')
            if ch not in self.channels.keys(): 
                ch_tab.setTabVisible(num, False)
            else: 
                tab_num = ch[-1]
                ch_tab.setTabText(num, 'Ch'+tab_num+': '+self.channels[ch])
            num +=1

        self.button_continue.clicked.connect(lambda: self.continue_next_tab())
        self.init_ch_progress()

    #- Init Ch Progress Table
    def init_ch_progress(self): 
        im_chs = [key for key in self.channels.keys() if key != 'chNS']
        workflow = self.organ.workflow['morphoHeart']
        self.tabW_progress_ch.setRowCount(len(im_chs))
        big_im_chs = [ch.title() for ch in im_chs]
        self.tabW_progress_ch.setVerticalHeaderLabels(big_im_chs)
        self.proc_keys = {'Ch':'gen','A-MaskChannel':'mask', 
                            'A-Autom':'autom','B-Manual': 'manual', 
                            'C-CloseInOut': 'trim', 'C-SelectCont': 'select'}
        cS = []
        #Adding channels to table
        row = 0
        for ch in im_chs:
            col = 0        
            for proc in self.proc_keys.keys():
                #Create Layout
                widget   = QWidget() 
                hL = QtWidgets.QHBoxLayout(widget)
                color_status = QtWidgets.QLineEdit()
                color_status.setEnabled(True)
                color_status.setMinimumSize(QtCore.QSize(15, 15))
                color_status.setMaximumSize(QtCore.QSize(15, 15))
                color_status.setStyleSheet("border-color: rgb(0, 0, 0);")
                color_status.setReadOnly(True)
                hL.addWidget(color_status)
                hL.setContentsMargins(0, 0, 0, 0)
                self.tabW_progress_ch.setCellWidget(row, col, widget)
                cS_name = 'cS_'+ch+'_'+self.proc_keys[proc]
                setattr(self, cS_name, color_status)
                cS.append(cS_name)
                col+=1
            row +=1                

        headerc = self.tabW_progress_ch.horizontalHeader()  
        for col in range(len(self.proc_keys)):   
            headerc.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
            # header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            # header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        headerr = self.tabW_progress_ch.verticalHeader()  
        for row in range(len(im_chs)):   
            headerr.setSectionResizeMode(row, QHeaderView.ResizeMode.Stretch)
            
        self.tabW_progress_ch.resizeColumnsToContents()
        self.tabW_progress_ch.resizeRowsToContents()
        self.segm_status = cS
        self.update_ch_progress()

    def update_ch_progress(self): 
        workflow = self.organ.workflow['morphoHeart']
        for cs in self.segm_status: 
            cS = getattr(self, cs)
            _, ch, proc = cs.split('_')
            if 'gen' in cs: 
                items = ['ImProc',ch,'Status']
            else: 
                for key in self.proc_keys:
                    if self.proc_keys[key] == proc:
                        keyf = key
                        break
                if 'autom' in cs or 'manual' in cs or 'trim' in cs:
                    items = ['ImProc',ch,'B-CloseCont','Steps', keyf,'Status']
                elif 'mask' in cs or 'select' in cs:
                    items = ['ImProc',ch,keyf,'Status']
            update_status(workflow, items, cS)         

    #- Init PROCESS AND ANALYSE Tab
    def init_pandq_tab(self): 

        #All Group box
        self.segmentationAll_play.setStyleSheet(style_play)
        # setup_play_btn(btn = self.segmentationAll_play, win = self)
        self.segmentationAll_play.setEnabled(False)
        self.segmentationAll_play.clicked.connect(lambda: self.run_segmentationAll())
        self.centreline_thicknessAll_play.setStyleSheet(style_play)
        self.centreline_thicknessAll_play.setEnabled(False)
        # self.centreline_thicknessAll_play.clicked.connect(lambda: self.())
        self.segments_sectionsAll_play.setStyleSheet(style_play)
        self.segments_sectionsAll_play.setEnabled(False)
        # self.segments_sectionsAll_play.clicked.connect(lambda: self.())

        #Keep largest
        self.init_keeplargest()
        if int(self.organ.mH_settings['setup']['no_chs'])>1:
            self.init_clean()
        else: 
            self.cleanup_all_widget.setVisible(False)
        self.init_trim()
        self.init_orientation()
        #ChNS
        if isinstance(self.organ.mH_settings['setup']['chNS'], dict):
            if self.organ.mH_settings['setup']['chNS']['layer_btw_chs']:
                self.init_chNS()
            else: 
                print('Initialisong chNS - dict but no layer_btw_chs?')
                alert('bubble')
        else:
            self.chNS_all_widget.setVisible(False)
            print('Dissapear chNS')
        #Summary whole
        self.init_summary_whole()
        #Measure
        self.init_measure_whole()
        #Centreline
        if len(self.organ.mH_settings['measure']['CL']) > 0:
            self.init_centreline()
        else: 
            self.centreline_all_widget.setVisible(False)
        'Thickness/Ballooning'
        if len(self.organ.mH_settings['measure']['th_i2e'])+len(self.organ.mH_settings['measure']['th_e2i'])+len(self.organ.mH_settings['measure']['ball'])>0:
            self.init_thickness_ballooning()
        else: 
            self.thickness_ballooning_all_widget.setVisible(False)
        #Segments
        if isinstance(self.organ.mH_settings['setup']['segm'], dict):
            self.init_segments()
        else: 
            self.segments_all_widget.setVisible(False)
        #Regions
        if isinstance(self.organ.mH_settings['setup']['sect'], dict):
            self.init_sections()
        else: 
            self.sections_all_widget.setVisible(False)
        #Segments-Regions 
        if isinstance(self.organ.mH_settings['setup']['segm-sect'], dict):
            self.init_segm_sect()
            print('aja, intit_segm_sect')
        else: 
            self.segm_sect_all_widget.setVisible(False)
        
        #User parameters
        self.init_user_param()
        #Plot results
        self.init_plot_results()
        #Results
        self.init_results_table()
        #Workflow
        self.init_workflow()

    #>> Initialise all modules of Process and Analyse
    def init_keeplargest(self): 
        #Buttons
        self.fillcolor_ch1_int.clicked.connect(lambda: self.color_picker(name = 'ch1_int'))
        self.fillcolor_ch1_tiss.clicked.connect(lambda: self.color_picker(name = 'ch1_tiss'))
        self.fillcolor_ch1_ext.clicked.connect(lambda: self.color_picker(name = 'ch1_ext'))
        self.fillcolor_ch2_int.clicked.connect(lambda: self.color_picker(name = 'ch2_int'))
        self.fillcolor_ch2_tiss.clicked.connect(lambda: self.color_picker(name = 'ch2_tiss'))
        self.fillcolor_ch2_ext.clicked.connect(lambda: self.color_picker(name = 'ch2_ext'))
        self.fillcolor_ch3_int.clicked.connect(lambda: self.color_picker(name = 'ch3_int'))
        self.fillcolor_ch3_tiss.clicked.connect(lambda: self.color_picker(name = 'ch3_tiss'))
        self.fillcolor_ch3_ext.clicked.connect(lambda: self.color_picker(name = 'ch3_ext'))
        self.fillcolor_ch4_int.clicked.connect(lambda: self.color_picker(name = 'ch4_int'))
        self.fillcolor_ch4_tiss.clicked.connect(lambda: self.color_picker(name = 'ch4_tiss'))
        self.fillcolor_ch4_ext.clicked.connect(lambda: self.color_picker(name = 'ch4_ext'))
      
        # -Keep largest
        self.keeplargest_open.clicked.connect(lambda: self.open_section(name = 'keeplargest'))
        self.keeplargest_set.clicked.connect(lambda: self.set_keeplargest())
        self.keeplargest_play.setStyleSheet(style_play)
        self.keeplargest_play.setEnabled(False)
        self.keeplargest_plot.clicked.connect(lambda: self.plot_meshes('all'))
        self.keeplargest_plot.setEnabled(False)
        self.q_keeplargest.clicked.connect(lambda: self.help('keeplargest'))
        self.keeplargest_plot_ch1.clicked.connect(lambda: self.plot_meshes('ch1') )
        self.keeplargest_plot_ch2.clicked.connect(lambda: self.plot_meshes('ch2') )
        self.keeplargest_plot_ch3.clicked.connect(lambda: self.plot_meshes('ch3') )
        self.keeplargest_plot_ch4.clicked.connect(lambda: self.plot_meshes('ch4') )

        self.keeplargest_plot_ch1.setEnabled(False)
        self.keeplargest_plot_ch2.setEnabled(False)
        self.keeplargest_plot_ch3.setEnabled(False)
        self.keeplargest_plot_ch4.setEnabled(False)

        for chk in ['ch1', 'ch2', 'ch3', 'ch4']:
            if chk not in self.channels.keys():
                getattr(self, 'kl_label_'+chk).setVisible(False)
                getattr(self, 'kl_'+chk+'_all').setVisible(False)
                getattr(self, 'keeplargest_plot_'+chk).setVisible(False)
                for contk in ['int', 'tiss', 'ext']:
                    getattr(self, 'kl_'+chk+'_'+contk).setVisible(False)
                    getattr(self, 'fillcolor_'+chk+'_'+contk).setVisible(False)
            else: 
                getattr(self, 'kl_label_'+chk).setText(chk.title()+': '+self.channels[chk].title())
                for contk in ['int', 'tiss', 'ext']:
                    color = self.organ.mH_settings['setup']['color_chs'][chk][contk]
                    print(chk, contk, '- color:', color)
                    btn_color = getattr(self, 'fillcolor_'+chk+'_'+contk)
                    color_btn(btn = btn_color, color = color)

        self.kl_ch1_all.stateChanged.connect(lambda: self.tick_all('ch1', 'kl'))
        self.kl_ch2_all.stateChanged.connect(lambda: self.tick_all('ch2', 'kl'))
        self.kl_ch3_all.stateChanged.connect(lambda: self.tick_all('ch3', 'kl'))
        self.kl_ch4_all.stateChanged.connect(lambda: self.tick_all('ch4', 'kl'))

        #Initialise with user settings, if they exist!
        self.user_keeplargest()

    def init_clean(self):
        #Buttons
        self.cleanup_open.clicked.connect(lambda: self.open_section(name='cleanup'))
        self.cleanup_plot_ch1.clicked.connect(lambda: self.plot_meshes('ch1'))
        self.cleanup_plot_ch2.clicked.connect(lambda: self.plot_meshes('ch2'))
        self.cleanup_plot_ch3.clicked.connect(lambda: self.plot_meshes('ch3'))
        self.cleanup_plot_ch4.clicked.connect(lambda: self.plot_meshes('ch4'))
        self.cleanup_plot_ch1.setEnabled(False)
        self.cleanup_plot_ch2.setEnabled(False)
        self.cleanup_plot_ch3.setEnabled(False)
        self.cleanup_plot_ch4.setEnabled(False)
        
        self.cleanup_set.clicked.connect(lambda: self.set_clean())
        self.cleanup_play.setStyleSheet(style_play)
        self.cleanup_play.setEnabled(False)
        self.clean_plot.clicked.connect(lambda: self.plot_meshes('all'))
        self.clean_plot.setEnabled(False)
        self.q_cleanup.clicked.connect(lambda: self.help('cleanup'))

        #  Segmentation cleanup setup
        for chs in ['ch1', 'ch2', 'ch3', 'ch4']:
            if chs not in self.channels.keys():
                getattr(self, 'clean_'+chs).setVisible(False)
                getattr(self, 'clean_'+chs+'_all').setVisible(False)
                getattr(self, 'clean_withch_'+chs).setVisible(False)
                getattr(self, 'clean_withcont_'+chs).setVisible(False)
                getattr(self, 'inverted_'+chs).setVisible(False)
                getattr(self, 'cleanup_plot_'+chs).setVisible(False)
                for cont in ['int', 'tiss', 'ext']:
                    getattr(self, 'clean_'+chs+'_'+cont).setVisible(False)
            else: 
                ch_opt = [cho for cho in self.channels if cho != 'chNS' and cho != chs]
                getattr(self, 'clean_withch_'+chs).addItems(ch_opt)
                getattr(self, 'clean_withcont_'+chs).addItems(['int', 'ext'])
        
        self.clean_ch1_all.stateChanged.connect(lambda: self.tick_all('ch1', 'clean'))
        self.clean_ch2_all.stateChanged.connect(lambda: self.tick_all('ch2', 'clean'))
        self.clean_ch3_all.stateChanged.connect(lambda: self.tick_all('ch3', 'clean'))
        self.clean_ch4_all.stateChanged.connect(lambda: self.tick_all('ch4', 'clean'))

        self.clean_plot2d.stateChanged.connect(lambda: self.n_slices('clean'))

        #Initialise with user settings, if they exist!
        self.user_clean()
    
    def init_trim(self):
        #Buttons
        self.trimming_open.clicked.connect(lambda: self.open_section(name='trimming'))
        self.trimming_plot_ch1.clicked.connect(lambda: self.plot_meshes('ch1'))
        self.trimming_plot_ch2.clicked.connect(lambda: self.plot_meshes('ch2'))
        self.trimming_plot_ch3.clicked.connect(lambda: self.plot_meshes('ch3'))
        self.trimming_plot_ch4.clicked.connect(lambda: self.plot_meshes('ch4'))
        self.trimming_plot_ch1.setEnabled(False)
        self.trimming_plot_ch2.setEnabled(False)
        self.trimming_plot_ch3.setEnabled(False)
        self.trimming_plot_ch4.setEnabled(False)
        
        self.trimming_set.clicked.connect(lambda: self.set_trim())
        self.trimming_play.setStyleSheet(style_play)
        self.trimming_play.setEnabled(False)
        self.trimming_plot.clicked.connect(lambda: self.plot_meshes('all'))
        self.trimming_plot.setEnabled(False)
        self.q_trimming.clicked.connect(lambda: self.help('trimming'))

        # Segmentation cleanup setup
        for chs in ['ch1', 'ch2', 'ch3', 'ch4']:
            if chs not in self.channels.keys():
                getattr(self, 'trim_'+chs).setVisible(False)
                getattr(self, 'top_'+chs+'_all').setVisible(False)
                getattr(self, 'bot_'+chs+'_all').setVisible(False)
                getattr(self, 'trimming_plot_'+chs).setVisible(False)
                for cont in ['int', 'tiss', 'ext']:
                    getattr(self, 'top_'+chs+'_'+cont).setVisible(False)
                    getattr(self, 'bot_'+chs+'_'+cont).setVisible(False)
        
        self.top_ch1_all.stateChanged.connect(lambda: self.tick_all('ch1','top'))
        self.top_ch2_all.stateChanged.connect(lambda: self.tick_all('ch2','top'))
        self.top_ch3_all.stateChanged.connect(lambda: self.tick_all('ch3','top'))
        self.top_ch4_all.stateChanged.connect(lambda: self.tick_all('ch4','top'))

        self.bot_ch1_all.stateChanged.connect(lambda: self.tick_all('ch1', 'bot'))
        self.bot_ch2_all.stateChanged.connect(lambda: self.tick_all('ch2', 'bot'))
        self.bot_ch3_all.stateChanged.connect(lambda: self.tick_all('ch3', 'bot'))
        self.bot_ch4_all.stateChanged.connect(lambda: self.tick_all('ch4', 'bot'))
        
        #Initialise with user settings, if they exist!
        self.user_trimming()

    def init_orientation(self):
        #Buttons
        self.orient_open.clicked.connect(lambda: self.open_section(name='orient'))
        orient_stack = self.organ.mH_settings['setup']['orientation']['stack']
        self.stack_orientation.setText(orient_stack)
        orient_roi = self.organ.mH_settings['setup']['orientation']['roi']
        self.roi_orientation.setText(orient_roi)
        self.stack_orient_plot.clicked.connect(lambda: self.plot_orient(name = 'stack'))
        self.roi_orient_plot.clicked.connect(lambda: self.plot_orient(name = 'roi'))

        self.q_orientation.clicked.connect(lambda: self.help('orientation'))
        self.orientation_set.clicked.connect(lambda: self.set_orientation())
        self.orientation_play.setStyleSheet(style_play)
        self.orientation_play.setEnabled(False)

        self.stack_orient_plot.setEnabled(False)
        self.roi_orient_plot.setEnabled(False)

        self.roi_reorient.stateChanged.connect(lambda: self.check_roi_reorient())
        self.radio_manual.toggled.connect(lambda: self.reorient_method(mtype = 'manual'))
        self.radio_centreline.toggled.connect(lambda: self.reorient_method(mtype = 'centreline'))

        items_cl = self.organ.mH_settings['measure']['CL'].keys()
        self.items_centreline = []
        for item in items_cl:
            ch, cont, segm = item.split('_')
            name = self.organ.mH_settings['setup']['name_chs'][ch] + ' ('+ch+'_'+cont+')'
            self.items_centreline.append(name)
        self.centreline_orientation.addItems(self.items_centreline)
        self.reorient_method(mtype = 'none')

        #Initialise with user settings, if they exist!
        self.user_orientation()
        
    def init_chNS(self):
        
        chns_name = self.organ.mH_settings
        self.label_chNS_extraction.setText('Channel from the negative space extraction  - ChNS: '+self.channels['chNS'].title())
        #Buttons
        self.chNS_open.clicked.connect(lambda: self.open_section(name='chNS'))
        self.chNS_plot.clicked.connect(lambda: self.plot_meshes('chNS'))
        self.chNS_plot.setEnabled(False)
        self.chNS_play.setStyleSheet(style_play)
        self.chNS_play.setEnabled(False)
        self.q_chNS.clicked.connect(lambda: self.help('chNS'))
        self.chNS_set.clicked.connect(lambda: self.set_chNS())

        self.fillcolor_chNS_int.clicked.connect(lambda: self.color_picker(name = 'chNS_int'))
        self.fillcolor_chNS_tiss.clicked.connect(lambda: self.color_picker(name = 'chNS_tiss'))
        self.fillcolor_chNS_ext.clicked.connect(lambda: self.color_picker(name = 'chNS_ext'))
        
        chNS_setup = self.organ.mH_settings['setup']['chNS']
        ch_ext = chNS_setup['ch_ext'][0]
        self.chNS_extch.setText(ch_ext.title()+': '+self.channels[ch_ext].title())
        self.chNS_extcont.setText(chNS_setup['ch_ext'][1]+'ernal')
        self.chNS_operation.setText(chNS_setup['operation'])
        ch_int = chNS_setup['ch_int'][0]
        self.chNS_intch.setText(ch_int.title()+': '+self.channels[ch_int].title())
        self.chNS_intcont.setText(chNS_setup['ch_int'][1]+'ernal')

        for contk in ['int', 'tiss', 'ext']:
            color = self.organ.mH_settings['setup']['chNS']['color_chns'][contk]
            # color_txt = "QPushButton{ border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); background-color: "+color+";} QPushButton:hover{border-color: rgb(255, 255, 255)}"
            btn_color = getattr(self, 'fillcolor_chNS_'+contk)
            color_btn(btn = btn_color, color = color)
            # color_btn.setStyleSheet(color_txt)

        self.chNS_plot2d.stateChanged.connect(lambda: self.n_slices('chNS'))

        #Initialise with user settings, if they exist!
        self.user_chNS()

    def init_summary_whole(self): 
        #Buttons
        self.fillcolor_ch1_intf.clicked.connect(lambda: self.color_picker(name = 'ch1_int'))
        self.fillcolor_ch1_tissf.clicked.connect(lambda: self.color_picker(name = 'ch1_tiss'))
        self.fillcolor_ch1_extf.clicked.connect(lambda: self.color_picker(name = 'ch1_ext'))
        self.fillcolor_ch2_intf.clicked.connect(lambda: self.color_picker(name = 'ch2_int'))
        self.fillcolor_ch2_tissf.clicked.connect(lambda: self.color_picker(name = 'ch2_tiss'))
        self.fillcolor_ch2_extf.clicked.connect(lambda: self.color_picker(name = 'ch2_ext'))
        self.fillcolor_ch3_intf.clicked.connect(lambda: self.color_picker(name = 'ch3_int'))
        self.fillcolor_ch3_tissf.clicked.connect(lambda: self.color_picker(name = 'ch3_tiss'))
        self.fillcolor_ch3_extf.clicked.connect(lambda: self.color_picker(name = 'ch3_ext'))
        self.fillcolor_ch4_intf.clicked.connect(lambda: self.color_picker(name = 'ch4_int'))
        self.fillcolor_ch4_tissf.clicked.connect(lambda: self.color_picker(name = 'ch4_tiss'))
        self.fillcolor_ch4_extf.clicked.connect(lambda: self.color_picker(name = 'ch4_ext'))
        self.fillcolor_chNS_intf.clicked.connect(lambda: self.color_picker(name = 'chNS_int'))
        self.fillcolor_chNS_tissf.clicked.connect(lambda: self.color_picker(name = 'chNS_tiss'))
        self.fillcolor_chNS_extf.clicked.connect(lambda: self.color_picker(name = 'chNS_ext'))

        self.summary_whole_plot_ch1.clicked.connect(lambda: self.plot_meshes('ch1'))
        self.summary_whole_plot_ch2.clicked.connect(lambda: self.plot_meshes('ch2'))
        self.summary_whole_plot_ch3.clicked.connect(lambda: self.plot_meshes('ch3'))
        self.summary_whole_plot_ch4.clicked.connect(lambda: self.plot_meshes('ch4'))
        self.summary_whole_plot_chNS.clicked.connect(lambda: self.plot_meshes('chNS'))
        self.summary_whole_plot_ch1.setEnabled(False)
        self.summary_whole_plot_ch2.setEnabled(False)
        self.summary_whole_plot_ch3.setEnabled(False)
        self.summary_whole_plot_ch4.setEnabled(False)
        self.summary_whole_plot_chNS.setEnabled(False) 

        # -Summary whole
        self.summary_whole_open.clicked.connect(lambda: self.open_section(name = 'summary_whole'))

        for chk in ['ch1', 'ch2', 'ch3', 'ch4', 'chNS']:
            if chk not in self.channels.keys():
                getattr(self, 'sum_label_'+chk+'f').setVisible(False)
                getattr(self, 'summary_whole_plot_'+chk).setVisible(False)
                for contk in ['int', 'tiss', 'ext']:
                    getattr(self, 'fillcolor_'+chk+'_'+contk+'f').setVisible(False)
                    getattr(self, 'alpha_'+chk+'_'+contk+'f').setVisible(False)
            else: 
                if 'NS' in chk: 
                    txt = 'ChNS: '+self.channels[chk].title()
                else: 
                    txt = chk.title()+': '+self.channels[chk].title()
                getattr(self, 'sum_label_'+chk+'f').setText(txt)
                for contk in ['int', 'tiss', 'ext']:
                    if 'NS' not in chk: 
                        color = self.organ.mH_settings['setup']['color_chs'][chk][contk]
                    else: 
                        color = self.organ.mH_settings['setup']['chNS']['color_chns'][contk]
                    print(chk, contk, '- color:', color)
                    btn_color = getattr(self, 'fillcolor_'+chk+'_'+contk+'f')
                    color_btn(btn = btn_color, color = color)
            
        self.alpha_ch1_intf.valueChanged.connect(lambda: self.update_alpha('ch1_int'))
        self.alpha_ch1_tissf.valueChanged.connect(lambda: self.update_alpha('ch1_tiss'))
        self.alpha_ch1_extf.valueChanged.connect(lambda: self.update_alpha('ch1_ext'))
        self.alpha_ch2_intf.valueChanged.connect(lambda: self.update_alpha('ch2_int'))
        self.alpha_ch2_tissf.valueChanged.connect(lambda: self.update_alpha('ch2_tiss'))
        self.alpha_ch2_extf.valueChanged.connect(lambda: self.update_alpha('ch2_ext'))
        self.alpha_ch3_intf.valueChanged.connect(lambda: self.update_alpha('ch3_int'))
        self.alpha_ch3_tissf.valueChanged.connect(lambda: self.update_alpha('ch3_tiss'))
        self.alpha_ch3_extf.valueChanged.connect(lambda: self.update_alpha('ch3_ext'))
        self.alpha_ch4_intf.valueChanged.connect(lambda: self.update_alpha('ch4_int'))
        self.alpha_ch4_tissf.valueChanged.connect(lambda: self.update_alpha('ch4_tiss'))
        self.alpha_ch4_extf.valueChanged.connect(lambda: self.update_alpha('ch4_ext'))
        self.alpha_chNS_intf.valueChanged.connect(lambda: self.update_alpha('chNS_int'))
        self.alpha_chNS_tissf.valueChanged.connect(lambda: self.update_alpha('chNS_tiss'))
        self.alpha_chNS_extf.valueChanged.connect(lambda: self.update_alpha('chNS_ext'))

        #Initialise with user settings, if they exist!
        self.user_summary_whole()
    
    def init_measure_whole(self): 
        #Buttons
        self.measure_wholeAll_play.setStyleSheet(style_play)
        self.measure_whole_open.clicked.connect(lambda: self.open_section(name='measure_whole'))

    def init_centreline(self):
        #Buttons
        self.centreline_open.clicked.connect(lambda: self.open_section(name='centreline'))
        self.centreline_play.setStyleSheet(style_play)
        self.centreline_play.setEnabled(False)
        self.centreline_clean_play.setStyleSheet(style_play)
        self.centreline_clean_play.setEnabled(False)
        self.centreline_ML_play.setStyleSheet(style_play)
        self.centreline_ML_play.setEnabled(False)
        self.centreline_vmtk_play.setStyleSheet(style_play)
        self.centreline_vmtk_play.setEnabled(False)
        self.centreline_select.setStyleSheet(style_play)
        self.centreline_select.setEnabled(False)
        self.q_centreline.clicked.connect(lambda: self.help('centreline'))
        self.centreline_set.clicked.connect(lambda: self.set_centreline())

        cl_to_extract = self.organ.mH_settings['measure']['CL']
        # print(cl_to_extract, len(cl_to_extract))
        cl_keys = list(cl_to_extract.keys())
        for nn in range(1,7,1):
            if nn <= len(cl_to_extract):
                ch, cont = cl_keys[nn-1].split('_')[0:-1]
                # print(ch, cont)
                namef = self.channels[ch]+' ('+ch+') - '+cont
                # namef = '_'.join(name)
                getattr(self, 'cL_name'+str(nn)).setText(namef)
                getattr(self, 'cl_plot'+str(nn)).setEnabled(False)
            else:
                getattr(self, 'label_cl'+str(nn)).setVisible(False)
                getattr(self, 'cL_name'+str(nn)).setVisible(False)
                getattr(self, 'clClean_status'+str(nn)).setVisible(False)
                getattr(self, 'cl_clean_plot'+str(nn)).setVisible(False)
                getattr(self, 'meshLab_status'+str(nn)).setVisible(False)
                getattr(self, 'vmtk_status'+str(nn)).setVisible(False)
                getattr(self, 'opt_cl_status'+str(nn)).setVisible(False)
                getattr(self, 'opt_cl'+str(nn)).setVisible(False)
                getattr(self, 'cl_plot'+str(nn)).setVisible(False)

        self.cl_clean_plot1.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'SimplifyMesh', btn = 'cl_clean_plot1'))
        self.cl_clean_plot2.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'SimplifyMesh', btn = 'cl_clean_plot2'))
        self.cl_clean_plot3.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'SimplifyMesh', btn = 'cl_clean_plot3'))
        self.cl_clean_plot4.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'SimplifyMesh', btn = 'cl_clean_plot4'))
        self.cl_clean_plot5.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'SimplifyMesh', btn = 'cl_clean_plot5'))
        self.cl_clean_plot6.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'SimplifyMesh', btn = 'cl_clean_plot6'))

        self.cl_plot1.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'Final', btn = 'cl_plot1'))
        self.cl_plot2.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'Final', btn = 'cl_plot2'))
        self.cl_plot3.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'Final', btn = 'cl_plot3'))
        self.cl_plot4.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'Final', btn = 'cl_plot4'))
        self.cl_plot5.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'Final', btn = 'cl_plot5'))
        self.cl_plot6.clicked.connect(lambda: self.plot_tempObj(proc = 'CL', sub = 'Final', btn = 'cl_plot6'))

        #Initialise with user settings, if they exist!
        self.user_centreline()

    def init_thickness_ballooning(self):
        #Buttons
        self.heatmaps_open.clicked.connect(lambda: self.open_section(name='heatmaps'))
        self.heatmaps2D_play.setStyleSheet(style_play)
        self.heatmaps2D_play.setEnabled(False)
        self.heatmaps3D_play.setStyleSheet(style_play)
        self.heatmaps3D_play.setEnabled(False)
        self.thickness_set.clicked.connect(lambda: self.set_thickness())
        self.q_heatmaps.clicked.connect(lambda: self.help('heatmaps'))

        #Plot buttons
        # 3D
        self.hm_plot1.clicked.connect(lambda: self.plot_heatmap3d(btn='1'))
        self.hm_plot2.clicked.connect(lambda: self.plot_heatmap3d(btn='2'))
        self.hm_plot3.clicked.connect(lambda: self.plot_heatmap3d(btn='3'))
        self.hm_plot4.clicked.connect(lambda: self.plot_heatmap3d(btn='4'))
        self.hm_plot5.clicked.connect(lambda: self.plot_heatmap3d(btn='5'))
        self.hm_plot6.clicked.connect(lambda: self.plot_heatmap3d(btn='6'))
        self.hm_plot7.clicked.connect(lambda: self.plot_heatmap3d(btn='7'))
        self.hm_plot8.clicked.connect(lambda: self.plot_heatmap3d(btn='8'))
        self.hm_plot9.clicked.connect(lambda: self.plot_heatmap3d(btn='9'))
        self.hm_plot10.clicked.connect(lambda: self.plot_heatmap3d(btn='10'))
        self.hm_plot11.clicked.connect(lambda: self.plot_heatmap3d(btn='11'))
        self.hm_plot12.clicked.connect(lambda: self.plot_heatmap3d(btn='12'))
        # 2D
        self.hm_plot1_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='1'))
        self.hm_plot2_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='2'))
        self.hm_plot3_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='3'))
        self.hm_plot4_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='4'))
        self.hm_plot5_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='5'))
        self.hm_plot6_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='6'))
        self.hm_plot7_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='7'))
        self.hm_plot8_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='8'))
        self.hm_plot9_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='9'))
        self.hm_plot10_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='10'))
        self.hm_plot11_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='11'))
        self.hm_plot12_2D.clicked.connect(lambda: self.plot_heatmap2d(btn='12'))

        #Default values
        self.def1.stateChanged.connect(lambda: self.default_range('1'))
        self.def2.stateChanged.connect(lambda: self.default_range('2'))
        self.def3.stateChanged.connect(lambda: self.default_range('3'))
        self.def4.stateChanged.connect(lambda: self.default_range('4'))
        self.def5.stateChanged.connect(lambda: self.default_range('5'))
        self.def6.stateChanged.connect(lambda: self.default_range('6'))
        self.def7.stateChanged.connect(lambda: self.default_range('7'))
        self.def8.stateChanged.connect(lambda: self.default_range('8'))
        self.def9.stateChanged.connect(lambda: self.default_range('9'))
        self.def10.stateChanged.connect(lambda: self.default_range('10'))
        self.def11.stateChanged.connect(lambda: self.default_range('11'))
        self.def12.stateChanged.connect(lambda: self.default_range('12'))

        self.all_def.stateChanged.connect(lambda: self.check_all(mtype = 'def'))
        self.all_d3d2.stateChanged.connect(lambda: self.check_all(mtype = 'd3d2'))

        #Heatmap settings
        self.hm_btns = {}
        setup = {'th_i2e': {'proc': ['measure','th_i2e'], 'name': 'Thickness (int>ext)', 'min_val': 0, 'max_val': 20}, 
                 'th_e2i': {'proc': ['measure','th_e2i'], 'name': 'Thickness (ext>int)', 'min_val': 0, 'max_val': 20},
                 'ball': {'proc': ['measure','ball'], 'name': 'Ballooning', 'min_val': 0, 'max_val': 60}}

        nn = 0
        cmaps = ['turbo','viridis', 'jet', 'magma', 'inferno', 'plasma']
        for proc in setup: 
            name = setup[proc]['name']
            minn = setup[proc]['min_val']
            maxx = setup[proc]['max_val']
            
            for item in self.organ.mH_settings['measure'][proc]:
                # print('item being set: ', item)
                if proc != 'ball': 
                    chh, conth, _ = item.split('_')
                    key = proc+'['+chh+'-'+conth+']'
                    nameff = name+' ['+chh+'-'+conth+']'
                else: #ball[ch1-int(CL.ch1-int)]
                    namef = item.replace('_(', '(CL.')
                    namef = namef.replace('_', '-')
                    nameff =  name+' ['+namef+']'
                    key = proc+'['+namef+']'
                
                #Assign objects to GUI
                label = getattr(self,'label_hm'+str(nn+1))
                mina = getattr(self,'min_hm'+str(nn+1))
                maxa = getattr(self,'max_hm'+str(nn+1))
                hm_plot = getattr(self, 'hm_plot'+str(nn+1))
                hm_plot2 = getattr(self, 'hm_plot'+str(nn+1)+'_2D')
                play = getattr(self, 'hm_play'+str(nn+1))
                play2d = getattr(self, 'hm2d_play'+str(nn+1))
                cm = getattr(self,'colormap'+str(nn+1))
                cm.clear()
                cm.addItems(cmaps)
                
                self.hm_btns[key] = {'name': nameff,
                                        'min_val': minn, 
                                        'max_val': maxx, 
                                        'num' : nn+1,
                                        'play': play, 
                                        'plot': hm_plot, 
                                        'play2d': play2d,
                                        'plot2d': hm_plot2}
                
                label.setText(nameff)
                mina.setValue(minn)
                maxa.setValue(maxx)
                play.setEnabled(False)
                hm_plot.setEnabled(False)
                play2d.setEnabled(False)
                hm_plot2.setEnabled(False)

                nn +=1
                
        print('hm_btns:', self.hm_btns)
        for num in range(nn,12,1):
            getattr(self,'label_hm'+str(num+1)).setVisible(False)
            getattr(self, 'def'+str(num+1)).setVisible(False)
            getattr(self,'min_hm'+str(num+1)).setVisible(False)
            getattr(self,'max_hm'+str(num+1)).setVisible(False)
            getattr(self,'colormap'+str(num+1)).setVisible(False)
            getattr(self,'d3d2_'+str(num+1)).setVisible(False)
            getattr(self, 'hm_plot'+str(num+1)).setVisible(False)
            getattr(self, 'hm_plot'+str(num+1)+'_2D').setVisible(False)
            getattr(self, 'cm_eg'+str(num+1)).setVisible(False)
            getattr(self, 'hm_play'+str(num+1)).setVisible(False)
            getattr(self, 'hm2d_play'+str(num+1)).setVisible(False)

        #Set all colormaps eg
        self.colormap1.currentIndexChanged.connect(lambda: self.set_colormap('1'))
        self.colormap2.currentIndexChanged.connect(lambda: self.set_colormap('2'))
        self.colormap3.currentIndexChanged.connect(lambda: self.set_colormap('3'))
        self.colormap4.currentIndexChanged.connect(lambda: self.set_colormap('4'))
        self.colormap5.currentIndexChanged.connect(lambda: self.set_colormap('5'))
        self.colormap6.currentIndexChanged.connect(lambda: self.set_colormap('6'))
        self.colormap7.currentIndexChanged.connect(lambda: self.set_colormap('7'))
        self.colormap8.currentIndexChanged.connect(lambda: self.set_colormap('8'))
        self.colormap9.currentIndexChanged.connect(lambda: self.set_colormap('9'))
        self.colormap10.currentIndexChanged.connect(lambda: self.set_colormap('10'))
        self.colormap11.currentIndexChanged.connect(lambda: self.set_colormap('11'))
        self.colormap12.currentIndexChanged.connect(lambda: self.set_colormap('12'))

        for num in range(1,13,1): 
            self.set_colormap(str(num))

        #Change if hm3d2t not selected, then set all widgets related to unlooping/unrolling to not visible
        if 'hm3Dto2D' in  self.organ.mH_settings['measure'].keys():
            if len(self.organ.mH_settings['measure']['hm3Dto2D'].keys())>0:
                hm_ch_cont = list(self.organ.mH_settings['measure']['hm3Dto2D'].keys())[0]
                ch, cont = hm_ch_cont.split('_')
                self.hm_centreline.setText(self.channels[ch]+' ('+ch+'-'+cont+')')
                self.cl4hm = hm_ch_cont
                hide = False
                for cut in ['Cut1','Cut2']: 
                    if cut in [key for key in segm_setup.keys() if 'Cut' in key]:
                        #Hereee!!!
                items_segments = 
                self.segm_use_hm2D.addItems(self.items_segments)
            else: 
                hide = True
        else: 
            hide = True

        if hide: 
            self.all_d3d2.setVisible(False)
            self.lab_hm3d2d.setVisible(False)
            self.hm_centreline.setVisible(False)
            self.lab_hm2d.setVisible(False)
            self.heatmaps2D_play.setVisible(False)
            self.lab_3d2d.setVisible(False)
            self.lab_2d.setVisible(False)
            self.lab_plot2d.setVisible(False)
            self.hm_centreline_status.setVisible(False)
            self.lab_hm2d_settings.setVisible(False)
            self.improve_hm2D.setVisible(False)
            self.segm_use_hm2D.setVisible(False)

            for num in range(1,13,1): 
                getattr(self, 'hm2d_play'+str(num)).setVisible(False)
                getattr(self, 'hm_plot'+str(num)+'_2D').setVisible(False)
                getattr(self, 'd3d2_'+str(num)).setVisible(False)
            
        #Initialise with user settings, if they exist!
        self.user_heatmaps()

    def init_segments(self):
        #Buttons
        self.segments_open.clicked.connect(lambda: self.open_section(name='segments'))
        self.segments_play.setStyleSheet(style_play)
        self.segments_play.setEnabled(False)
        self.q_segments.clicked.connect(lambda: self.help('segments'))
        self.segments_set.clicked.connect(lambda: self.set_segments())

        #Fill color
        self.fillcolor_cut1_segm1.clicked.connect(lambda: self.color_picker(name = 'cut1_segm1'))
        self.fillcolor_cut1_segm2.clicked.connect(lambda: self.color_picker(name = 'cut1_segm2'))
        self.fillcolor_cut1_segm3.clicked.connect(lambda: self.color_picker(name = 'cut1_segm3'))
        self.fillcolor_cut1_segm4.clicked.connect(lambda: self.color_picker(name = 'cut1_segm4'))
        self.fillcolor_cut1_segm5.clicked.connect(lambda: self.color_picker(name = 'cut1_segm5'))
        self.fillcolor_cut2_segm1.clicked.connect(lambda: self.color_picker(name = 'cut2_segm1'))
        self.fillcolor_cut2_segm2.clicked.connect(lambda: self.color_picker(name = 'cut2_segm2'))         
        self.fillcolor_cut2_segm3.clicked.connect(lambda: self.color_picker(name = 'cut2_segm3'))
        self.fillcolor_cut2_segm4.clicked.connect(lambda: self.color_picker(name = 'cut2_segm4'))
        self.fillcolor_cut2_segm5.clicked.connect(lambda: self.color_picker(name = 'cut2_segm5'))                                       

        segm_setup = self.organ.mH_settings['setup']['segm']
        no_cuts = [key for key in segm_setup.keys() if 'Cut' in key]
        palette =  palette_rbg("husl", 10)
        self.segm_btns = {}
        
        for optcut in ['1','2']:
            cutl = 'cut'+optcut
            cutb = 'Cut'+optcut
            if cutb in no_cuts: 
                if 'colors' not in self.organ.mH_settings['setup']['segm'][cutb].keys():
                    colors_initialised = False
                    self.organ.mH_settings['setup']['segm'][cutb]['colors'] = {}
                else: 
                    colors_initialised = True

                lab_names_segm = getattr(self, 'names_segm_'+cutl)
                bb = set_qtextedit_text(lab_names_segm, segm_setup[cutb]['name_segments'], 'segm')
                set_qtextedit_size(lab_names_segm, (100, (bb+1)*25))

                getattr(self, 'obj_segm_'+cutl).setText(segm_setup[cutb]['obj_segm'])
                for nn in range(1,6,1):
                    if nn > bb+1:
                        getattr(self, 'label_'+cutl+'_segm'+str(nn)).setVisible(False)
                        getattr(self, 'fillcolor_'+cutl+'_'+'segm'+str(nn)).setVisible(False)
                    else: 
                        if not colors_initialised: 
                            color = palette[5*(int(optcut)-1)+(nn-1)]
                            self.organ.mH_settings['setup']['segm'][cutb]['colors']['segm'+str(nn)] = color
                        else: 
                            color = self.organ.mH_settings['setup']['segm'][cutb]['colors']['segm'+str(nn)]
                            # print(cutb, str(nn), '- color:', color)
                        btn_color = getattr(self, 'fillcolor_'+cutl+'_'+'segm'+str(nn))
                        color_btn(btn = btn_color, color = color)

                #Add ch-cont combinations to list of cuts to make
                ch_keys = sorted(list(self.organ.mH_settings['setup']['segm'][cutb]['ch_segments'].keys()))
                nn = 1
                for ch in ch_keys: 
                    cont_keys = sorted(self.organ.mH_settings['setup']['segm'][cutb]['ch_segments'][ch])
                    for cont in cont_keys:
                        getattr(self, cutl+'_chcont_segm'+str(nn)).setText(str(nn)+'. '+ch+'_'+cont)
                        getattr(self, cutl+'_play_segm'+str(nn)).setEnabled(False)
                        getattr(self, cutl+'_plot_segm'+str(nn)).setEnabled(False)
                        self.segm_btns[cutb+':'+ch+'_'+cont] = {'num': str(nn), 
                                                                'play': getattr(self, cutl+'_play_segm'+str(nn)),
                                                                'plot': getattr(self, cutl+'_plot_segm'+str(nn))}
                        nn+=1
                #Make invisible the rest of the items
                for el in range(nn,13,1):
                    getattr(self, cutl+'_chcont_segm'+str(el)).setVisible(False)
                    getattr(self, cutl+'_play_segm'+str(el)).setVisible(False)
                    getattr(self, cutl+'_plot_segm'+str(el)).setVisible(False)

            else: 
                getattr(self, 'label_segm_'+cutl).setVisible(False)
                getattr(self, 'names_segm_'+cutl).setVisible(False)
                getattr(self, 'obj_segm_'+cutl).setVisible(False)
                # getattr(self, 'segm_'+cutl+'_plot').setVisible(False)
                for nn in range(1,6,1):
                    getattr(self, 'label_'+cutl+'_segm'+str(nn)).setVisible(False)
                    getattr(self, 'fillcolor_'+cutl+'_'+'segm'+str(nn)).setVisible(False)
                for el in range(1,13,1):
                    getattr(self, cutl+'_chcont_segm'+str(el)).setVisible(False)
                    getattr(self, cutl+'_play_segm'+str(el)).setVisible(False)
                    getattr(self, cutl+'_plot_segm'+str(el)).setVisible(False)
        
        if len(no_cuts) == 1: 
            for aa in range(1,5,1): 
                getattr(self, 'segm_line'+str(aa)).setVisible(False)
            getattr(self, 'radius_segm_cut2').setVisible(False)
            getattr(self, 'radius_val_cut2').setVisible(False)
            getattr(self, 'radius_segm_unit2').setVisible(False)

        # print('Setup segments: ', self.organ.mH_settings['setup']['segm'])
        print('segm_btns:', self.segm_btns)

        self.segm_use_centreline.stateChanged.connect(lambda: self.segm_centreline())
        self.segm_centreline2use.addItems(self.items_centreline)

        #Plot buttons
        self.cut1_plot_segm1.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm1'))
        self.cut1_plot_segm2.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm2'))
        self.cut1_plot_segm3.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm3'))
        self.cut1_plot_segm4.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm4'))
        self.cut1_plot_segm5.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm5'))
        self.cut1_plot_segm6.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm6'))
        self.cut1_plot_segm7.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm7'))
        self.cut1_plot_segm8.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm8'))
        self.cut1_plot_segm9.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm9'))
        self.cut1_plot_segm10.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm10'))
        self.cut1_plot_segm11.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm11'))
        self.cut1_plot_segm12.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_segm12'))

        self.cut2_plot_segm1.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm1'))
        self.cut2_plot_segm2.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm2'))
        self.cut2_plot_segm3.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm3'))
        self.cut2_plot_segm4.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm4'))
        self.cut2_plot_segm5.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm5'))
        self.cut2_plot_segm6.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm6'))
        self.cut2_plot_segm7.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm7'))
        self.cut2_plot_segm8.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm8'))
        self.cut2_plot_segm9.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm9'))
        self.cut2_plot_segm10.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm10'))
        self.cut2_plot_segm11.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm11'))
        self.cut2_plot_segm12.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_segm12'))

        #Initialise with user settings, if they exist!
        self.user_segments()

    def init_sections(self):
        #Buttons
        self.sections_open.clicked.connect(lambda: self.open_section(name='sections'))
        self.sections_play.setStyleSheet(style_play)
        self.sections_play.setEnabled(False)
        self.q_sections.clicked.connect(lambda: self.help('sections'))
        self.sections_set.clicked.connect(lambda: self.set_sections())

        self.fillcolor_cut1_sect1.clicked.connect(lambda: self.color_picker(name = 'cut1_sect1'))
        self.fillcolor_cut1_sect2.clicked.connect(lambda: self.color_picker(name = 'cut1_sect2'))
        self.fillcolor_cut2_sect1.clicked.connect(lambda: self.color_picker(name = 'cut2_sect1'))
        self.fillcolor_cut2_sect2.clicked.connect(lambda: self.color_picker(name = 'cut2_sect2'))    

        self.dir_sect_cut1.clicked.connect(lambda: self.select_extension_plane(cut = 'cut1'))            
        self.dir_sect_cut2.clicked.connect(lambda: self.select_extension_plane(cut = 'cut2'))                                  

        sect_setup = self.organ.mH_settings['setup']['sect']
        no_cuts = [key for key in sect_setup.keys() if 'Cut' in key]
        palette =  palette_rbg("Set2", 4)
        self.sect_btns = {}
        
        for optcut in ['1','2']:
            cutl = 'cut'+optcut
            cutb = 'Cut'+optcut
            if cutb in no_cuts: 
                if 'colors' not in self.organ.mH_settings['setup']['sect'][cutb].keys():
                    colors_initialised = False
                    self.organ.mH_settings['setup']['sect'][cutb]['colors'] = {}
                else: 
                    colors_initialised = True

                lab_names_sect = getattr(self, 'names_sect_'+cutl)
                bb = set_qtextedit_text(lab_names_sect, sect_setup[cutb]['name_sections'], 'sect')
                set_qtextedit_size(lab_names_sect, (100, (bb+1)*25))

                getattr(self, 'sect_cl_'+cutl).addItems(self.items_centreline)
                for nn in range(1,3,1):
                    if not colors_initialised: 
                        color = palette[2*(int(optcut)-1)+(nn-1)]
                        self.organ.mH_settings['setup']['sect'][cutb]['colors']['sect'+str(nn)] = color
                    else: 
                        color = self.organ.mH_settings['setup']['sect'][cutb]['colors']['sect'+str(nn)]
                    btn_color = getattr(self, 'fillcolor_'+cutl+'_'+'sect'+str(nn))
                    color_btn(btn = btn_color, color = color)
                    
                #Add ch-cont combinations to list of cuts to make
                ch_keys = sorted(list(self.organ.mH_settings['setup']['sect'][cutb]['ch_sections'].keys()))
                nn = 1
                for ch in ch_keys: 
                    cont_keys = sorted(self.organ.mH_settings['setup']['sect'][cutb]['ch_sections'][ch])
                    for cont in cont_keys:
                        getattr(self, cutl+'_chcont_sect'+str(nn)).setText(str(nn)+'. '+ch+'_'+cont)
                        getattr(self, cutl+'_play_sect'+str(nn)).setEnabled(False)
                        getattr(self, cutl+'_plot_sect'+str(nn)).setEnabled(False)
                        self.sect_btns[cutb+':'+ch+'_'+cont] = {'num': str(nn), 
                                                                'play': getattr(self, cutl+'_play_sect'+str(nn)),
                                                                'plot': getattr(self, cutl+'_plot_sect'+str(nn))}
                        nn+=1
                #Make invisible the rest of the items
                for el in range(nn,13,1):
                    getattr(self, cutl+'_chcont_sect'+str(el)).setVisible(False)
                    getattr(self, cutl+'_play_sect'+str(el)).setVisible(False)
                    getattr(self, cutl+'_plot_sect'+str(el)).setVisible(False)

            else: 
                getattr(self, 'label_sect_'+cutl).setVisible(False)
                getattr(self, 'names_sect_'+cutl).setVisible(False)
                getattr(self, 'obj_sect_'+cutl).setVisible(False)
                getattr(self, 'sect_cl_'+cutl).setVisible(False)
                getattr(self, 'blank1_'+cutl).setVisible(False)
                getattr(self, 'lab_nPoints_'+cutl).setVisible(False)
                getattr(self, 'sect_nPoints_'+cutl).setVisible(False)
                getattr(self, 'blank2_'+cutl).setVisible(False)
                getattr(self, 'lab_nRes_'+cutl).setVisible(False)
                getattr(self, 'sect_nRes_'+cutl).setVisible(False)    
                getattr(self, 'lab_cl_ext_'+cutl).setVisible(False)
                getattr(self, 'lab_axis_'+cutl).setVisible(False)
                getattr(self, 'radio_roi_'+cutl).setVisible(False)
                getattr(self, 'radio_stack_'+cutl).setVisible(False)
                getattr(self, 'lab_dir_'+cutl).setVisible(False)
                getattr(self, 'sect_dir_'+cutl).setVisible(False)
                getattr(self, 'lab_colors_'+cutl).setVisible(False)
                getattr(self, 'cl_ext_'+cutl).setVisible(False)
                getattr(self, 'dir_sect_'+cutl).setVisible(False)
                for nn in range(1,3,1):
                    getattr(self, 'label_'+cutl+'_sect'+str(nn)).setVisible(False)
                    getattr(self, 'fillcolor_'+cutl+'_'+'sect'+str(nn)).setVisible(False)
                for el in range(1,13,1):
                    getattr(self, cutl+'_chcont_sect'+str(el)).setVisible(False)
                    getattr(self, cutl+'_play_sect'+str(el)).setVisible(False)
                    getattr(self, cutl+'_plot_sect'+str(el)).setVisible(False)

        if len(no_cuts) == 1: 
            for aa in range(1,5,1): 
                getattr(self, 'sect_line'+str(aa)).setVisible(False)

        self.radio_roi_cut1.setChecked(True)
        self.radio_roi_cut2.setChecked(True)

        # print('Setup Sections: ', self.organ.mH_settings['setup']['sect'])
        print('sect_btns:', self.sect_btns)

        #Plot buttons
        self.cut1_plot_sect1.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect1'))
        self.cut1_plot_sect2.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect2'))
        self.cut1_plot_sect3.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect3'))
        self.cut1_plot_sect4.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect4'))
        self.cut1_plot_sect5.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect5'))
        self.cut1_plot_sect6.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect6'))
        self.cut1_plot_sect7.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect7'))
        self.cut1_plot_sect8.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect8'))
        self.cut1_plot_sect9.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect9'))
        self.cut1_plot_sect10.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect10'))
        self.cut1_plot_sect11.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect11'))
        self.cut1_plot_sect12.clicked.connect(lambda: self.plot_segm_sect(btn='cut1_sect12'))

        self.cut2_plot_sect1.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect1'))
        self.cut2_plot_sect2.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect2'))
        self.cut2_plot_sect3.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect3'))
        self.cut2_plot_sect4.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect4'))
        self.cut2_plot_sect5.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect5'))
        self.cut2_plot_sect6.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect6'))
        self.cut2_plot_sect7.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect7'))
        self.cut2_plot_sect8.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect8'))
        self.cut2_plot_sect9.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect9'))
        self.cut2_plot_sect10.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect10'))
        self.cut2_plot_sect11.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect11'))
        self.cut2_plot_sect12.clicked.connect(lambda: self.plot_segm_sect(btn='cut2_sect12'))

        #CL extension buttons
        self.cl_ext_cut1.clicked.connect(lambda: self.plot_cl_ext(cut = 'cut1'))
        self.cl_ext_cut2.clicked.connect(lambda: self.plot_cl_ext(cut = 'cut2'))

        #Initialise with user settings, if they exist!
        self.user_sections()

    def init_segm_sect(self): 
        #Buttons
        self.segm_sect_open.clicked.connect(lambda: self.open_section(name='segm_sect'))
        self.segm_sect_play.setStyleSheet(style_play)
        self.segm_sect_play.setEnabled(False)
        self.q_segm_sect.clicked.connect(lambda: self.help('segm_sect'))
        # self.segm_sect_set.clicked.connect(lambda: self.set_segm_sect())

        #sCut1_Cut1
        self.fillcolor_sCut1_Cut1_segm1_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm1_sect1'))
        self.fillcolor_sCut1_Cut1_segm1_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm1_sect2'))
        self.fillcolor_sCut1_Cut1_segm2_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm2_sect1'))
        self.fillcolor_sCut1_Cut1_segm2_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm2_sect2'))
        self.fillcolor_sCut1_Cut1_segm3_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm3_sect1'))
        self.fillcolor_sCut1_Cut1_segm3_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm3_sect2'))
        self.fillcolor_sCut1_Cut1_segm4_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm4_sect1'))
        self.fillcolor_sCut1_Cut1_segm4_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm4_sect2'))
        self.fillcolor_sCut1_Cut1_segm5_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm5_sect1'))
        self.fillcolor_sCut1_Cut1_segm5_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut1_segm5_sect2'))

        #sCut1_Cut2
        self.fillcolor_sCut1_Cut2_segm1_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm1_sect1'))
        self.fillcolor_sCut1_Cut2_segm1_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm1_sect2'))
        self.fillcolor_sCut1_Cut2_segm2_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm2_sect1'))
        self.fillcolor_sCut1_Cut2_segm2_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm2_sect2'))
        self.fillcolor_sCut1_Cut2_segm3_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm3_sect1'))
        self.fillcolor_sCut1_Cut2_segm3_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm3_sect2'))
        self.fillcolor_sCut1_Cut2_segm4_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm4_sect1'))
        self.fillcolor_sCut1_Cut2_segm4_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm4_sect2'))
        self.fillcolor_sCut1_Cut2_segm5_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm5_sect1'))
        self.fillcolor_sCut1_Cut2_segm5_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut1_Cut2_segm5_sect2'))

        #sCut2_Cut1
        self.fillcolor_sCut2_Cut1_segm1_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm1_sect1'))
        self.fillcolor_sCut2_Cut1_segm1_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm1_sect2'))
        self.fillcolor_sCut2_Cut1_segm2_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm2_sect1'))
        self.fillcolor_sCut2_Cut1_segm2_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm2_sect2'))
        self.fillcolor_sCut2_Cut1_segm3_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm3_sect1'))
        self.fillcolor_sCut2_Cut1_segm3_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm3_sect2'))
        self.fillcolor_sCut2_Cut1_segm4_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm4_sect1'))
        self.fillcolor_sCut2_Cut1_segm4_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm4_sect2'))
        self.fillcolor_sCut2_Cut1_segm5_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm5_sect1'))
        self.fillcolor_sCut2_Cut1_segm5_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut1_segm5_sect2'))

        #sCut2_Cut2
        self.fillcolor_sCut2_Cut2_segm1_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm1_sect1'))
        self.fillcolor_sCut2_Cut2_segm1_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm1_sect2'))
        self.fillcolor_sCut2_Cut2_segm2_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm2_sect1'))
        self.fillcolor_sCut2_Cut2_segm2_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm2_sect2'))
        self.fillcolor_sCut2_Cut2_segm3_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm3_sect1'))
        self.fillcolor_sCut2_Cut2_segm3_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm3_sect2'))
        self.fillcolor_sCut2_Cut2_segm4_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm4_sect1'))
        self.fillcolor_sCut2_Cut2_segm4_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm4_sect2'))
        self.fillcolor_sCut2_Cut2_segm5_sect1.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm5_sect1'))
        self.fillcolor_sCut2_Cut2_segm5_sect2.clicked.connect(lambda: self.color_picker(name = 'sCut2_Cut2_segm5_sect2'))

        segm_sect_setup = self.organ.mH_settings['setup']['segm-sect']
        segm_setup = self.organ.mH_settings['setup']['segm']
        # no_cuts_segm = [key for key in segm_setup.keys() if 'Cut' in key]
        sect_setup = self.organ.mH_settings['setup']['sect']
        # no_cuts_sect = [key for key in sect_setup.keys() if 'Cut' in key]
        self.segm_sect_btns = {}

        palettes = ['Accent', 'Dark2','Paired', 'Set1']
        print('SETTINGSS:', segm_sect_setup, '\n', segm_setup, '\n', sect_setup)

        nun = 0
        for cut in ['Cut1', 'Cut2']: 
            scut = 's'+cut
            if scut in segm_sect_setup.keys(): 
                n_segm = segm_setup[cut]['no_segments']
                print('Aja -', scut, ' In ')
                for rcut in ['Cut1', 'Cut2']:
                    if rcut in segm_sect_setup[scut].keys():
                        n_sect = sect_setup[rcut]['no_sections']
                        print('Aja -', rcut, ' In ')
                        if 'colors' not in self.organ.mH_settings['setup']['segm-sect'][scut][rcut].keys():
                            colors_initialised = False
                            self.organ.mH_settings['setup']['segm-sect'][scut][rcut]['colors'] = {}
                        else: 
                            colors_initialised = True

                        lab_names_segm = getattr(self, 'names_'+scut+'_'+rcut+'_segm')
                        bbsegm = set_qtextedit_text(lab_names_segm, segm_setup[cut]['name_segments'], 'segm')
                        set_qtextedit_size(lab_names_segm, (100, (bbsegm+1)*25))

                        lab_names_sect = getattr(self, 'names_'+scut+'_'+rcut+'_sect')
                        bbsect = set_qtextedit_text(lab_names_sect, sect_setup[rcut]['name_sections'], 'sect')
                        set_qtextedit_size(lab_names_sect, (100, (bbsect+1)*25))

                        palette = palette_rbg(palettes[nun], 10); nun+=1
                        num = 1
                        for ns in range(1,6,1):#n_segm+1,1):
                            for nr in range(1,3,1):#n_sect+1,1):
                                if ns > bbsegm+1: 
                                    # label_sCut1_Cut1_segm1_sect1
                                    getattr(self, 'label_'+scut+'_'+rcut+'_segm'+str(ns)+'_sect'+str(nr)).setVisible(False)
                                    getattr(self, 'fillcolor_'+scut+'_'+rcut+'_segm'+str(ns)+'_sect'+str(nr)).setVisible(False)
                                else:
                                    if not colors_initialised: 
                                        color = palette[num-1]
                                        self.organ.mH_settings['setup']['segm-sect'][scut][rcut]['colors']['segm'+str(ns)+'_sect'+str(nr)] = color
                                    else: 
                                        color = self.organ.mH_settings['setup']['segm-sect'][scut][rcut]['colors']['segm'+str(ns)+'_sect'+str(nr)]
                                    btn_color = getattr(self, 'fillcolor_'+scut+'_'+rcut+'_segm'+str(ns)+'_sect'+str(nr))
                                    print('color:', color)
                                    color_btn(btn = btn_color, color = color)
                                num+=1

                        ch_conts = sorted(self.organ.mH_settings['setup']['segm-sect'][scut][rcut]['ch_segm_sect'])
                        mm = 1
                        for ch_cont in ch_conts: 
                            #scut1_cut1_chcont_sect1
                            getattr(self, scut.lower()+'_'+rcut.lower()+'_chcont_sect'+str(mm)).setText(str(mm)+'. '+ch_cont)
                            #scut1_cut1_play_sect1
                            getattr(self, scut.lower()+'_'+rcut.lower()+'_play_sect'+str(mm)).setEnabled(False)
                            #scut1_cut1_plot_sect1
                            getattr(self,  scut.lower()+'_'+rcut.lower()+'_plot_sect'+str(mm)).setEnabled(False)
                            self.segm_sect_btns[scut+'_o_'+rcut+':'+ch_cont] = {'num': str(mm), 
                                                                            'play': getattr(self, scut.lower()+'_'+rcut.lower()+'_play_sect'+str(mm)),
                                                                            'plot': getattr(self, scut.lower()+'_'+rcut.lower()+'_plot_sect'+str(mm))}
                            mm+=1
                        #Make invisible the rest of the items
                        for el in range(mm,13,1):
                            getattr(self, scut.lower()+'_'+rcut.lower()+'_chcont_sect'+str(el)).setVisible(False)
                            getattr(self, scut.lower()+'_'+rcut.lower()+'_play_sect'+str(el)).setVisible(False)
                            getattr(self, scut.lower()+'_'+rcut.lower()+'_plot_sect'+str(el)).setVisible(False)

                    else: 
                        print('Aja -', rcut, ' Out ')
                        getattr(self, 'names_'+scut+'_'+rcut+'_segm').setVisible(False)
                        getattr(self, 'names_'+scut+'_'+rcut+'_sect').setVisible(False)
                        getattr(self, 'wcolor_'+scut+'_'+rcut).setVisible(False)
                        getattr(self, 'wbuttons_'+scut+'_'+rcut).setVisible(False)
                        getattr(self, 'segm_sect_line_'+scut+'_1').setVisible(False)
                        getattr(self, 'segm_sect_line_'+scut+'_2').setVisible(False)
                        getattr(self, 'segm_sect_line_'+scut+'_3').setVisible(False)
            else: 
                print('-', scut, ' Out ')
                getattr(self, 'segm_sect_line_sCut1_sCut2_1').setVisible(False)
                getattr(self, 'segm_sect_line_sCut1_sCut2_2').setVisible(False)
                getattr(self, 'segm_sect_line_sCut1_sCut2_3').setVisible(False)
                getattr(self, 'segm_sect_line_sCut1_sCut2_4').setVisible(False)
                getattr(self, 'segm_sect_line_sCut2_1').setVisible(False)
                getattr(self, 'segm_sect_line_sCut2_2').setVisible(False)
                getattr(self, 'segm_sect_line_sCut2_3').setVisible(False)
                for rcut in ['Cut1', 'Cut2']:
                    getattr(self, 'names_'+scut+'_'+rcut+'_segm').setVisible(False)
                    getattr(self, 'names_'+scut+'_'+rcut+'_sect').setVisible(False)
                    getattr(self, 'wcolor_'+scut+'_'+rcut).setVisible(False)
                    getattr(self, 'wbuttons_'+scut+'_'+rcut).setVisible(False)

        print('segm_sect_btns:', self.segm_sect_btns)
        print('mH-colors:', self.organ.mH_settings['setup']['segm-sect'])

        #Plot buttons
        self.scut1_cut1_plot_sect1.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect1'))
        self.scut1_cut1_plot_sect2.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect2'))
        self.scut1_cut1_plot_sect3.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect3'))
        self.scut1_cut1_plot_sect4.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect4'))
        self.scut1_cut1_plot_sect5.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect5'))
        self.scut1_cut1_plot_sect6.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect6'))
        self.scut1_cut1_plot_sect7.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect7'))
        self.scut1_cut1_plot_sect8.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect8'))
        self.scut1_cut1_plot_sect9.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect9'))
        self.scut1_cut1_plot_sect10.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect10'))
        self.scut1_cut1_plot_sect11.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect11'))
        self.scut1_cut1_plot_sect12.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut1_plot_sect12'))

        self.scut1_cut2_plot_sect1.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect1'))
        self.scut1_cut2_plot_sect2.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect2'))
        self.scut1_cut2_plot_sect3.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect3'))
        self.scut1_cut2_plot_sect4.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect4'))
        self.scut1_cut2_plot_sect5.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect5'))
        self.scut1_cut2_plot_sect6.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect6'))
        self.scut1_cut2_plot_sect7.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect7'))
        self.scut1_cut2_plot_sect8.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect8'))
        self.scut1_cut2_plot_sect9.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect9'))
        self.scut1_cut2_plot_sect10.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect10'))
        self.scut1_cut2_plot_sect11.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect11'))
        self.scut1_cut2_plot_sect12.clicked.connect(lambda: self.plot_segm_section(btn='scut1_cut2_plot_sect12'))

        self.scut2_cut1_plot_sect1.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect1'))
        self.scut2_cut1_plot_sect2.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect2'))
        self.scut2_cut1_plot_sect3.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect3'))
        self.scut2_cut1_plot_sect4.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect4'))
        self.scut2_cut1_plot_sect5.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect5'))
        self.scut2_cut1_plot_sect6.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect6'))
        self.scut2_cut1_plot_sect7.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect7'))
        self.scut2_cut1_plot_sect8.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect8'))
        self.scut2_cut1_plot_sect9.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect9'))
        self.scut2_cut1_plot_sect10.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect10'))
        self.scut2_cut1_plot_sect11.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect11'))
        self.scut2_cut1_plot_sect12.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut1_plot_sect12'))

        self.scut2_cut2_plot_sect1.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect1'))
        self.scut2_cut2_plot_sect2.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect2'))
        self.scut2_cut2_plot_sect3.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect3'))
        self.scut2_cut2_plot_sect4.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect4'))
        self.scut2_cut2_plot_sect5.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect5'))
        self.scut2_cut2_plot_sect6.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect6'))
        self.scut2_cut2_plot_sect7.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect7'))
        self.scut2_cut2_plot_sect8.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect8'))
        self.scut2_cut2_plot_sect9.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect9'))
        self.scut2_cut2_plot_sect10.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect10'))
        self.scut2_cut2_plot_sect11.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect11'))
        self.scut2_cut2_plot_sect12.clicked.connect(lambda: self.plot_segm_section(btn='scut2_cut2_plot_sect12'))

        #Initialise with user settings, if they exist!
        self.user_segm_sect()

    def init_user_param(self): 

        self.user_params_open.clicked.connect(lambda: self.open_section(name = 'user_params'))

        user_params = self.organ.mH_settings['setup']['params']
        measure = self.organ.mH_settings['measure']
        widgets_params = {'continuous': {'enable': False, 'n_params': 0}, 
                          'descriptive': {'enable': False,'n_params': 0},  
                          'categorical': {'enable': False,'n_params': 0}}
        gui_user_params = {'continuous': {}, 
                           'descriptive': {}, 
                           'categorical': {}}
        
        for key in user_params: 
            if int(key)>5: 
                ptype = user_params[key]['type']
                if ptype == 'categorical':
                    if not widgets_params[ptype]['enable']:
                        widgets_params[ptype]['enable'] = True
                    label = user_params[key]['l']
                    short = user_params[key]['s']
                    categories = user_params[key]['categories']
                    gui_user_params['categorical'][short] = {}
                    nn = 1
                    for item in measure[short].keys(): 
                        getattr(self, 'lab_categorical'+str(nn)).setText(label)
                        getattr(self, 'lab_categorical'+str(nn)).setEnabled(True)
                        getattr(self, 'tiss_cont_categorical'+str(nn)).setText(item)
                        getattr(self, 'tiss_cont_categorical'+str(nn)).setEnabled(True)
                        getattr(self, 'value_categorical'+str(nn)).addItems(categories)
                        getattr(self, 'value_categorical'+str(nn)).setEnabled(True)
                        gui_user_params['categorical'][short][item] = {'num': nn}
                        nn+=1
                    for aa in range(nn,7,1):
                        getattr(self, 'lab_categorical'+str(aa)).setVisible(False)
                        getattr(self, 'tiss_cont_categorical'+str(aa)).setVisible(False)
                        getattr(self, 'value_categorical'+str(aa)).setVisible(False)
                    
                elif ptype == 'continuous' or ptype == 'descriptive': 
                    if not widgets_params[ptype]['enable']:
                        widgets_params[ptype]['enable'] = True
                    label = user_params[key]['l']
                    short = user_params[key]['s']
                    gui_user_params[ptype][short] = {}
                    mm = 1
                    for item in measure[short].keys(): 
                        getattr(self, 'lab_'+ptype+str(mm)).setText(label)
                        getattr(self, 'lab_'+ptype+str(mm)).setEnabled(True)
                        getattr(self, 'tiss_cont_'+ptype+str(mm)).setText(item)
                        getattr(self, 'tiss_cont_'+ptype+str(mm)).setEnabled(True)
                        getattr(self, 'value_'+ptype+str(mm)).setEnabled(True)
                        gui_user_params[ptype][short][item] = {'num': mm, }
                        mm+=1
                    for bb in range(mm,7,1):
                        getattr(self, 'lab_'+ptype+str(bb)).setVisible(False)
                        getattr(self, 'tiss_cont_'+ptype+str(bb)).setVisible(False)
                        getattr(self, 'value_'+ptype+str(bb)).setVisible(False)
                else: #ptype == '
                    print('other?')
        
        at_least_one = False
        for mtype in widgets_params: 
            if widgets_params[mtype]['enable']: 
                getattr(self, mtype).setEnabled(True)
                at_least_one = True
            else: 
                getattr(self, mtype).setVisible(False)
        
        if not at_least_one: 
            self.user_params_widget.setVisible(False)
            self.user_params_open.setVisible(False)
            self.label_user_params.setVisible(False)
            self.spacer_user_params.setVisible(False)
        else: 
            self.continuous_set.clicked.connect(lambda: self.set_user_user_params(ptype='continuous'))
            self.categorical_set.clicked.connect(lambda: self.set_user_user_params(ptype='categorical'))
            self.descriptive_set.clicked.connect(lambda: self.set_user_user_params(ptype='descriptive'))

        self.gui_key_user_params = gui_user_params
        #Initialise with user settings, if they exist!
        self.user_user_params()

    def init_results_table(self): 
        self.results_open.clicked.connect(lambda: self.open_section(name = 'results'))

        #Setup results
        self.fill_results()
        self.results_save.clicked.connect(lambda: self.save_results())

        #Init measure_status
        self.user_measure_whole()

    def init_plot_results(self):
        self.plot_open.clicked.connect(lambda: self.open_section(name = 'plot')) 
        self.open_section(name='plot')

    def init_workflow(self):
        #Setup workflow
        self.fill_workflow()

    def update_status(self, root_dict, items, fillcolor, override=False):
        update_status(root_dict, items, fillcolor, override)
        
    #Functions to fill sections according to user's selections
    def user_keeplargest(self): 
        wf_info = self.organ.mH_settings['wf_info']
        workflow = self.organ.workflow['morphoHeart']['MeshesProc']['A-Create3DMesh']
        if 'keep_largest' in wf_info.keys():
            done_all = []
            for ch in wf_info['keep_largest']: 
                done = []
                for cont in ['int', 'tiss', 'ext']:
                    cB = getattr(self, 'kl_'+ch+'_'+cont)
                    cB.setChecked(wf_info['keep_largest'][ch][cont])
                    done.append(workflow[ch][cont]['Status'])
                if all(flag == 'DONE' for flag in done):
                    plot_btn = getattr(self, 'keeplargest_plot_'+ch)
                    plot_btn.setEnabled(True)
                    done_all.append(True)
                else: 
                    done_all.append(False)

            if all(done_all): 
                #Toggle Button
                self.keeplargest_set.setChecked(True)
                self.keeplargest_play.setChecked(True)
                #Enable other buttons
                self.keeplargest_plot.setEnabled(True)
                #Update Status in GUI
                self.update_status(None, 'DONE', self.keeplargest_status, override=True)
                self.keeplargest_open.setChecked(True)
                self.open_section(name = 'keeplargest')
            elif any(done_all):
                #Update Status in GUI
                self.update_status(None, 'Initialised', self.keeplargest_status, override=True)
            else: 
                pass
            
            #Run Set Function 
            self.set_keeplargest()
        else: 
            pass
        
    def user_clean(self): 
        wf_info = self.organ.mH_settings['wf_info']
        if 'cleanup' in wf_info.keys():
            done_all = []
            for ch in wf_info['cleanup']:
                if 'ch' in ch:
                    done = []
                    workflow_ch = self.organ.workflow['morphoHeart']['ImProc'][ch]['E-CleanCh']
                    for cont in wf_info['cleanup'][ch]['cont']:
                        cB = getattr(self, 'clean_'+ch+'_'+cont)
                        cB.setChecked(True)
                        done.append(workflow_ch['Info'][cont]['Status'])
                    with_ch = getattr(self, 'clean_withch_'+ch)
                    with_ch.setCurrentText(wf_info['cleanup'][ch]['with_ch'])
                    with_cont = getattr(self, 'clean_withcont_'+ch)
                    with_cont.setCurrentText(wf_info['cleanup'][ch]['with_cont'])
                    inv = getattr(self, 'inverted_'+ch)
                    inv.setChecked(wf_info['cleanup'][ch]['inverted'])
                    
                    if all(flag == 'DONE' for flag in done):
                        plot_btn = getattr(self, 'cleanup_plot_'+ch)
                        plot_btn.setEnabled(True)
                        done_all.append(True)
                    else: 
                        done_all.append(False)
        
            if wf_info['cleanup']['plot2d']: 
                self.clean_plot2d.setChecked(True)
                self.clean_n_slices.setValue(wf_info['cleanup']['n_slices'])

            if all(done_all):
                #Toggle Button
                self.cleanup_set.setChecked(True)
                self.cleanup_play.setChecked(True)
                #Enable other buttons
                self.clean_plot.setEnabled(True)
                #Update Status in GUI
                self.update_status(None, 'DONE', self.cleanup_status, override=True)
                self.cleanup_open.setChecked(True)
                self.open_section(name = 'cleanup')
            elif any(done_all):
                #Update Status in GUI
                self.update_status(None, 'Initialised', self.cleanup_status, override=True)
            
            #Run Set Function 
            self.set_clean() 
        else: 
            pass

    def user_trimming(self): 
        wf_info = self.organ.mH_settings['wf_info']
        workflow = self.organ.workflow['morphoHeart']['MeshesProc']['B-TrimMesh']
        if 'trimming' in wf_info.keys():
            done_all = []
            for ch in wf_info['trimming']['top']['chs']:
                done_ch = []
                for side in ['top', 'bottom']: 
                    done_cont = [] 
                    for cont in ['int', 'tiss', 'ext']:
                        cB = getattr(self, side[0:3]+'_'+ch+'_'+cont)
                        cB.setChecked(wf_info['trimming'][side]['chs'][ch][cont])
                        done_cont.append(workflow[ch][cont]['Status'])
                    if all(flag == 'DONE' for flag in done_cont) or all(flag == 'DONE-NoCut' for flag in done_cont): 
                        done_ch.append(True)
                    else: 
                        done_ch.append(False)
                    getattr(self, side[0:3]+'_cut_opts').setCurrentText(wf_info['trimming'][side]['object'])
                
                if all(done_ch): 
                    plot_btn = getattr(self, 'trimming_plot_'+ch)
                    plot_btn.setEnabled(True)
                    done_all.append(True)
                else: 
                    done_all.append(False)
            
            if all(done_all):
                #Toggle Button
                self.trimming_set.setChecked(True)
                self.trimming_play.setChecked(True)
                #Update Status in GUI
                self.update_status(None, 'DONE', self.trimming_status, override=True)
                self.trimming_open.setChecked(True)
                self.open_section(name = 'trimming')
            elif any(done_all):
                #Update Status in GUI
                self.update_status(None, 'Initialised', self.trimming_status, override=True)
            else: 
                pass
        
            #Run Set Function 
            self.set_trim(init = True)
        else: 
            pass
            
    def user_orientation(self): 
        wf_info = self.organ.mH_settings['wf_info']
        workflow = self.organ.workflow['morphoHeart']['MeshesProc']['A-Set_Orientation']
        if 'orientation' in wf_info.keys():
            #Organ/ROI
            reorient = getattr(self, 'roi_reorient')
            try: 
                reorient.setChecked(wf_info['orientation']['roi']['reorient'])
            except: 
                reorient.setChecked(wf_info['orientation']['roi']['rotate'])
            if reorient.isChecked(): 
                method = wf_info['orientation']['roi']['method']
                if method == 'Centreline':
                    self.radio_centreline.setChecked(True)
                    self.centreline_orientation.setCurrentText(wf_info['orientation']['roi']['centreline'])
                    self.plane_orient.setCurrentText(wf_info['orientation']['roi']['plane_orient'])
                    self.vector_orient.setCurrentText(wf_info['orientation']['roi']['vector_orient']) 
                else: 
                    self.radio_manual.setChecked(True)
                    self.reorient_angles.setText(wf_info['orientation']['roi']['angles'])

            for item in ['Stack', 'ROI']:
                if workflow[item] == 'DONE':
                    getattr(self, item.lower()+'_orient_plot').setEnabled(True)
            
            #Update Status in GUI
            if workflow['Status'] == 'Initialised' or 'DONE': 
                #Toggle Button
                self.orientation_set.setChecked(True)
                self.orientation_play.setChecked(True)
            if workflow['Status'] == 'DONE': 
                self.orient_open.setChecked(True)
                self.open_section(name = 'orient')
            #Update Status in GUI
            self.update_status(workflow, ['Status'], self.orient_status)

            #Run Set Function 
            self.set_orientation(init=True)
        else: 
            pass
    
    def user_chNS(self):
        wf_info = self.organ.mH_settings['wf_info']
        if 'chNS' in wf_info.keys():
            if wf_info['chNS']['plot2d']: 
                self.chNS_plot2d.setChecked(True)
                self.chNS_n_slices.setValue(wf_info['chNS']['n_slices'])

            workflow = self.organ.workflow['morphoHeart']['ImProc']['chNS']['D-S3Create']['Status']
            if workflow == 'DONE': 
                plot_btn = getattr(self, 'chNS_plot')
                plot_btn.setEnabled(True)
                #Toggle Button
                self.chNS_set.setChecked(True)
                #Update Status in GUI
                self.update_status(None, 'DONE', self.chNS_status, override=True)
                self.chNS_play.setChecked(True)
                self.chNS_open.setChecked(True)
                self.open_section(name = 'chNS')

            #Run Set Function 
            self.set_chNS()
        else: 
            pass

    def user_summary_whole(self): 
        wf_info = self.organ.mH_settings['wf_info']
        workflow = self.organ.workflow['morphoHeart']['MeshesProc']['A-Create3DMesh']

        for ch in self.channels.keys():
            if 'NS' not in ch: 
                for cont in ['int', 'tiss', 'ext']: 
                    alpha_spin = getattr(self, 'alpha_'+ch+'_'+cont+'f')
                    try: 
                        alpha_val = self.organ.mH_settings['setup']['alpha'][ch][cont]
                    except: 
                        alpha_val = 0.05
                    alpha_spin.setValue(alpha_val)

                    if workflow[ch][cont]['Status'] == 'DONE':
                        getattr(self, 'summary_whole_plot_'+ch).setEnabled(True)
            else: 
                if workflow[ch]['Status'] == 'DONE':
                    for cont in ['int', 'tiss', 'ext']: 
                        alpha_spin = getattr(self, 'alpha_'+ch+'_'+cont+'f')
                        try: 
                            alpha_val = self.organ.mH_settings['setup']['chNS']['alpha'][cont]
                        except: 
                            alpha_val = 0.05
                        alpha_spin.setValue(alpha_val)

                        getattr(self, 'summary_whole_plot_'+ch).setEnabled(True)

    def user_measure_whole(self): 
        measurements = self.organ.mH_settings['measure']
        whole_done = []
        for index, val in self.df_res.iterrows():
            var, tiss, _, = index
            if 'whole' in tiss and var != 'Centreline': 
                if val[0] != 'TBO': 
                    whole_done.append(True)
                else:
                    whole_done.append(False)

        if all(whole_done): 
            self.update_status(None, 'DONE', self.measure_whole_status, override=True)
            self.measure_wholeAll_play.setChecked(True)
        elif any(whole_done): 
            self.update_status(None, 'Initialised', self.measure_whole_status, override=True)
        else: 
            self.update_status(None, 'NI', self.measure_whole_status, override=True)
        
    def user_centreline(self): 

        wf = self.organ.workflow['morphoHeart']['MeshesProc']['C-Centreline']
        wf_info = self.organ.mH_settings['wf_info']
        if 'centreline' in wf_info.keys():
            self.tolerance.setValue(wf_info['centreline']['SimplifyMesh']['tol'])
            self.cB_voronoi.setChecked(wf_info['centreline']['vmtk_CL']['voronoi'])
            self.nPoints.setValue(wf_info['centreline']['buildCL']['nPoints'])
            self.cB_same_planes.setChecked(wf_info['centreline']['SimplifyMesh']['same_planes'])
            #Enable set button 
            plot_btn = getattr(self, 'centreline_set')
            plot_btn.setEnabled(True)
            #Enable button for clean
            plot_btn = getattr(self, 'centreline_clean_play')
            plot_btn.setEnabled(True)

            cl_to_extract = self.organ.mH_settings['measure']['CL']
            cl_keys = list(cl_to_extract.keys())
            directory = self.organ.dir_res(dir ='centreline')
            for nn in range(len(cl_keys)):
                ch, cont = cl_keys[nn].split('_')[0:-1]
                if wf['SimplifyMesh'][ch][cont]['Status'] == 'DONE':
                    #Update Status in GUI
                    status_sq = getattr(self, 'clClean_status'+str(nn+1))
                    self.update_status(wf, ['SimplifyMesh',ch,cont,'Status'], status_sq)
                    #Enable button for plot
                    plot_btn = getattr(self, 'cl_clean_plot'+str(nn+1))
                    plot_btn.setEnabled(True)
                    #Enable button for ML
                    plot_btn = getattr(self, 'centreline_ML_play')
                    plot_btn.setEnabled(True)
                    #Check button
                    self.centreline_clean_play.setChecked(True)

                if self.organ.mH_settings['wf_info']['centreline']['dirs'] != None: 
                    if ch in self.organ.mH_settings['wf_info']['centreline']['dirs'].keys():
                        if cont in self.organ.mH_settings['wf_info']['centreline']['dirs'][ch].keys():
                            name_ML = self.organ.mH_settings['wf_info']['centreline']['dirs'][ch][cont]['dir_meshLabMesh']
                            mesh_dir = directory / name_ML
                            if mesh_dir.is_file():
                                #Update Status in GUI
                                status_sq = getattr(self, 'meshLab_status'+str(nn+1))
                                self.update_status(None, 'DONE', status_sq, override=True)
                                #Enable button for vmtk
                                plot_btn = getattr(self, 'centreline_vmtk_play')
                                plot_btn.setEnabled(True)
                                #Check button
                                self.centreline_ML_play.setChecked(True)

                if wf['vmtk_CL'][ch][cont]['Status'] == 'DONE': 
                    #Update Status in GUI
                    status_sq = getattr(self, 'vmtk_status'+str(nn+1))
                    self.update_status(wf, ['vmtk_CL',ch,cont,'Status'], status_sq)
                    #Enable button for select
                    plot_btn = getattr(self, 'centreline_select')
                    plot_btn.setEnabled(True)
                    #Check button
                    self.centreline_vmtk_play.setChecked(True)
                
                if wf['buildCL'][ch][cont]['Status'] == 'DONE': 
                    #Update Status in GUI
                    status_sq = getattr(self, 'opt_cl_status'+str(nn+1))
                    self.update_status(wf, ['buildCL',ch,cont,'Status'], status_sq)
                    #Enable button for plot
                    plot_btn = getattr(self, 'cl_plot'+str(nn+1))
                    plot_btn.setEnabled(True)
                    #Check button
                    self.centreline_select.setChecked(True)

                    value = wf_info['centreline']['buildCL']['connect_cl'][ch+'_'+cont]
                    valuef = value.split('-')[0]
                    getattr(self, 'opt_cl'+str(nn+1)).setText(valuef)

                    self.centreline_open.setChecked(True)
                    self.open_section(name = 'centreline')
            
            #Update Status in GUI
            self.update_status(wf, ['Status'], self.centreline_status)

            #Run Set Function 
            self.set_centreline(init=True)
        else: 
            pass

    def user_heatmaps(self): 
        wf = self.organ.workflow['morphoHeart']['MeshesProc']
        wf_info = self.organ.mH_settings['wf_info']
        at_least_one = False
        if 'heatmaps' in wf_info.keys():
            print('wf_info[heatmaps]:', wf_info['heatmaps'])

            for item in self.hm_btns.keys(): 
                nn = self.hm_btns[item]['num']
                getattr(self, 'def'+str(nn)).setChecked(wf_info['heatmaps'][item]['default'])
                getattr(self, 'min_hm'+str(nn)).setValue(wf_info['heatmaps'][item]['min_val'])
                getattr(self, 'max_hm'+str(nn)).setValue(wf_info['heatmaps'][item]['max_val'])
                getattr(self, 'colormap'+str(nn)).setCurrentText(wf_info['heatmaps'][item]['colormap'])
                getattr(self, 'd3d2_'+str(nn)).setChecked(wf_info['heatmaps'][item]['d3d2'])

                if 'th' in item: #'th_i2e[ch1-tiss]'
                    if 'i2e' in item: 
                        process = 'D-Thickness_int>ext'
                    else: 
                        process = 'D-Thickness_ext>int'
                    ch_cont = item[0:-1].split('[')[1]
                    ch, cont = ch_cont.split('-')
                    proc = [process, ch, cont, 'Status']
                else: #'ball[ch1-int(CL:ch1-int)]'
                    process = 'D-Ballooning'
                    ch_cl_info = item[0:-2].split('[')[1]
                    ch_info, cl_info = ch_cl_info.split('(CL.')
                    ch, cont = ch_info.split('-')
                    proc = [process, ch, cont+'_('+cl_info.replace('-','_')+')', 'Status']
                    
                # print('proc:', get_by_path(wf, proc))
                if get_by_path(wf, proc) == 'DONE':
                    # print('done')
                    self.hm_btns[item]['play'].setChecked(True)
                    self.hm_btns[item]['play'].setEnabled(True)
                    self.hm_btns[item]['plot'].setEnabled(True)
                    if getattr(self, 'd3d2_'+str(nn)).isChecked():
                        self.hm_btns[item]['play2d'].setEnabled(True)
                    at_least_one = True
                else: 
                    # print('not done')
                    if 'th' in item:
                        self.hm_btns[item]['play'].setEnabled(True)
                    else: 
                        # print('\nnot thickness')
                        cl_ch, cl_cont = cl_info.split('-')
                        wf_cl = ['C-Centreline', 'buildCL', cl_ch, cl_cont, 'Status']
                        cl_done = get_by_path(wf, wf_cl)
                        # print(wf_cl, cl_done)
                        if cl_done == 'DONE': 
                            self.hm_btns[item]['play'].setEnabled(True)

            done_all = []
            for proc_n in ['D-Thickness_int>ext','D-Thickness_ext>int','D-Ballooning']:
                done_all.append(get_by_path(wf, [proc_n, 'Status']) == 'DONE')

            #Update Status in GUI
            if all(done_all): 
                self.update_status(None, 'DONE', self.heatmaps_status, override=True)
            elif any(done_all) or at_least_one: 
                self.update_status(None, 'Initialised', self.heatmaps_status, override=True)
            else: 
                pass
                    
            #Run Set Function 
            self.set_thickness(init=True)

        else: 
            pass

        #Update status of hm_cl if centreline has been already obtained
        if hasattr(self, 'cl4hm'):
            ch4cl, cont4cl = self.cl4hm.split('_')
            proc4cl = ['C-Centreline', 'buildCL', ch4cl, cont4cl, 'Status']
            if get_by_path(wf, proc4cl) == 'DONE':
                self.update_status(None, 'DONE', self.hm_centreline_status, override=True)

    def user_segments(self):

        wf = self.organ.workflow['morphoHeart']['MeshesProc']['E-Segments']
        wf_info = self.organ.mH_settings['wf_info']
        if 'segments' in wf_info.keys():
            print('wf_info[segments]:', wf_info['segments'])
            if wf_info['segments']['use_centreline']: 
                getattr(self, 'segm_use_centreline').setChecked(True)
                getattr(self, 'segm_centreline2use').setCurrentText(wf_info['segments']['centreline'])
                getattr(self, 'segm_centreline2use').setEnabled(True)
            else: 
                getattr(self, 'segm_use_centreline').setChecked(False)

            segm_setup = self.organ.mH_settings['setup']['segm']
            no_cuts = [key for key in segm_setup.keys() if 'Cut' in key]
        
            for optcut in ['1','2']:
                cutb = 'Cut'+optcut
                if cutb in no_cuts: 
                    getattr(self, 'radius_val_cut'+optcut).setVisible(True)
                    getattr(self, 'radius_val_cut'+optcut).setValue(wf_info['segments']['radius'][cutb])
                    getattr(self, 'radius_segm_cut'+optcut).setVisible(True)
                    getattr(self, 'radius_segm_unit'+optcut).setVisible(True)
                else: 
                    getattr(self, 'radius_val_cut'+optcut).setVisible(False)
                    getattr(self, 'radius_segm_cut'+optcut).setVisible(False)
                    getattr(self, 'radius_segm_unit'+optcut).setVisible(False)

            #Enable buttons if cuts have been made
            for name in self.segm_btns.keys():
                cut, ch_cont = name.split(':')
                ch, cont = ch_cont.split('_')
                num = self.segm_btns[name]['num']
                if get_by_path(wf, [cut, ch, cont, 'Status']) == 'DONE':
                    btn_play = self.segm_btns[name]['play']
                    btn_play.setChecked(True)
                    btn_plot = self.segm_btns[name]['plot']
                    btn_plot.setEnabled(True)
                if wf_info['segments']['setup'][cut]['ch_info'][ch][cont] == 'ext-ext':
                    #If ext-ext cut has been made then enable other buttons 
                    if get_by_path(wf, [cut, ch, cont, 'Status']) == 'DONE':
                        for sgmt in self.segm_btns.keys():
                            if sgmt != name: 
                                play_btn = self.segm_btns[sgmt]['play']
                                play_btn.setEnabled(True)

            #Update Status in GUI
            self.update_status(wf, ['Status'], self.segments_status)

            #Run Set Function 
            self.set_segments(init=True)
        
        else: 
            pass
    
    def user_sections(self):
        wf = self.organ.workflow['morphoHeart']['MeshesProc']['E-Sections']
        wf_info = self.organ.mH_settings['wf_info']
        if 'sections' in wf_info.keys():
            print('wf_info[sections]:', wf_info['sections'])
            sect_setup = self.organ.mH_settings['setup']['sect']
            no_cuts = [key for key in sect_setup.keys() if 'Cut' in key]

            for ct in no_cuts: 
                cut = ct.title()
                centreline = wf_info['sections'][cut]['centreline']
                nPoints = wf_info['sections'][cut]['nPoints']
                nRes = wf_info['sections'][cut]['nRes']
                axis = wf_info['sections'][cut]['axis_lab'].lower()
                direction = wf_info['sections'][cut]['direction']

                cut = ct.lower()
                getattr(self, 'sect_cl_'+cut).setCurrentText(centreline)
                getattr(self, 'sect_nPoints_'+cut).setValue(nPoints)
                getattr(self, 'sect_nRes_'+cut).setValue(nRes)
                getattr(self, 'radio_'+axis+'_'+cut).setChecked(True)
                getattr(self, 'sect_dir_'+cut).setText('Face No.'+str(direction['plane_no']))
                set_btn = getattr(self, 'dir_sect_'+cut)
                set_btn.setChecked(True)
                setattr(self, 'extend_dir_'+cut, direction)

                if 'mask_name' in self.organ.mH_settings['wf_info']['sections'][cut.title()].keys(): 
                    mask_name = self.organ.mH_settings['wf_info']['sections'][cut.title()]['mask_name']
                    mask_dir = self.organ.dir_res(dir ='s3_numpy') / mask_name
                    if mask_dir.is_file():
                        cl_ext_btn = getattr(self, 'cl_ext_'+cut.lower())
                        cl_ext_btn.setEnabled(True)
                        for sect in self.sect_btns.keys():
                            play_btn = self.sect_btns[sect]['play']
                            play_btn.setEnabled(True)

            #Enable buttons if cuts have been made
            for name in self.sect_btns.keys():
                cut, ch_cont = name.split(':')
                ch, cont = ch_cont.split('_')
                num = self.sect_btns[name]['num']
                if get_by_path(wf, [cut, ch, cont, 'Status']) == 'DONE':
                    self.sect_btns[name]['plot'].setEnabled(True)
                    self.sect_btns[name]['play'].setChecked(True)

            #Update Status in GUI
            self.update_status(wf, ['Status'], self.sections_status)

            #Run Set Function 
            self.set_sections(init=True)
            
        else: 
            pass
  
    def user_segm_sect(self): 
        pass
    
    def user_user_params(self): 

        print('self.gui_key_user_params: ', self.gui_key_user_params)
        wf_info = self.organ.mH_settings['wf_info']
        if 'user_params' in wf_info.keys(): 
            print('wf_info[user_params]:', wf_info['user_params'])

    #Functions specific to gui functionality
    def open_section(self, name): 
        #Get button
        btn = getattr(self, name+'_open')
        wdg = getattr(self, name+'_widget')
        if btn.isChecked():
            wdg.setVisible(False)
            btn.setText('v')
        else:
            wdg.setVisible(True)
            btn.setText('o')

    def tick_all(self, ch, proc): 
        tick_int = getattr(self, proc+'_'+ch+'_int')
        tick_ext = getattr(self, proc+'_'+ch+'_ext')
        tick_tiss = getattr(self, proc+'_'+ch+'_tiss')
        if getattr(self, proc+'_'+ch+'_all').isChecked(): 
            setChecked = True
        else: 
            setChecked = False
        
        for tick in [tick_int, tick_tiss, tick_ext]: 
            tick.setChecked(setChecked)

    def color_picker(self, name): 

        color = QColorDialog.getColor()
        if color.isValid():
            print('The selected color is: ', color.name())
            red, green, blue, _ = color.getRgb() #[red, green, blue]

            #Color the buttons
            fill = getattr(self, 'fillcolor_'+name)
            color_btn(btn = fill, color = color.name())
            try: 
                fillf = getattr(self, 'fillcolor_'+name+'f')
                color_btn(btn = fillf, color = color.name())
            except: 
                pass
            
            #Update colour in mH_settings
            name_split = name.split('_')
            if len(name_split) == 2: 
                chk, contk = name_split
                if chk != 'chNS' and contk in ['int', 'ext', 'tiss']: 
                    self.organ.mH_settings['setup']['color_chs'][chk][contk] = [red, green, blue]
                    try: 
                        self.organ.obj_meshes[chk+'_'+contk].set_color([red, green, blue])
                    except: 
                        pass
                elif chk == 'chNS': 
                    self.organ.mH_settings['setup'][chk]['color_chns'][contk] = [red, green, blue]#color.name()
                    try: 
                        self.organ.obj_meshes[chk+'_'+contk].set_color([red, green, blue])#color.name())
                    except: 
                        pass
                else: # 'cut1_sect1' or 'cut1_segm1'
                    if 'segm' in contk: 
                        stype = 'segm'
                    else: 
                        stype = 'sect'
                    self.organ.mH_settings['setup'][stype][chk.title()]['colors'][contk] = [red, green, blue]#color.name()
            else: 
                print('name:', name) #sCut1_Cut1_segm1_sect1
                scut, rcut, segm, sect = name_split
                self.organ.mH_settings['setup']['segm-sect'][scut][rcut]['colors'][segm+'_'+sect] = [red, green, blue]
   
    def update_alpha(self, name): 
        alpha_value = getattr(self, 'alpha_'+name+'f').value()
        # print('The updated alpha value for '+name+' is: '+ str(alpha_value))
        chk,contk = name.split('_')
        if chk != 'chNS': 
            self.organ.update_settings(['setup','alpha', chk, contk], alpha_value, 'mH')
        else: 
            self.organ.update_settings(['setup',chk,'alpha',contk], alpha_value, 'mH')

        try: 
            self.organ.obj_meshes[chk+'_'+contk].set_alpha(alpha_value)
        except: 
            pass

    def set_colormap(self, name):
        value = getattr(self, 'colormap'+name).currentText()
        dir_pix = 'images/'+value+'.png'
        pixmap = QPixmap(dir_pix)
        cm_eg = getattr(self, 'cm_eg'+name)
        cm_eg.setPixmap(pixmap)
        cm_eg.setScaledContents(True)

        wf_info = self.organ.mH_settings['wf_info']
        if 'heatmaps' in wf_info.keys() and hasattr(self, 'gui_thickness_ballooning'):
            for key in list(self.hm_btns.keys()): 
                num_key = self.hm_btns[key]['num']
                if int(num_key) == int(name): 
                    item = key
                    break
            
            self.gui_thickness_ballooning[item]['colormap'] = value
            print('Updated colormap: ',self.gui_thickness_ballooning[item])

    def fill_workflow(self):
                
        flat_wf = flatdict.FlatDict(self.organ.workflow['morphoHeart']['MeshesProc'])
        keys_flat = flat_wf.keys()
        keys_flat_filtered = [key for key in keys_flat if 'F-Measure' not in key]
        # print('keys_flat_filtered:', keys_flat_filtered)
        main_titles = []
        for key in keys_flat_filtered: 
            split_key = key.split(':')
            if len(split_key) == 2: 
                main_titles.append(split_key[0])
                if 'Orientation' not in key:
                    keys_flat_filtered.remove(key)
        try:
            keys_flat_filtered.remove('Status')
        except: 
            print('Status was not a key')
        try: 
            keys_flat_filtered.remove('A-Set_Orientation:Status')
        except: 
            print('A-Set_Orientation:Status was not a key')

        print('keys_flat_filtered:', keys_flat_filtered)
        self.workflow_keys = keys_flat_filtered
        main_titles_set = sorted(list(set(main_titles)))
        print('main_titles_set_sorted:', main_titles_set)

        dict_titles = {'A-Create3DMesh': {'title': 'Create 3D Mesh', 'short': 'createMesh'},
                        'A-Set_Orientation' : {'title': 'Set Orientation', 'short': 'setOrientation'},
                        'B-TrimMesh': {'title': 'Trim Meshes', 'short': 'trimMesh'},
                        'C-Centreline' : {'title': 'Extract Centreline', 'short': 'setCentreline', 
                                        'subprocesses': {'SimplifyMesh':{'title': 'Simplify Mesh', 'short': 'simpMesh'},
                                                            'vmtk_CL':{'title': 'vmtk', 'short': 'vmtkCL'},
                                                            'buildCL':{'title': 'Build Centreline', 'short': 'buildCL'}}},
                        'D-Ballooning' : {'title': 'Centreline>Tissue', 'short': 'ballooning'},
                        'D-Thickness_ext>int' : {'title': 'Tissue Thickness (ext>int*)', 'short': 'thExtInt'},
                        'D-Thickness_int>ext' : {'title': 'Tissue Thickness (int>ext*)', 'short': 'thIntExt'},
                        'E-Sections' : {'title': 'Regions', 'short': 'sect'},
                        'E-Segments' : {'title': 'Segments', 'short': 'segm'},
                        'E-Segments_Sections': {'title': 'Segments-Regions', 'short': 'segm-sect'}}

        #Add here the heatmaps 2D that have been added to analysis 
        # hereee!

        #Set row count
        self.tabW_progress_pandq.setRowCount(len(keys_flat_filtered)+len(main_titles_set))
        cS = []

        font = QFont()
        font.setFamily('Calibri')
        font.setBold(True)
        font.setItalic(True)
        font.setPointSize(10)

        main_titles_set_all = list(dict_titles.keys())

        row = 0
        for title in main_titles_set_all:
            if title in main_titles_set: 
                #Create a first label
                label = dict_titles[title]['title']
                short = dict_titles[title]['short']
                #Assign label to table 
                item = QTableWidgetItem(label)
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
                item.setFont(font)
                self.tabW_progress_pandq.setItem(row,0, item)
                row +=1

                #Find all keys that contain this title: 
                keys_title = [key for key in keys_flat_filtered if title+':' in key]
                # print('keys_title:', keys_title)

                for key in keys_title: 
                    sub_title = False
                    split_key = key.split(':')
                    if title == 'A-Set_Orientation':
                        cleaned_key = split_key[-1]
                        label_key = cleaned_key
                        cS_name = short+'_('+label_key+')'
                        # print('aaa:', row, label_key, cS_name)
                    elif title == 'C-Centreline':
                        if len(split_key) == 3: 
                            cleaned_key = dict_titles[title]['subprocesses'][split_key[1]]['title']
                            label_key = '    - '+cleaned_key
                            # print('bbb:', row, label_key)
                            sub_title = True
                        else: 
                            cleaned_key = split_key[2:-1]
                            label_key = '_'.join(cleaned_key)
                            # print('ccc:', row, label)
                            # print(key)
                            subproc = dict_titles[title]['subprocesses'][split_key[1]]['short']
                            cS_name = short+'_'+subproc+'_('+label_key+')'
                    else: 
                        cleaned_key = split_key[1:-1]
                        # print('cleaned_key:',cleaned_key)
                        label_key = '_'.join(cleaned_key)
                        cS_name = short+'_('+label_key+')'
                        # print('bbb:', row, label_key)

                    #Assign label to table 
                    item_key = QTableWidgetItem(label_key)
                    if sub_title: 
                        item_key.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
                    else: 
                        item_key.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
                    self.tabW_progress_pandq.setItem(row, 0, item_key)

                    if not sub_title: 
                        #Create status 
                        widget   = QWidget() 
                        hL = QtWidgets.QHBoxLayout(widget)
                        color_status = QtWidgets.QLineEdit()
                        color_status.setEnabled(True)
                        color_status.setMinimumSize(QtCore.QSize(15, 15))
                        color_status.setMaximumSize(QtCore.QSize(15, 15))
                        color_status.setStyleSheet("border-color: rgb(0, 0, 0);")
                        color_status.setReadOnly(True)
                        hL.addWidget(color_status)
                        hL.setContentsMargins(0, 0, 0, 0)
                        self.tabW_progress_pandq.setCellWidget(row, 1, widget)
                        setattr(self, cS_name, color_status)
                        cS.append(cS_name)
                    
                    self.tabW_progress_pandq.setRowHeight(row, 20)
                    row +=1
                
        headerc = self.tabW_progress_pandq.horizontalHeader()  
        for col in range(1):
            headerc.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        self.tabW_progress_pandq.setColumnWidth(1, 60)

        headerr = self.tabW_progress_pandq.verticalHeader()  
        for row in range(len(keys_flat_filtered)+len(main_titles_set)):   
            headerr.setSectionResizeMode(row, QHeaderView.ResizeMode.Stretch)
        
        self.workflow_status = cS
        print('self.workflow_status:', self.workflow_status)
        self.update_workflow_progress()

    def update_workflow_progress(self): 
        # print('self.workflow_keys:', self.workflow_keys)
        titles_inv = {'createMesh': 'A-Create3DMesh',
                       'setOrientation': 'A-Set_Orientation',
                       'trimMesh': 'B-TrimMesh',
                       'setCentreline_simpMesh': 'C-Centreline:SimplifyMesh', 
                       'setCentreline_vmtkCL': 'C-Centreline:vmtk_CL', 
                       'setCentreline_buildCL': 'C-Centreline:buildCL', 
                       'ballooning' : 'D-Ballooning',
                       'thExtInt' : 'D-Thickness_ext>int',
                       'thIntExt' : 'D-Thickness_int>ext' ,
                       'sect' : 'E-Sections',
                       'segm' : 'E-Segments', 
                       'segm-sect': 'E-Segments_Sections'}
        
        workflow = self.organ.workflow['morphoHeart']['MeshesProc']
        for cs in self.workflow_status: 
            cS = getattr(self, cs)
            split_cs = cs.split('_(')
            # print('cs:', cs, split_cs)
            if len(split_cs) == 2: 
                if 'Orientation' in cs: 
                    proc, orient = split_cs
                    proc_inv = titles_inv[proc]
                    final_key = proc_inv+':'+orient[:-1]
                else: 
                    proc, ch_info = split_cs
                    proc_inv = titles_inv[proc]
                    split_ch_info = ch_info[:-1].split('_')
                    if len(split_ch_info) == 1: #chNS
                        ch = split_ch_info
                        final_key = proc_inv+':'+ch[0]+':Status'
                    elif len(split_ch_info) == 2: 
                        ch, cont = split_ch_info
                        final_key = proc_inv+':'+ch+':'+cont+':Status'
                    elif len(split_ch_info) == 3: 
                        cut, ch, cont = split_ch_info
                        final_key = proc_inv+':'+cut+':'+ch+':'+cont+':Status'
            else: 
                #Ballooning
                proc, ch_info, cl_info = split_cs
                proc_inv = titles_inv[proc]
                ch, cont = ch_info.split('_')
                cl_info = cl_info.split(')')[0]
                final_key = proc_inv+':'+ch+':'+cont+'_('+cl_info+'):Status'

            if final_key in self.workflow_keys:
                items = final_key.split(':')
                update_status(workflow, items, cS)
                # print('Updated:', final_key)
            else: 
                print('---False:', final_key)
                alert('error_beep')

    def fill_results(self): 
        self.get_results_df()

        #Set row count
        self.tabW_results.setRowCount(len(self.df_res))
        row = 0
        for index, rowv in self.df_res.iterrows(): 
            col0, _, col2 = index
            value = rowv['Value']
            if isinstance(value, float): 
                valuef = "%.2f" % value
            elif isinstance(value, str): 
                valuef = value

            item_col0 = QTableWidgetItem(col0)
            self.tabW_results.setItem(row, 0, item_col0)
            item_col0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
            item_col2 = QTableWidgetItem(col2)
            self.tabW_results.setItem(row, 1, item_col2)
            item_col2.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
            item_value = QTableWidgetItem(valuef)
            self.tabW_results.setItem(row, 2, item_value)
            item_value.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)

            row+=1

        headerc = self.tabW_results.horizontalHeader()  
        for col in range(1):
            headerc.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        self.tabW_results.setColumnWidth(1, 270)
        self.tabW_results.setColumnWidth(2, 100)
        
        headerr = self.tabW_results.verticalHeader()  
        for row in range(len(self.df_res)):   
            headerr.setSectionResizeMode(row, QHeaderView.ResizeMode.Stretch)

        #Update measure_status
        col_list = self.df_res["Value"].values.tolist()
        if all(flag == 'TBO' for flag in col_list):
            self.update_status(None, 'NI', self.measure_status, override=True)
            self.organ.measure_status = 'NI'
        elif any(flag == 'TBO' for flag in col_list):
            self.update_status(None, 'Initialised', self.measure_status, override=True)
            self.organ.measure_status = 'Initialised'
        else: 
            self.update_status(None, 'DONE', self.measure_status, override=True)
            self.organ.measure_status = 'DONE'

    def get_results_df(self): 
        #Actual names
        params = self.organ.mH_settings['setup']['params']
        dict_names = {}
        for pp in params:
            var = params[pp]
            dict_names[var['s']] = var['l']
        dict_names['Ellip'] = 'Ellipsoid'
        dict_names['Angles'] = 'Angles'

        measurements = self.organ.mH_settings['measure']
        df_index = pd.DataFrame.from_dict(measurements, orient='index')
        # print('df_index', df_index)
        vars2drop = ['th_e2i', 'th_i2e', 'ball', 'hm3Dto2D']
        vars = list(df_index.index)
        for var in vars: 
            if var in vars2drop: 
                df_index = df_index.drop(var)
        cols = list(df_index.columns)

        #Add column with actual names of variables
        var_names = []
        for index, row in df_index.iterrows(): 
            try: 
                var_names.append(dict_names[index])
            except: 
                var, typpe = index.split('(')
                if typpe == 'segm)': 
                    name = 'Segment'
                elif typpe == 'segm-sect)': 
                    name = 'Segm-Reg'
                else: 
                    name == 'Region'
                var_names.append(dict_names[var]+': '+name)

        df_index['Parameter'] = var_names
        df_index = df_index.reset_index()
        df_index = df_index.drop(['index'], axis=1)
        df_melt = pd.melt(df_index, id_vars = ['Parameter'],  value_vars=cols, value_name='Value')
        df_melt = df_melt.rename(columns={"variable": "Tissue-Contour"})
        df_meltf = df_melt.dropna()
        mult_index= ['Parameter', 'Tissue-Contour']
        df_multi = df_meltf.set_index(mult_index)

        df_new = df_multi.copy(deep=True)
        key_cl = {'lin_length': 'Linear Length', 'looped_length': 'Looped Length'}
        if 'CL' in vars:
            dict_CL = {}
            df_CL = df_multi.loc[[dict_names['CL']]]
            for index, row in df_CL.iterrows():
                # print(index, row['Value'])
                if isinstance(row['Value'], dict): 
                    merge = True
                    df_new.drop(index, axis=0, inplace=True)
                    for key, item in row['Value'].items():
                        # print(key, item) 
                        new_index = 'Centreline: '+key_cl[key]
                        new_variable = index[1]
                        dict_CL[(new_index, new_variable)] = item

            # print('dict_CL:',  dict_CL)
            if len(dict_CL) != 0: 
                df_CL = pd.DataFrame(dict_CL, index =[0])
                # print('df_CL:', df_CL)
                df_CL_melt = pd.melt(df_CL, var_name=mult_index,value_name='Value')
                df_CL_melt = df_CL_melt.set_index(mult_index)
                df_final = pd.concat([df_new, df_CL_melt])
                df_final = df_final.sort_values(by=['Parameter'])
            else: 
                df_final = df_new.sort_values(by=['Parameter'])

        # key_ellip = {'lin_length': 'Linear Length', 'looped_length': 'Looped Length'}

        #Change True Values to TBO
        values_updated = []
        for index, row in df_final.iterrows(): 
            # print(index, type(row['Value']))
            if isinstance(row['Value'], bool): 
                values_updated.append('TBO')
            else: 
                values_updated.append(row['Value'])

        #Add column with better names
        user_tiss_cont = []
        name_chs = self.organ.mH_settings['setup']['name_chs']
        if isinstance(self.organ.mH_settings['setup']['segm'], dict):
            name_segm = {}
            for cut in [key for key in self.organ.mH_settings['setup']['segm'] if 'Cut' in key]:
                name_segm[cut] = self.organ.mH_settings['setup']['segm'][cut]['name_segments']
        if isinstance(self.organ.mH_settings['setup']['sect'], dict):
            name_sect = {}
            for cut in [key for key in self.organ.mH_settings['setup']['sect'] if 'Cut' in key]:
                name_sect[cut] = self.organ.mH_settings['setup']['sect'][cut]['name_sections']
        name_cont = {'int': 'internal', 'tiss': 'tissue', 'ext': 'external'}

        for index, _ in df_final.iterrows(): 
            param, tiss_cont = index
            split_name = tiss_cont.split('_')
            # print(split_name, len(split_name))
            if len(split_name) == 1 and tiss_cont == 'roi': 
                namef = 'Organ/ROI'
            elif len(split_name) == 3: 
                ch, cont, _ = split_name
                namef = name_chs[ch]+ ' ('+name_cont[cont]+')'
            elif len(split_name) == 4: 
                # print('split_name:', split_name)
                cut, ch, cont, subm = split_name
                if 'segm' in subm: 
                    namef = cut+': '+name_chs[ch]+ '-'+name_cont[cont]+' ('+name_segm[cut][subm]+')'
                else: 
                    namef = cut+': '+name_chs[ch]+ '-'+name_cont[cont]+' ('+name_sect[cut][subm]+')'
                # print(namef)
            elif len(split_name) == 6: #Intersections
                # print('split_name:', split_name)
                scut, rcut, ch, cont, segm, sect = split_name
                namef = scut[1:]+'-'+rcut+': '+name_chs[ch]+ '-'+name_cont[cont]+' ('+name_segm[scut[1:]][segm]+'-'+name_sect[rcut][sect]+')'
            else: 
                print(index, len(split_name))
                namef = 'Check: '+tiss_cont
            
            # print(index, namef.title())
            nameff = namef.title()
            user_tiss_cont.append(nameff)

        df_final['Value'] = values_updated
        df_final['User (Tissue-Contour)'] = user_tiss_cont
        df_finalf = df_final.reset_index()
        df_finalf = df_finalf.set_index(mult_index+['User (Tissue-Contour)'])

        df_finalf = df_finalf.sort_values(['Parameter','Tissue-Contour'],
                                                ascending = [True, True])
        
        print('df_finalf: ', df_finalf)
        self.df_res = df_finalf
            
    def n_slices(self, process):
        cB = getattr(self, process+'_plot2d')
        if cB.isChecked():
            state = True
        else: 
            state = False
        getattr(self, process+'_lab1').setEnabled(state)
        getattr(self, process+'_n_slices').setEnabled(state)
        getattr(self, process+'_lab2').setEnabled(state)

    def default_range(self, btn_num):
        btn = getattr(self, 'def'+btn_num)
        if btn.isChecked(): 
            bol_val = False
        else: 
            bol_val = True

        getattr(self, 'min_hm'+btn_num).setEnabled(bol_val)
        getattr(self, 'max_hm'+btn_num).setEnabled(bol_val)

    def check_all(self, mtype):
        check_btn = getattr(self, 'all_'+mtype)
        if check_btn.isChecked(): 
            value = True
        else:
            value = False
        
        if mtype == 'def': 
            cB_name = 'def'
        elif mtype == 'd3d2':
            cB_name = 'd3d2_'
        else: 
            print('other name?')

        for num in range(1,13,1): 
            getattr(self, cB_name+str(num)).setChecked(value)
  
    def segm_centreline(self): 
        if self.segm_use_centreline.isChecked():
            self.segm_centreline2use.setEnabled(True)
        else: 
            self.segm_centreline2use.setEnabled(False)

    def select_extension_plane(self, cut): 
        #Section names
        sect_settings = self.organ.mH_settings['setup']['sect']
        names_sect = sect_settings[cut.title()]['name_sections']
        names = [names_sect[name] for name in names_sect]
        namesf = ', '.join(names) 
        print(namesf)
        #Cuts 
        cuts = [key for key in sect_settings.keys() if 'Cut' in key]
        print('cuts:', cuts)

        if getattr(self, 'sect_cl_'+cut).currentText() != '----':

            #Get Centreline
            cl_name = getattr(self, 'sect_cl_'+cut).currentText().split('(')[1][:-1]
            nPoints = getattr(self, 'sect_nPoints_'+cut).value()
            mesh_cl = self.organ.obj_meshes[cl_name].get_centreline(nPoints = nPoints)

            #Get Mesh
            mesh_name = [key for key in self.sect_btns.keys() if cut.title() in key][0]
            ch, cont = mesh_name.split(':')[1].split('_')
            mesh = self.organ.obj_meshes[ch+'_'+cont]

            #Get Axis to extend cl
            for opt in ['roi', 'stack']:
                if getattr(self, 'radio_'+opt+'_'+cut).isChecked():
                    axis_selected = opt
                    cube2use = getattr(self.organ, opt+'_cube')
                    break
            print(axis_selected, cube2use)
            orient_cube_clear = cube2use['clear']
            orient_cube = cube2use['cube']
            side = self.gui_orientation[axis_selected][axis_selected+'_cube']['side']

            color_o = 'white'
            com = orient_cube.center_of_mass()
            sph = vedo.Sphere(pos = com, r = side/12, c = color_o)
            sph1 = vedo.Sphere(pos = com, r = side/12, c = color_o)
            extend_dir = {'plane_no': None, 'plane_normal': None}

            arrows = []
            for n, centre in enumerate(orient_cube.cell_centers()):
                cells = orient_cube.cells()[n]
                points = [orient_cube.points()[cell] for cell in cells]
                plane_fit = vedo.fit_plane(points, signed=True)
                normal = plane_fit.normal
                end_pt = centre + (normal*side/3)
                arrow = vedo.Arrow(start_pt=(centre), end_pt=end_pt, c='cyan').legend('No.'+str(n))
                arrows.append(arrow)
            
            def select_cube_face(evt):
                orient_cube = evt.actor
                if not orient_cube:
                    return
                pt = evt.picked3d
                idcell = orient_cube.closest_point(pt, return_cell_id=True)
                print("You clicked (idcell):", idcell)

                #Set arrow and sphere 
                cell_centre = orient_cube.cell_centers()[int(idcell)]
                sph.pos(cell_centre)
                sil = arrows[idcell].silhouette().linewidth(6).c('gold')
                sil.name = "silu" # give it a name so we can remove the old one
                plt.remove('silu').add(sil)
                
                #Set arrow and sphere 1
                if idcell%2 == 0: 
                    idcell1 = idcell+1
                else: 
                    idcell1 = idcell-1
                cell_centre1 = orient_cube.cell_centers()[int(idcell1)]
                sph1.pos(cell_centre1)
                sil1 = arrows[idcell1].silhouette().linewidth(6).c('gold')
                sil1.name = "silu1" # give it a name so we can remove the old one
                plt.remove('silu1').add(sil1)

                #Get plane 
                cells = orient_cube.cells()[idcell]
                points = [orient_cube.points()[cell] for cell in cells]
                plane_fit = vedo.fit_plane(points, signed=True)

                msg.text("You selected face number: " + str(idcell))
                extend_dir['plane_no'] = idcell
                extend_dir['plane_normal'] = plane_fit.normal

            msg = vedo.Text2D("", pos="bottom-center",  c=txt_color, font=txt_font, s=txt_size, alpha=0.8)
            txt0 = vedo.Text2D('Reference cube and mesh to select the plane into which the centreline will be projected \nto cut tissues into  -'+ namesf +'-  regions',  c=txt_color, font=txt_font, s=txt_size)
            txt1 = vedo.Text2D('Select (click) the cube face into which the centreline will be projected \nand close the window when done.',  c=txt_color, font=txt_font, s=txt_size)
    
            plt = vedo.Plotter(N=2, axes=1)
            plt.add_callback("mouse click", select_cube_face)
            plt.show(mesh.mesh, mesh_cl, orient_cube_clear, txt0, at=0)
            plt.show(orient_cube, sph, arrows, msg, txt1, at=1, azimuth=45, elevation=30, zoom=0.8, interactive=True)        

            print('extend_dir:', extend_dir)
            face_num = extend_dir['plane_no']
            label_axis = getattr(self, 'sect_dir_'+cut).setText('Face No.'+str(face_num))
            setattr(self, 'extend_dir_'+cut, extend_dir)

            #Toggle button
            btn = getattr(self, 'dir_sect_'+cut)
            btn.setChecked(True)

            done = []
            for ct in cuts: 
                done.append(hasattr(self, 'extend_dir_'+ct.lower()))
            print('done sect:',done)
            if all(done): 
                self.set_sections()
        else: 
            error_txt = '*(Regions: '+cut.title()+') Please select the Centreline you want to use to cut tissue into  -'+namesf+'-  regions to continue.'
            self.win_msg(error_txt, getattr(self, 'dir_sect_'+cut))

    #Set functions 
    def set_keeplargest(self): 
        wf_info = self.organ.mH_settings['wf_info']
        current_gui_keep_largest = self.gui_keep_largest_n()
        if 'keep_largest' not in wf_info.keys():
            self.gui_keep_largest = current_gui_keep_largest
        else: 
            gui_keep_largest_loaded = self.organ.mH_settings['wf_info']['keep_largest']
            self.gui_keep_largest, changed  = update_gui_set(loaded = gui_keep_largest_loaded, 
                                                                current = current_gui_keep_largest)
            if changed:
                self.win_msg("Remember to re-run  -Keep Largest-  section to make sure changes are made and saved!")
                self.update_status(None, 're-run', self.keeplargest_status, override=True)

        self.keeplargest_set.setChecked(True)
        print('self.gui_keep_largest:',self.gui_keep_largest)
        self.keeplargest_play.setEnabled(True)

        # Update mH_settings
        proc_set = ['wf_info']
        update = self.gui_keep_largest
        self.organ.update_settings(proc_set, update, 'mH', add='keep_largest')

    def gui_keep_largest_n(self):
        gui_keep_largest = {}
        for ch in self.channels: 
            if ch != 'chNS':
                gui_keep_largest[ch] = {}
                for cont in ['int', 'tiss', 'ext']:
                    cB = getattr(self, 'kl_'+ch+'_'+cont)
                    gui_keep_largest[ch][cont] = cB.isChecked() 
        self.rotateZ_90 = True

        return gui_keep_largest

    def set_clean(self): 
        wf_info = self.organ.mH_settings['wf_info']
        current_gui_clean = self.gui_clean_n()
        if 'cleanup' not in wf_info.keys():
            self.gui_clean = current_gui_clean
        else: 
            gui_clean_loaded = self.organ.mH_settings['wf_info']['cleanup']
            self.gui_clean, changed = update_gui_set(loaded = gui_clean_loaded, 
                                                        current = current_gui_clean)
            if changed: 
                self.win_msg("Remember to re-run  -Segmentation Clean-Up-  section to make sure changes are made and saved!")
                self.update_status(None, 're-run', self.cleanup_status, override=True)

        self.cleanup_set.setChecked(True)
        print('self.gui_clean: ', self.gui_clean)
        self.cleanup_play.setEnabled(True)

        # Update mH_settings
        proc_set = ['wf_info']
        update = self.gui_clean
        self.organ.update_settings(proc_set, update, 'mH', add='cleanup')

    def gui_clean_n(self):
        #Check first if any cont selected that the ch and cont are selected
        im_chs = [ch for ch in self.channels if ch != 'chNS']
        chs_sel = []
        for ch in im_chs: 
            selected = []
            for cont in ['int', 'tiss', 'ext']: 
                selected.append(getattr(self, 'clean_'+ch+'_'+cont).isChecked())
            if any(selected): 
                chs_sel.append(ch)
                withch = getattr(self, 'clean_withch_'+ch).currentText()
                withcont = getattr(self, 'clean_withcont_'+ch).currentText()
                if withch == '----' or withcont == '----': 
                    self.win_msg('*Please select the channel and contour to use as mask for '+ch.title(), self.cleanup_set)
                    return
                else: 
                    continue
                
        gui_clean = {}
        for chc in chs_sel: 
            gui_clean[chc] = {'cont': []}
            for cont in ['int', 'tiss', 'ext']: 
                val = getattr(self, 'clean_'+chc+'_'+cont).isChecked()
                if val: 
                    gui_clean[chc]['cont'].append(cont)
                gui_clean[chc]['with_ch'] = getattr(self, 'clean_withch_'+chc).currentText()
                gui_clean[chc]['with_cont'] = getattr(self, 'clean_withcont_'+chc).currentText()
                gui_clean[chc]['inverted'] = getattr(self, 'inverted_'+chc).isChecked()

        if self.clean_plot2d.isChecked():
            gui_clean['plot2d'] =  True
            gui_clean['n_slices'] = self.clean_n_slices.value()
        else: 
            gui_clean['plot2d'] = False
        
        return gui_clean

    def set_trim(self, init=False): 
        wf_info = self.organ.mH_settings['wf_info']
        current_gui_trim = self.gui_trim_n()
        if 'trimming' not in wf_info.keys():
            self.gui_trim = current_gui_trim
        else: 
            gui_trim_loaded = self.organ.mH_settings['wf_info']['trimming']
            self.gui_trim, changed = update_gui_set(loaded = gui_trim_loaded, 
                                                    current = current_gui_trim)
            if changed: 
                self.win_msg("Remember to re-run  -Meshes Trimming-  section to make sure changes are made and saved!")
                self.update_status(None, 're-run', self.trimming_status, override=True)
        
        self.trimming_set.setChecked(True)
        print('self.gui_trim: ', self.gui_trim)
        self.trimming_play.setEnabled(True)

         # Update mH_settings
        proc_set = ['wf_info']
        update = self.gui_trim
        self.organ.update_settings(proc_set, update, 'mH', add='trimming')
    
    def gui_trim_n(self):
        gui_trim = {}
        im_chs = [ch for ch in self.channels if ch != 'chNS']
        for side in ['top', 'bottom']: 
            gui_trim[side] = {'chs': {}}
            for cht in im_chs: 
                gui_trim[side]['chs'][cht] = {}
                for cont in ['int', 'tiss', 'ext']: 
                    val = getattr(self, side[0:3]+'_'+cht+'_'+cont).isChecked()
                    gui_trim[side]['chs'][cht][cont] = val
        
            obj = getattr(self, side[0:3]+'_cut_opts').currentText()
            gui_trim[side]['object'] = obj
        
        return gui_trim

    def check_roi_reorient(self):

        if self.roi_reorient.isChecked():
            self.radio_manual.setEnabled(True)
            self.radio_centreline.setEnabled(True)
            self.reorient_method(mtype ='centreline')
        else: 
            self.radio_manual.setEnabled(False)
            self.radio_centreline.setEnabled(False)
            self.reorient_method(mtype ='none')

    def reorient_method(self, mtype:str):
        # print('Checked:', mtype)
        if self.radio_manual.isChecked(): 
            self.reorient_angles.setEnabled(True)
            self.centreline_orientation.setEnabled(False)
            self.lab_plane.setEnabled(False)
            self.plane_orient.setEnabled(False)
            self.lab_vector.setEnabled(False)
            self.vector_orient.setEnabled(False)
        elif self.radio_centreline.isChecked(): 
            self.reorient_angles.setEnabled(False)
            self.centreline_orientation.setEnabled(True)
            self.lab_plane.setEnabled(True)
            self.plane_orient.setEnabled(True)
            self.lab_vector.setEnabled(True)
            self.vector_orient.setEnabled(True)
        else: 
            self.reorient_angles.setEnabled(False)
            self.centreline_orientation.setEnabled(False)
            self.lab_plane.setEnabled(False)
            self.plane_orient.setEnabled(False)
            self.lab_vector.setEnabled(False)
            self.vector_orient.setEnabled(False)
    
    def set_orientation(self, init=False): 
        wf_info = self.organ.mH_settings['wf_info']
        current_gui_orientation = self.gui_orientation_n()
        if current_gui_orientation != None: 
            if 'orientation' not in wf_info.keys():
                self.gui_orientation = current_gui_orientation
            else: 
                gui_orientation_loaded = self.organ.mH_settings['wf_info']['orientation']
                self.gui_orientation, changed = update_gui_set(loaded = gui_orientation_loaded, 
                                                        current = current_gui_orientation)
                if changed: 
                    self.win_msg("Remember to re-run  -Organ/ROI Axis Labels-  section to make sure changes are made and saved!")
                    self.update_status(None, 're-run', self.orient_status, override=True)

            self.orientation_set.setChecked(True)
            print('self.gui_orientation: ', self.gui_orientation)
            self.orientation_play.setEnabled(True)

            # Update mH_settings
            proc_set = ['wf_info']
            update = self.gui_orientation
            self.organ.update_settings(proc_set, update, 'mH', add='orientation')
        else:
            return

    def gui_orientation_n(self): 
        #Stack
        gui_orientation = {}
        gui_orientation['stack'] = {'axis': self.organ.mH_settings['setup']['orientation']['stack']}

        #ROI
        roi_reorient = self.roi_reorient.isChecked()
        gui_orientation['roi'] = {'axis': self.organ.mH_settings['setup']['orientation']['roi'],
                                        'reorient': roi_reorient}
        if roi_reorient: 
            for rB in ['radio_manual', 'radio_centreline']:
                if getattr(self, rB).isChecked():
                    rB_checked = rB
                    break
                else: 
                    rB_checked = None

            if rB_checked == 'radio_manual': 
                gui_orientation['roi']['method'] = 'Manual'
            elif rB_checked == 'radio_centreline': 
                centreline = self.centreline_orientation.currentText()
                if centreline != '----': 
                    plane_orient = self.plane_orient.currentText()
                    vector_orient = self.vector_orient.currentText()
                    gui_orientation['roi']['method'] = 'Centreline'
                    gui_orientation['roi']['centreline'] = centreline
                    gui_orientation['roi']['plane_orient'] = plane_orient
                    gui_orientation['roi']['vector_orient'] = vector_orient
                else: 
                    self.win_msg('*Select the centreline you want to use to reorient the organ!', self.orientation_set)
                    return None
            else: 
                self.win_msg('*Please select the method you want to use to reorient the organ!', self.orientation_set)
                return None
        else: 
            pass

        return gui_orientation

    def set_chNS(self):
        wf_info = self.organ.mH_settings['wf_info']
        current_gui_chNS = self.gui_chNS_n()
        if 'chNS' not in wf_info.keys():
            self.gui_chNS = current_gui_chNS
        else: 
            gui_chNS_loaded = self.organ.mH_settings['wf_info']['chNS']
            self.gui_chNS, changed = update_gui_set(loaded = gui_chNS_loaded, 
                                                       current = current_gui_chNS)
            if changed: 
                self.win_msg("If you want to plot2D with the new settings remember to re-run  -Channel from the negative space extraction-  section!")
                self.update_status(None, 're-run', self.chNS_status, override=True)

        self.chNS_set.setChecked(True)
        print('self.gui_chNS: ', self.gui_chNS)
        self.chNS_play.setEnabled(True)   

        # Update mH_settings
        proc_set = ['wf_info']
        update = self.gui_chNS
        self.organ.update_settings(proc_set, update, 'mH', add='chNS')
    
    def gui_chNS_n(self): 
        gui_chNS = {}
        if self.chNS_plot2d.isChecked():
            gui_chNS = {'plot2d': True, 
                            'n_slices': self.chNS_n_slices.value()}
        else: 
            gui_chNS['plot2d'] = False

        return gui_chNS

    def set_centreline(self, init=False):

        wf_info = self.organ.mH_settings['wf_info']
        current_gui_centreline = self.gui_centreline_n()
        if 'centreline' not in wf_info.keys():
            self.gui_centreline = current_gui_centreline
        else: 
            self.gui_centreline = self.organ.mH_settings['wf_info']['centreline']
            # gui_centreline_loaded = self.organ.mH_settings['wf_info']['centreline']
            # self.gui_centreline, changed = update_gui_set(loaded = gui_centreline_loaded, 
            #                                         current = current_gui_centreline)
            # if changed: 
            #     self.win_msg("Remember to re-run  -Keep Largest-  section to make sure changes are made and saved!")
            #     self.update_status(None, 're-run', self.centreline_status, override=True)
        
        self.centreline_set.setChecked(True)
        print('self.gui_centreline: ', self.gui_centreline)
        self.centreline_clean_play.setEnabled(True) 

        #Update mH_settings
        proc_set = ['wf_info']
        update =  self.gui_centreline
        self.organ.update_settings(proc_set, update, 'mH', add='centreline')  

    def gui_centreline_n(self):
        cl_names = list(self.organ.mH_settings['measure']['CL'].keys())
        connect_cl = {}
        for name in cl_names: 
            namef = name.split('_whole')[0]
            connect_cl[namef] = None

        same_planes = self.cB_same_planes.isChecked()
        tol = self.tolerance.value()
        voronoi = self.cB_voronoi.isChecked()
        nPoints = self.nPoints.value()
        gui_centreline =  {'SimplifyMesh': {'same_planes': same_planes, 'plane_cuts': None, 'tol': tol},
                                'vmtk_CL': {'voronoi': voronoi},
                                'buildCL': {'nPoints': nPoints, 'connect_cl': connect_cl}, 
                                'dirs' : None}
        return gui_centreline

    def set_thickness(self, init=False): 

        wf_info = self.organ.mH_settings['wf_info']
        current_gui_thickness_ballooning = self.gui_thickness_ballooning_n()
        if 'heatmaps' not in wf_info.keys():
            self.gui_thickness_ballooning = current_gui_thickness_ballooning
        else: 
            gui_thickness_ballooning_loaded = self.organ.mH_settings['wf_info']['heatmaps']
            self.gui_thickness_ballooning, changed = update_gui_set(loaded = gui_thickness_ballooning_loaded, 
                                                                current = current_gui_thickness_ballooning)
            if changed: 
                # self.win_msg("Remember to re-run  -Thickness / Ballooning Measurements-  section to make sure changes are made and saved!")
                self.update_status(None, 're-run', self.heatmaps_status, override=True)
            
        self.update_3d2d()

        # Update mH_settings
        proc_set = ['wf_info']
        update = self.gui_thickness_ballooning
        self.organ.update_settings(proc_set, update, 'mH', add='heatmaps')

        self.thickness_set.setChecked(True)
        print('self.gui_thickness_ballooning: ', self.gui_thickness_ballooning)

    def gui_thickness_ballooning_n(self):
        gui_thickness_ballooning = {}
        nn = 1
        for item in self.hm_btns:
            default = getattr(self, 'def'+str(nn)).isChecked()
            if default: 
                min_val = None
                max_val = None
            else: 
                min_val = getattr(self, 'min_hm'+str(nn)).value()
                max_val = getattr(self, 'max_hm'+str(nn)).value()
            colormap = getattr(self, 'colormap'+str(nn)).currentText()
            d3d2 = getattr(self, 'd3d2_'+str(nn)).isChecked()
            gui_thickness_ballooning[item] = {'default': default, 
                                                   'min_val': min_val, 
                                                   'max_val': max_val, 
                                                   'colormap': colormap, 
                                                   'd3d2': d3d2}
            nn+=1

        return gui_thickness_ballooning
    
    def update_3d2d(self): 

        wf = self.organ.workflow['morphoHeart']['MeshesProc']
        for item in self.hm_btns: 
            if 'th' in item: #'th_i2e[ch1-tiss]'
                if 'i2e' in item: 
                    process = 'D-Thickness_int>ext'
                else: 
                    process = 'D-Thickness_ext>int'
                ch_cont = item[0:-1].split('[')[1]
                ch, cont = ch_cont.split('-')
                btn_play = self.hm_btns[item]['play']
                btn_play.setEnabled(True)
                proc = [process, ch, cont, 'Status']
                        
            else: #'ball[ch1-int(CL:ch1-int)]'
                process = 'D-Ballooning'
                ch_cl_info = item[0:-2].split('[')[1]
                ch_info, cl_info = ch_cl_info.split('(CL.')
                ch, cont = ch_info.split('-')
                cl_ch, cl_cont = cl_info.split('-')
                proc_cl = ['C-Centreline', 'buildCL', cl_ch, cl_cont, 'Status']
                if get_by_path(wf, proc_cl) == 'DONE':
                    btn_play = self.hm_btns[item]['play']
                    btn_play.setEnabled(True)
                    proc = [process, ch, cont+'_('+cl_info.replace('-','_')+')', 'Status']

            if self.gui_thickness_ballooning[item]['d3d2']: 
                ch4cl, cont4cl = self.cl4hm.split('_')
                proc4cl = ['C-Centreline', 'buildCL', ch4cl, cont4cl, 'Status']
                if get_by_path(wf, proc) == 'DONE' and get_by_path(wf, proc4cl) == 'DONE' :
                    print('done')
                    self.hm_btns[item]['play2d'].setEnabled(True)

        if hasattr(self, 'cl4hm'):
            ch4cl, cont4cl = self.cl4hm.split('_')
            proc4cl = ['C-Centreline', 'buildCL', ch4cl, cont4cl, 'Status']
            print(proc4cl, get_by_path(wf, proc4cl))
            if get_by_path(wf, proc4cl):
                self.update_status(None, 'DONE', self.hm_centreline_status, override=True)
   
    def set_segments(self, init=False):
        wf_info = self.organ.mH_settings['wf_info']
        current_gui_segm = self.gui_segments_n()
        if current_gui_segm != None: 
            if 'segments' not in wf_info.keys():
                self.gui_segm = current_gui_segm
            else: 
                gui_segm_loaded = self.organ.mH_settings['wf_info']['segments']
                self.gui_segm, changed = update_gui_set(loaded = gui_segm_loaded, 
                                                        current = current_gui_segm)
                if changed: 
                    # self.win_msg("If you want to plot2D with the new settings remember to re-run  -Channel from the negative space extraction-  section!")
                    self.update_status(None, 're-run', self.segments_status, override=True)

            self.segments_set.setChecked(True)
            print('self.gui_segm: ', self.gui_segm)
            self.segments_play.setEnabled(True)   

            # Update mH_settings
            proc_set = ['wf_info']
            update = self.gui_segm
            self.organ.update_settings(proc_set, update, 'mH', add='segments')

        else: 
            return

    def gui_segments_n(self): 

        segm_setup = self.organ.mH_settings['setup']['segm']
        no_cuts = [key for key in segm_setup.keys() if 'Cut' in key]
        
        gui_segm = {'radius' : {}}
        for optcut in ['1','2']:
            cutb = 'Cut'+optcut
            if cutb in no_cuts: 
                radius = getattr(self, 'radius_val_cut'+optcut).value()
                gui_segm['radius'][cutb] = radius

        use_cl = getattr(self, 'segm_use_centreline').isChecked()
        if use_cl: 
            cl2use = getattr(self, 'segm_centreline2use').currentText()
            if cl2use != '----':
                gui_segm['use_centreline'] = use_cl
                gui_segm['centreline'] = cl2use
            else: 
                self.win_msg('*Please select the centreline you want to use to aid tissue division into segments!', self.segments_set)
                return None
        else: 
            gui_segm['use_centreline'] = use_cl

        segm_set = self.organ.mH_settings['setup']['segm']
        segments = {}; measure = {}

        #Set the way in which each mesh is going to be cut
        if self.organ.mH_settings['setup']['all_contained'] or self.organ.mH_settings['setup']['one_contained']: 
            ext_ch = self.organ.get_ext_int_chs()
            ext_ch_name = ext_ch.channel_no
            nn = 1
            for cut in [key for key in segm_set.keys() if 'Cut' in key]:
                segments[cut] = {'ch_info': {}, 'measure': {}, 'dirs': {}}
                for ch in segm_set[cut]['ch_segments']: 
                    segments[cut]['ch_info'][ch] = {}
                    segments[cut]['measure'][ch] = {}
                    segments[cut]['dirs'][ch] = {}
                    segments[cut]['names'] ={}
                    if ch != 'chNS': 
                        relation = self.organ.mH_settings['setup']['chs_relation'][ch]
                    else: 
                        relation = 'chNS'

                    if relation == 'external': 
                        for cont in segm_set[cut]['ch_segments'][ch]: 
                            if cont == 'ext': 
                                txt = 'ext-ext'
                                btn = self.segm_btns[cut+':'+ch+'_'+cont]['play']
                                btn.setEnabled(True)
                            else: 
                                txt = 'cut_with_ext-ext'
                            segments[cut]['ch_info'][ch][cont] = txt
                            segments[cut]['measure'][ch][cont] = {}
                            segments[cut]['dirs'][ch][cont] = {}
                    elif relation == 'internal' or relation == 'middle' or relation == 'chNS': 
                        for cont in segm_set[cut]['ch_segments'][ch]: 
                            txt = 'cut_with_other_ext-ext'
                            segments[cut]['ch_info'][ch][cont] = txt
                            segments[cut]['measure'][ch][cont] = {}
                            segments[cut]['dirs'][ch][cont] = {}
                    else: # relation == 'independent'
                        for cont in segm_set[cut]['ch_segments'][ch]: 
                            if cont == 'ext':
                                txt = 'indep-ext'
                                btn = self.segm_btns[cut+':'+ch+'_'+cont]['play']
                                btn.setEnabled(True)
                            else: 
                                txt = 'cut_with_ext-indep'
                            segments[cut]['ch_info'][ch][cont] = txt
                            segments[cut]['measure'][ch][cont] = {}
                            segments[cut]['dirs'][ch][cont] = {}
        else: 
            for cut in [key for key in segm_set.keys() if 'Cut' in key]:
                segments[cut] = {'ch_info': {}}
                for ch in segm_set[cut]['ch_segments']: 
                    segments[cut]['ch_info'][ch] = {}
                    segments[cut]['measure'][ch] = {}
                    segments[cut]['dirs'][ch] = {}
                    relation = self.organ.mH_settings['setup']['chs_relation'][ch]
                    for cont in segm_set[cut]['ch_segments'][ch]: 
                        if cont == 'ext':
                            txt = 'indep-ext'
                        else: 
                            txt = 'cut_with_ext-indep'
                        segments[cut]['ch_info'][ch][cont] = txt
                        segments[cut]['measure'][ch][cont] = {}
                        segments[cut]['dirs'][ch][cont] = {}
        gui_segm['setup'] = segments

        return gui_segm

    def set_sections(self, init=False): 

        sect_setup = self.organ.mH_settings['setup']['sect']
        no_cuts = [key for key in sect_setup.keys() if 'Cut' in key]
        done_set = []
        for cut_no in no_cuts: 
            done_set.append(hasattr(self, 'extend_dir_'+cut_no.lower()))
        print('Done selecting sections cut direction:', done_set)

        if all(done_set): 
            wf_info = self.organ.mH_settings['wf_info']
            current_gui_sect = self.gui_sections_n()
            if current_gui_sect != None: 
                if 'sections' not in wf_info.keys():
                    self.gui_sect = current_gui_sect
                else: 
                    gui_sect_loaded = self.organ.mH_settings['wf_info']['sections']
                    self.gui_sect, changed = update_gui_set(loaded = gui_sect_loaded, 
                                                            current = current_gui_sect)
                    if changed: 
                        # self.win_msg("If you want to plot2D with the new settings remember to re-run  -Channel from the negative space extraction-  section!")
                        self.update_status(None, 're-run', self.sections_status, override=True)

                self.sections_set.setChecked(True)
                print('self.gui_sect: ', self.gui_sect)
                self.sections_play.setEnabled(True)   
                for btn in self.sect_btns.keys():
                    self.sect_btns[btn]['play'].setEnabled(True)

                # Update mH_settings
                proc_set = ['wf_info']
                update = self.gui_sect
                self.organ.update_settings(proc_set, update, 'mH', add='sections')
            else: 
                return 
        else: 
            cut_not_done = [nn for nn, val in enumerate(done_set) if val==False][0]
            print('cut_not_done:', cut_not_done)
            error_txt = '* Please set the direction to extend the centreline for  -'+no_cuts[cut_not_done].title() +'-  to set the regions settings.'
            self.win_msg(error_txt, self.sections_set)

    def gui_sections_n(self):

        sect_setup = self.organ.mH_settings['setup']['sect']
        no_cuts = [key for key in sect_setup.keys() if 'Cut' in key]
        
        gui_sect= {}
        for optcut in ['1','2']:
            cutb = 'Cut'+optcut
            if cutb in no_cuts: 
                gui_sect[cutb] = {}
                centreline = getattr(self, 'sect_cl_cut'+optcut).currentText()
                gui_sect[cutb]['centreline'] = centreline
                gui_sect[cutb]['nPoints'] = getattr(self, 'sect_nPoints_cut'+optcut).value()
                gui_sect[cutb]['nRes'] = getattr(self, 'sect_nRes_cut'+optcut).value()
                for reg in ['roi', 'stack']: 
                    if getattr(self, 'radio_'+reg+'_cut'+optcut).isChecked(): 
                        selected = reg
                        break
                gui_sect[cutb]['axis_lab'] = selected.title()
                direction = getattr(self, 'extend_dir_cut'+optcut)
                gui_sect[cutb]['direction'] = direction
            
        return gui_sect

    def set_user_user_params(self, ptype):
        wf_info = self.organ.mH_settings['wf_info']
        current_gui_user_params = self.gui_user_params_n(ptype) 
        if current_gui_user_params != None: 
            if 'user_params' not in wf_info.keys():
                self.gui_user_params = current_gui_user_params
            else: 
                gui_user_params_loaded = self.organ.mH_settings['wf_info']['user_params']
                self.gui_user_params, changed = update_gui_set(loaded = gui_user_params_loaded, 
                                                                current = current_gui_user_params)
                # if changed: 
                #     # # self.win_msg("If you want to plot2D with the new settings remember to re-run  -Channel from the negative space extraction-  section!")
                #     # self.update_status(None, 're-run', self.gui_user_params_loaded, override=True)
    
            set_btn = getattr(self, ptype+'_set')
            set_btn.setChecked(True)
            print('self.gui_user_params: ', self.gui_user_params)

        else: 
            return

    def gui_user_params_n(self, ptype): 

        gui_user_params = {}
        if len(self.gui_key_user_params[ptype]) > 0: 
            gui_user_params[ptype] = {}
            #Get values
            for param in self.gui_key_user_params[ptype].keys(): 
                gui_user_params[ptype][param] = {}
                for item in self.gui_key_user_params[ptype][param].keys(): 
                    num = self.gui_key_user_params[ptype][param][item]['num']
                    gui_user_params[ptype][param][item] = {'num': int(num)}
                    if ptype == 'categorical': 
                        value = getattr(self, 'value_categorical'+str(num)).currentText()
                    else: 
                        value = getattr(self, 'value_'+ptype+str(num)).text()
                    gui_user_params[ptype][param][item]['value'] = value

                self.organ.mH_settings['measure'][param][item] = value

        print('gui_user_params:', gui_user_params)
        print('self.gui_key_user_params:', self.gui_key_user_params)
        self.fill_results()                    

        return gui_user_params
    
    #Plot functions
    def plot_meshes(self, ch, chNS=False):
        self.win_msg('Plotting meshes ('+ch+')')
        print('Plotting meshes ('+ch+')')

        txt = [(0, self.organ.user_organName)]
        obj = []
        if ch != 'all': 
            for cont in ['int', 'tiss', 'ext']: 
                obj.append(self.organ.obj_meshes[ch+'_'+cont].mesh)
        else: 
            print('self.channels:', self.channels)
            if not chNS:
                im_chs = [ch for ch in self.channels if ch != 'chNS']
            else: 
                im_chs = self.channels
            
            for ch in im_chs: 
                for cont in ['ext', 'tiss', 'int']: 
                    obj.append(self.organ.obj_meshes[ch+'_'+cont].mesh)
    
        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(self.organ.get_maj_bounds()))

    def plot_tempObj(self, proc, sub, btn):
        self.win_msg('Plotting meshes ('+proc+'-'+sub+')')
        print('Plotting tempObj ('+proc+'-'+sub+')')
        txt = [(0, self.organ.user_organName)]
        obj = []
        if proc == 'CL': 
            #Get button number
            btn_num = int(btn[-1])-1
            #Get centreline for that position
            cl_to_extract = list(self.organ.mH_settings['measure']['CL'].keys())
            cl_name = cl_to_extract[btn_num]
            ch, cont, _ = cl_name.split('_')
            mesh = self.organ.obj_meshes[ch+'_'+cont]

            if sub == 'SimplifyMesh': 
                # First see if obj_temp is loaded with the info needed
                if self.organ.obj_temp['centreline'][sub][ch+'_'+cont]['mesh'] != None: 
                    m4clf = self.organ.obj_temp['centreline'][sub][ch+'_'+cont]
                else: 
                    # Load objects
                    obj_temp = self.organ.load_objTemp(proc = 'centreline', key = 'SimplifyMesh', 
                                                    ch_cont = ch+'_'+cont, obj_temp = self.organ.obj_temp)
                    m4clf = obj_temp['centreline'][sub][ch+'_'+cont]
            
                item = []
                for key in m4clf: 
                    if isinstance(m4clf[key], dict):
                        for kk in m4clf[key].keys():
                            item.append(m4clf[key][kk])
                    else: 
                        item.append(m4clf[key])
                obj.append(tuple(item))
            else: 
                nPoints = self.organ.mH_settings['wf_info']['centreline']['buildCL']['nPoints']
                mesh = self.organ.obj_meshes[ch+'_'+cont].mesh
                cl_final = self.organ.obj_meshes[ch+'_'+cont].get_centreline(nPoints=nPoints)
                obj = [(mesh, cl_final)]

        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(self.organ.get_maj_bounds()))

    def plot_heatmap3d(self, btn):
        from ..modules.mH_funcMeshes import sphs_in_spline

        txt = [(0, self.organ.user_organName)]
        #Get button number
        btn_num = int(btn[-1])-1
        hm_all = list(self.hm_btns.keys())
        hm_name = hm_all[btn_num]
        short, ch_info = hm_name.split('[')
        self.win_msg('Plotting heatmaps3D ('+hm_name+')')
        print('Plotting heatmaps3D ('+hm_name+')')

        if 'th' in short: 
            ch, cont = ch_info.split('-')
            _, th_val = short.split('_')
            if th_val == 'i2e': #int>ext': 
                mesh_to = self.organ.obj_meshes[ch+'_ext']
                mesh_from = self.organ.obj_meshes[ch+'_int'].mesh
                mtype = 'thck(intTOext)'
                short = 'th_i2e'
                from_name = 'int>ext'
            else:# n_type == 'ext>int': 
                mesh_to = self.organ.obj_meshes[ch+'_int']
                mesh_from = self.organ.obj_meshes[ch+'_ext'].mesh
                mtype = 'thck(extTOint)'
                short = 'th_e2i'
                from_name = 'ext>int'
            mesh_tiss = self.organ.obj_meshes[ch+'_tiss'].mesh
            mesh_thck = self.organ.obj_meshes[ch+'_tiss'].mesh_meas[mtype]

            print('mesh_to.legend:', mesh_to.legend)
            title = mesh_to.legend+'\nThickness [um]\n('+from_name+')'
            mesh_thck = self.set_scalebar(mesh=mesh_thck, name = hm_name, proc = short, title = title)

            txt = [(0, self.organ.user_organName +' - Thickness Measurement Setup')]
            obj = [(mesh_from, mesh_to.mesh), (mesh_tiss), (mesh_thck)]

        else: #'ball' in short
            ch_cont, cl_info = ch_info.split('(CL.')
            ch, cont = ch_cont.split('-')
            from_cl, from_cl_type = cl_info[:-2].split('-')
            # short = 'ball'
            
            #Get meshes
            mesh2ball = self.organ.obj_meshes[ch+'_'+cont]
            cl4ball = self.organ.obj_meshes[from_cl+'_'+from_cl_type].get_centreline()
            sph4ball = sphs_in_spline(kspl=cl4ball,every=0.6)
            sph4ball.legend('sphs_ball').alpha(0.1)
            m_type = 'ballCL('+from_cl+'_'+from_cl_type+')'
            mesh_ball = mesh2ball.mesh_meas[m_type]

            title = mesh2ball.legend+'\nBallooning [um]\nCL('+from_cl+'_'+from_cl_type+')'
            mesh_ball = self.set_scalebar(mesh=mesh_ball, name = hm_name, proc = short, title = title)

            txt = [(0, self.organ.user_organName +' - Ballooning Measurement Setup')]
            obj = [(mesh2ball.mesh, cl4ball, sph4ball), (mesh_ball, cl4ball, sph4ball)]

        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(self.organ.get_maj_bounds()))

    def set_scalebar(self, mesh, name, proc, title):
        if self.gui_thickness_ballooning[name]['default']: 
            min_val = self.organ.mH_settings['measure'][proc]['range_o']['min_val']
            max_val = self.organ.mH_settings['measure'][proc]['range_o']['max_val']
        else: 
            min_val = self.gui_thickness_ballooning[name]['min_val']
            max_val = self.gui_thickness_ballooning[name]['max_val']
        color_map = self.gui_thickness_ballooning[name]['colormap']

        mesh.cmap(color_map)
        mesh.add_scalarbar(title=title, pos=(0.7, 0.05))
        mesh.mapper().SetScalarRange(min_val,max_val)

        return mesh

    def plot_heatmap2d(self, btn): 
        print('Plotting heatmap2d: ', btn)

    def plot_segm_sect(self, btn):
        #btn = cut1_segm1 / cut1_sect1

        #Get button number
        cut, subname = btn.split('_')
        if 'segm' in subname: 
            num = subname.split('segm')[1]
            txt = [(0, self.organ.user_organName + ' - Segment division')]
            list_btns = self.segm_btns
            colors = self.organ.mH_settings['setup']['segm'][cut.title()]['colors']
            name = 'segments'
            short = 'segm'
        else: #sect
            num = subname.split('sect')[1]
            txt = [(0, self.organ.user_organName + ' - Region division')]
            list_btns = self.sect_btns
            colors = self.organ.mH_settings['setup']['sect'][cut.title()]['colors']
            name = 'sections'
            short = 'sect'

        key_list = list(list_btns.keys())
        for key in key_list: 
            cut_key = key.split(':')[0]
            num_key = list_btns[key]['num']
            if cut_key == cut.title() and int(num_key) == int(num): 
                key2cut = key # Cut1:ch1_ext
                break

        self.win_msg('Plotting '+name+' ('+key2cut+')')
        print('Plotting '+name+' ('+key2cut+')')
    
        obj_meshes = []
        print('list_btns: ', list_btns)
        try: 
            #get submesh from list buttons if it was saved in there...
            meshes = list_btns[key2cut]['meshes']
            print('Meshes from try!')
        except: 
            print('Meshes from except!')
            #Get submesh from organ
            cut, subm_info = key2cut.split(':')
            ch, cont = subm_info.split('_') #Cut1_ch1_ext_segm1
            # Do a for to load all the segments of that mesh
            meshes = {}
            print(cut, ch, cont)
            for subm in self.organ.mH_settings['setup'][short][cut]['name_'+name].keys():
                submesh_name = cut.title()+'_'+ch+'_'+cont+'_'+subm
                submesh = self.organ.obj_subm[submesh_name]
                if 'segm' in subm: 
                    meshes[subm] = submesh.get_segm_mesh()
                else: #'sect' in segm
                    print('do this part of the code!')
                    meshes[subm] = submesh.get_sect_mesh()

        for mesh in meshes.keys(): 
            if isinstance(meshes[mesh], vedo.Mesh):
                color = colors[mesh]
                mesh = meshes[mesh]
                mesh.color(color)
                obj_meshes.append(mesh)
            else: 
                pass

        obj = [tuple(obj_meshes)]
        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(self.organ.get_maj_bounds()))

    def plot_segm_section(self, btn): 
        print('plotting..', btn)

    def plot_orient(self, name): 

        ext_ch = self.organ.get_ext_int_chs()
        if isinstance(ext_ch, str) and ext_ch == 'independent':
            ext_ch = self.organ.obj_imChannels[list(self.organ.obj_imChannels.keys())[0]]

        mesh_ext = self.organ.obj_meshes[ext_ch.channel_no+'_tiss']
        cubes = getattr(self.organ, name+'_cube')
        orient_cube = cubes['cube']
        orient_cube_clear = cubes['clear']

        views = self.organ.mH_settings['setup']['orientation'][name].split(', ')
        colors = [[255,215,0,200],[0,0,205,200],[255,0,0,200]]

        txt0 = vedo.Text2D(self.organ.user_organName+' - Reference cube and mesh to visualise planar views in '+name.title()+'...', c=txt_color, font=txt_font, s=txt_size)
        if name == 'roi': 
            namef = name.upper()
        else: 
            namef = name.title()

        txt1 = vedo.Text2D('- Reference cube with coloured faces that represent planar views in '+namef+'...', c=txt_color, font=txt_font, s=txt_size)
        
        mks = []; sym = ['o']*len(views)
        for n, view, col in zip(count(), views, colors):
            mks.append(vedo.Marker('*').c(col[0:-1]).legend(view))
        lb = vedo.LegendBox(mks, markers=sym, font=txt_font, 
                            width=leg_width/1.5, height=leg_height/1.5)
        
        path_logo = path_mHImages / 'logo-07.jpg'
        logo = vedo.Picture(str(path_logo))

        vp = vedo.Plotter(N=2, axes=1)
        vp.add_icon(logo, pos=(0.1,1), size=0.25)
        vp.show(mesh_ext.mesh, orient_cube_clear,txt0, at=0)
        vp.show(orient_cube, lb, txt1, at=1, azimuth=45, elevation=30, zoom=0.8, interactive=True)

    def plot_cl_ext(self, cut): 

        clRib_type = 'ext2sides'
        cl_name = self.gui_sect[cut.title()]['centreline'].split('(')[1][:-1]
        mesh_cl = self.organ.obj_meshes[cl_name]
        nPoints = self.gui_sect[cut.title()]['nPoints']
        nRes = self.gui_sect[cut.title()]['nRes']
        ext_plane = getattr(self, 'extend_dir_'+cut.lower())['plane_normal']
        cl_ribbon = mesh_cl.get_clRibbon(nPoints=nPoints, nRes=nRes, 
                                            pl_normal=ext_plane, 
                                            clRib_type=clRib_type)
        #Get first mesh from buttons 
        name_mesh = list(self.sect_btns.keys())[0].split(':')[1]
        mesh2cut = self.organ.obj_meshes[name_mesh]

        #Get Filled mask corresponding to sect1
        mask_name = self.organ.mH_settings['wf_info']['sections'][cut.title()]['mask_name'] # getattr(self.organ, 'mask_sect_'+cut.lower())
        mask_dir = self.organ.dir_res(dir ='s3_numpy') / mask_name
        s3_mask = np.load(str(mask_dir))
        sect_name = self.organ.mH_settings['setup']['sect'][cut.title()]['name_sections']['sect1']
        sect_namef = 'Mask Section No.1 ('+sect_name+')'
        mask_cube = s3_to_mesh(s3_mask, res=mesh2cut.resolution, name=sect_namef, color='coral')
        mask_cube.alpha(0.1)

        txt = [(0, self.organ.user_organName + ' - Centreline Extension ('+cut.title()+')')]
        obj = [(mesh2cut.mesh, cl_ribbon), (mesh2cut.mesh, cl_ribbon, mask_cube)]
        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(self.organ.get_maj_bounds()), azimuth=45, elevation=20)

    #Help functions
    def help(self, process): 
        print('User clicked help '+process)

    def run_segmentationAll(self): 
        print('Running segmentation All!')
    
    #Save functions
    def save_results(self): 
        if self.cB_transpose.isChecked():
            df_final = self.df_res.T
        else: 
            df_final = self.df_res
        
        ext = self.cB_extension.currentText()
        filename = self.organ.folder+'_results'+ext
        df_dir = self.organ.dir_res() / filename
        df_final.to_csv(df_dir, index=True) 
        alert('countdown') 
        self.win_msg('Results file  -'+ filename + '  was succesfully saved!')

    #Functions for all tabs
    def continue_next_tab(self): #A delete bit
        if self.tabWidget.currentIndex() == 0: 
            #check the status of all channels 
            channels = [ch for ch in self.channels if ch != 'chNS']
            ch_status = []
            for ch in channels: 
                ch_status.append(self.organ.workflow['morphoHeart']['ImProc'][ch]['Status'])

            if all(ch_status):
                self.tabWidget.setCurrentIndex(1)
        
        elif self.tabWidget.currentIndex() == 1:
            print('develop') 
        
        elif self.tabWidget.currentIndex() == 2:
            print('develop')

        else: #self.tabWidget.currentIndex() == 3: 
            print('develop') 

    def init_morphoCell_tab(self): 
        print('Setting up morphoCell Tab')

    def init_plot_tab(self): 
        print('Setting Plot Tab')

    #Menu functions
    def save_project_and_organ_pressed(self, alert_on=True):
        print('Save project and organ was pressed')
        self.organ.save_organ(alert_on)
        self.proj.add_organ(self.organ)
        self.proj.save_project(alert_on)
        self.win_msg('Project  -'+ self.proj.user_projName + '-  and Organ  -'+ self.organ.user_organName +'-  were succesfully saved!')
    
    def close_morphoHeart_pressed(self):
        print('Close was pressed')
        msg = ["Do you want to save the changes to this Organ and Project before closing?","If you don't save your changes will be lost."]
        self.prompt = Prompt_save_all(msg, info=[self.organ, self.proj], parent=self)
        self.prompt.exec()
        print('output:',self.prompt.output, '\n')

        if self.prompt.output == 'Save All': 
            for item in [self.organ, self.proj]: 
                if isinstance(item, Organ): 
                    item.save_organ()
                    self.win_msg('Organ '+ self.organ.user_organName +' was saved succesfully!')
                elif isinstance(item, Project):
                    item.save_project()
                    self.win_msg('Project '+ self.proj.user_projName +' was saved succesfully!')
    
            print('All saved!')
            self.close()

        elif self.prompt.output == 'Discard': 
            print('Save All Discarded')
            self.close()
        
        elif self.prompt.output == 'Cancel': 
            print('Save All Cancelled')

    def closeEvent(self, event):
        msg = ["Do you want to save the changes to this Organ and Project before closing?","If you don't save your changes will be lost."]
        self.prompt = Prompt_save_all(msg, info=[self.organ, self.proj], parent=self)
        self.prompt.exec()
        print('output:',self.prompt.output, '\n')

        if self.prompt.output == 'Save All': 
            for item in [self.organ, self.proj]: 
                if isinstance(item, Organ): 
                    item.save_organ()
                    self.win_msg('Organ file saved correctly!')
                elif isinstance(item, Project):
                    item.save_project()
                    self.win_msg('Project file saved correctly!')
            print('All saved!')
            event.accept()

        elif self.prompt.output == 'Discard': 
            print('Save All Discarded')
            event.accept()
        
        elif self.prompt.output == 'Cancel': 
            print('Save All Cancelled')
            event.ignore()

        # reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

		# if reply == QMessageBox.Yes:
		# 	event.accept()
		# 	print('Window closed')
		# else:
		# 	event.ignore()

#%% Other classes GUI related - ########################################################
class MyToggle(QtWidgets.QPushButton):
    #https://stackoverflow.com/questions/56806987/switch-button-in-pyqt
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(70)
        self.setMinimumHeight(22)
        self.setStyleSheet("color: rgb(0,0,0)")

    def paintEvent(self, event):
        label = "ON" if self.isChecked() else "OFF"
        bg_color = QColor(162,0,122,180) if self.isChecked() else QColor(255,255,255)
        brush_color = QColor(255,255,255) if self.isChecked() else QColor(0,0,0)

        radius = 10
        width = 20
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(center)
        painter.setBrush(brush_color)

        pen = QPen(QColor(192,192,192))
        pen.setWidth(1)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignmentFlag.AlignCenter, label)

        font = QFont()
        font.setFamily('Calibri Light')
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)

class MyTreeItem(QtWidgets.QWidget): #to delete
    def __init__(self, subproc, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QHBoxLayout(self)
        # keep only the default margin on the left
        layout.setContentsMargins(-1, 0, 0, 0)
        self.label = QtWidgets.QLabel()
        self.label.setText(subproc)

        # verticalSpacer = QSpacerItem(20, 40)#, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.status = QtWidgets.QLabel()
        self.status.setStyleSheet("QLabel {background-color:rgb(255, 255, 0); border-width: 2px; border-style: outset; border-color: rgb(0,0, 0);}")
        self.status.resize(18, 18)
        self.status.setMaximumWidth(20)

        layout.addWidget(self.label)
        # layout.addItem(verticalSpacer)
        layout.addWidget(self.status)
        layout.addStretch()
        self.setMaximumWidth(200)

class MyPandasTable(QAbstractTableModel): #to delete
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
    
    # def __init__(self, data):
    #     super(TableModel, self).__init__()
    #     self._data = data

    def rowCount(self, index): 
        return self._data.shape[0]
    
    def columnCount(self, index): 
        return self._data.shape[1]
    
    def data(self, index, role):
        value = self._data.iloc[index.row(), index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value
            if isinstance(value, str):
                # Render strings with quotes
                return '"%s"' % value
            return value
        
        if role == Qt.ItemDataRole.TextAlignmentRole:
            # value = self._data[index.row()][index.column()]
            # Align right, vertical middle.
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter
        
        if role == Qt.ItemDataRole.ForegroundRole:
            # value = self._data[index.row()][index.column()]
            if isinstance(value, str):
                return QColor('blue')
        
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

#%% SOUNDS - ########################################################
# Sound functions
def add_sound_bar(win, layout):
    win.sound_on_off = MyToggle()
    win.sound_on_off.setChecked(True)
    layout.insertWidget(len(layout), win.sound_on_off)

    win.sound_type = QtWidgets.QComboBox()
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(win.sound_type.sizePolicy().hasHeightForWidth())
    win.sound_type.setSizePolicy(sizePolicy)
    win.sound_type.setMinimumSize(QtCore.QSize(70, 20))
    win.sound_type.setMaximumSize(QtCore.QSize(70, 20))
    win.sound_type.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
    win.sound_type.setAutoFillBackground(False)
    win.sound_type.setStyleSheet("border-color: rgb(173, 173, 173); font: 25 10pt 'Calibri Light';")
    win.sound_type.setFrame(True)
    win.sound_type.addItems(['All', 'Minimal'])
    layout.insertWidget(len(layout), win.sound_type)

    # Buttons
    # - Sounds on/off
    win.sound_on_off.clicked.connect(lambda: sound_toggled(win))
    win.sound_type.currentIndexChanged.connect(lambda: sound_opt(win))

def sound_toggled(win): 
    if win.sound_on_off.isChecked(): 
        # print('button is ON')
        win.sound_type.setEnabled(True)
        win.sound = (True, win.sound_type.currentText())
    else: 
        # print('button is OFF')
        win.sound_type.setEnabled(False)
        win.sound = (False, )
    mH_config.gui_sound = win.sound
    print('changed gui_sound:', win.sound)

def sound_opt(win): 
    win.sound = (True, win.sound_type.currentText())
    mH_config.gui_sound = win.sound
    print('opt gui_sound:', win.sound)
    
#%% GUI Related Functions - ########################################################
# Update workflow colors
def update_status(root_dict, items, fillcolor, override=False): 
    if not override: 
        wf_status = get_by_path(root_dict, items)
        # print('wf_status gbp:', wf_status)
    else: 
        wf_status = items
        # print('wf_status:', wf_status)

    if wf_status == 'NI': 
        color = 'rgb(255, 255, 127)'
    elif wf_status == 'Initialised': 
        color = 'rgb(255, 151, 60)'
    elif wf_status == 'DONE' or wf_status == 'Done':
        color = 'rgb(0, 255, 0)'
    elif wf_status == 'N/A': 
        color = 'rgb(0, 0, 0)'
    elif wf_status == 're-run': 
        color = 'rgb(35, 207, 255)'
    elif wf_status == 'DONE-NoCut':
        color = 'rgb(0, 85, 127)'
    elif wf_status == 'DONE-Loaded':
        color = 'rgb(0,170,127)'
    else: 
        color = 'rgb(255, 0, 255)'
        print('other status unknown: ', fillcolor)
    
    color_btn(btn = fillcolor, color = color)

# Button general functions
def setup_play_btn(btn, win): 
    pixmapi = getattr(QStyle.StandardPixmap, 'SP_MediaPlay')
    icon = win.style().standardIcon(pixmapi)
    btn.setIcon(icon)
    st1 = 'QPushButton{border-radius:12px; border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); background-color:  rgb(0, 199, 0);}'
    st2 = ' QPushButton:hover{background-color: rgb(0, 227, 0); border-color: rgb(115, 115, 115)}'
    st3 = ' QPushButton:checked{background-color: rgb(0, 85, 0); border-color: rgb(115, 115, 115)}'
    btn.setStyleSheet(st1+st2+st3)
    
def color_btn(btn, color, small=True): 

    if isinstance(color, list): 
        color = 'rgb'+str(tuple(color))
    else: 
        pass

    if small: 
        pt = "25 2pt 'Calibri Light'"
    else: 
        pt = "25 10pt 'Calibri Light'"

    if isinstance(btn, QPushButton):#QLineEdit):
        color_txt = "QPushButton{border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); background-color: "+str(color)+"; font: "+pt+"} QPushButton:hover{border-color: rgb(255, 255, 255)}"
    else: 
        color_txt = "background-color: "+color+"; border-color: rgb(0, 0, 0); border-width: 1px; border-style: outset; font: "+pt+"; color: "+color+";"

    btn.setStyleSheet(color_txt)

def always_checked(tick):
    tick.setChecked(True)
    if tick.isChecked():
        tick.setChecked(True)
    else: 
        tick.setChecked(True)

#String validation
def split_str(input_str):
    inv_chars = ['(',')', ':', '-']
    input_str = input_str.split(',')
    output_str = []
    for xx, nam in enumerate(input_str):
        if ' ' in nam: 
            if nam[0] == ' ':
                nam = nam[1:]
            if nam[-1] == ' ':
                nam = nam[0:-1]
            if ' ' in nam: 
                nam = nam.replace(' ', '_')
            input_str[xx] = nam
        for char in inv_chars:
            if char in nam:
                # print('char:', char)
                nam = nam.replace(char,'')
        if nam == '': 
            nam.remove('')
        # print(nam)
        output_str.append(nam)

    # print('Result split_str: ', output_str)
    return output_str

def validate_txt(input_str):
    inv_chars = ['(',')', ':', '-', '/', '\\', '.']
    for char in inv_chars:
        if input_str.find(char) != -1:
            error = char
            break
        else:
            error = None
    return error

# QTextEdit label and size
def set_qtextedit_text(label, dict_names, stype): 
    # names_list = []
    names_f = ''
    style = '</style></head><body style=" font-family:"Calibri Light"; font-size:10pt; font-weight:24; font-style:normal;">'
    beg = '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">'
    end = '</p>'
    end_end = '</p></body></html>'
    for bb, segm in enumerate(list(dict_names.keys())):
        name_add = dict_names[segm]
        # names_list.append(dict_names[segm])
        if bb == 0: 
            names_f = style+beg+roman_num[stype][bb]+'. '+name_add
        else: 
            names_f = names_f+', '+end+beg+roman_num[stype][bb]+'. '+name_add
    names_f = names_f+end_end
    label.setHtml(names_f)
    # print('bb:', bb)
    return bb

def set_qtextedit_size(label, size):
    w, h = size
    # print(size)
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
    sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
    label.setSizePolicy(sizePolicy)
    label.setMinimumSize(QtCore.QSize(w, h))
    label.setMaximumSize(QtCore.QSize(w, h))

# Color palette as RGB
def palette_rbg(name:str, num:int):
    rgb = []
    palette =  sns.color_palette(name, num)
    for color in palette:
        tup = []
        for value in color:
            tup.append(round(value*255))
        rgb.append(tuple(tup))

    return rgb

def set_txts(): 
    #% Link to images
    mH_icon = 'images/logos_w_icon_2o5mm.png'#'images/cat-its-mouth-open.jpg'#
    mH_big = 'images/logos_7o5mm.png'
    mH_top_corner = 'images/logos_1o75mm.png'
    mH_images = [mH_icon, mH_big, mH_top_corner]

    # Play buttons
    play_bw = 'images/logos_play_black_white.png'
    play_gw = 'images/logos_play_green_white.png'
    play_gb = 'images/logos_play_green_dark.png'
    play_grw = 'images/logos_play_gray_white.png'
    play_colors = [play_bw, play_gw, play_gb, play_grw]

    play_btn = "QPushButton {border-image: url("+play_gw+"); background-repeat: no-repeat; width: 65px; height: 56px;} "
    hover_btn = "QPushButton:hover {border-image: url("+play_bw+")} "
    pressed_btn = "QPushButton:checked {border-image: url("+play_gb+")}; "
    disbled_btn = "QPushButton:disabled {border-image: url("+play_grw+")}; "
    style_play = play_btn+hover_btn+pressed_btn+disbled_btn

    html_txt = ['<html><head><meta name="qrichtext" content="1" /><style type="text/css"> p, li { white-space: pre-wrap; } </style></head><body style=" font-family:"Calibri Light"; font-size:11pt; font-weight:24; font-style:normal;">',
                '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">',
                '</p></body></html>']
    reg_exps = {'num': '[+]?((\d+(\.\d*)?)|(\.\d+))', 'all': '.*'}

    error_style = 'font: 25 9pt "Calibri Light"; background-color: rgb(250, 250, 250); color: rgb(217, 48, 42);'
    note_style = 'font: 25 9pt "Calibri Light"; background-color: rgb(250, 250, 250); color: rgb(0, 161, 118);'
    msg_style = 'font: 25 9pt "Calibri Light"; background-color: rgb(250, 250, 250);color: rgb(170, 0, 127);'
    tE_styles = [error_style, note_style, msg_style]

    # https://www.pythonguis.com/faq/avoid-gray-background-for-selected-icons/
    list_all = [mH_images, play_colors, style_play, html_txt, reg_exps, tE_styles]
    return list_all

others = False 
if others:
    #Others 
    # class Dialog_mH(QDialog):
    #     def __init__(self, title:str, msg:str, parent=None):
    #         super().__init__()
    #         uic.loadUi('gui/prompt_options_select.ui', self)
    #         self.setWindowTitle(title)
    #         self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
    #         self.setWindowIcon(QIcon(mH_icon))
    #         self.textEdit.setText(msg)
    #         self.parent = parent
    #         layout = self.hLayout
    #         btn_stylesheet = "QPushButton{height:20; padding:0px; width:100; border-radius:10px; border-width: 1px;border-style: outset; border-color: rgb(66, 66, 66); background-color: rgb(211, 211, 211); color: rgb(39, 39, 39); font: 11pt \"Calibri Light\";} QPushButton:hover{background-color: #eb6fbd; border-color: #672146;}"
            
    #         btn_yes =  QtWidgets.QPushButton()
    #         btn_yes.setStyleSheet(btn_stylesheet)
    #         btn_yes_name = 'Yes'
    #         btn_yes.setObjectName(btn_yes_name)
    #         btn_yes.setText(btn_yes_name)
    #         self.btn_yes = btn_yes
    #         self.hLayout.addWidget(self.btn_yes)
    #         btn_yes.clicked.connect(lambda: self.yes_func())

    #         btn_no =  QtWidgets.QPushButton()
    #         btn_no.setStyleSheet(btn_stylesheet)
    #         btn_no_name = 'No'
    #         btn_no.setObjectName(btn_no_name)
    #         btn_no.setText(btn_no_name)
    #         self.btn_no = btn_no
    #         self.hLayout.addWidget(self.btn_no)
    #         btn_no.clicked.connect(lambda: self.no_func())

    #         self.setModal(True)
    #         self.show()
        
    #     def yes_func(self):
    #         print('Yes!')
    #         self.parent.prompt_val.setText('Yes')
    #         self.close()

    #     def no_func(self):
    #         print('No!')
    #         self.parent.prompt_val.setText('No')
    #         self.close()
        
    # class Prompt_options_input(QDialog):
    #     def __init__(self, title:str, msg:str, res:dict, parent=None):
    #         super().__init__(parent)
    #         uic.loadUi('gui/prompt_options_input.ui', self)
    #         self.setWindowTitle(title)
    #         self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
    #         self.setWindowIcon(QIcon(mH_icon))
    #         self.textEdit_msg.setText(msg)

    #         #Set options list 
    #         res_txt = ''
    #         for num, item in res.items():
    #             res_txt += '#'+str(num)+': '+ item+'\n'
    #         self.textEdit_options.setText(res_txt)
    #         print(res_txt)

    #         reg_ex = QRegularExpression("(\d+(?:-\d+)?)((?:(?:,)(\d+(?:-\d+)?))*)")
    #         input_validator = QRegularExpressionValidator(reg_ex, self.user_input)
    #         self.user_input.setValidator(input_validator)

    #         self.buttonBox.accepted.connect(self.accept)
    #         self.buttonBox.rejected.connect(self.reject)
    #         self.show()

    # https://www.pythonguis.com/tutorials/pyqt-dialogs/
    #
    #Check: https://programtalk.com/python-examples/PyQt5.QtWidgets.QDialogButtonBox.Yes/
    #https://www.youtube.com/watch?v=vIqw411xoj0
    #https://www.youtube.com/watch?v=RI646fqeFDQ
    #https://www.pythonguis.com/tutorials/pyqt6-creating-dialogs-qt-designer/
    #https://www.google.com/search?client=firefox-b-d&q=custom+inputdialogs+pyqt6
    #https://pythonpyqt.com/pyqt-input-dialog/
    #https://python.hotexamples.com/examples/PyQt5.QtWidgets/QDialogButtonBox/setStandardButtons/python-qdialogbuttonbox-setstandardbuttons-method-examples.html
    pass

#%% Module loaded
print('morphoHeart! - Loaded gui_classes')
list_all = set_txts()
mH_images, play_colors, style_play, html_txt, reg_exps, tE_styles = list_all
mH_icon, mH_big, mH_top_corner = mH_images
play_bw, play_gw, play_gb, play_btn = play_colors
error_style, note_style, msg_style = tE_styles
roman_num ={'sect': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], 
            'segm': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']}