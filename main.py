'''
morphoHeart

Version: Apr 26, 2023
@author: Juliana Sanchez-Posada

'''

#%% Imports - ########################################################
import sys
# from PyQt6 import uic
from PyQt6 import QtWidgets#, QtCore
# from pathlib import Path

#%% morphoHeart Imports - ##################################################
from gui.gui_classes import *
from src.modules import mH_classes as mHC
# from src.modules import mH_funcBasics as fcBasics
# from src.modules import mH_funcContours as fcCont
# from src.modules import mH_funcMeshes as fcMeshes

#https://www.color-hex.com/color-palette/96194
#https://www.color-hex.com/color-palette/96197
#https://www.color-hex.com/color-palette/1024322
#%% API
class Controller: 
    def __init__(self):
        self.welcome_win = None
        self.new_proj_win = None
        self.meas_param_win = None
        self.load_proj_win = None
        pass

    def show_welcome(self):
        if self.new_proj_win == None: 
            self.welcome_win = WelcomeScreen()
        if self.new_proj_win != None:
            self.new_proj_win.close()
        if self.load_proj_win != None:
            self.load_proj_win.close()
        self.welcome_win.show()
        self.welcome_win.button_new_proj.clicked.connect(lambda: self.show_create_new_proj())
        self.welcome_win.button_load_proj.clicked.connect(lambda: self.show_load_proj())
    
    def show_create_new_proj(self):
        if self.new_proj_win == None: 
            self.new_proj_win = CreateNewProj()
        self.welcome_win.close()
        self.new_proj_win.show()
        # Go Back Button
        self.new_proj_win.button_go_back.clicked.connect(lambda: self.show_welcome())
        # Set Measurement Parameters Button
        self.new_proj_win.set_meas_param_all.clicked.connect(lambda: self.set_meas_param())
        # Set Create New Project Button
        self.new_proj_win.button_new_proj.clicked.connect(lambda: self.new_proj())

    def show_meas_param(self):
        if self.meas_param_win == None: 
            self.meas_param_win = SetMeasParam(mH_settings = self.new_proj_win.mH_settings, 
                                               parent=self.new_proj_win)
        self.meas_param_win.show()
        self.meas_param_win.button_set_params.clicked.connect(lambda: self.set_params())

    def show_load_proj(self): 
        if self.load_proj_win == None:
            self.load_proj_win = LoadProj() 
        self.welcome_win.close()
        self.load_proj_win.show()
        self.load_proj_win.button_go_back.clicked.connect(lambda: self.show_welcome())

    #Functions related to API
    def set_meas_param(self): 
        print('self.mH_settings (set_meas_param):',self.new_proj_win.mH_settings)
        valid = []
        if self.new_proj_win.button_set_initial_set.isChecked(): 
            valid.append(True)
        else: 
            error_txt = 'You need to set initial settings first to set measurement parameters.'
            self.new_proj_win.tE_validate.setText(error_txt)
            return

        if self.new_proj_win.checked('chNS'): 
            if self.new_proj_win.button_set_chNS.isChecked():
                valid.append(True)
            else: 
                error_txt = 'You need to set Channel NS settings first to set measurement parameters.'
                self.new_proj_win.tE_validate.setText(error_txt)
                return
        
        if self.new_proj_win.checked('segm'): 
            if self.new_proj_win.button_set_segm.isChecked():
                valid.append(True)
            else: 
                error_txt = 'You need to set segments settings first to set measurement parameters.'
                self.new_proj_win.tE_validate.setText(error_txt)
                return
            
        if self.new_proj_win.checked('sect'): 
            if self.new_proj_win.button_set_sect.isChecked():
                valid.append(True)
            else: 
                error_txt = 'You need to set sections settings first to set measurement parameters.'
                self.new_proj_win.tE_validate.setText(error_txt)
                return
            
        if all(valid): 
            self.show_meas_param()

    def set_params(self): 
        selected_params = {}
        for btn in self.meas_param_win.btn_meas:
            is_checked = getattr(self.meas_param_win, btn).isChecked()
            par, info = btn.split('(')[1].split(')')[0].split('_o_')
            ch_o, cont_o = info.split('_')
            selected_params[ch_o+':'+cont_o+':'+'whole'+':'+par] = is_checked
        
        self.user_params = selected_params
        self.meas_param_win.button_set_params.setChecked(True)
        self.new_proj_win.set_meas_param_all.setChecked(True)
        toggled(self.meas_param_win.button_set_params)
        toggled(self.new_proj_win.set_meas_param_all)
        self.meas_param_win.close()
        print(self.user_params)

    def new_proj(self):
        self.meas_param_win.button_new_proj.setChecked(True)
        toggled(self.new_proj_win.button_new_proj)
        self.meas_param_win.button_new_proj.setDisabled(True)
        if self.new_proj_win.set_meas_param_all.isChecked(): 
            print('mH_settings:',self.new_proj_win.mH_settings)
            print('notes: ',self.new_proj_win.textEdit_ref_notes.toPlainText())
            self.proj = mHC.Project(name=self.new_proj_win.lineEdit_proj_name.text(), 
                               notes=self.new_proj_win.textEdit_ref_notes.toPlainText(),
                               date = self.new_proj_win.dateEdit.date().toPyDate(),
                               analysis=self.new_proj_win.checked_analysis, 
                               dir_proj = self.new_proj_win.proj_dir)
            print(self.proj.__dict__)
            # self.proj.set_settings(mH_settings=self.new_proj_win.mH_settings, 
            #                   mC_settings=self.new_proj_win.mC_settings)
            
        else: 
            print('not done!')

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_welcome()
    try: 
        sys.exit(app.exec())
    except: 
        print('Exiting')

    
    # widget = QtWidgets.QStackedWidget()
    # welcome = WelcomeScreen(widget)
    # widget.addWidget(welcome)
    # # widget.setFixedSize(1001,981)
    # widget.show()



   

if __name__ == '__main__':
    main()

#python pyuic6 -x name.ui -o name.py
#C:\Users\bi1jsa\Desktop\pyqt6>D:\Applications\Miniconda\envs\mHpy39_qt\Scripts\pyuic6.exe -x C:\Users\bi1jsa\Desktop\pyqt6\test.ui -o C:\Users\bi1jsa\Desktop\pyqt6\test.py dragging and dropping all the files to get their path


