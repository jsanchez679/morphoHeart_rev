
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
        
class CreateNewProj(QDialog):

    def __init__(self, parent=None):
        super().__init__()
        self.proj_name = ''
        self.proj_dir_parent = ''
        uic.loadUi('new_project_screen.ui', self)
        self.setFixedSize(1001,975)
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
        self.set_sect.setVisible(False)
        # -- Sections
        self.tick_sect1.setEnabled(True)
        self.tick_sect1.setChecked(True)
        self.set_sect.setVisible(False)
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
            # print(self.proj_dir_parent)
            if self.proj_dir_parent.is_dir() and len(str(self.proj_dir_parent))>1:
                valid.append(True)
            else: 
                self.button_select_proj_dir.setChecked(False)
                toggled(self.button_select_proj_dir)
                error_txt = '*The selected project directory is invalid. Please select another directory.'
                self.tE_validate.setText(error_txt)
                return

        # print('valid:', valid)
        if len(valid)== 3 and all(valid):
            self.button_validate_new_proj.setChecked(True)
            proj_folder = 'R_'+self.proj_name
            self.proj_dir = self.proj_dir_parent / proj_folder
            # print(self.proj_dir, type(self.proj_dir))
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
            self.prompt = PromptWindow(msg='Give the name of the three different custom orientations for the -'+ortype.upper()+'- separated by a comma:', 
                                        title = 'Custom Orientation', info=ortype, parent = self)
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
                names.append(getattr(self, ch+'_username').text())
                if len(getattr(self, ch+'_username').text()) <= 3:
                    names_valid.append(False)
                else: 
                    names_valid.append(True)

        if not all(names_valid):
            error_txt = '*Active channels must have a name longer than three (3) characters.'
            self.tE_validate.setText(error_txt)
            return
        else: 
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
            error_txt = '*Please select the internal and external channels and contours that need to be used to extract the channel from the negativa space.'
            self.tE_validate.setText(error_txt)
            return

        # print('valid:', valid)
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
    
    def set_tables(self, table, ch_selected, stype):
        table.horizontalHeader().setVisible(False)
        #table.verticalHeader().setVisible(False)
        h_labels = ['int', 'tiss', 'ext']*len(ch_selected)
        # print('h_labels:', h_labels)
        table.setColumnCount(len(h_labels))

        #Get Number of cuts selected
        cuts_sel = {'Cut1': getattr(self, 'tick_'+stype+'1').isChecked(), 'Cut2':getattr(self, 'tick_'+stype+'2').isChecked()}
        # print('cuts_sel:', cuts_sel)
        v_labels = ['---','---']+[key for key in cuts_sel.keys() if cuts_sel[key]==True]
        # print('v_labels:', v_labels)
        table.setRowCount(len(v_labels))
        table.setVerticalHeaderLabels(v_labels)

        for col in range(table.columnCount()):
            table.setColumnWidth(col, 30)
        for row in range(table.rowCount()):
            table.setRowHeight(row, 16)

        #Set first row labels
        # print(list(range(0,len(h_labels),3)))
        for n, col in enumerate(range(0,len(h_labels),3)):
            # print(n, col)
            table.setSpan(0,col,1,3)
            table.setItem(0,col, QTableWidgetItem(ch_selected[n]))
            # print(ch_selected[n])
        #Set second row labels
        for n, ccl in enumerate(range(len(h_labels))):
            table.setItem(1,ccl,QTableWidgetItem(h_labels[n]))

        # print('len(colum):', table.columnCount())
        # print('len(rows):', table.rowCount())
        # print(ch_selected)

        btn_stype = []
        row_n = 2
        for v_lab in v_labels[2:]:
            row_name = v_lab
            col_n = 0
            for mm, h_lab in enumerate(h_labels):
                cont_name = h_lab
                ch_num = (mm//3)
                print('mm:',mm, '-ch_num:',ch_num, h_lab)
                ch_name = ch_selected[ch_num]
                widget   = QWidget()
                checkbox = QCheckBox()
                checkbox.setChecked(False)
                layoutH = QHBoxLayout(widget)
                layoutH.addWidget(checkbox)
                btn_name = 'cB_'+stype+'_('+row_name+'-'+ch_name+'_'+cont_name+')'
                btn_stype.append(btn_name)
                setattr(self, btn_name, checkbox)
                # layoutH.setAlignment(Qt.AlignCenter)
                layoutH.setContentsMargins(0, 0, 0, 0)
                table.setCellWidget(row_n, col_n, widget)   
                col_n +=1   
            row_n +=1 

        setattr(self, 'btn_'+stype, btn_stype)
        # print(getattr(self, 'btn_'+stype))

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
                
            if len(valid) == 1 and all(valid): 
                valid_all.append(True)
        
        if all(valid_all): 
            self.apply_segm.setChecked(True)
            self.tE_validate.setText('All good, continue selecting the channel-contours from which these segments will be extracted!')
            self.set_tables(self.tabW_segm, self.ch_selected, 'segm')
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
                
            if len(valid) == 1 and all(valid): 
                valid_all.append(True)
        
        if all(valid_all): 
            self.apply_sect.setChecked(True)
            self.tE_validate.setText('All good, continue selecting the channel-contours from which these sections will be extracted!')
            self.set_tables(self.tabW_sect, self.ch_selected, 'sect')
        else: 
            self.apply_sect.setChecked(False)
        toggled(self.apply_sect)

    def validate_segm_settings(self): 
        valid_all = []
        segm_settings = {'cutLayersIn2Segments': True}
        stype = 'segm'
        cuts_sel = {'Cut1': getattr(self, 'tick_'+stype+'1').isChecked(), 'Cut2':getattr(self, 'tick_'+stype+'2').isChecked()}
        for cut in cuts_sel.keys(): 
            valid = []; error_txt = ''
            if cuts_sel[cut]:
                cut_no = cut[-1]
                #Get values
                no_segm = getattr(self, 'sB_no_segm'+cut_no).value()
                obj_type = getattr(self, 'cB_obj_segm'+cut_no).currentText()
                no_obj = getattr(self, 'sB_segm_noObj'+cut_no).value()
                names_segm = getattr(self, 'names_segm'+cut_no).text()
                names_segm = split_str(names_segm)

                #Check values
                if len(names_segm) != int(no_segm):
                    error_txt = '*'+cut+": The number of segments need to match the number of segment names given."
                    self.tE_validate.setText(error_txt)
                    return
                elif len(set(names_segm)) != int(no_segm):
                    error_txt = '*'+cut+": Segment names need to be different."
                    self.tE_validate.setText(error_txt)
                    return
                else: 
                    valid.append(True)

                #Check apply has been pressed
                if self.apply_segm.isChecked(): 
                    valid.append(True)
                else: 
                    error_txt = "You need to apply the segment cut's settings and select the channel contours to cut before continuing."
                    self.tE_validate.setText(error_txt)
                    return
                
                #Check box selection
                tiss_cut = []
                for btn in self.btn_segm:
                    if 'Cut'+cut_no in btn: 
                        aaa = btn.split('(')[1]
                        bbb = aaa.split('-')[1]
                        ccc = bbb.split(')')[0]
                        ch_s, cont_s = ccc.split('_')
                        cB = getattr(self, btn).isChecked()
                        if cB: 
                            tiss_cut.append((ch_s,cont_s))

                if len(tiss_cut) <= 0: 
                    error_txt = '*'+cut+": At least one channel contour needs to be selected for this segments cut."
                    self.tE_validate.setText(error_txt)
                    return
                else: 
                    valid.append(True)

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

                print('segm:',valid)
                if len(valid) == 4 and all(valid): 
                    #Get names
                    names_segmF = {}
                    for dd in range(int(no_segm)): 
                        segm_no = 'segm'+str(dd+1)
                        names_segmF[segm_no] = names_segm[dd]
                    
                    #Get selected contours
                    tiss_cut = []
                    for btn in self.btn_segm:
                        if 'Cut'+cut_no in btn: 
                            aaa = btn.split('(')[1]
                            bbb = aaa.split('-')[1]
                            ccc = bbb.split(')')[0]
                            ch_s, cont_s = ccc.split('_')
                            cB = getattr(self, btn).isChecked()
                            if cB: 
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
        segm_settings['measure'] = {'volume': meas_vol, 'area': meas_area, 'ellipsoids': meas_ellip}
        self.mH_settings['segm'] = segm_settings
        print('self.mH_settings (validate_segm_settings):',self.mH_settings)
        if all(valid_all):
            self.button_set_segm.setChecked(True)
            self.tE_validate.setText('All good, continue!')
        else: 
            self.button_set_segm.setChecked(False)
        toggled(self.button_set_segm)

    def validate_sect_settings(self): 
        valid_all = []
        sect_settings = {'cutLayersIn2Sections': True}
        stype = 'sect'
        cuts_sel = {'Cut1': getattr(self, 'tick_'+stype+'1').isChecked(), 'Cut2':getattr(self, 'tick_'+stype+'2').isChecked()}
        for cut in cuts_sel.keys(): 
            valid = []; error_txt = ''
            if cuts_sel[cut]:
                cut_no = cut[-1]
                #Get values
                obj_type = getattr(self, 'cB_obj_sect'+cut_no).currentText()
                names_sect = getattr(self, 'names_sect'+cut_no).text()
                names_sect = split_str(names_sect)

                #Check values
                if len(names_sect) != 2:
                    error_txt = '*'+cut+": Sections cut only produce two objects. Please provide two section names."
                    self.tE_validate.setText(error_txt)
                    return
                elif len(set(names_sect)) != 2:
                    error_txt = '*'+cut+": Section names need to be different."
                    self.tE_validate.setText(error_txt)
                    return
                else: 
                    valid.append(True)

                #Check apply has been pressed
                if self.apply_sect.isChecked(): 
                    valid.append(True)
                else: 
                    error_txt = "You need to apply the section cut's settings and select the channel contours to cut before continuing."
                    self.tE_validate.setText(error_txt)
                    return

                #Check box selection
                tiss_cut = []
                for btn in self.btn_sect:
                    if 'Cut'+cut_no in btn: 
                        aaa = btn.split('(')[1]
                        bbb = aaa.split('-')[1]
                        ccc = bbb.split(')')[0]
                        ch_s, cont_s = ccc.split('_')
                        cB = getattr(self, btn).isChecked()
                        if cB: 
                            tiss_cut.append((ch_s,cont_s))
                
                if len(tiss_cut) <= 0: 
                    error_txt = '*'+cut+": At least one channel contour needs to be selected for this section cut."
                    self.tE_validate.setText(error_txt)
                    return
                else: 
                    valid.append(True)

                #Check measurement parameters to measure
                meas_vol = getattr(self, 'cB_volume_'+stype).isChecked()
                meas_area = getattr(self, 'cB_area_'+stype).isChecked()
                if any([meas_vol, meas_area]):
                    valid.append(True)
                else: 
                    error_txt = "*Please select the measurement parameter(s) (e.g. volume and/or surface area) you want to extract from the sections"
                    self.tE_validate.setText(error_txt)
                    return

                print('sect:',valid)
                if len(valid) == 4 and all(valid): 
                    #Get names
                    names_sectF = {}
                    for dd in range(2): 
                        sect_no = 'sect'+str(dd+1)
                        names_sectF[sect_no] = names_sect[dd]
                    
                    #Get selected contours
                    tiss_cut = []
                    for btn in self.btn_sect:
                        if 'Cut'+cut_no in btn: 
                            aaa = btn.split('(')[1]
                            bbb = aaa.split('-')[1]
                            ccc = bbb.split(')')[0]
                            ch_s, cont_s = ccc.split('_')
                            cB = getattr(self, btn).isChecked()
                            if cB: 
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
                                'obj_segm': obj_type,
                                'name_segments': names_sectF,
                                'ch_segments': ch_sections}
                                
                    sect_settings[cut] = dict_cut
                    valid_all.append(True)

        # print('valid_all:', valid_all)
        sect_settings['measure'] = {'volume': meas_vol, 'area': meas_area}
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
        self.setFixedSize(791,561)
        self.setWindowTitle('Select the parameters to measure from the segmented channels...')
        self.mH_logo_XS.setPixmap(QPixmap(mH_top_corner))
        self.setWindowIcon(QIcon(mH_icon))

        #Create table 
        self.set_meas_param_table(mH_settings)

        #Buttons
        self.button_add_param.clicked.connect(lambda: self.add_user_param())

    def set_meas_param_table(self, mH_settings:dict): 
        
        ch_all = mH_settings['name_chs']
        if isinstance(mH_settings['chNS'], dict) and len(list(mH_settings['chNS'].keys()))>0:
            if mH_settings['chNS']['layer_btw_chs']:
                ch_all['chNS'] = mH_settings['chNS']['user_nsChName']
        
        table = self.tabW_meas
        table.horizontalHeader().setVisible(False)
        #table.verticalHeader().setVisible(False)
        h_labels = ['int', 'tiss', 'ext']*len(ch_all)
        # print('h_labels:', h_labels)
        table.setColumnCount(len(h_labels))

        #Set Measurement Parameters
        params = {'SA': 'surface area', 'Vol':'volume','CL':'centreline','CLlin':'centreline length','CLloop':'centreline looped length', 
                  'th_i2e':'thickness (int>ext)','th_e2i':'thickness (ext>int)', 'bal': 'centreline>tissue (ballooning)'}
        
        v_labels = ['---','---']+[params[val] for val in params]
        # print('v_labels:', v_labels)
        table.setRowCount(len(v_labels))
        table.setVerticalHeaderLabels(v_labels)

        for col in range(table.columnCount()):
            table.setColumnWidth(col, 30)
        for row in range(table.rowCount()):
            table.setRowHeight(row, 16)

        #Set first row labels
        for n, col, chn in zip(count(), range(0,len(h_labels),3), ch_all):
            # print(n, col, chn)
            table.setSpan(0,col,1,3)
            table.setItem(0,col, QTableWidgetItem(ch_all[chn]))
        #Set second row labels
        for ccl, h_lab in enumerate(h_labels):
            table.setItem(1,ccl,QTableWidgetItem(h_lab))

        btn_stype = []
        row_n = 2
        for aa, v_lab, param in zip(count(), v_labels[2:], params.keys()):
            row_name = param#[param]
            col_n = 0
            for mm, h_lab in enumerate(h_labels):
                cont_name = h_lab
                ch_num = (mm//3)
                # print('mm:',mm, '-ch_num:',ch_num, h_lab)
                ch_name = list(ch_all.keys())[ch_num]
                widget   = QWidget()
                checkbox = QCheckBox()
                checkbox.setChecked(False)
                layoutH = QHBoxLayout(widget)
                layoutH.addWidget(checkbox)
                btn_name = 'cB_('+row_name+'_o_'+ch_name+'_'+cont_name+')'
                btn_stype.append(btn_name)
                setattr(self, btn_name, checkbox)
                # layoutH.setAlignment(Qt.AlignCenter)
                layoutH.setContentsMargins(0, 0, 0, 0)
                table.setCellWidget(row_n, col_n, widget)   
                col_n +=1   
            row_n +=1 

        setattr(self, 'btn_meas', btn_stype)
        disable_pars = {'th_i2e':['int', 'ext'],'th_e2i':['int', 'ext'], 'bal': ['tiss']}
        for chs in ch_all.keys():
            for pars in disable_pars:
                for cont in disable_pars[pars]:
                    cB_name = 'cB_('+pars+'_o_'+chs+'_'+cont+')'
                    cB = getattr(self, cB_name)
                    cB.setDisabled(True)

        print(getattr(self, 'btn_meas'))
        self.params = params
        self.h_labels = h_labels
        self.v_labels = v_labels
        self.ch_all = ch_all

    def add_user_param(self):
        error_txt = ''
        param_name = self.lineEdit_param_name.text()
        param_desc = self.textEdit_param_desc.toPlainText()
        param_class = self.textEdit_param_classes.toPlainText()

        if len(param_name)<=5: 
            error_txt = "Parameter's name needs to be longer than 5 characters"
            self.tE_validate.setText(error_txt)
            return
        else: 
            param_name_line = param_name.replace(' ', '_')
        
            param_classes = split_str(param_class)
            v_labels = ['---','---']+[self.params[val] for val in self.params]+[param_name]
            self.params[param_name_line] = (param_name, param_desc, param_classes)

            rowPosition = self.tabW_meas.rowCount()
            self.tabW_meas.insertRow(rowPosition)
            self.tabW_meas.setVerticalHeaderLabels(v_labels)

            col_n = 0
            for mm, h_lab in enumerate(self.h_labels):
                cont_name = h_lab
                ch_num = (mm//3)
                ch_name = list(self.ch_all.keys())[ch_num]
                widget   = QWidget()
                checkbox = QCheckBox()
                checkbox.setChecked(False)
                layoutH = QHBoxLayout(widget)
                layoutH.addWidget(checkbox)
                btn_name = 'cB_('+param_name_line+'_o_'+ch_name+'_'+cont_name+')'
                self.btn_meas.append(btn_name)
                setattr(self, btn_name, checkbox)
                # layoutH.setAlignment(Qt.AlignCenter)
                layoutH.setContentsMargins(0, 0, 0, 0)
                self.tabW_meas.setCellWidget(rowPosition, col_n, widget) 
                col_n +=1  
            
            print(self.params)
            print(self.btn_meas)

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

