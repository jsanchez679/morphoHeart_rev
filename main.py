import sys
from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QTabWidget
from PyQt6.QtGui import QPixmap

from pathlib import Path
import os

class WelcomeScreen(QDialog):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('welcome_screen.ui', self)
        mH_logoXL = QPixmap('images/logos_7o5mm.png')
        self.mH_logo_XL.setPixmap(mH_logoXL)
        self.button_new_proj.clicked.connect(self.go_to_create_new_proj)
        self.button_load_proj.clicked.connect(self.go_to_load_proj)

    def go_to_create_new_proj(self): 
        new_proj = CreateNewProj()
        widget.addWidget(new_proj)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_load_proj(self): 
        load_proj = LoadProj()
        widget.addWidget(load_proj)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateNewProj(QDialog):
    def __init__(self):
        super().__init__()
        self.proj_name = ''
        self.proj_dir_parent = ''
        uic.loadUi('new_project_screen.ui', self)
        mH_logoXS = QPixmap('images/logos_1o75mm.png')
        self.mH_logo_XS.setPixmap(mH_logoXS)

        #Get project directory
        self.button_select_proj_dir.clicked.connect(self.get_proj_dir)
        #Validate the entries (proj_name and proj_dir)
        self.button_validate_new_proj.clicked.connect(self.create_new_proj)

        #Set Tab Widgets
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.tabWidget.setTabText(0,'Morphological (morphoHeart)')
        self.tabWidget.setTabText(1,'Cellular (morphoCell)')

    def checked_analysis(self):
        self.user_analysis = {'morphoHeart': self.checkBox_mH.isChecked(), 'morphoCell': self.checkBox_mC.isChecked(), 'morphoPlot': self.checkBox_mP.isChecked()}
        print(self.user_analysis)
            
    def get_proj_dir(self):
        response = QFileDialog.getExistingDirectory(self, caption='Select a Directory to save New Project Files')
        self.proj_dir_parent = Path(response)
        self.lab_filled_proj_dir.setText(str(self.proj_dir_parent))
    
    def create_new_proj(self):
        #Get project name
        self.proj_name = self.lineEdit_proj_name.text()
        #Get Analysis Pipeline
        self.checked_analysis()
        checked = [self.user_analysis[key] for key in self.user_analysis]
        if len(self.proj_name) == 0 or isinstance(self.proj_dir_parent, str) or not(any(checked)):
            self.lab_validate_create_new_proj.setText('Please input a -Project Name-, define Analysis Pipeline and Select a Directory to save the new project files.')
        else: 
            proj_folder = 'R_'+self.proj_name
            self.proj_dir = self.proj_dir_parent / proj_folder
            print(self.proj_dir, type(self.proj_dir))
            if self.proj_dir.is_dir():
                self.lab_validate_create_new_proj.setText('There is already a project named "'+self.proj_name+'" in the selected directory.')
            else: 
                self.lab_filled_proj_dir.setText(str(self.proj_dir))
                self.lab_validate_create_new_proj.setText('New project  "'+self.proj_name+'" created correctly.')

    def tabChanged(self):
        print('Tab was changed to ', self.tabWidget.currentIndex())

    def get_image_dir(self): 
        file_filter = 'Image File (*.png *.jpg *.tif)'
        response = QFileDialog.getOpenFileName(parent=self, caption='Select file image', 
                                               directory=os.getcwd(), filter=file_filter, 
                                               initialFilter=file_filter)
        print(response)


class LoadProj(QDialog):
    def __init__(self):
        super().__init__()
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

    
# main
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