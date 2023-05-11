
'''
morphoHeart_GUI_classes

Version: Apr 26, 2023
@author: Juliana Sanchez-Posada

'''
#%% Imports - ########################################################
# import sys
from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QDate, Qt, QRegularExpression
from PyQt6.QtWidgets import (QDialog, QApplication, QMainWindow, QWidget, QFileDialog, QTabWidget,
                              QGridLayout, QVBoxLayout, QHBoxLayout, QLayout, QLabel, QPushButton, QLineEdit,
                              QColorDialog, QTableWidgetItem, QCheckBox)
from PyQt6.QtGui import QPixmap, QIcon, QFont, QRegularExpressionValidator
# from PyQt6.QtCore import QRegExp
# from PyQt6.QtGui import QRegExpValidator
from qtwidgets import Toggle, AnimatedToggle

from pathlib import Path
import flatdict
# import os
from itertools import count
import webbrowser
from skimage import measure, io
import copy

#%% morphoHeart Imports - ##################################################
# from ..src.modules.mH_funcBasics import get_by_path
from functools import reduce  
import operator

#%% Link to images
mH_icon = 'images/logos_w_icon_2o5mm.png'#'images/cat-its-mouth-open.jpg'
mH_big = 'images/logos_7o5mm.png'
mH_top_corner = 'images/logos_1o75mm.png'

#%% Classes - ########################################################
class WelcomeScreen(QDialog):

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('gui/welcome_screen.ui', self)
        self.setFixedSize(600,590)
        self.setWindowTitle('Welcome to morphoHeart...')
        self.mH_logo_XL.setPixmap(QPixmap(mH_big))
        self.setWindowIcon(QIcon(mH_icon))

        # self.btn_link2paper.clicked.connect(lambda: self.get_file())#webbrowser.open('https://github.com/jsanchez679/morphoHeart'))
        # self.btn_link2docs.clicked.connect(lambda: webbrowser.open('https://github.com/jsanchez679/morphoHeart'))
        self.btn_link2github.clicked.connect(lambda: webbrowser.open('https://github.com/jsanchez679/morphoHeart'))

        self.theme = self.cB_theme.currentText()
        self.cB_theme.currentIndexChanged.connect(lambda: self.theme_changed())

        layout = self.hL_toggle_on_off 
        # print(layout.__dict__)
        # toggle_2 = AnimatedToggle(
        #     checked_color="#FFB000",
        #     pulse_checked_color="#44FFB000")
        # layout.insertWidget(len(layout) - 2, toggle_2)

    # def get_file(self): 
    #     title = 'Import images for '
    #     cwd = Path().absolute()
    #     file_name, _ = QFileDialog.getOpenFileName(self, title, str(cwd), "Image Files (*.tif)")
    #     print(file_name)
    #     return True

    def theme_changed(self):
        if self.cB_theme.currentText() == 'Dark': 
            uic.loadUi('gui/welcome_screen_dark.ui', self)
        else: 
            uic.loadUi('gui/welcome_screen.ui', self)
        self.setFixedSize(600,575)
        self.setWindowTitle('Welcome to morphoHeart...')
        self.mH_logo_XL.setPixmap(QPixmap(mH_big))
        self.setWindowIcon(QIcon(mH_icon))
        self.theme = self.cB_theme.currentText()

class PromptWindow(QDialog):

    def __init__(self, msg:str, title:str, info:str, parent=None):
        super().__init__()
        uic.loadUi('gui/prompt_user_input.ui', self)
        self.setFixedSize(400,250)
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
        if len(user_input) <=1: 
            error_txt = "*The organ's "+name+" needs to have more than 1 character."
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

    def __init__(self, msg:str, title:str, parent=None):
        super().__init__()
        uic.loadUi('gui/prompt_ok_cancel.ui', self)
        self.setFixedSize(400,250)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setText(msg)
        
        self.button_ok.clicked.connect(lambda: self.user_ok())
        self.button_cancel.clicked.connect(lambda: self.user_cancel())
        self.user_input = None

        self.show()

    def user_ok(self): 
        self.user_input = 'OK'
        print(self.user_input)
        self.close()

    def user_cancel(self): 
        self.user_input = 'Cancel'
        print(self.user_input)
        self.close()

class CreateNewProj(QDialog):

    def __init__(self, parent=None):
        super().__init__()
        self.proj_name = ''
        self.proj_dir_parent = ''
        uic.loadUi('gui/new_project_screen.ui', self)
        self.setFixedSize(1035,851)
        self.setWindowTitle('Create New Project...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))

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

    def init_gral_proj_set(self):
        now = QDate.currentDate()
        self.dateEdit.setDate(now)

        self.checked_analysis = {'morphoHeart': self.checkBox_mH.isChecked(), 
                                'morphoCell': self.checkBox_mC.isChecked(), 
                                'morphoPlot': self.checkBox_mP.isChecked()}
        #Set validator
        self.lineEdit_proj_name.setValidator(QRegularExpressionValidator(self.reg_ex, self.lineEdit_proj_name))

        # Create a new project
        self.tE_validate.setText("Create a new project by providing a project's name, directory and analysis pipeline. Then press -Validate- and -Create-.")

        #Get project directory
        self.button_select_proj_dir.clicked.connect(lambda: self.get_proj_dir())
        #Validate and Create Initial Project (proj_name, analysis_pipeline, proj_dir)
        self.button_validate_new_proj.clicked.connect(lambda: self.validate_new_proj())
        self.button_create_initial_proj.clicked.connect(lambda: self.create_new_proj())

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
        self.hLayout_Ch1.setEnabled(True)
        self.fillcolor_ch1_int_btn.clicked.connect(lambda: self.color_picker('ch1_int'))
        self.fillcolor_ch1_tiss_btn.clicked.connect(lambda: self.color_picker('ch1_tiss'))
        self.fillcolor_ch1_ext_btn.clicked.connect(lambda: self.color_picker('ch1_ext'))
        #Ch2
        self.hLayout_Ch2.setEnabled(True)
        self.tick_ch2.stateChanged.connect(lambda: self.add_channel('ch2'))
        self.fillcolor_ch2_int_btn.clicked.connect(lambda: self.color_picker('ch2_int'))
        self.fillcolor_ch2_tiss_btn.clicked.connect(lambda: self.color_picker('ch2_tiss'))
        self.fillcolor_ch2_ext_btn.clicked.connect(lambda: self.color_picker('ch2_ext'))
        #Ch3
        self.hLayout_Ch3.setEnabled(True)
        self.tick_ch3.stateChanged.connect(lambda: self.add_channel('ch3'))
        self.fillcolor_ch3_int_btn.clicked.connect(lambda: self.color_picker('ch3_int'))
        self.fillcolor_ch3_tiss_btn.clicked.connect(lambda: self.color_picker('ch3_tiss'))
        self.fillcolor_ch3_ext_btn.clicked.connect(lambda: self.color_picker('ch3_ext'))
        #Ch4
        self.hLayout_Ch4.setEnabled(True)
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
        self.button_validate_initial_set.clicked.connect(lambda: self.validate_initial_settings())
        self.button_set_initial_set.clicked.connect(lambda: self.set_initial_settings())

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
        self.apply_segm.clicked.connect(lambda: self.validate_segments())
        self.button_set_segm.clicked.connect(lambda: self.set_segm_settings())

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
        self.apply_sect.clicked.connect(lambda: self.validate_sections())
        self.button_set_sect.clicked.connect(lambda: self.set_sect_settings())

    def init_mCell_tab(self):
        pass

    #Functions for General Project Settings   
    def get_proj_dir(self):
        self.button_validate_new_proj.setChecked(False)
        toggled(self.button_validate_new_proj)
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
        if len(self.lineEdit_proj_name.text())<=5:
            error_txt = '*Project name needs to be longer than five (5) characters'
            self.tE_validate.setText(error_txt)
            return
        elif validate_txt(self.lineEdit_proj_name.text()) != None:
            error_txt = "Please avoid using invalid characters in the project's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.tE_validate.setText(error_txt)
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
            self.tE_validate.setText(error_txt)
            return
        else: 
            valid.append(True)
        
        #Get Directory
        if isinstance(self.proj_dir_parent, str): 
            error_txt = '*Please select a project directory where the new project will be saved.'
            self.tE_validate.setText(error_txt)
            return
        else:  
            if self.proj_dir_parent.is_dir() and len(str(self.proj_dir_parent))>1:
                valid.append(True)
            else: 
                self.button_select_proj_dir.setChecked(False)
                toggled(self.button_select_proj_dir)
                error_txt = '*The selected project directory is invalid. Please select another directory.'
                self.tE_validate.setText(error_txt)
                return

        if len(valid)== 3 and all(valid):
            proj_folder = 'R_'+self.proj_name
            self.proj_dir = self.proj_dir_parent / proj_folder
            if self.proj_dir.is_dir():
                self.button_validate_new_proj.setChecked(False)
                self.tE_validate.setText('*There is already a project named "'+self.proj_name+'" in the selected directory. Please select a different name for the new project.')
                toggled(self.button_validate_new_proj)
                return 
            else: 
                self.button_validate_new_proj.setChecked(True)
                self.lab_filled_proj_dir.setText(str(self.proj_dir))
                self.tE_validate.setText('All good. Select -Create- to create "'+self.proj_name+'" as a new project.')   
                toggled(self.button_validate_new_proj)  
                return True   
        else: 
            self.tE_validate.setText(error_txt)
            self.button_validate_new_proj.setChecked(False)
            toggled(self.button_validate_new_proj)
            return 

    def create_new_proj(self):
        if self.button_validate_new_proj.isChecked(): 
            toggled(self.button_create_initial_proj)
            self.tabWidget.setEnabled(True)
            self.tab_mHeart.setEnabled(self.checked_analysis['morphoHeart'])
            self.tab_mCell.setEnabled(self.checked_analysis['morphoCell'])
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

            if self.checked_analysis['morphoCell']:
                self.mC_settings = {}
            else: 
                self.mC_settings = None
                self.mC_user_params = None
        
            #Disable all fields from Gral Project Settings
            self.tE_validate.setText('New project  "'+self.proj_name+'" has been created! Continue by setting the channel information.')
            self.gral_proj_settings.setDisabled(True)
            if self.checked_analysis['morphoHeart']:
                self.tabWidget.setCurrentIndex(0)
            else: 
                self.tabWidget.setCurrentIndex(1)
            # print('self.mH_settings (create_new_proj):', self.mH_settings)
        else: 
            self.tE_validate.setText("*Project's name, analysis pipeline and directory need to be validated for the new project to be created!")

    #Functions for Initial Set-up 
    # -- Functions for orientation
    def custom_orient(self, ortype): 
        user_or = getattr(self,'cB_'+ortype+'_orient').currentText()
        if user_or == 'custom':
            msg = "Give the name of the three different custom orientations for the  '"+ortype.upper()+"'  separated by a comma:"
            title = 'Custom Orientation'
            self.prompt = PromptWindow(msg = msg, title = title, info = ortype, parent = self)
        else: 
            pass 

    def set_orientation_settings(self):
        valid = []; error_txt = ''
        stack_or = self.cB_stack_orient.currentText()
        if stack_or == '--select--': 
            error_txt = '*Please select a stack orientation coordinates'
            self.tE_validate.setText(error_txt)
            return
        else: 
            valid.append(True)

        roi_or = self.cB_roi_orient.currentText()
        if roi_or == '--select--': 
            error_txt = '*Please select an ROI orientation coordinates'
            self.tE_validate.setText(error_txt)
            return
        else: 
            valid.append(True)

        if len(valid) == 2 and all(valid):
            # print(self.cB_stack_orient.currentText())
            self.mH_settings['orientation'] = {'stack': self.cB_stack_orient.currentText(),
                                                'roi': self.cB_roi_orient.currentText()}
            self.tE_validate.setText('Great! Continue setting up the new project!')
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
            self.tE_validate.setText(error_txt)
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
                if len(ch_name) <= 3:
                    error_txt = '*Active channels must have a name longer than three (3) characters.'
                    self.tE_validate.setText(error_txt)
                    return
                elif validate_txt(ch_name) != None:
                    error_txt = "Please avoid using invalid characters in the channel's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
                    self.tE_validate.setText(error_txt)
                    return
                else: 
                    names.append(ch_name)
                    names_valid.append(True)

        if all(names_valid):
            valid.append(True)

        #Check names are different
        if len(names) > len(set(names)):
            error_txt = '*The names given to the selected channels need to be unique.'
            self.tE_validate.setText(error_txt)
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
            self.tE_validate.setText(error_txt)
            return
        else: 
            valid.append(True)
        
        #Check relation
        ch_relation = []
        for ch in ['ch1', 'ch2', 'ch3', 'ch4']:
            tick = getattr(self, 'tick_'+ch)
            if tick.isChecked():
                ch_relation.append(getattr(self, 'cB_'+ch).currentText())

        internal_count = ch_relation.count('internal layer')
        external_count = ch_relation.count('external layer') 
        
        if sum(ch_ticked) == 1: 
            if external_count != 1: 
                error_txt = '*Please define the active channel as external.'
            else: 
                valid.append(True)
                # print('AAA: internal_count', internal_count, '-external_count', external_count)
        elif sum(ch_ticked) == 2: 
            if internal_count != 1 or external_count != 1:
                error_txt = '*One channel needs to be selected as the internal layer and other as the external.'
                self.tE_validate.setText(error_txt)
            elif internal_count == 1 and external_count == 1:
                valid.append(True)
            # else:  
            #     print('BBB: internal_count', internal_count, '-external_count', external_count)
        elif sum(ch_ticked) > 2: 
            if internal_count != 1 or external_count != 1:
                error_txt = '*One channel needs to be selected as the internal layer, other as the external and the other(s) as middle.'
                self.tE_validate.setText(error_txt)
            elif internal_count == 1 and external_count == 1:
                valid.append(True)
            # else: 
            #     print('CCC: internal_count', internal_count, '-external_count', external_count)

        if sum(ch_ticked) == 1 and self.tick_chNS.isChecked():
            error_txt = 'At least two channels need to be selected to create a tissue from the negative space.'
            self.tE_validate.setText(error_txt)
        else: 
            valid.append(True)

        # print('valid:', valid)
        if len(valid)== 6 and all(valid):
            self.tE_validate.setText('All done!... Press -Set Initial Settings- to continue.')
            self.button_validate_initial_set.setChecked(True)
            toggled(self.button_validate_initial_set)
            return True
        else: 
            self.button_validate_initial_set.setChecked(False)
            toggled(self.button_validate_initial_set)
            return False

    def set_initial_settings(self):
        if self.button_validate_initial_set.isChecked():
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

            #Get info from checked boxes
            __ = self.checked('chNS')
            #---- Segments
            __ = self.checked('segm')   
            #---- Sections
            __ = self.checked('sect')
            # print(self.mH_settings)

            if self.tick_chNS.isChecked():
                #Set the comboBoxes for chNS
                self.ext_chNS.clear(); self.int_chNS.clear()
                self.ext_chNS.addItems(['----']+ch_selected)
                self.int_chNS.addItems(['----']+ch_selected)
                ch_selected.append('chNS')
            self.ch_selected = ch_selected
            # print(self.ch_selected)
            #Set Table for Segments
            for ch in ['ch1', 'ch2', 'ch3', 'ch4', 'chNS']:
                for cont in ['int', 'tiss', 'ext']:
                    for stype in ['segm', 'sect']:
                        for cut in ['Cut1', 'Cut2']:
                            if ch in ch_selected:
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

            self.tE_validate.setText("Great! Now setup details for the selected processes.")
            return True
        else: 
            error_txt = "You first need to validate the channels' settings to continue setting the project."
            self.tE_validate.setText(error_txt)
            return False
    
    # -- Functions for ChannelNS
    def validate_chNS_settings(self): 
        valid = []; error_txt = ''
        #Check name
        name_chNS = self.chNS_username.text()
        names_ch = [self.mH_settings['name_chs'][key] for key in self.mH_settings['name_chs'].keys()]
        # print('names_ch:',names_ch)
        if len(name_chNS)<= 3: 
            error_txt = '*Channel from the negative space must have a name longer than three (3) characters.'
            self.tE_validate.setText(error_txt)
            return
        elif validate_txt(name_chNS) != None:
            error_txt = "Please avoid using invalid characters in the chNS's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.tE_validate.setText(error_txt)
            return
        else: 
            if name_chNS not in names_ch:
                valid.append(True)
            else:
                error_txt = 'The name given to the channel obtained from the negative space needs to be different to that of the other channels.'
                self.tE_validate.setText(error_txt)
                return
            
        #Check colors
        all_colors = []
        for cont in ['int', 'tiss', 'ext']:
            all_colors.append(getattr(self, 'fillcolor_chNS_'+cont).text() != '')
        
        if not all(all_colors):
            error_txt = '*Make sure you have selected colors for the channel obtained from the negative space.'
            self.tE_validate.setText(error_txt)
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
                self.tE_validate.setText(error_txt)
                return
            else: 
                valid.append(True)
        else: 
            error_txt = '*Please select the internal and external channels and contours that need to be used to extract the channel from the negative space.'
            self.tE_validate.setText(error_txt)
            return
        
        #Check operation
        chNS_operation = self.chNS_operation.currentText()
        if chNS_operation != '----': 
            valid.append(True)
        else: 
            error_txt = '*Please select an operation to extract the channel from the negative space.'
            self.tE_validate.setText(error_txt)
            return
            
        if len(valid)== 4 and all(valid):
            self.tE_validate.setText('All done setting ChannelNS!...')
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
                            'color_chns': color_chNS}
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
                    error_txt = cut+": The number of segments need to match the number of segment names given."
                    self.tE_validate.setText(error_txt)
                    return
                elif len(set(names_segm)) != int(no_segm):
                    error_txt = '*'+cut+": Segment names need to be different."
                    self.tE_validate.setText(error_txt)
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
                    self.tE_validate.setText(error_txt)
                    return

                #Check measurement parameters to measure
                meas_vol = getattr(self, 'cB_volume_'+stype).isChecked()
                meas_area = getattr(self, 'cB_area_'+stype).isChecked()
                meas_ellip = getattr(self, 'cB_ellip_'+stype).isChecked()
                if any([meas_vol, meas_area, meas_ellip]):
                    valid.append(True)
                else: 
                    error_txt = "*Please select the measurement parameter(s) (e.g. volume and/or surface area) you want to extract from the segments"
                    self.tE_validate.setText(error_txt)
                    return

            if len(valid) == 3 and all(valid): 
                valid_all.append(True)
        
        if all(valid_all): 
            self.apply_segm.setChecked(True)
            self.tE_validate.setText('All good, now press -Set Segments- to save selected settings!')
        else: 
            self.apply_segm.setChecked(False)
        toggled(self.apply_segm)

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
                    error_txt = cut+":  Sections cut only produce two objects. Please provide two section names."
                    self.tE_validate.setText(error_txt)
                    return
                elif len(set(names_sect)) != 2:
                    error_txt = '*'+cut+": Section names need to be different."
                    self.tE_validate.setText(error_txt)
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
                    self.tE_validate.setText(error_txt)
                    return
                
                #Check measurement parameters to measure
                meas_vol = getattr(self, 'cB_volume_'+stype).isChecked()
                meas_area = getattr(self, 'cB_area_'+stype).isChecked()
                if any([meas_vol, meas_area]):
                    valid.append(True)
                else: 
                    error_txt = "*Please select the measurement parameter(s) (e.g. volume and/or surface area) you want to extract from the sections"
                    self.tE_validate.setText(error_txt)
                    return
                
            if len(valid) == 3 and all(valid): 
                valid_all.append(True)
        
        if all(valid_all): 
            self.apply_sect.setChecked(True)
            self.tE_validate.setText('All good, now press -Set Sections- to save selected settings!')
        else: 
            self.apply_sect.setChecked(False)
        toggled(self.apply_sect)

    def set_segm_settings(self): 
        if self.apply_segm.isChecked(): 
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
            self.mH_settings['segm'] = segm_settings
            # print('self.mH_settings (set_segm_settings):',self.mH_settings)
            if all(valid_all):
                self.button_set_segm.setChecked(True)
                self.tE_validate.setText('All good, continue!')
            else: 
                self.button_set_segm.setChecked(False)
            toggled(self.button_set_segm)

    def set_sect_settings(self): 
        if self.apply_sect.isChecked(): 
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
            self.mH_settings['sect'] = sect_settings
            # print('self.mH_settings (set_sect_settings):',self.mH_settings)
            if all(valid_all):
                self.button_set_sect.setChecked(True)
                self.tE_validate.setText('All good, continue!')
            else: 
                self.button_set_sect.setChecked(False)
            toggled(self.button_set_sect)

    def validate_set_all(self): #to develop? 
        print('\n\nValidating Project!')
        return True
        # valid = []
        # if self.set_orientation_settings():
        #     valid.append(True)
        # else:
        #     return 
        # if self.validate_initial_settings():
        #     valid.append(True)
        # else:
        #     return 
        # if self.set_initial_settings():
        #     valid.append(True)
        # else:
        #     return 
        # if self.checked('chNS'): 
        #     if self.validate_chNS_settings():
        #         valid.append(True)
        #     else:
        #         return 
        #     if self.set_chNS_settings():
        #         valid.append(True)
        #     else:
        #         return 
        # if self.checked('segm'): 
        #     if self.validate_segments():
        #         valid.append(True)
        #     else:
        #         return 
        #     if self.set_segm_settings():
        #         valid.append(True)
        #     else:
        #         return 
        # if self.checked('sect'):
        #     if self.validate_sections():
        #         valid.append(True)
        #     else:
        #         return 
        #     if self.set_sect_settings():
        #         valid.append(True)
        #     else:
        #         return 

        # print('Valid all:',valid)
        # if all(valid): 
        #     return True
        # else: 
        #     return False

    # -- Functions Set Measurement Parameters
    def check_to_set_params(self): 
        # print('self.mH_settings (set_meas_param):',self.mH_settings)
        valid = []
        if self.button_set_orient.isChecked(): 
            valid.append(True)
        else: 
            error_txt = 'You need to set orientation settings first to set measurement parameters.'
            self.tE_validate.setText(error_txt)
            return
        if self.button_set_initial_set.isChecked(): 
            valid.append(True)
        else: 
            error_txt = 'You need to set initial settings first to set measurement parameters.'
            self.tE_validate.setText(error_txt)
            return
        if self.checked('chNS'): 
            if self.button_set_chNS.isChecked():
                valid.append(True)
            else: 
                error_txt = 'You need to set Channel NS settings first to set measurement parameters.'
                self.tE_validate.setText(error_txt)
                return
        if self.checked('segm'): 
            if self.button_set_segm.isChecked():
                valid.append(True)
            else: 
                error_txt = 'You need to set segments settings first to set measurement parameters.'
                self.tE_validate.setText(error_txt)
                return
        if self.checked('sect'): 
            if self.button_set_sect.isChecked():
                valid.append(True)
            else: 
                error_txt = 'You need to set sections settings first to set measurement parameters.'
                self.tE_validate.setText(error_txt)
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
        
        uic.loadUi('gui/set_meas_screen.ui', self)
        self.setWindowTitle('Set Parameters to Measure...')
        self.setFixedSize(690,860)
        self.setWindowTitle('Select the parameters to measure from the segmented channels...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.mH_settings = mH_settings

        self.params = {0: {'s': 'SA', 'l':'surface area'},
                        1: {'s': 'Vol', 'l':'volume'},
                        2: {'s': 'CL', 'l':'centreline'},
                        3: {'s': 'th_i2e', 'l':'thickness (int>ext)'},
                        4: {'s': 'th_e2i','l':'thickness (ext>int)'}, 
                        5: {'s': 'ball','l':'centreline>tissue (ballooning)'}}
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

        #Set validators
        self.reg_ex = QRegularExpression("[a-z-A-Z_ 0-9,]+")
        self.lineEdit_param_name.setValidator(QRegularExpressionValidator(self.reg_ex, self.lineEdit_param_name))
        self.reg_ex_no_spaces = QRegularExpression("[a-z-A-Z_0-9]+")
        self.lineEdit_param_abbr.setValidator(QRegularExpressionValidator(self.reg_ex_no_spaces, self.lineEdit_param_abbr))
        self.reg_ex_most = QRegularExpression("[a-z-A-Z_ 0-9,.:/+-]+")
        self.lineEdit_param_classes.setValidator(QRegularExpressionValidator(self.reg_ex_most, self.lineEdit_param_classes))

        #Buttons
        self.button_add_param.clicked.connect(lambda: self.add_user_param())
        self.button_validate_params.clicked.connect(lambda: self.validate_params())

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
        setattr(self, 'dict_meas', dict_meas)
        # print('self.dict_meas:',self.dict_meas)

    def set_meas_param_table(self): 
        #Set Measurement Parameters
        for key in self.params.keys():
            getattr(self, 'lab_param'+str(key)).setEnabled(True)
            getattr(self, 'lab_param'+str(key)).setText(self.params[key]['l'])
            
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
        param_class = self.lineEdit_param_classes.text()

        if len(param_name)<=5: 
            error_txt = "Parameter's name needs to be longer than 5 characters"
            self.tE_validate.setText(error_txt)
            return
        elif validate_txt(param_name) != None:
            error_txt = "Please avoid using invalid characters in the parameter's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.tE_validate.setText(error_txt)
            return
        else: 
            valid.append(True)
        
        if len(param_abbr)<=5: 
            error_txt = "Parameter's name needs to be at least 5 characters long"
            self.tE_validate.setText(error_txt)
            return
        elif validate_txt(param_abbr) != None:
            error_txt = "Please avoid using invalid characters in the parameter's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.tE_validate.setText(error_txt)
            return
        else: 
            valid.append(True)
            param_abbr_line = param_abbr.replace(' ', '_')
        
        try: 
            param_classes = split_str(param_class)
            valid.append(True)
        except: 
            error_txt = "Please check the values introduced in Parameter Classes."
            self.tE_validate.setText(error_txt)
            return
        
        if len(valid) == 3 and all(valid):
            param_num = len(self.params)
            self.params[param_num]={'s': param_abbr_line, 'l': param_name, 
                                        'description': param_desc, 'classes': param_classes}
            # print(self.params)
            self.set_meas_param_table()
            param_name = self.lineEdit_param_name.clear()
            param_abbr = self.lineEdit_param_abbr.clear()
            param_desc = self.textEdit_param_desc.clear()
            param_class = self.lineEdit_param_classes.clear()
        
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
        # print('cB_checked: ',cB_checked)

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
        # print('names: ', names)
        
        #Now double check them 
        if set(list(cB_checked.keys())) != set(list(names.keys())):
            diff = set(list(cB_checked.keys())) - set(list(names.keys()))
            error_txt = "You have not selected the centreline to use for "+str(diff)
            self.tE_validate.setText(error_txt)
            return 
        else: 
            for name in names: 
                if not names[name]['ch']: 
                    error_txt = "You have not selected the channel centreline to use for "+name
                    self.tE_validate.setText(error_txt)
                    return 
                elif not names[name]['cont']: 
                    error_txt = "You have not selected the contour type centreline to use for "+name
                    self.tE_validate.setText(error_txt)
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
            self.tE_validate.setText('All done setting measurement parameters!')
            self.get_parameters()
        else: 
            return 
        
    def check_meas_param(self): #to finish!
        msg = "You have not selected any measurement parameters to obtain from the segmented channels. If you want to go back and select some measurement parameters, press 'Cancel', else if you are happy with this decision press 'OK'."
        title = 'No Measurement Parameters Selected'
        self.prompt_ok = Prompt_ok_cancel(msg = msg, title = title,  parent=self)

        if self.prompt_ok.user_input == 'OK': 
            return True
        else: 
            print('cancel? or close?')
            error_txt = "Select measurement parameters for the channel-contours."
            self.tE_validate.setText(error_txt)
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
        
        # Toggle button
        self.button_validate_params.setChecked(True)
        toggled(self.button_validate_params)

        # Toggle button and close window
        self.final_params = {'ballooning': ballooning, 
                             'centreline': centreline}
        # print('self.final_params:',self.final_params)

class NewOrgan(QDialog):
    def __init__(self, proj, parent=None):
        super().__init__()
        uic.loadUi('gui/create_organ_screen.ui', self)
        self.setFixedSize(735,845)
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

        #Buttons
        self.button_validate_organ.clicked.connect(lambda: self.validate_organ(proj = proj))
        #Select files
        self.browse_ch1.clicked.connect(lambda: self.get_file('ch1'))
        self.browse_ch2.clicked.connect(lambda: self.get_file('ch2'))
        self.browse_ch3.clicked.connect(lambda: self.get_file('ch3'))
        self.browse_ch4.clicked.connect(lambda: self.get_file('ch4'))

        self.browse_mask_ch1.clicked.connect(lambda: self.get_file_mask('ch1'))
        self.browse_mask_ch2.clicked.connect(lambda: self.get_file_mask('ch2'))
        self.browse_mask_ch3.clicked.connect(lambda: self.get_file_mask('ch3'))
        self.browse_mask_ch4.clicked.connect(lambda: self.get_file_mask('ch4'))

    def set_project_info(self, proj):

        if proj.analysis['morphoHeart']: 
            self.tab_mHeart.setEnabled(True)
        else: 
            self.tab_mHeart.setEnabled(False)

        if proj.analysis['morphoCell']: 
            self.tab_mCell.setEnabled(True)
        else: 
            self.tab_mCell.setEnabled(False)  

        self.lab_filled_proj_name.setText(proj.info['user_projName'])
        self.lab_filled_ref_notes.setText(proj.info['user_projNotes'])
        self.lab_filled_proj_dir.setText(str(proj.dir_proj))

        self.cB_strain.clear()
        self.cB_strain.addItems(['--select--', 'add']+proj.gui_custom_data['strain'])
        self.cB_stage.clear()
        self.cB_stage.addItems(['--select--', 'add']+proj.gui_custom_data['stage'])
        self.cB_genotype.clear()
        self.cB_genotype.addItems(['--select--', 'add']+proj.gui_custom_data['genotype'])
        self.cB_manipulation.clear()
        self.cB_manipulation.addItems(['None', 'add']+proj.gui_custom_data['manipulation'])
        self.cB_stack_orient.clear()
        self.cB_stack_orient.addItems(['--select--', 'add']+proj.gui_custom_data['im_orientation'])
        self.cB_units.clear()
        self.cB_units.addItems(['--select--']+proj.gui_custom_data['im_res_units'])

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
            self.prompt = PromptWindow(msg = msg, title = title, info = name, parent = self)
        else: 
            pass 

    def validate_organ(self, proj):
        valid = []; error_txt = ''
        #Check the name is unique within the project
        organ_folder = self.lineEdit_organ_name.text()
        organ_dir = Path(proj.dir_proj) / organ_folder 
        if organ_dir.is_dir(): 
            error_txt = '*There is already an organ within this project with the same name. Please give this organ a new name to continue.'
            self.tE_validate.setText(error_txt)
            return
        else: 
            valid.append(True)

        #Get organ name
        if len(self.lineEdit_organ_name.text())<=5:
            error_txt = '*Organ name needs to be longer than five (5) characters'
            self.tE_validate.setText(error_txt)
            return
        elif validate_txt(self.lineEdit_organ_name.text()) != None:
            error_txt = "Please avoid using invalid characters in the project's name e.g.['(',')', ':', '-', '/', '\', '.', ',']"
            self.tE_validate.setText(error_txt)
            return
        else: 
            self.organ_name = self.lineEdit_organ_name.text()
            valid.append(True)
        
        #Get Strain, stage and genotype
        for name in ['strain', 'stage', 'genotype', 'stack_orient', 'units']:
            cB_data = getattr(self, 'cB_'+name).currentText()
            if cB_data == '--select--':
                error_txt = "*Please select the organ's "+name.upper()+"."
                self.tE_validate.setText(error_txt)
                return
            else: 
                setattr(self, name, cB_data)
                valid.append(True)

        if self.cB_stack_orient.currentText() == 'custom':
            if len(self.cust_angle.text()) == 0: 
                error_txt = "*Please input custom angle for imaging orientation."
                self.tE_validate.setText(error_txt)
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
                self.tE_validate.setText(error_txt)
                return
            else: 
                valid_axis.append(True)

        if all(valid_axis): 
            self.set_resolution()
            valid.append(True)
        
        # print('valid:', valid)
        if all(valid):
            self.button_validate_organ.setChecked(True)
            self.tE_validate.setText('All good. Continue setting up new organ.')        
        else: 
            self.button_validate_organ.setChecked(False)
        toggled(self.button_validate_organ)

    def set_resolution(self): 
        resolution = {}
        units = getattr(self, 'cB_units').currentText()
        for axis in ['x', 'y', 'z']:
            res = getattr(self, 'scaling_'+axis).text()
            resolution[axis] = {'scaling': float(res), 'units': units}
        self.resolution = resolution
        # print('resolution: ', self.resolution)

    def get_file(self, ch):
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
            self.tE_validate.setText(error_txt)
            return

        btn_file.setChecked(True)
        toggled(btn_file)

    def get_file_mask(self, ch):
        btn_file = getattr(self, 'browse_mask_'+ch)
    
        if 'image' not in self.img_dirs[ch].keys(): 
            error_txt = '*Please select first the images for '+ch+', then select their corresponding mask.'
            self.tE_validate.setText(error_txt)
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
                    self.tE_validate.setText(error_txt)
                    return
                else: 
                    self.img_dirs[ch]['mask'] = {}
                    self.img_dirs[ch]['mask']['dir'] = Path(file_name)
                    self.img_dirs[ch]['mask']['shape'] = mask_o.shape
                    check.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(0, 255, 0); color: rgb(0, 255, 0); font: 25 2pt 'Calibri Light'")
                    check.setText('Done')
            else: 
                error_txt = '*Something went wrong importing the mask images for '+ch+'. Please try again.'
                self.tE_validate.setText(error_txt)
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
        print('Valid checking channel selection: ', valid)
        if not all(valid): 
            error_txt = "*Please load the images (and masks) for all the organ's channels."
            self.tE_validate.setText(error_txt)
            return
        elif len(set_paths_chs) != len(paths_chs):
            error_txt = "*The image files loaded for each channel needs to be different. Please check and retry."
            self.tE_validate.setText(error_txt)
            for ch in proj.mH_channels.keys():
                getattr(self, 'browse_'+ch).setChecked(False)
                getattr(self, 'lab_filled_dir_'+ch).clear()
                check_ch = getattr(self, 'check_'+ch)
                check_ch.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); color: rgb(0, 255, 0); font: 25 2pt 'Calibri Light'")
                check_ch.setText('')
                # getattr(self, 'browse_mask_'+ch).setChecked(False)
                # getattr(self, 'lab_filled_dir_mask_'+ch).clear()
                # check_mk = getattr(self, 'check_mask_'+ch)
                # check_mk.setStyleSheet("border-color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); color: rgb(0, 255, 0); font: 25 2pt 'Calibri Light'")
                # check_mk.setText('')
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
            print('cleaned img_dirs:', self.img_dirs)
            return True
        else:
            error_txt = '*The shape of all the selected images do not match. Check and try again.'
            self.tE_validate.setText(error_txt)
            for ch in proj.mH_channels: 
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
        uic.loadUi('gui/load_project_screen.ui', self)
        self.setFixedSize(830,540)
        self.setWindowTitle('Load Existing Project...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.proj = None

        #Buttons
        self.button_load_organs.clicked.connect(lambda: self.load_proj_organs(proj = self.proj))

    def load_proj(self):
        response = QFileDialog.getExistingDirectory(self, caption="Select the Project's directory")
        print(response)
        test_proj_name = str(Path(response).name)[2:]
        json_name = 'mH_'+test_proj_name+'_project.json'
        test_proj_sett = Path(response) / 'settings' / json_name
        print(test_proj_name, '\n', json_name,'\n', test_proj_sett)
        if test_proj_sett.is_file(): 
            self.proj = mHC.Project(name = proj_name, dir_proj = dir_proj)
            proj_dir = Path(response)
            proj_name = test_proj_name
            print(proj_dir.name)
            self.lineEdit_proj_name.setText(test_proj_name)
            self.lab_filled_proj_dir.setText(str(self.proj_dir))
            self.lab_filled_proj_name.setText(str(self.proj_name))
            self.tE_validate.setText('Project -'+self.proj_name+'- was loaded successfully!')
        else: 
            self.tE_validate.setText('There is no settings file for a project within the selected directory. Please select a new directory.')

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
        cBs = []
        if len(proj.organs) > 0: 
            self.tabW_select_organ.clear()
            wf_flat = self.get_proj_wf(proj)
            blind = self.cB_blind.isChecked()
            self.tabW_select_organ.setRowCount(len(proj.organs)+2)
            keys = {'X':['select'],'Name': ['user_organName'], 'Notes': ['user_organNotes'], 'Strain': ['strain'], 'Stage': ['stage'], 
                    'Genotype':['genotype'], 'Manipulation': ['manipulation']}
            for wf_key in wf_flat.keys():
                nn,proc,sp,_ = wf_key.split(':')
                keys[sp] = ['workflow']+wf_key.split(':')
            if blind:
                keys.pop('Genotype', None); keys.pop('Manipulation', None) 
            print(keys) 

            self.tabW_select_organ.setColumnCount(len(keys))
            row = 2
            for organ in proj.organs:
                print('Loading info organ: ', organ)   
                col = 0        
                for nn, key in keys.items(): 
                    if len(key) == 1 and nn == 'X': 
                        widget   = QWidget()
                        checkbox = QCheckBox()
                        checkbox.setChecked(False)
                        layoutH = QHBoxLayout(widget)
                        layoutH.addWidget(checkbox)
                        # layoutH.setAlignment(Qt.AlignCenter)
                        layoutH.setContentsMargins(0, 0, 0, 0)
                        self.tabW_select_organ.setCellWidget(row, 0, widget)
                        cB_name = 'cB_'+proj.organs[organ]['user_organName']
                        setattr(self, cB_name, checkbox)
                        cBs.append(cB_name)
                    elif 'workflow' not in key: 
                        self.tabW_select_organ.setItem(row,col,QtWidgets.QTableWidgetItem(get_by_path(proj.organs[organ],key)))
                    else: 
                        widget   = QWidget()
                        checkbox = QCheckBox()
                        checkbox.setChecked(False)
                        layoutH = QHBoxLayout(widget)
                        layoutH.addWidget(checkbox)
                        # layoutH.setAlignment(Qt.AlignCenter)
                        layoutH.setContentsMargins(0, 0, 0, 0)
                        value = get_by_path(proj.organs[organ],key)
                        if value == 'NI':
                            checkbox.setStyleSheet("QCheckBox::indicator {background-color : rgb(255, 255, 127);}")
                        elif value == 'Initialised':
                            checkbox.setStyleSheet("QCheckBox::indicator {background-color : rgb(255, 151, 60);}")
                        else:# value == 'Done':
                            checkbox.setStyleSheet("QCheckBox::indicator {background-color :  rgb(0, 255, 0);}")
                        self.tabW_select_organ.setCellWidget(row, col, widget)
                    col+=1
                row +=1
            self.tabW_select_organ.setHorizontalHeaderLabels([key for key in keys])
            self.tabW_select_organ.resizeColumnsToContents()
            self.tabW_select_organ.resizeRowsToContents()
            self.tabW_select_organ.verticalHeader().setVisible(False)
            
        print(cBs)

      
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('gui/main_window_screen.ui', self)
        self.setFixedSize(1176,866)
        mH_logoXS = QPixmap('images/logos_1o75mm.png')
        self.mH_logo_XS.setPixmap(mH_logoXS)

        self.actionSave_Project.triggered.connect(self.save_project_pressed)
        self.actionSave_Organ.triggered.connect(self.save_organ_pressed)
        self.actionClose.triggered.connect(self.close_morphoHeart_pressed)

    def save_project_pressed(self):
        print('Save project was pressed')

    def save_organ_pressed(self):
        print('Save organ was pressed')
    
    def close_morphoHeart_pressed(self):
        print('Close was pressed')

#%% GUI Related Functions - ########################################################
# Button general functions
def toggled(button_name): 
    style = 'border-radius:10px; border-width: 1px; border-style: outset; color: rgb(71, 71, 71); font: 10pt "Calibri Light";'
    if button_name.isChecked():
        style_f = 'QPushButton{background-color: #eb6fbd; border-color: #672146;'+style+'}'
    else: 
        style_f = 'QPushButton{background-color: rgb(211, 211, 211); border-color: rgb(66, 66, 66);'+style+'}'
    button_name.setStyleSheet(style_f)

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


def get_by_path(root_dict, items):
    """Access a nested object in root_dict by item sequence.
    by Martijn Pieters (https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """
    return reduce(operator.getitem, items, root_dict)