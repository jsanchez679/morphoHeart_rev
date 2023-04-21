import sys
from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (QDialog, QApplication, QMainWindow, QWidget, QFileDialog, QTabWidget,
                              QGridLayout, QVBoxLayout, QHBoxLayout, QLayout, QLabel, QPushButton, QLineEdit,
                              QColorDialog, QTableWidgetItem, QCheckBox)
from PyQt6.QtGui import QPixmap, QFont

from pathlib import Path
import os

#https://www.color-hex.com/color-palette/96194
#https://www.color-hex.com/color-palette/96197
#https://www.color-hex.com/color-palette/1024322


class WelcomeScreen(QDialog):

    # switch_window = QtCore.pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('welcome_screen.ui', self)
        self.setWindowTitle('Welcome to morphoHeart...')
        mH_logoXL = QPixmap('images/logos_7o5mm.png')
        self.mH_logo_XL.setPixmap(mH_logoXL)
        self.button_new_proj.clicked.connect(lambda: self.go_to_create_new_proj())
        self.button_load_proj.clicked.connect(lambda: self.go_to_load_proj())

    def go_to_create_new_proj(self): 
        # self.switch_window.emit()
        new_proj = CreateNewProj()
        widget.addWidget(new_proj)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_load_proj(self): 
        # self.switch_window.emit()
        load_proj = LoadProj()
        widget.addWidget(load_proj)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
class CreateNewProj(QDialog):
    def __init__(self):
        super().__init__()
        self.proj_name = ''
        self.proj_dir_parent = ''
        self.setWindowTitle('Create New Project...')
        uic.loadUi('new_project_screen.ui', self)
        mH_logoXS = QPixmap('images/logos_1o75mm.png')
        self.mH_logo_XS.setPixmap(mH_logoXS)

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

        #Set Tab Widgets
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.tabWidget.setTabText(0,'Morphological [morphoHeart]')
        self.tabWidget.setTabText(1,'Cellular [morphoCell]')
        self.tabWidget.setEnabled(False)

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

        # -- Channel NS
        self.set_chNS.setDisabled(True)
        self.set_chNS.setVisible(False)
        self.fillcolor_chNS_int_btn.clicked.connect(lambda: self.color_picker('chNS_int'))
        self.fillcolor_chNS_tiss_btn.clicked.connect(lambda: self.color_picker('chNS_tiss'))
        self.fillcolor_chNS_ext_btn.clicked.connect(lambda: self.color_picker('chNS_ext'))
        
        #Default colors (ChannelNS)
        self.ck_def_colorsNS.stateChanged.connect(lambda: self.default_colors('chNS'))

        # -- Segments
        self.set_segm.setVisible(False)
        list_obj_segm = ['Disc']#, 'Plane']
        for cB in [self.cB_obj_segm1, self.cB_obj_segm2]:
            for obj in list_obj_segm: 
                cB.addItem(obj)
        for sB in [self.sB_no_segm1, self.sB_no_segm2, self.sB_segm_noObj1, self.sB_segm_noObj2]:
            sB.setMinimum(1)
            sB.setMaximum(5)
        self.apply_segm.clicked.connect(lambda: self.set_tables(self.tabW_segm, self.ch_selected, 'segm'))

        # -- Sections
        self.set_sect.setVisible(False)
        list_obj_sect = ['Centreline']#, 'Plane']
        for cB in [self.cB_obj_sect1, self.cB_obj_sect2]:
            for obj in list_obj_sect: 
                cB.addItem(obj)
        self.apply_segm.clicked.connect(lambda: self.set_tables(self.tabW_sect, self.ch_selected, 'sect'))
        
        #Go back to Welcome Page
        self.button_go_back.clicked.connect(self.go_to_welcome)

    #Functions for General Project Settings   
    def get_proj_dir(self):
        self.button_validate_new_proj.setChecked(False)
        self.toggled(self.button_validate_new_proj)
        self.button_create_initial_proj.setChecked(False)
        self.toggled(self.button_create_initial_proj)
        self.button_select_proj_dir.setChecked(True)
        self.toggled(self.button_select_proj_dir)
        response = QFileDialog.getExistingDirectory(self, caption='Select a Directory to save New Project Files')
        self.proj_dir_parent = Path(response)
        self.lab_filled_proj_dir.setText(str(self.proj_dir_parent))

    def validate_new_proj(self): 
        #Get project name
        if len(self.lineEdit_proj_name.text())<=5:
            error_txt = 'Project name needs to be longer than five (5) characters'
            self.tE_validate.setText(error_txt)
            return
        else: 
            self.proj_name = self.lineEdit_proj_name.text()
        #Get Analysis Pipeline
        self.checked_analysis = {'morphoHeart': self.checkBox_mH.isChecked(), 
                              'morphoCell': self.checkBox_mC.isChecked(), 
                              'morphoPlot': self.checkBox_mP.isChecked()}
        checked = [self.checked_analysis[key] for key in self.checked_analysis]
        if len(self.proj_name) == 0 or isinstance(self.proj_dir_parent, str) or not(any(checked)):
            error_txt = '*Please '
            if len(self.proj_name) == 0: 
                error_txt += 'input a Project Name'            
            if not(any(checked)):
                if error_txt != '*Please  ':
                    error_txt += ', '
                error_txt += 'define an Analysis Pipeline'
            if isinstance(self.proj_dir_parent, str):
                if error_txt != '*Please  ':
                    error_txt += ' and '
                error_txt += 'Select Directory'
            error_txt += '.'
            self.tE_validate.setText(error_txt)
            self.button_validate_new_proj.setChecked(False)
        else: 
            self.button_validate_new_proj.setChecked(True)
            self.toggled(self.button_validate_new_proj)
            proj_folder = 'R_'+self.proj_name
            self.proj_dir = self.proj_dir_parent / proj_folder
            print(self.proj_dir, type(self.proj_dir))
            if self.proj_dir.is_dir():
                self.tE_validate.setText('*There is already a project named "'+self.proj_name+'" in the selected directory.')
            else: 
                self.lab_filled_proj_dir.setText(str(self.proj_dir))
                self.tE_validate.setText('All good. Select -Create- to create "'+self.proj_name+'" as a new project.')

    def create_new_proj(self):
        if self.button_validate_new_proj.isChecked(): 
            self.toggled(self.button_create_initial_proj)
            self.tabWidget.setEnabled(True)
            self.tab_mHeart.setEnabled(self.checked_analysis['morphoHeart'])
            self.tab_mCell.setEnabled(self.checked_analysis['morphoCell'])
            if self.checked_analysis['morphoHeart']:
                self.mH_settings = {'no_chs': 0,
                                    'name_chs': 0,
                                    'chs_relation': 0,
                                    'color_chs': 0,
                                    'chNS': 0,
                                    'segm': 0,
                                    'sect': 0,
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
        else: 
            self.tE_validate.setText("*Project's name, analysis pipeline and directory need to be validated for the new project to be created!")

    #Functions for Initial Set-up 
    # Functions for channels
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

    def color_picker(self, name):
        color = QColorDialog.getColor()
        if color.isValid():
            print('The selected color is: ', color.name())
            fill = getattr(self, 'fillcolor_'+name)
            fill.setStyleSheet("background-color: "+color.name()+"; color: "+color.name()+"; font: 25 2pt 'Calibri Light'")#+"; border: 1px solid "+color.name())
            fill.setText(color.name())
            print('Color:', fill.text())
            
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
            s_set.setVisible(True)
            s_set.setEnabled(True)
            self.mH_settings[stype] = {}
        else: 
            s_set.setVisible(False)
            s_set.setEnabled(False)
            self.mH_settings[stype] = False
    
    def validate_initial_settings(self):
        valid = []; error_txt = ''
        self.tick_ch1.setChecked(True)
        # Get ticked channels:
        ch_ticked = [self.tick_ch1.isChecked(), self.tick_ch2.isChecked(), 
                     self.tick_ch3.isChecked(), self.tick_ch4.isChecked()]
        print('ch_ticked:',ch_ticked)
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
                print('AAA: internal_count', internal_count, '-external_count', external_count)
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

        print('valid:', valid)
        if len(valid)== 6 and all(valid):
            self.tE_validate.setText('All done!... Press -Set Initial Settings- to continue.')
            self.button_validate_initial_set.setChecked(True)
        else: 
            self.button_validate_initial_set.setChecked(False)
        self.toggled(self.button_validate_initial_set)

    def set_initial_settings(self):
        if self.button_validate_initial_set.isChecked():
            self.toggled(self.button_set_initial_set)
            self.tick_ch1.setChecked(True)
            #Get data from initial settings
            # Get data form ticked channels:
            ch_ticked = [self.tick_ch1.isChecked(), self.tick_ch2.isChecked(), 
                        self.tick_ch3.isChecked(), self.tick_ch4.isChecked()]
            
            self.mH_settings['no_chs'] = sum(ch_ticked)
            user_name = {}
            color_chs = {}
            ch_relation = {}
            ch_selected = []
            for ch in ['ch1', 'ch2', 'ch3', 'ch4']:
                tick = getattr(self, 'tick_'+ch)
                if tick.isChecked(): 
                    ch_selected.append(ch)
                    user_name[ch] = getattr(self, ch+'_username').text()
                    ch_relation[ch] = getattr(self, 'cB_'+ch).currentText()
                    color_chs['ch'] = {}
                    for cont in ['int', 'tiss', 'ext']:
                        color_chs['ch'][cont] = getattr(self, 'fillcolor_'+ch+'_'+cont).text()

            self.mH_settings['name_chs'] = user_name
            self.mH_settings['chs_relation'] = ch_relation
            self.mH_settings['color_chs'] = color_chs

            #Get info from checked boxes
            self.checked('chNS')
            #---- Segments
            self.checked('segm')
            #---- Sections
            self.checked('sect')
            print(self.mH_settings)

            if self.tick_chNS.isChecked():
                #Set the comboBoxes for chNS
                self.ext_chNS.addItems(['----']+ch_selected)
                self.int_chNS.addItems(['----']+ch_selected)
                ch_selected.append('chNS')

            self.ch_selected = ch_selected
        else: 
            error_txt = "You first need to validate the channels' settings to continue setting the project."
            self.tE_validate.setText(error_txt)
    
    def set_tables(self, table, ch_selected, stype):
        table.horizontalHeader().setVisible(False)
        #table.verticalHeader().setVisible(False)
        h_labels = ['int', 'tiss', 'ext']*len(ch_selected)
        print('h_labels:', h_labels)
        table.setColumnCount(len(h_labels))

        #Get Number of cuts selected
        cuts_sel = {'Cut1': getattr(self, 'tick_'+stype+'1').isChecked(), 'Cut2':getattr(self, 'tick_'+stype+'2').isChecked()}
        print('cuts_sel:', cuts_sel)
        v_labels = ['---','---']+[key for key in cuts_sel.keys() if cuts_sel[key]==True]
        print('v_labels:', v_labels)
        table.setRowCount(len(v_labels))
        table.setVerticalHeaderLabels(v_labels)

        for col in range(table.columnCount()):
            table.setColumnWidth(col, 30)
        for row in range(table.rowCount()):
            table.setRowHeight(row, 16)

        #Set first row labels
        print(list(range(0,len(h_labels),3)))
        for n, col in enumerate(range(0,len(h_labels),3)):
            print(n, col)
            table.setSpan(0,col,1,3)
            table.setItem(0,col, QTableWidgetItem(ch_selected[n]))
            print(ch_selected[n])
        #Set second row labels
        for n, ccl in enumerate(range(len(h_labels))):
            table.setItem(1,ccl,QTableWidgetItem(h_labels[n]))

        print('len(colum):', table.columnCount())
        print('len(rows):', table.rowCount())

        row_n = 2
        for nn in range(len(v_labels[2:])):
            col_n = 0
            for mm in range(len(h_labels)):
                print(row_n, col_n)
                widget   = QWidget()
                checkbox = QCheckBox()
                checkbox.setChecked(False)
                layoutH = QHBoxLayout(widget)
                layoutH.addWidget(checkbox)
                # layoutH.setAlignment(Qt.AlignCenter)
                layoutH.setContentsMargins(0, 0, 0, 0)
                table.setCellWidget(row_n, col_n, widget)   
                col_n +=1   
            row_n +=1 




    # def apply_segm(self):


    def create_user_settings_to_fill(self): 
        self.toggled(self.button_validate_initial_set)
        #Get info from initial set-up
        no_chs = self.spinBox_noCh.value()
        layer_btw_chs = self.tick_chNS.isChecked()
        cutLayersIn2Segments = self.tick_segments.isChecked()
        obj2cutSegm = self.comboBox_obj_segm.currentText()
        no_segments = self.spinBox_noSegm.value()
        no_cuts_4segments = self.spinBox_segm_noObj.value()
        cutLayersIn2Sections = self.tick_sections.isChecked()
        obj2cutSect = self.comboBox_obj_sect.currentText()
        no_sections = self.spinBox_noSect.value()
        no_sect_cuts = self.spinBox_noSectCuts.value()
        print(no_chs, layer_btw_chs)
        print(cutLayersIn2Segments, obj2cutSegm, no_segments, no_cuts_4segments)
        print(cutLayersIn2Sections, obj2cutSect, no_sections, no_sect_cuts)

        # #Setup of channels, segments, sections
        # #Set the initial labels 
        # initial_row = QHBoxLayout(QWidget())
        # initial_row.addWidget(QLabel('Channel', self))
        # initial_row.addWidget(QLabel('Name', self))
        # initial_row.addWidget(QLabel('color-int', self))
        # initial_row.addWidget(QLabel('color-tiss', self))
        # initial_row.addWidget(QLabel('color-ext', self))
        # initial_row.addWidget(QLabel('Apply mask', self))
        # self.verticalLayout.addLayout(initial_row)
        # for n, ch in enumerate(range(no_chs)): 
        #     row_layout = QHBoxLayout()
        #     #Add widgets
        #     row_layout.addWidget(QLabel('Ch'+str(n), self))
        #     row_layout.addWidget(QLineEdit(placeholderText='Channel name'))
        #     row_layout.addWidget(QPushButton('Pick-color'))
        #     row_layout.addWidget(QPushButton('Pick-color'))
        #     row_layout.addWidget(QPushButton('Pick-color'))
        #     row_layout.addWidget(QPushButton('Toggle'))
        #     self.verticalLayout.addLayout(row_layout)

        # self.table_channel_settings.setRowCount(no_chs)

    

    def get_image_dir(self): 
        file_filter = 'Image File (*.png *.jpg *.tif)'
        response = QFileDialog.getOpenFileName(parent=self, caption='Select file image', 
                                               directory=os.getcwd(), filter=file_filter, 
                                               initialFilter=file_filter)
        print(response)

    def go_to_welcome(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    # Button general functions
    def toggled(self, button_name): 
        style = 'border-radius:10px; border-width: 1px; border-style: outset; color: rgb(71, 71, 71); font: 10pt "Calibri Light";'
        if button_name.isChecked():
            style_f = 'QPushButton{background-color: #eb6fbd; border-color: #672146;'+style+'}'
        else: 
            style_f = 'QPushButton{background-color: rgb(211, 211, 211); border-color: rgb(66, 66, 66);'+style+'}'
        button_name.setStyleSheet(style_f)

    #Tab general functions
    def tabChanged(self):
        print('Tab was changed to ', self.tabWidget.currentIndex())

class LoadProj(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Load Existing Project...')
        uic.loadUi('load_project_screen.ui', self)
        mH_logoXS = QPixmap('images/logos_1o75mm.png')
        self.mH_logo_XS.setPixmap(mH_logoXS)

        #Browse project
        self.button_browse_proj.clicked.connect(self.load_proj)

        #Table of organs
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,100)

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

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ui = MainWindow()
#     ui.show()
#     app.exec()

# class Controller: 
#     def __init__(self):
#         pass

#     def show_welcome(self): 
#         self.welcome = WelcomeScreen()
#         self.welcome.switch_window

# main
# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     controller = Controller()
#     controller.show_login()
#     sys.exit(app.exec_())

app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedSize(1000,940)
widget.show()

try: 
    sys.exit(app.exec())
except: 
    print('Exiting')


#python pyuic6 -x name.ui -o name.py
#C:\Users\bi1jsa\Desktop\pyqt6>D:\Applications\Miniconda\envs\mHpy39_qt\Scripts\pyuic6.exe -x C:\Users\bi1jsa\Desktop\pyqt6\test.ui -o C:\Users\bi1jsa\Desktop\pyqt6\test.py dragging and dropping all the files to get their path

# #--- form layout to set names of channels 
        # form_layout = QtWidgets.QFormLayout()
        # self.setLayout(form_layout)

        # #Add stuff/widgets
        # label_1 = QtWidgets.QLabel('This is a cool Label Row')
        # label_1.setFont(QFont('Calibri', 10))
        # f_name = QtWidgets.QLineEdit(self)
        # l_name = QtWidgets.QLineEdit(self)

        # #Add rows to app
        # form_layout.addRow(label_1)
        # form_layout.addRow('First Name', f_name)
        # form_layout.addRow('Last Name', l_name)
        # form_layout.addRow(QtWidgets.QPushButton('Press me', clicked = lambda: press_it()))

        # def press_it():
        #     label_1.setText(f'You clicked the button, {f_name.text()}!')