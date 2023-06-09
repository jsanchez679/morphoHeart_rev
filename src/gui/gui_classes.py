
'''
morphoHeart_GUI_classes

Version: Apr 26, 2023
@author: Juliana Sanchez-Posada

'''
#%% Imports - ########################################################
# import sys
from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import pyqtSlot, QDate, Qt, QRegularExpression, QRect, QSize
from PyQt6.QtWidgets import (QDialog, QApplication, QMainWindow, QWidget, QFileDialog, QTabWidget,
                              QGridLayout, QVBoxLayout, QHBoxLayout, QLayout, QLabel, QPushButton, QLineEdit,
                              QColorDialog, QTableWidgetItem, QCheckBox, QTreeWidgetItem, QSpacerItem, QSizePolicy, 
                              QDialogButtonBox, QMessageBox, QHeaderView)
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

#%% morphoHeart Imports - ##################################################
# from .src.modules.mH_funcBasics import get_by_path
# from .src.modules.mH_funcMeshes import * 
from ..modules.mH_funcBasics import get_by_path
from ..modules.mH_funcContours import checkWfCloseCont
from ..modules.mH_funcMeshes import plot_grid
from ..modules.mH_classes_new import Project, Organ
from .config import mH_config

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
        # print('gui_sound:',gui_sound)

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
                rB.setStyleSheet("font: 25 10pt \"Calibri Light\";")
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
                    reg_ex = QRegularExpression(reg_exps[items[key]['regEx']])
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
                cB.setStyleSheet("font: 25 10pt \"Calibri Light\";")
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
    def __init__(self, msg:str, title:str, info:str, parent=None):
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
        if len(user_input) <= 1: 
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

class Propmt_save_all(QDialog): 
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
        # self.meas_param = None
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
        #- morphoCell
        self.init_mCell_tab()

        #Project template
        self.cB_proj_as_template.stateChanged.connect(lambda: self.save_as_template())
        self.lineEdit_template_name.setValidator(QRegularExpressionValidator(self.reg_ex, self.lineEdit_template_name))

    def win_msg(self, msg): 
        if not self.tabWidget.isEnabled(): 
            tE = self.tE_validate
        else: 
            tE = self.tE_validate2

        if msg[0] == '*':
            tE.setStyleSheet(error_style)
            msg = 'Error: '+msg
        elif msg[0] == '!':
            tE.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            tE.setStyleSheet(msg_style)
        tE.setText(msg)

    def init_gral_proj_set(self):
        now = QDate.currentDate()
        self.dateEdit.setDate(now)

        self.checked_analysis = {'morphoHeart': self.checkBox_mH.isChecked(), 
                                'morphoCell': self.checkBox_mC.isChecked(), 
                                'morphoPlot': self.checkBox_mP.isChecked()}
        #Set validator
        self.lineEdit_proj_name.setValidator(QRegularExpressionValidator(self.reg_ex, self.lineEdit_proj_name))

        # Create a new project
        self.win_msg("Create a new project by providing a project's name, directory and analysis pipeline. Then press 'Create' to create the new project.")

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

    def init_mCell_tab(self):
        pass

    #Functions for General Project Settings   
    def get_proj_dir(self):
        self.button_create_initial_proj.setChecked(False)
        toggled(self.button_create_initial_proj)
        self.button_select_proj_dir.setChecked(True)
        toggled(self.button_select_proj_dir)
        response = QFileDialog.getExistingDirectory(self, caption='Select a Directory to save New Project Files')
        self.proj_dir_parent = Path(response)
        self.lab_filled_proj_dir.setText(str(self.proj_dir_parent))

    def validate_new_proj(self): 
        valid = []; error_txt = ''
        #Get project name
        if len(self.lineEdit_proj_name.text())<5:
            error_txt = '*Project name needs to have at least five (5) characters'
            self.win_msg(error_txt)
            return
        elif validate_txt(self.lineEdit_proj_name.text()) != None:
            error_txt = "Please avoid using invalid characters in the project's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt)
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
            self.win_msg(error_txt)
            return
        else: 
            valid.append(True)
        
        #Get Directory
        if isinstance(self.proj_dir_parent, str): 
            error_txt = '*Please select a project directory where the new project will be saved.'
            self.win_msg(error_txt)
            return
        else:  
            if self.proj_dir_parent.is_dir() and len(str(self.proj_dir_parent))>1:
                valid.append(True)
            else: 
                self.button_select_proj_dir.setChecked(False)
                toggled(self.button_select_proj_dir)
                error_txt = '*The selected project directory is invalid. Please select another directory.'
                self.win_msg(error_txt)
                return

        #Check and if all valid create new project
        if len(valid)== 3 and all(valid):
            proj_folder = 'R_'+self.proj_name#.replace(' ','_')
            self.proj_dir = self.proj_dir_parent / proj_folder
            if self.proj_dir.is_dir():
                self.win_msg('*There is already a project named "'+self.proj_name+'" in the selected directory. Please select a different name for the new project.')
                return 
            else: 
                self.lab_filled_proj_dir.setText(str(self.proj_dir))
                self.win_msg('All good. Continue setting up new project!')   
                self.create_new_proj()  
        else: 
            self.win_msg(error_txt)
            return 

    def create_new_proj(self):
        toggled(self.button_create_initial_proj)
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
            self.win_msg(error_txt)
            return
        else: 
            valid.append(True)

        roi_or = self.cB_roi_orient.currentText()
        if roi_or == '--select--': 
            error_txt = '*Please select axis labels for the Organ/ROI'
            self.win_msg(error_txt)
            return
        else: 
            valid.append(True)

        if len(valid) == 2 and all(valid):
            # print(self.cB_stack_orient.currentText())
            self.mH_settings['orientation'] = {'stack': self.cB_stack_orient.currentText(),
                                                'roi': self.cB_roi_orient.currentText()}
            self.win_msg('Great! Continue setting up the new project!')
            self.button_set_orient.setChecked(True)
            toggled(self.button_set_orient)
            # print('self.mH_settings (set_orientation_settings):', self.mH_settings)
            return True
        else: 
            self.button_set_orient.setChecked(False)
            toggled(self.button_set_orient)
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
            color_txt = "background-color: rgb(255, 255, 255); color: rgb(255, 255, 255); font: 25 2pt 'Calibri Light'"
            for cont in ['int', 'tiss', 'ext']:
                fill = getattr(self, 'fillcolor_'+name+'_'+cont)
                fill.setStyleSheet(color_txt)
                fill.setText('rgb(255, 255, 255)')

    def color_picker(self, name):
        color = QColorDialog.getColor()
        if color.isValid():
            # print('The selected color is: ', color.name())
            fill = getattr(self, 'fillcolor_'+name)
            fill.setStyleSheet("background-color: "+color.name()+"; color: "+color.name()+"; font: 25 2pt 'Calibri Light'")#+"; border: 1px solid "+color.name())
            fill.setText(color.name())
            # print('Color:', fill.text())
            
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
                        fill.setStyleSheet("background-color: "+color+"; color: "+color+"; font: 25 2pt 'Calibri Light'")#+"; border: 1px solid "+color.name())
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
        # print('ch_ticked:',ch_ticked)
        if not any(ch_ticked):
            error_txt = '*Please select at least one channel.'
            self.win_msg(error_txt)
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
                    self.win_msg(error_txt)
                    return
                elif validate_txt(ch_name) != None:
                    error_txt = "*Please avoid using invalid characters in the channel's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
                    self.win_msg(error_txt)
                    return
                else: 
                    names.append(ch_name)
                    names_valid.append(True)

        if all(names_valid):
            valid.append(True)

        #Check names are different
        if len(names) > len(set(names)):
            error_txt = '*The names given to the selected channels need to be unique.'
            self.win_msg(error_txt)
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
            self.win_msg(error_txt)
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
                    self.win_msg(error_txt)
                    return
                else: 
                    valid.append(True)
            elif sum(ch_ticked) == 2: 
                if internal_count != 1 or external_count != 1:
                    error_txt = '*One channel needs to be selected as the internal layer and other as the external.'
                    self.win_msg(error_txt)
                    return
                elif internal_count == 1 and external_count == 1:
                    valid.append(True)

            elif sum(ch_ticked) > 2: 
                if internal_count != 1 or external_count != 1:
                    error_txt = '*One channel needs to be selected as the internal layer, other as the external and the other(s) as middle/independent.'
                    self.win_msg(error_txt)
                    return
                elif internal_count == 1 and external_count == 1:
                    valid.append(True)
        else: 
            if sum(ch_ticked) == 1: 
                if indep_count != 1: 
                    error_txt = '*Please define the active channel as independent layer.'
                    self.win_msg(error_txt)
                    return
                else: 
                    valid.append(True)
            elif blank_count != 0: 
                error_txt = '*Please define the channel organisation for all channels.'
                self.win_msg(error_txt)
                return
            else: 
                valid.append(True)

        if sum(ch_ticked) == 1 and self.tick_chNS.isChecked() and (self.ck_chs_contained.isChecked() or self.ck_chs_allcontained.isChecked()):
            error_txt = '*At least an external channel and an internal channel need to be selected to create a tissue from the negative space.'
            self.win_msg(error_txt)
        else: 
            valid.append(True)

        if all(valid):
            self.win_msg('All done!... Press -Set Initial Settings- to continue.')
            self.set_initial_settings()
        else: 
            return False

    def set_initial_settings(self):
        self.set_processes.setEnabled(True)
        toggled(self.button_set_initial_set)
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
        self.ext_chNS.clear(); self.int_chNS.clear()
        self.ext_chNS.addItems(['----']+self.ch_selected)
        self.int_chNS.addItems(['----']+self.ch_selected)
        
        self.win_msg("Great! Now select the processes you would like to include in the workflow and setup their details.")

        return True
    
    def set_selected_processes(self): 
        #Get info from checked boxes
        __ = self.checked('chNS')
        #---- Segments
        __ = self.checked('segm')   
        #---- Sections
        __ = self.checked('sect')
        # print(self.mH_settings)

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

        self.button_set_processes.setChecked(True)
        toggled(self.button_set_processes)

    # -- Functions for ChannelNS
    def validate_chNS_settings(self): 
        valid = []; error_txt = ''
        #Check name
        name_chNS = self.chNS_username.text()
        names_ch = [self.mH_settings['name_chs'][key] for key in self.mH_settings['name_chs'].keys()]
        # print('names_ch:',names_ch)
        if len(name_chNS)< 3: 
            error_txt = '*Channel from the negative space must have a name with at least three (3) characters.'
            self.win_msg(error_txt)
            return
        elif validate_txt(name_chNS) != None:
            error_txt = "*Please avoid using invalid characters in the chNS's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt)
            return
        else: 
            if name_chNS not in names_ch:
                valid.append(True)
            else:
                error_txt = '*The name given to the channel obtained from the negative space needs to be different to that of the other channels.'
                self.win_msg(error_txt)
                return
            
        #Check colors
        all_colors = []
        for cont in ['int', 'tiss', 'ext']:
            all_colors.append(getattr(self, 'fillcolor_chNS_'+cont).text() != '')
        
        if not all(all_colors):
            error_txt = '*Make sure you have selected colors for the channel obtained from the negative space.'
            self.win_msg(error_txt)
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
                self.win_msg(error_txt)
                return
            else: 
                valid.append(True)
        else: 
            error_txt = '*Please select the internal and external channels and contours that need to be used to extract the channel from the negative space.'
            self.win_msg(error_txt)
            return
        
        #Check operation
        chNS_operation = self.chNS_operation.currentText()
        if chNS_operation != '----': 
            valid.append(True)
        else: 
            error_txt = '*Please select an operation to extract the channel from the negative space.'
            self.win_msg(error_txt)
            return
            
        if all(valid): # and len(valid)== 4 
            self.win_msg('All done setting ChannelNS!...')
            self.button_set_chNS.setChecked(True)
            self.set_chNS_settings()
            toggled(self.button_set_chNS)
            return True
        else: 
            self.button_set_chNS.setChecked(False)
            toggled(self.button_set_chNS)
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
        # print(self.mH_settings)

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
                    self.win_msg(error_txt)
                    return
                elif len(set(names_segm)) != int(no_segm):
                    error_txt = '*'+cut+": Segment names need to be different."
                    self.win_msg(error_txt)
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
                    self.win_msg(error_txt)
                    return

                #Check measurement parameters to measure
                meas_vol = getattr(self, 'cB_volume_'+stype).isChecked()
                meas_area = getattr(self, 'cB_area_'+stype).isChecked()
                meas_ellip = getattr(self, 'cB_ellip_'+stype).isChecked()
                if any([meas_vol, meas_area, meas_ellip]):
                    valid.append(True)
                else: 
                    error_txt = "*Please select the measurement parameter(s) (e.g. volume and/or surface area) you want to extract from the segments"
                    self.win_msg(error_txt)
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
                    self.win_msg(error_txt)
                    return
                elif len(set(names_sect)) != 2:
                    error_txt = '*'+cut+": Section names need to be different."
                    self.win_msg(error_txt)
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
                    self.win_msg(error_txt)
                    return
                
                #Check measurement parameters to measure
                meas_vol = getattr(self, 'cB_volume_'+stype).isChecked()
                meas_area = getattr(self, 'cB_area_'+stype).isChecked()
                if any([meas_vol, meas_area]):
                    valid.append(True)
                else: 
                    error_txt = "*Please select the measurement parameter(s) (e.g. volume and/or surface area) you want to extract from the sections"
                    self.win_msg(error_txt)
                    return
                
            if len(valid) == 3 and all(valid): 
                valid_all.append(True)
        
        if all(valid_all): 
            self.win_msg('All good! Sections have been set (1).')
            self.set_sect_settings()
        else: 
            print('Aja? - sections')

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
        segm_settings['measure'] = {'Vol': meas_vol, 'SA': meas_area, 'Ellip': meas_ellip}
        
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
        toggled(self.button_set_segm)

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
            self.win_msg('All good! Sections have been set.')
        else: 
            self.button_set_sect.setChecked(False)
        toggled(self.button_set_sect)

    def validate_set_all(self): 
        print('\n\nValidating Project!')
        valid = []
        if self.mH_user_params != None and self.set_meas_param_all.isChecked():
            valid.append(True)
        else: 
            error_txt = '*You need to set the parameters you want to extract from the segmented tissues before creating the new project.'
            self.win_msg(error_txt)
            return

        if self.checked('segm'): 
            if self.button_set_segm.isChecked():
                valid.append(True)
            else: 
                error_txt = '*You need to set segments settings before creating the new project.'
                self.win_msg(error_txt)
                return
            
        if self.checked('sect'): 
            if self.button_set_sect.isChecked():
                valid.append(True)
            else: 
                error_txt = '*You need to set sections settings before creating the new project.'
                self.win_msg(error_txt)
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
            self.win_msg(error_txt)
            return
        if self.button_set_initial_set.isChecked(): 
            valid.append(True)
        else: 
            error_txt = '*You need to set initial settings first to set measurement parameters.'
            self.win_msg(error_txt)
            return
        if self.checked('chNS'): 
            if self.button_set_chNS.isChecked():
                valid.append(True)
            else: 
                error_txt = '*You need to set Channel NS settings first to set measurement parameters.'
                self.win_msg(error_txt)
                return
            
        if all(valid): 
            return True
        
    # -- Tab general functions
    def tabChanged(self):
        print('Tab was changed to ', self.tabWidget.currentIndex())

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

    def win_msg(self, msg): 
        if msg[0] == '*':
            self.tE_validate.setStyleSheet(error_style)
            msg = 'Error: '+msg
        elif msg[0] == '!':
            self.tE_validate.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            self.tE_validate.setStyleSheet(msg_style)
        self.tE_validate.setText(msg)

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
            self.win_msg(error_txt)
            return
        elif validate_txt(param_name) != None:
            error_txt = "*Please avoid using invalid characters in the parameter's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt)
            return
        else: 
            valid.append(True)
        
        if len(param_abbr)<3: 
            error_txt = "*Parameter's abbreviation needs to have between 3 and 12 characters."
            self.win_msg(error_txt)
            return
        elif validate_txt(param_abbr) != None:
            error_txt = "*Please avoid using invalid characters in the parameter's abbreviation e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt)
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
                self.win_msg(error_txt)
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
            self.win_msg(error_txt)
            return 
        else: 
            for name in names: 
                if not names[name]['ch']: 
                    error_txt = "*You have not selected the channel centreline to use for "+name
                    self.win_msg(error_txt)
                    return 
                elif not names[name]['cont']: 
                    error_txt = "*You have not selected the contour type centreline to use for "+name
                    self.win_msg(error_txt)
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
        msg = "You have not selected any measurement parameters to obtain from the segmented channels. If you want to go back and select some measurement parameters, press 'Cancel', else if you are happy with this decision press 'OK'."
        title = 'No Measurement Parameters Selected'
        self.prompt_ok = Prompt_ok_cancel(msg = msg, title = title,  parent=self)

        if self.prompt_ok.user_input == 'OK': 
            return True
        else: 
            print('cancel? or close?')
            error_txt = "Select measurement parameters for the channel-contours."
            self.win_msg(error_txt)
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
                
        centreline = {'looped_length': getattr(self, 'cB_cl_LoopLen').isChecked(),
                        'linear_length': getattr(self, 'cB_cl_LinLen').isChecked()}
        
        self.final_params = {'ballooning': ballooning, 
                             'centreline': centreline}
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

    def win_msg(self, msg): 
        if msg[0] == '*':
            self.tE_validate.setStyleSheet(error_style)
            msg = 'Error: '+msg
        elif msg[0] == '!':
            self.tE_validate.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            self.tE_validate.setStyleSheet(msg_style)
        self.tE_validate.setText(msg)

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
            self.win_msg(error_txt)
            return
        else: 
            valid.append(True)

        #Get organ name
        if len(self.lineEdit_organ_name.text())<5:
            error_txt = '*Organ name needs to be longer than five (5) characters'
            self.win_msg(error_txt)
            return
        elif validate_txt(self.lineEdit_organ_name.text()) != None:
            error_txt = "*Please avoid using invalid characters in the project's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.win_msg(error_txt)
            return
        else: 
            self.organ_name = self.lineEdit_organ_name.text()
            valid.append(True)
        
        #Get Strain, stage and genotype
        for name in ['strain', 'stage', 'genotype', 'manipulation','stack_orient', 'units']:
            cB_data = getattr(self, 'cB_'+name).currentText()
            if cB_data == '--select--':
                error_txt = "*Please select the organ's "+name.upper()+"."
                self.win_msg(error_txt)
                return
            else: 
                setattr(self, name, cB_data)
                valid.append(True)

        if self.cB_stack_orient.currentText() == 'custom':
            if len(self.cust_angle.text()) == 0: 
                error_txt = "*Please input custom angle for imaging orientation."
                self.win_msg(error_txt)
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
                self.win_msg(error_txt)
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
        else: 
            error_txt = '*Something went wrong importing the images for '+ch+'. Please try again.'
            self.win_msg(error_txt)
            return

        btn_file.setChecked(True)
        toggled(btn_file)

    def get_file_mask(self, ch):
        self.win_msg('Loading mask for '+ch+'... Wait for the indicator to turn green, then continue.')
        btn_file = getattr(self, 'browse_mask_'+ch)
        if 'image' not in self.img_dirs[ch].keys(): 
            error_txt = '*Please select first the images for '+ch+', then select their corresponding mask.'
            self.win_msg(error_txt)
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
                    self.win_msg(error_txt)
                    return
                else: 
                    self.img_dirs[ch]['mask'] = {}
                    self.img_dirs[ch]['mask']['dir'] = Path(file_name)
                    self.img_dirs[ch]['mask']['shape'] = mask_o.shape
                    check.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(0, 255, 0); color: rgb(0, 255, 0); font: 25 2pt 'Calibri Light'")
                    check.setText('Done')
            else: 
                error_txt = '*Something went wrong importing the mask images for '+ch+'. Please try again.'
                self.win_msg(error_txt)
                return
                
        btn_file.setChecked(True)
        toggled(btn_file)

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
            self.win_msg(error_txt)
            return
        elif len(set_paths_chs) != len(paths_chs):
            error_txt = "*The image files loaded for each channel needs to be different. Please check and retry."
            self.win_msg(error_txt)
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
            self.win_msg(error_txt)
            for ch in proj.mH_channels: 
                if ch != 'chNS':
                    bws_ch = getattr(self,'browse_'+ch)
                    bws_ch.setChecked(False)
                    toggled(bws_ch)
                    label = getattr(self, 'lab_filled_dir_'+ch)
                    label.clear()
                    check_ch = getattr(self, 'check_'+ch)
                    check_ch.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255);")
                    check_ch.clear()
                    bws_mk = getattr(self, 'browse_mask_'+ch) 
                    bws_mk.setChecked(False)
                    toggled(bws_mk)
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

    def win_msg(self, msg): 
        if msg[0] == '*':
            self.tE_validate.setStyleSheet(error_style)
            msg = 'Error: '+msg
        elif msg[0] == '!':
            self.tE_validate.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            self.tE_validate.setStyleSheet(msg_style)
        self.tE_validate.setText(msg)
    
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
        toggled(self.button_browse_proj)
    
    def get_proj_wf(self, proj): 
        flat_wf = flatdict.FlatDict(copy.deepcopy(proj.workflow))
        keep_keys = [key for key in flat_wf.keys() if len(key.split(':'))== 4 and 'Status' in key]
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
                print(keys) 
                name_keys = list(range(len(keys)))

                keys_wf = {}
                for wf_key in wf_flat.keys():
                    nn,proc,sp,_ = wf_key.split(':')
                    keys_wf[sp] = ['workflow']+wf_key.split(':')
                # print(keys_wf) 
                
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
                    # print('Loading info organ: ', organ)   
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

                # delegate = AlignDelegate(self.tabW_select_organ)
                # self.tabW_select_organ.setItemDelegate(delegate)

                # for rr in range(self.tabW_select_organ.rowCount()): 
                #     for cc in range(self.tabW_select_organ.columnCount()):
                #         item = self.tabW_select_organ.item(rr, cc)
                #         # print(item)
                #         if item != None: 
                #             item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
            else: 
                error_txt = "!The project selected does not contain organs. Add a new organ to this project by selecting 'Create New Organ'."
                self.win_msg(error_txt)
                self.button_load_organs.setChecked(True)
                toggled(self.button_load_organs)
                self.organ_checkboxes = None
                return

            # print(cBs)
            self.organ_checkboxes = cBs
            self.button_load_organs.setChecked(True)
            toggled(self.button_load_organs)
        else: 
            self.button_load_organs.setChecked(False)
            toggled(self.button_load_organs)
            error_txt = '*You need to first load a project to load all the organs comprising it.'
            self.win_msg(error_txt)
    
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
                print(organ_cB)
                cb = getattr(self, organ_cB).isChecked()
                checked.append(cb)
            
            if sum(checked) <= 0: 
                self.organ_selected = None
            elif sum(checked) > 1:
                error_txt = '*Please select only one organ to analyse.'
                self.win_msg(error_txt)
            else: 
                if len(checked) > 1:
                    index = [i for i, x in enumerate(checked) if x][0]
                    print('len>1:',index)
                    self.organ_selected = organ_cB[index].split('cB_')[1]
                else: 
                    print('len=1:',organ_cB)
                    self.organ_selected = organ_cB.split('cB_')[1]
            print(self.organ_selected)
        else: 
            error_txt = '*Please select one organ to analyse.'
            self.win_msg(error_txt)

class MainWindow(QMainWindow):

    def __init__(self, proj, organ):
        super().__init__()
        uic.loadUi('src/gui/ui/main_window_screen.ui', self)
        self.setWindowTitle('morphoHeart')
        mH_logoXS = QPixmap('images/logos_1o75mm.png')
        self.mH_logo_XS.setPixmap(mH_logoXS)
        self.setWindowIcon(QIcon(mH_icon))
        self.setStyleSheet("background-color:  rgb(255, 255, 255);")

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

    def win_msg(self, msg): 
        if msg[0] == '*':
            self.tE_validate.setStyleSheet(error_style)
            msg = 'Error: '+msg
        elif msg[0] == '!':
            self.tE_validate.setStyleSheet(note_style)
            msg = msg[1:]
        else: 
            self.tE_validate.setStyleSheet(msg_style)
        self.tE_validate.setText(msg)
        
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
    
    #- Init tabs
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

    def init_pandq_tab(self): 
        #All Group box
        self.segmentationAll_play.setStyleSheet(style_play)
        self.segmentationAll_play.setEnabled(False)
        self.segmentationAll_play.clicked.connect(lambda: self.run_segmentationAll())
        self.centreline_thicknessAll_play.setStyleSheet(style_play)
        self.centreline_thicknessAll_play.setEnabled(False)
        # self.centreline_thicknessAll_play.clicked.connect(lambda: self.())
        self.segments_sectionsAll_play.setStyleSheet(style_play)
        self.segments_sectionsAll_play.setEnabled(False)
        # self.segments_sectionsAll_play.clicked.connect(lambda: self.())

        self.init_keeplargest()
        self.init_clean()
        self.init_trim()
        self.init_orientation()
        if self.organ.mH_settings['setup']['chNS']['layer_btw_chs']:
            self.init_chNS()
        else: 
            self.chNS_all_widget.setVisible(False)
            print('Dissapear chNS')

        if len(self.organ.mH_settings['measure']['CL']) > 0:
            self.init_centreline()
        else: 
            self.centreline_all_widget.setVisible(False)

        if len(self.organ.mH_settings['measure']['th_i2e'])+len(self.organ.mH_settings['measure']['th_e2i'])+len(self.organ.mH_settings['measure']['ball'])>0:
            self.init_thickness_ballooning()
        else: 
            self.thickness_ballooning_all_widget.setVisible(False)

        if isinstance(self.organ.mH_settings['setup']['segm'], dict):
            self.init_segments()
        else: 
            self.segments_widget.setVisible(False)

        if isinstance(self.organ.mH_settings['setup']['sect'], dict):
            self.init_sections()
        else: 
            self.sections_widget.setVisible(False)
        
        #Setup workflow
        self.fill_workflow(tree= self.treeWorkflow, value = self.organ.workflow['morphoHeart']['MeshesProc'])

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
        #Adding organs to table
        row = 0
        for ch in im_chs:
            col = 0        
            for proc in self.proc_keys.keys():
                #Create Layout
                widget   = QWidget() 
                hL = QtWidgets.QHBoxLayout(widget)
                hL.setObjectName("hL_"+ch)
                color_status = QtWidgets.QLineEdit()
                color_status.setEnabled(True)
                color_status.setMinimumSize(QtCore.QSize(15, 15))
                color_status.setMaximumSize(QtCore.QSize(15, 15))
                color_status.setStyleSheet("border-color: rgb(0, 0, 0);")
                color_status.setObjectName("color_status_"+ch)
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
                getattr(self, 'kl_label_'+chk).setText(self.channels[chk]+' ('+chk+')')
                for contk in ['int', 'tiss', 'ext']:
                    color = self.organ.mH_settings['setup']['color_chs'][chk][contk]
                    color_txt = "QPushButton{ border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); background-color: "+color+";} QPushButton:hover{border-color: rgb(255, 255, 255)}"
                    color_btn = getattr(self, 'fillcolor_'+chk+'_'+contk)
                    color_btn.setStyleSheet(color_txt)

        self.kl_ch1_all.stateChanged.connect(lambda: self.tick_all('ch1', 'kl'))
        self.kl_ch2_all.stateChanged.connect(lambda: self.tick_all('ch2', 'kl'))
        self.kl_ch3_all.stateChanged.connect(lambda: self.tick_all('ch3', 'kl'))
        self.kl_ch4_all.stateChanged.connect(lambda: self.tick_all('ch4', 'kl'))

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

    def init_orientation(self):
        #Buttons
        self.orient_open.clicked.connect(lambda: self.open_section(name='orient'))
        orient_stack = self.organ.mH_settings['setup']['orientation']['stack']
        self.stack_orientation.setText(orient_stack)
        orient_roi = self.organ.mH_settings['setup']['orientation']['roi']
        self.roi_orientation.setText(orient_roi)
        # self.stack_orient_plot.clicked.connect(lambda: )
        # self.roi_orient_plot.clicked.connect(lambda: )

        self.q_orientation.clicked.connect(lambda: self.help('orientation'))
        self.orientation_set.clicked.connect(lambda: self.set_orientation())
        self.orientation_play.setStyleSheet(style_play)
        self.orientation_play.setEnabled(False)

        self.stack_orient_plot.setEnabled(False)
        self.roi_orient_plot.setEnabled(False)

        self.roi_rotate.stateChanged.connect(lambda: self.check_roi_rotate())
        self.radio_manual.toggled.connect(lambda: self.rotate_method(mtype = 'manual'))
        self.radio_centreline.toggled.connect(lambda: self.rotate_method(mtype = 'centreline'))

        items_cl = self.organ.mH_settings['measure']['CL'].keys()
        items_cB = []
        for item in items_cl:
            ch, cont, segm = item.split('_')
            name = self.organ.mH_settings['setup']['name_chs'][ch] + ' ('+ch+'_'+cont+')'
            items_cB.append(name)
        self.centreline_orientation.addItems(items_cB)
        self.rotate_method(mtype = 'none')
        
    def init_chNS(self):
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
        self.chNS_extch.setText(self.channels[ch_ext]+' ('+ch_ext+')')
        self.chNS_extcont.setText(chNS_setup['ch_ext'][1]+'ernal')
        self.chNS_operation.setText(chNS_setup['operation'])
        ch_int = chNS_setup['ch_int'][0]
        self.chNS_intch.setText(self.channels[ch_int]+' ('+ch_int+')')
        self.chNS_intcont.setText(chNS_setup['ch_int'][1]+'ernal')

        for contk in ['int', 'tiss', 'ext']:
            color = self.organ.mH_settings['setup']['chNS']['color_chns'][contk]
            color_txt = "QPushButton{ border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); background-color: "+color+";} QPushButton:hover{border-color: rgb(255, 255, 255)}"
            color_btn = getattr(self, 'fillcolor_chNS_'+contk)
            color_btn.setStyleSheet(color_txt)

        self.chNS_plot2d.stateChanged.connect(lambda: self.n_slices('chNS'))

    def init_centreline(self):
        #Buttons
        self.centreline_open.clicked.connect(lambda: self.open_section(name='centreline'))
        self.centreline_play.setStyleSheet(style_play)
        self.centreline_play.setEnabled(False)
        self.centreline_clean_play.setStyleSheet(style_play)
        self.centreline_clean_play.setEnabled(False)
        self.centreline_ML_play.setStyleSheet(style_play)
        self.centreline_ML_play.setEnabled(False)
        self.q_centreline.clicked.connect(lambda: self.help('centreline'))

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
                getattr(self, 'meshLab_status'+str(nn)).setVisible(False)
                getattr(self, 'vmtk_status'+str(nn)).setVisible(False)
                getattr(self, 'opt_cl_status'+str(nn)).setVisible(False)
                getattr(self, 'opt_cl'+str(nn)).setVisible(False)
                getattr(self, 'cl_plot'+str(nn)).setVisible(False)

    def init_thickness_ballooning(self):
        #Buttons
        self.heatmaps_open.clicked.connect(lambda: self.open_section(name='heatmaps'))
        self.heatmaps2D_play.setStyleSheet(style_play)
        self.heatmaps2D_play.setEnabled(False)
        # self.heatmaps2D_play.clicked.connect(lambda: )
        self.heatmaps3D_play.setStyleSheet(style_play)
        self.heatmaps3D_play.setEnabled(False)
        # self.heatmaps3D_play.clicked.connect(lambda: )

        #Heatmap settings
        heatmap_dict = {}
        lists = [['measure','th_i2e'], ['measure','th_e2i'], ['measure','ball']]
        names = ['Th(int>ext)', 'Th(ext>int)', 'Ball']
        min_val = [0,0,0]
        max_val = [20, 20, 60]

        for aa, ll, nn, minn, maxx in zip(count(), lists, names, min_val, max_val): 
            # print(aa, ll, nn, minn, maxx)
            variable = ll[1]
            sp_dict = get_by_path(self.organ.mH_settings, ll)
            for item in sp_dict: 
                if nn != 'Ball':
                    chh, conth, _ = item.split('_')
                    heatmap_dict[variable+'['+chh+'-'+conth+']'] = {'name': nn+'['+chh+'-'+conth+']',
                                                                'min_val': minn, 
                                                                'max_val': maxx}
                else: 
                    namef = item.replace('_(', '(CL:')
                    namef = namef.replace('_', '-')
                    heatmap_dict[variable+'['+namef+']'] = {'name': nn+'['+namef+']',
                                                                'min_val': minn, 
                                                                'max_val': maxx}
            
        cmaps = ['turbo','viridis', 'jet', 'magma', 'inferno', 'plasma']
        hm_items = list(heatmap_dict.keys())
        for num in range(1,13,1):
            label = getattr(self,'label_hm'+str(num))
            mina = getattr(self,'min_hm'+str(num))
            maxa = getattr(self,'max_hm'+str(num))
            cm = getattr(self,'colormap'+str(num))
            cm.clear()
            cm.addItems(cmaps)
            d3d2 = getattr(self,'d3d2_'+str(num))
            hm_plot = getattr(self, 'hm_plot'+str(num))
            hm_plot2 = getattr(self, 'hm_plot'+str(num)+'_2D')
            hm_eg = getattr(self, 'cm_eg'+str(num))
            if num < len(hm_items): 
                label.setText(heatmap_dict[hm_items[num]]['name'])
                mina.setValue(heatmap_dict[hm_items[num]]['min_val'])
                maxa.setValue(heatmap_dict[hm_items[num]]['max_val'])
                d3d2.setChecked(True)
                hm_eg.setEnabled(True)
                hm_plot.setEnabled(False)
                hm_plot2.setEnabled(False)
            else: 
                label.setVisible(False)
                mina.setVisible(False)
                maxa.setVisible(False)
                cm.setVisible(False)
                d3d2.setVisible(False)
                hm_eg.setVisible(False)
                hm_plot.setVisible(False)
                hm_plot2.setVisible(False)

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

        cl_keys = list(self.organ.mH_settings['measure']['CL'].keys())
        cl_names = []
        for key in cl_keys: 
            ch, cont, _ = key.split('_')
            namef = self.channels[ch]+' ('+ch+') - '+cont
            cl_names.append(namef)
        self.hm_centreline.addItems(cl_names)

    def init_segments(self):
        #Buttons
        self.segments_open.clicked.connect(lambda: self.open_section(name='segments'))
        self.segments_play.setStyleSheet(style_play)
        self.segments_play.setEnabled(False)
        # self.segments_play
        # self.segments_plot.
        self.segments_plot.setEnabled(False)
        # self.q_segments

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
        
        for optcut in ['1','2']:
            name_segm = []
            cutl = 'cut'+optcut
            cutb = 'Cut'+optcut
            if cutb in no_cuts: 
                if 'colors' not in self.organ.mH_settings['setup']['segm'][cutb].keys():
                    colors_initialised = False
                    self.organ.mH_settings['setup']['segm'][cutb]['colors'] = {}
                else: 
                    colors_initialised = True

                for segm in segm_setup[cutb]['name_segments'].keys():
                    name_segm.append(segm_setup[cutb]['name_segments'][segm])
                getattr(self, 'names_segm_'+cutl).setText(', '.join(name_segm))
                getattr(self, 'obj_segm_'+cutl).setText(segm_setup[cutb]['obj_segm'])
                for nn in range(1,6,1):
                    if nn > len(name_segm):
                        getattr(self, 'label_'+cutl+'_segm'+str(nn)).setVisible(False)
                        getattr(self, 'fillcolor_'+cutl+'_'+'segm'+str(nn)).setVisible(False)
                    else: 
                        if not colors_initialised: 
                            color = palette[5*(int(optcut)-1)+(nn-1)]
                            self.organ.mH_settings['setup']['segm'][cutb]['colors']['segm'+str(nn)] = color
                        else: 
                            color = self.organ.mH_settings['setup']['segm'][cutb]['colors']['segm'+str(nn)]
                        color_txt = "QPushButton{ border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); background-color: rgb"+str(color)+";} QPushButton:hover{border-color: rgb(255, 255, 255)}"
                        color_btn = getattr(self, 'fillcolor_'+cutl+'_'+'segm'+str(nn))
                        color_btn.setStyleSheet(color_txt)
                getattr(self, 'segm_'+cutl+'_plot').setEnabled(False)
            else: 
                getattr(self, 'label_segm_'+cutl).setVisible(False)
                getattr(self, 'names_segm_'+cutl).setVisible(False)
                getattr(self, 'obj_segm_'+cutl).setVisible(False)
                getattr(self, 'segm_'+cutl+'_plot').setVisible(False)
                for nn in range(1,6,1):
                    getattr(self, 'label_'+cutl+'_segm'+str(nn)).setVisible(False)
                    getattr(self, 'fillcolor_'+cutl+'_'+'segm'+str(nn)).setVisible(False)

        print('Setup segments: ', self.organ.mH_settings['setup']['segm'])

    def init_sections(self):
        #Buttons
        self.sections_open.clicked.connect(lambda: self.open_section(name='sections'))
        self.sections_play.setStyleSheet(style_play)
        self.sections_play.setEnabled(False)
        # self.sections_play
        # self.sections_plot
        self.sections_plot.setEnabled(False)
        # self.q_sections

        self.fillcolor_cut1_sect1.clicked.connect(lambda: self.color_picker(name = 'cut1_sect1'))
        self.fillcolor_cut1_sect2.clicked.connect(lambda: self.color_picker(name = 'cut1_sect2'))
        self.fillcolor_cut2_sect1.clicked.connect(lambda: self.color_picker(name = 'cut2_sect1'))
        self.fillcolor_cut2_sect2.clicked.connect(lambda: self.color_picker(name = 'cut2_sect2'))                                         

        sect_setup = self.organ.mH_settings['setup']['sect']
        no_cuts = [key for key in sect_setup.keys() if 'Cut' in key]
        palette =  palette_rbg("Set2", 4)
        
        for optcut in ['1','2']:
            name_sect = []
            cutl = 'cut'+optcut
            cutb = 'Cut'+optcut
            if cutb in no_cuts: 
                if 'colors' not in self.organ.mH_settings['setup']['sect'][cutb].keys():
                    colors_initialised = False
                    self.organ.mH_settings['setup']['sect'][cutb]['colors'] = {}
                else: 
                    colors_initialised = True
                for sect in sect_setup[cutb]['name_sections'].keys():
                    name_sect.append(sect_setup[cutb]['name_sections'][sect])
                getattr(self, 'names_sect_'+cutl).setText(', '.join(name_sect))
                getattr(self, 'obj_sect_'+cutl).setText(sect_setup[cutb]['obj_sect'])
                for nn in range(1,3,1):
                    if not colors_initialised: 
                        color = palette[2*(int(optcut)-1)+(nn-1)]
                        self.organ.mH_settings['setup']['sect'][cutb]['colors']['sect'+str(nn)] = color
                    else: 
                        color = self.organ.mH_settings['setup']['sect'][cutb]['colors']['sect'+str(nn)]
                    color_txt = "QPushButton{ border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); background-color: rgb"+str(color)+";} QPushButton:hover{border-color: rgb(255, 255, 255)}"
                    color_btn = getattr(self, 'fillcolor_'+cutl+'_'+'sect'+str(nn))
                    color_btn.setStyleSheet(color_txt)
                getattr(self, 'sect_'+cutl+'_plot').setEnabled(False)
            else: 
                getattr(self, 'label_sect_'+cutl).setVisible(False)
                getattr(self, 'names_sect_'+cutl).setVisible(False)
                getattr(self, 'obj_sect_'+cutl).setVisible(False)
                getattr(self, 'sect_'+cutl+'_plot').setVisible(False)
                for nn in range(1,6,1):
                    getattr(self, 'label_'+cutl+'_sect'+str(nn)).setVisible(False)
                    getattr(self, 'fillcolor_'+cutl+'_'+'sect'+str(nn)).setVisible(False)

        print('Setup Sections: ', self.organ.mH_settings['setup']['sect'])

    def update_status(self, root_dict, items, fillcolor):
        update_status(root_dict, items, fillcolor)
        
    #Functions specific to gui functionality
    def open_section(self, name): 
        print('Open-close: '+name)
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

    def color_picker(self, name): #Add update color in mesh!

        color = QColorDialog.getColor()
        if color.isValid():
            # print('The selected color is: ', color.name())
            fill = getattr(self, 'fillcolor_'+name)
            color_txt = "QPushButton{ border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); background-color: "+color.name()+";} QPushButton:hover{border-color: rgb(255, 255, 255)}"
            fill.setStyleSheet(color_txt)
            chk, contk = name.split('_')
            if chk != 'chNS' and contk in ['int', 'ext', 'tiss']: 
                # print('not chNS')
                self.organ.mH_settings['setup']['color_chs'][chk][contk] = color.name()
            elif chk == 'chNS': 
                # print('chNS')
                self.organ.mH_settings['setup'][chk]['color_chns'][contk] = color.name()
            else: 
                if 'segm' in contk: 
                    stype = 'segm'
                else: 
                    stype - 'sect'
                self.organ.mH_settings['setup'][stype]['Cut'+chk[-1]]['colors'][contk] = color.name()
            
    def set_colormap(self, name):
        value = getattr(self, 'colormap'+name).currentText()
        dir_pix = 'images/'+value+'.png'
        pixmap = QPixmap(dir_pix)
        cm_eg = getattr(self, 'cm_eg'+name)
        cm_eg.setPixmap(pixmap)
        cm_eg.setScaledContents(True)

    def fill_workflow(self, tree, value):

        tree.setColumnCount(2)
        tree.setHeaderLabels(['Process', 'Status'])
        tree.setColumnWidth(0, 100)
        tree.setColumnWidth(1, 20)

        # tree.invisibleRootItem().setExpanded(True)
        root_item = tree.invisibleRootItem()
        root_item.setExpanded(True)
        self.topLevelItem = QTreeWidgetItem()
        for method in self.proj.mH_methods:
            # print(method)
            method_item = QTreeWidgetItem(tree)
            method_item.setText(0,method)
            #set child 
            keys_method = self.organ.workflow['morphoHeart']['MeshesProc'][method].keys()
            # print(keys_method)
            for subproc in keys_method:
                if subproc != 'Status':
                    child = QtWidgets.QTreeWidgetItem(tree)
                    labeltree = MyTreeItem(subproc, tree)
                    # method_item.addChild(labeltree)
                    tree.setItemWidget(child, 1, labeltree)

                    # root = QTreeWidgetItem(self.treeWidget, ["root"])
                    # A = QTreeWidgetItem(root, ["A"])
                    # barA = QTreeWidgetItem(A, ["bar", "i", "ii"])
                    # bazA = QTreeWidgetItem(A, ["baz", "a", "b"])

                    # labeltree = QTreeWidgetItem(method_item)
                    # subproc_label =  QtWidgets.QLabel()
                    # subproc_label.setStyleSheet("QLabel {background-color:rgb(255, 255, 0); border-width: 2px; border-style: outset; border-color: rgb(0,0, 0);}")
                    # subproc_label.resize(18, 18)

                    # subproc_method = QTreeWidgetItem(method_item, [subproc, subproc_label])
                    # # subproc_method.setText(0, subproc)
                    # method_item.addChild(subproc_method)
                    # method_item.setExpanded(True)

                    #Create the label widget
                    # labeltree = QTreeWidgetItem(method_item)
                    # subproc_label =  QtWidgets.QLabel()
                    # subproc_label.setStyleSheet("QLabel {background-color:rgb(255, 255, 0); border-width: 2px; border-style: outset; border-color: rgb(0,0, 0);}")
                    # subproc_label.resize(18, 18)
                    # tree.setItemWidget(labeltree, 1, subproc_label)


        #  for department in departments:
        #     department_item = QTreeWidgetItem(tree)
        #     department_item.setText(0,department)
        #     # set the child
        #     for employee in employees[department]:
        #         employee_item   = QTreeWidgetItem(tree)
        #         employee_item.setText(1,employee)

        #         department_item.addChild(employee_item)

        #///
        # tree.clear()
        # self.fill_wf_item(tree.invisibleRootItem(), value)

    def fill_wf_item(self, item, value):
        item.setExpanded(True)
        if type(value) is dict:
            print('dict:',value)
            print('type val', type(value))
            for key, val in value.items():
                child = QTreeWidgetItem()
                child.setText(0, str(key))#0, unicode(key))
                item.addChild(child)
                self.fill_wf_item(child, val)
        elif type(value) is list:
            print('list:',value)
            for val in value:
                child = QTreeWidgetItem()
                item.addChild(child)
                print('type val', type(val))
                if type(val) is dict:     
                    print('dict2:',val) 
                    child.setText(0, '[dict]')
                    self.fill_wf_item(child, val)
                elif type(val) is list:
                    print('list2:',val) 
                    child.setText(0, '[list]')
                    self.fill_wf_item(child, val)
                else:
                    print('??2:',val) 
                    child.setText(0, str(val))              
                child.setExpanded(True)
        else:
            if value == 'Status': 
                print('Aja')
            else: 
                child = QTreeWidgetItem()
                child.setText(0, str(value))#unicode(value))
                item.addChild(child)
            
    def n_slices(self, process):
        cB = getattr(self, process+'_plot2d')
        if cB.isChecked():
            state = True
        else: 
            state = False
        getattr(self, process+'_lab1').setEnabled(state)
        getattr(self, process+'_n_slices').setEnabled(state)
        getattr(self, process+'_lab2').setEnabled(state)

    #Set functions 
    def set_keeplargest(self): 
        self.gui_keep_largest = {}
        for ch in self.channels: 
            if ch != 'chNS':
                self.gui_keep_largest[ch] = {}
                for cont in ['int', 'tiss', 'ext']:
                    cB = getattr(self, 'kl_'+ch+'_'+cont)
                    self.gui_keep_largest[ch][cont] = cB.isChecked() 

        self.rotateZ_90 = True
        self.keeplargest_set.setChecked(True)
        toggled(self.keeplargest_set)
        print('self.gui_keep_largest:',self.gui_keep_largest)
        self.keeplargest_play.setEnabled(True)

    def set_clean(self): 
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
                    self.win_msg('*Please select the channel and contour to use as mask for '+ch.title())
                    return
                else: 
                    continue
                
        self.gui_clean = {}
        for chc in chs_sel: 
            self.gui_clean[chc] = {'cont': []}
            for cont in ['int', 'tiss', 'ext']: 
                val = getattr(self, 'clean_'+chc+'_'+cont).isChecked()
                if val: 
                    self.gui_clean[chc]['cont'].append(cont)
                self.gui_clean[chc]['with_ch'] = getattr(self, 'clean_withch_'+chc).currentText()
                self.gui_clean[chc]['with_cont'] = getattr(self, 'clean_withcont_'+chc).currentText()
                self.gui_clean[chc]['inverted'] = getattr(self, 'inverted_'+chc).isChecked()

        if self.clean_plot2d.isChecked():
            self.gui_clean['plot2d'] =  True
            self.gui_clean['n_slices'] = self.clean_n_slices.value()
        else: 
            self.gui_clean['plot2d'] = False

        self.cleanup_set.setChecked(True)
        toggled(self.cleanup_set)
        print('self.gui_clean: ', self.gui_clean)
        self.cleanup_play.setEnabled(True)

    def set_trim(self): 
        self.gui_trim = {}
        im_chs = [ch for ch in self.channels if ch != 'chNS']
        for side in ['top', 'bottom']: 
            self.gui_trim[side] = {'chs': {}}
            for cht in im_chs: 
                self.gui_trim[side]['chs'][cht] = {}
                for cont in ['int', 'tiss', 'ext']: 
                    val = getattr(self, side[0:3]+'_'+cht+'_'+cont).isChecked()
                    self.gui_trim[side]['chs'][cht][cont] = val
        
            obj = getattr(self, side[0:3]+'_cut_opts').currentText()
            self.gui_trim[side]['object'] = obj

        self.trimming_set.setChecked(True)
        toggled(self.trimming_set)
        print('self.gui_trim: ', self.gui_trim)
        self.trimming_play.setEnabled(True)
    
    def set_chNS(self):
        self.gui_chNS = {}
        if self.chNS_plot2d.isChecked():
            self.gui_chNS = {'plot2d': True, 
                             'n_slices': self.chNS_n_slices.value()}
        else: 
            self.gui_chNS['plot2d'] = False

        self.chNS_set.setChecked(True)
        toggled(self.chNS_set)
        print('self.gui_chNS: ', self.gui_chNS)
        self.chNS_play.setEnabled(True)

    def check_roi_rotate(self):

        if self.roi_rotate.isChecked():
            self.radio_manual.setEnabled(True)
            self.radio_centreline.setEnabled(True)
            self.rotate_method(mtype ='centreline')
        else: 
            self.radio_manual.setEnabled(False)
            self.radio_centreline.setEnabled(False)
            self.rotate_method(mtype ='none')

    def rotate_method(self, mtype:str):
        print('Checked:', mtype)

        if self.radio_manual.isChecked(): 
            self.rotate_angles.setEnabled(True)
            self.centreline_orientation.setEnabled(False)
            self.lab_plane.setEnabled(False)
            self.plane_orient.setEnabled(False)
            self.lab_vector.setEnabled(False)
            self.vector_orient.setEnabled(False)
        elif self.radio_centreline.isChecked(): 
            self.rotate_angles.setEnabled(False)
            self.centreline_orientation.setEnabled(True)
            self.lab_plane.setEnabled(True)
            self.plane_orient.setEnabled(True)
            self.lab_vector.setEnabled(True)
            self.vector_orient.setEnabled(True)
        else: 
            self.rotate_angles.setEnabled(False)
            self.centreline_orientation.setEnabled(False)
            self.lab_plane.setEnabled(False)
            self.plane_orient.setEnabled(False)
            self.lab_vector.setEnabled(False)
            self.vector_orient.setEnabled(False)
    
    def set_orientation(self): 

        #Stack
        self.gui_orientation = {}
        self.gui_orientation['stack'] = {'axis': self.organ.mH_settings['setup']['orientation']['stack']}

        #ROI
        roi_rotate = self.roi_rotate.isChecked()
        self.gui_orientation['roi'] = {'axis': self.organ.mH_settings['setup']['orientation']['roi'],
                                        'rotate': roi_rotate}
        if roi_rotate: 
            for rB in ['radio_manual', 'radio_centreline']:
                btn = getattr(self, rB)
                if btn.isChecked():
                    rB_checked = rB
                    break
            if rB_checked == 'radio_manual': 
                self.gui_orientation['roi']['method'] = 'Manual'
            else: 
                plane_orient = self.plane_orient.currentText()
                vector_orient = self.vector_orient.currentText()
                centreline = self.centreline_orientation.currentText()
                self.gui_orientation['roi']['method'] = 'Centreline'
                self.gui_orientation['roi']['centreline'] = centreline
                self.gui_orientation['roi']['plane_orient'] = plane_orient
                self.gui_orientation['roi']['vector_orient'] = vector_orient
        else: 
            pass
            
        self.orientation_set.setChecked(True)
        toggled(self.orientation_set)
        print('self.gui_orientation: ', self.gui_orientation)
        self.orientation_play.setEnabled(True)



    #Plot functions
    def plot_meshes(self, ch, chNS=False):
        txt = [(0, self.organ.user_organName)]
        obj = []
        if ch != 'all': 
            for cont in ['ext', 'tiss', 'int']: 
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

    #Help functions
    def help(self, process): 
        print('User clicked help '+process)

    # def help_keeplargest(self): 
    #     print('User clicked help keep largest')


    def run_segmentationAll(self): 
        print('Running segmentation All!')
    
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
    def save_project_and_organ_pressed(self):
        print('Save project and organ was pressed')
        self.organ.save_organ()
        self.win_msg('Organ  -'+ self.organ.user_organName +'-  was saved succesfully!')
        self.proj.save_project()
        self.win_msg('Project  -'+ self.proj.user_projName +'-  was saved succesfully!')
    
    def close_morphoHeart_pressed(self):
        print('Close was pressed')
        msg = ["Do you want to save the changes to this Organ and Project before closing?","If you don't save your changes will be lost."]
        self.prompt = Propmt_save_all(msg, info=[self.organ, self.proj], parent=self)
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
        self.prompt = Propmt_save_all(msg, info=[self.organ, self.proj], parent=self)
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

class MyTreeItem(QtWidgets.QWidget):
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
def update_status(root_dict, items, fillcolor): 
    wf_status = get_by_path(root_dict, items)
    if wf_status == 'NI': 
        color_txt = "background-color: rgb(255, 255, 127); border-color: rgb(0, 0, 0);"
    elif wf_status == 'Initialised': 
        color_txt = "background-color: rgb(255, 151, 60); border-color: rgb(0, 0, 0);"
    elif wf_status == 'DONE' or wf_status == 'Done':
        color_txt = "background-color:  rgb(0, 255, 0); border-color: rgb(0, 0, 0);"
    elif wf_status == 'N/A': 
        color_txt = "background-color:  rgb(0, 0, 0); border-color: rgb(0, 0, 0);"
    else: 
        color_txt = "background-color:  rgb(255, 0, 255); border-color: rgb(0, 0, 0);"
        print('other status unknown')
    fillcolor.setStyleSheet(color_txt)

# Button general functions
def toggled(button_name): 
    style = 'border-radius:10px; border-width: 1px; border-style: outset; color: rgb(71, 71, 71); font: 10pt "Calibri Light";'
    if button_name.isChecked():
        style_f = 'QPushButton{background-color: #eb6fbd; border-color: #672146;'+style+'}'
    else: 
        style_f = 'QPushButton{background-color: rgb(211, 211, 211); border-color: rgb(66, 66, 66);'+style+'}'
    button_name.setStyleSheet(style_f)

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


def set_txts(): 
    #% Link to images
    mH_icon = 'images/logos_w_icon_2o5mm.png'#'images/cat-its-mouth-open.jpg'#
    mH_big = 'images/logos_7o5mm.png'
    mH_top_corner = 'images/logos_1o75mm.png'
    mH_images = [mH_icon, mH_big, mH_top_corner]

    # Play buttons
    play_bw = 'images/logos_play_black_white.png'
    play_gw = 'images/logos_play_green_white.png'
    play_gb = 'images/logos_play_green_black.png'
    play_grw = 'images/logos_play_gray_white.png'
    play_colors = [play_bw, play_gw, play_gb, play_grw]

    play_btn = "QPushButton {border-image: url("+play_gw+"); background-repeat: no-repeat; width: 65px; height: 56px;} "
    hover_btn = "QPushButton:hover {border-image: url("+play_bw+")} "
    pressed_btn = "QPushButton:pressed {border-image: url("+play_gb+")}; "
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

#%% Module loaded
print('morphoHeart! - Loaded gui_classes')
list_all = set_txts()
mH_images, play_colors, style_play, html_txt, reg_exps, tE_styles = list_all
mH_icon, mH_big, mH_top_corner = mH_images
play_bw, play_gw, play_gb, play_btn = play_colors
error_style, note_style, msg_style = tE_styles