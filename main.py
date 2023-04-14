import sys
from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QTabWidget
from PyQt6.QtGui import QPixmap

from pathlib import Path
import os

class WelcomeScreen(QDialog):

    # switch_window = QtCore.pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('welcome_screen.ui', self)
        self.setWindowTitle('Welcome to morphoHeart...')
        mH_logoXL = QPixmap('images/logos_7o5mm.png')
        self.mH_logo_XL.setPixmap(mH_logoXL)
        self.button_new_proj.clicked.connect(self.go_to_create_new_proj)
        self.button_load_proj.clicked.connect(self.go_to_load_proj)

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

        #Get project directory
        self.button_select_proj_dir.clicked.connect(self.get_proj_dir)
        #Validate and Create Initial Project (proj_name, analysis_pipeline, proj_dir)
        self.button_validate_new_proj.clicked.connect(self.validate_new_proj)
        self.button_create_initial_proj.clicked.connect(self.create_new_proj)
        #Validate initial settings
        self.button_validate_initial_set.clicked.connect(self.create_user_settings_to_fill)

        #Set Tab Widgets
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.tabWidget.setTabText(0,'Morphological [morphoHeart]')
        self.tabWidget.setTabText(1,'Cellular [morphoCell]')
        self.tabWidget.setEnabled(False)

        #Initial set-up objects
        #---- No Channels and ChNegativeSpace
        self.spinBox_noCh.setMinimum(1)
        self.spinBox_noCh.setMaximum(5)

        #---- Segments
        self.checkBox_segments.stateChanged.connect(self.checked_segm)
        self.checked_segm()
        list_obj_segm = ['Disc']#, 'Plane']
        for obj in list_obj_segm: 
            self.comboBox_obj_segm.addItem(obj)
        self.spinBox_noSegm.setMinimum(1)
        self.spinBox_noSegm.setMaximum(5)
        self.spinBox_segm_noObj.setMinimum(1)
        self.spinBox_segm_noObj.setMaximum(5)

        #---- Sections
        self.checkBox_sections.stateChanged.connect(self.checked_sect)
        self.checked_sect()
        list_obj_sect = ['Centreline']#, 'Plane']
        for obj in list_obj_sect: 
            self.comboBox_obj_sect.addItem(obj)
        self.spinBox_noSect.setMinimum(1)
        self.spinBox_noSect.setMaximum(5)
        self.spinBox_noSectCuts.setMinimum(1)
        self.spinBox_noSectCuts.setMaximum(5)

        #Setup of channels, segments, sections
        

        #Go back to Welcome Page
        self.button_go_back.clicked.connect(self.go_to_welcome)

    def checked_analysis(self):
        self.user_analysis = {'morphoHeart': self.checkBox_mH.isChecked(), 'morphoCell': self.checkBox_mC.isChecked(), 'morphoPlot': self.checkBox_mP.isChecked()}

    def toggled(self, button_name): 
        if button_name.isChecked():
            button_name.setStyleSheet('QPushButton {background-color: rgba(170, 0, 127, 80); border-radius:10px; border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); color: rgb(71, 71, 71); font: 10pt "Calibri Light";}')
        else: 
            button_name.setStyleSheet('QPushButton {background-color: rgb(211, 211, 211); border-radius:10px; border-width: 1px; border-style: outset; border-color: rgb(66, 66, 66); color: rgb(71, 71, 71); font: 10pt "Calibri Light";}')
            
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
        self.proj_name = self.lineEdit_proj_name.text()
        #Get Analysis Pipeline
        self.checked_analysis()
        checked = [self.user_analysis[key] for key in self.user_analysis]
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
            self.lab_validate_create_new_proj.setText(error_txt)
            self.button_validate_new_proj.setChecked(False)
        else: 
            self.button_validate_new_proj.setChecked(True)
            self.toggled(self.button_validate_new_proj)
            proj_folder = 'R_'+self.proj_name
            self.proj_dir = self.proj_dir_parent / proj_folder
            print(self.proj_dir, type(self.proj_dir))
            if self.proj_dir.is_dir():
                self.lab_validate_create_new_proj.setText('*There is already a project named "'+self.proj_name+'" in the selected directory.')
            else: 
                self.lab_filled_proj_dir.setText(str(self.proj_dir))
                self.lab_validate_create_new_proj.setText('All good. Select -Create- to create "'+self.proj_name+'" as a new project.')

    def create_new_proj(self):
        if self.button_validate_new_proj.isChecked(): 
            self.toggled(self.button_create_initial_proj)
            self.tabWidget.setEnabled(True)
            self.tab_mHeart.setEnabled(self.user_analysis['morphoHeart'])
            self.tab_mCell.setEnabled(self.user_analysis['morphoCell'])

            #Disable all fields from Gral Project Settings
            self.lab_validate_create_new_proj.setText('New project  "'+self.proj_name+'" has been created!')
            self.gral_proj_settings.setDisabled(True)

            if self.user_analysis['morphoHeart']:
                self.tabWidget.setCurrentIndex(0)
            else: 
                self.tabWidget.setCurrentIndex(1)
        else: 
            self.lab_validate_create_new_proj.setText("*Project's name, analysis pipeline and directory need to be validated for the new project to be created!")

    def checked_segm(self):
        if self.checkBox_segments.isChecked():
            self.comboBox_obj_segm.setDisabled(False)
            self.spinBox_noSegm.setDisabled(False)
            self.spinBox_segm_noObj.setDisabled(False)
        else:
            self.comboBox_obj_segm.setDisabled(True)
            self.spinBox_noSegm.setDisabled(True)
            self.spinBox_segm_noObj.setDisabled(True)

    def checked_sect(self):
        if self.checkBox_sections.isChecked():
            self.comboBox_obj_sect.setDisabled(False)
            self.spinBox_noSect.setDisabled(False)
            self.spinBox_noSectCuts.setDisabled(False)
        else:
            self.comboBox_obj_sect.setDisabled(True)
            self.spinBox_noSect.setDisabled(True)
            self.spinBox_noSectCuts.setDisabled(True)

    def create_user_settings_to_fill(self): 
        self.toggled(self.button_validate_initial_set)
        #Get info from initial set-up
        no_chs = self.spinBox_noCh.value()
        layer_btw_chs = self.checkBox_chNS.isChecked()
        cutLayersIn2Segments = self.checkBox_segments.isChecked()
        obj2cutSegm = self.comboBox_obj_segm.currentText()
        no_segments = self.spinBox_noSegm.value()
        no_cuts_4segments = self.spinBox_segm_noObj.value()
        cutLayersIn2Sections = self.checkBox_sections.isChecked()
        obj2cutSect = self.comboBox_obj_sect.currentText()
        no_sections = self.spinBox_noSect.value()
        no_sect_cuts = self.spinBox_noSectCuts.value()
        print(no_chs, layer_btw_chs)
        print(cutLayersIn2Segments, obj2cutSegm, no_segments, no_cuts_4segments)
        print(cutLayersIn2Sections, obj2cutSect, no_sections, no_sect_cuts)

        self.table_channel_settings.setRowCount(no_chs)

    def tabChanged(self):
        print('Tab was changed to ', self.tabWidget.currentIndex())

    def get_image_dir(self): 
        file_filter = 'Image File (*.png *.jpg *.tif)'
        response = QFileDialog.getOpenFileName(parent=self, caption='Select file image', 
                                               directory=os.getcwd(), filter=file_filter, 
                                               initialFilter=file_filter)
        print(response)

    def go_to_welcome(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

class LoadProj(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Load Existing Project...')
        uic.loadUi('load_project_screen.ui', self)
        mH_logoXS = QPixmap('images/logos_1o75mm.png')
        self.mH_logo_XS.setPixmap(mH_logoXS)

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
            self.lab_validate_create_new_proj.setText('Project -'+self.proj_name+'- was loaded successfully!')
        else: 
            self.lab_validate_create_new_proj.setText('There is no settings file for a project within the selected directory. Please select a new directory.')


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window_screen.ui', self)
        mH_logoXS = QPixmap('images/logos_1o75mm.png')
        self.mH_logo_XS.setPixmap(mH_logoXS)

    
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
widget.setFixedSize(700,900)
widget.show()

try: 
    sys.exit(app.exec())
except: 
    print('Exiting')


#python pyuic6 -x name.ui -o name.py
#C:\Users\bi1jsa\Desktop\pyqt6>D:\Applications\Miniconda\envs\mHpy39_qt\Scripts\pyuic6.exe -x C:\Users\bi1jsa\Desktop\pyqt6\test.ui -o C:\Users\bi1jsa\Desktop\pyqt6\test.py dragging and dropping all the files to get their path