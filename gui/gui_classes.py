
'''
morphoHeart_GUI_classes

Version: Apr 26, 2023
@author: Juliana Sanchez-Posada

'''
#%% Imports - ########################################################
# import sys
from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (QDialog, QApplication, QMainWindow, QWidget, QFileDialog, QTabWidget,
                              QGridLayout, QVBoxLayout, QHBoxLayout, QLayout, QLabel, QPushButton, QLineEdit,
                              QColorDialog, QTableWidgetItem, QCheckBox)
from PyQt6.QtGui import QPixmap, QIcon, QFont

from pathlib import Path
# import flatdict
# import os
from itertools import count

#%% Link to images
mH_icon = 'images/cat-its-mouth-open.jpg'#'images/logos_w_icon_2o5mm.png'
mH_big = 'images/logos_7o5mm.png'
mH_top_corner = 'images/logos_1o75mm.png'

#%% Classes - ########################################################
class WelcomeScreen(QDialog):

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('welcome_screen.ui', self)
        self.setFixedSize(601,401)
        self.setWindowTitle('Welcome to morphoHeart...')
        self.mH_logo_XL.setPixmap(QPixmap(mH_big))
        self.setWindowIcon(QIcon(mH_icon))

class PromptWindow(QDialog):

    def __init__(self, msg:str, title:str, info:str, parent=None):
        super().__init__()
        uic.loadUi('prompt_user_input.ui', self)
        self.setFixedSize(400,250)
        self.setWindowTitle(title)
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))
        self.textEdit.setText(msg)
        
        if title == 'Custom Orientation':
            self.custom_or = None
            self.button_ok.clicked.connect(lambda: self.validate_custom_or(parent, info))
        
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

        print('self.custom_or:',self.custom_or)
        
class Prompt_ok_cancel(QDialog):

    def __init__(self, msg:str, title:str, parent=None):
        super().__init__()
        uic.loadUi('prompt_ok_cancel.ui', self)
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
        uic.loadUi('new_project_screen.ui', self)
        self.setFixedSize(1010,920)
        self.setWindowTitle('Create New Project...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))

        #Initialise variables
        self.meas_param = None

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

    def init_gral_proj_set(self):
        now = QDate.currentDate()
        self.dateEdit.setDate(now)

        self.checked_analysis = {'morphoHeart': self.checkBox_mH.isChecked(), 
                                'morphoCell': self.checkBox_mC.isChecked(), 
                                'morphoPlot': self.checkBox_mP.isChecked()}

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
        self.button_set_chNS.clicked.connect(lambda: self.set_chNS_settings())
        
        #Default colors (ChannelNS)
        self.ck_def_colorsNS.stateChanged.connect(lambda: self.default_colors('chNS'))

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
        self.apply_segm.clicked.connect(lambda: self.apply_segments())
        self.button_set_segm.clicked.connect(lambda: self.validate_segm_settings())

    def init_sections_group(self):
        # -- Segments
        self.set_sect.setDisabled(True)
        self.set_sect.setVisible(False)
        # -- Sections
        self.tick_sect1.setEnabled(True)
        self.tick_sect1.setChecked(True)
        self.cB_obj_sect1.setEnabled(True)
        self.names_sect1.setEnabled(True)

        self.tick_sect2.setEnabled(True)
        self.tick_sect2.setChecked(False)
        self.cB_obj_sect2.setEnabled(False)
        self.names_sect2.setEnabled(False)
        self.tick_sect2.stateChanged.connect(lambda: self.add_segm_sect('sect'))
        list_obj_sect = ['Centreline']#, 'Plane']
        for cB in [self.cB_obj_sect1, self.cB_obj_sect2]:
            for obj in list_obj_sect: 
                cB.addItem(obj)
        self.apply_sect.clicked.connect(lambda: self.apply_sections())
        self.button_set_sect.clicked.connect(lambda: self.validate_sect_settings())

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
            self.button_validate_new_proj.setChecked(True)
            proj_folder = 'R_'+self.proj_name
            self.proj_dir = self.proj_dir_parent / proj_folder
            if self.proj_dir.is_dir():
                self.tE_validate.setText('*There is already a project named "'+self.proj_name+'" in the selected directory.')
            else: 
                self.lab_filled_proj_dir.setText(str(self.proj_dir))
                self.tE_validate.setText('All good. Select -Create- to create "'+self.proj_name+'" as a new project.')        
        else: 
            self.tE_validate.setText(error_txt)
            self.button_validate_new_proj.setChecked(False)
        toggled(self.button_validate_new_proj)

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
            if self.checked_analysis['morphoCell']:
                self.mC_settings = {}
        
            #Disable all fields from Gral Project Settings
            self.tE_validate.setText('New project  "'+self.proj_name+'" has been created! Continue by setting the channel information.')
            self.gral_proj_settings.setDisabled(True)
            if self.checked_analysis['morphoHeart']:
                self.tabWidget.setCurrentIndex(0)
            else: 
                self.tabWidget.setCurrentIndex(1)
            print('self.mH_settings (create_new_proj):', self.mH_settings)
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
            print(self.cB_stack_orient.currentText())
            self.mH_settings['orientation'] = {'stack': self.cB_stack_orient.currentText(),
                                                'roi': self.cB_roi_orient.currentText()}
            self.tE_validate.setText('Great! Continue setting up the new project!')
            self.button_set_orient.setChecked(True)
            print('self.mH_settings (set_orientation_settings):', self.mH_settings)
        else: 
            self.button_set_orient.setChecked(False)
        toggled(self.button_set_orient)

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
            else:  
                print('BBB: internal_count', internal_count, '-external_count', external_count)
        elif sum(ch_ticked) > 2: 
            if internal_count != 1 or external_count != 1:
                error_txt = '*One channel needs to be selected as the internal layer, other as the external and the other(s) as middle.'
                self.tE_validate.setText(error_txt)
            elif internal_count == 1 and external_count == 1:
                valid.append(True)
            else: 
                print('CCC: internal_count', internal_count, '-external_count', external_count)

        if sum(ch_ticked) == 1 and self.tick_chNS.isChecked():
            error_txt = 'At least two channels need to be selected to create a tissue from the negative space.'
            self.tE_validate.setText(error_txt)
        else: 
            valid.append(True)

        # print('valid:', valid)
        if len(valid)== 6 and all(valid):
            self.tE_validate.setText('All done!... Press -Set Initial Settings- to continue.')
            self.button_validate_initial_set.setChecked(True)
        else: 
            self.button_validate_initial_set.setChecked(False)
        toggled(self.button_validate_initial_set)

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
            print(self.mH_settings)

            if self.tick_chNS.isChecked():
                #Set the comboBoxes for chNS
                self.ext_chNS.addItems(['----']+ch_selected)
                self.int_chNS.addItems(['----']+ch_selected)
                ch_selected.append('chNS')
            self.ch_selected = ch_selected
            print(self.ch_selected)
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
        else: 
            error_txt = "You first need to validate the channels' settings to continue setting the project."
            self.tE_validate.setText(error_txt)
    
    # -- Functions for ChannelNS
    def set_chNS_settings(self): 
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
            
        if len(valid)== 3 and all(valid):
            self.tE_validate.setText('All done setting ChannelNS!...')
            self.button_set_chNS.setChecked(True)
            self.get_chNS_settings()
        else: 
            self.button_set_chNS.setChecked(False)
        toggled(self.button_set_chNS)

    def get_chNS_settings(self):
        ch_ext = self.ext_chNS.currentText()
        ext_cont = self.ext_contNS.currentText()
        ch_int = self.int_chNS.currentText()
        int_cont = self.int_contNS.currentText()

        color_chNS = {}
        for cont in ['int', 'tiss', 'ext']:
            color_chNS[cont] = getattr(self, 'fillcolor_chNS_'+cont).text()

        chNS_settings = {'layer_btw_chs': self.tick_chNS.isChecked(),
                            'ch_ext': (ch_ext.lower(), ext_cont[0:3]),
                            'ch_int': (ch_int.lower(), int_cont[0:3]),
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

    def apply_segments(self): 
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

    def apply_sections(self): 
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

    def validate_segm_settings(self): 
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
            print('self.mH_settings (validate_segm_settings):',self.mH_settings)
            if all(valid_all):
                self.button_set_segm.setChecked(True)
                self.tE_validate.setText('All good, continue!')
            else: 
                self.button_set_segm.setChecked(False)
            toggled(self.button_set_segm)

    def validate_sect_settings(self): 
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
            print('self.mH_settings (validate_sect_settings):',self.mH_settings)
            if all(valid_all):
                self.button_set_sect.setChecked(True)
                self.tE_validate.setText('All good, continue!')
            else: 
                self.button_set_sect.setChecked(False)
            toggled(self.button_set_sect)

    # -- Tab general functions
    def tabChanged(self):
        print('Tab was changed to ', self.tabWidget.currentIndex())

class SetMeasParam(QDialog):

    def __init__(self, mH_settings:dict, parent=None):
        super().__init__(parent)
        
        uic.loadUi('set_meas_screen.ui', self)
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
        print(getattr(self, 'dict_meas'))

    def add_user_param(self):
        valid = []; error_txt = ''
        param_name = self.lineEdit_param_name.text()
        param_abbr = self.lineEdit_param_abbr.text()
        param_desc = self.textEdit_param_desc.toPlainText()
        param_class = self.textEdit_param_classes.toPlainText()

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
            print(self.params)
            self.set_meas_param_table()
            param_name = self.lineEdit_param_name.clear()
            param_abbr = self.lineEdit_param_abbr.clear()
            param_desc = self.textEdit_param_desc.clear()
            param_class = self.textEdit_param_classes.clear()
        
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
        print('settings_ballooning:'+name)
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

                
class LoadProj(QDialog):

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('load_project_screen.ui', self)
        self.setFixedSize(701,541)
        self.setWindowTitle('Load Existing Project...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))

        #Browse project
        self.button_browse_proj.clicked.connect(self.load_proj)

    def load_proj(self):
        response = QFileDialog.getExistingDirectory(self, caption="Select the Project's directory")
        print(response)
        test_proj_name = str(Path(response).name)[2:]
        json_name = 'mH_'+test_proj_name+'_project.json'
        test_proj_sett = Path(response) / 'settings' / json_name
        print(test_proj_name, '\n', json_name,'\n', test_proj_sett)
        if test_proj_sett.is_file(): 
            self.proj_dir = Path(response)
            self.proj_name = test_proj_name
            print(self.proj_dir.name)
            self.lab_filled_proj_dir.setText(str(self.proj_dir))
            self.lab_filled_proj_name.setText(str(self.proj_name))
            self.tE_validate.setText('Project -'+self.proj_name+'- was loaded successfully!')
        else: 
            self.tE_validate.setText('There is no settings file for a project within the selected directory. Please select a new directory.')

    def load_organs_data(self):
        row=0
        self.tableWidget.setRowCount(len(df_organs))
        for organ in df_organs: 
            self.tableWidget.setItem(row,0,QWidgets.QTableWidgetItem(df_organs[organ]['organ_UserName']))
            row += 1
            
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('main_window_screen.ui', self)
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
                print('char:', char)
                nam = nam.replace(char,'')
        if nam == '': 
            nam.remove('')
        # print(nam)
        output_str.append(nam)

    print('Result split_str: ', output_str)
    return output_str

def validate_txt(input_str):
    inv_chars = ['(',')', ':', '-', '/', '\\', '.', ',']
    for char in inv_chars:
        if input_str.find(char) != -1:
            error = char
            break
        else:
            error = None
    return error

