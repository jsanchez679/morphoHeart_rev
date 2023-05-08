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
from src.modules import mH_classes_new as mHC
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
        self.new_organ_win = None

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
        # Set Create New Organ Button
        self.new_proj_win.button_add_organ.clicked.connect(lambda: self.show_new_organ(parent_win='new_proj_win'))

    def show_meas_param(self):
        if self.meas_param_win == None: 
            self.meas_param_win = SetMeasParam(mH_settings = self.new_proj_win.mH_settings, 
                                               parent=self.new_proj_win)
        self.meas_param_win.show()
        self.meas_param_win.button_set_params.clicked.connect(lambda: self.validate_params())

    def show_load_proj(self): 
        if self.load_proj_win == None:
            self.load_proj_win = LoadProj() 
        self.welcome_win.close()
        self.load_proj_win.show()
        self.load_proj_win.button_go_back.clicked.connect(lambda: self.show_welcome())

    def show_new_organ(self, parent_win:str):
        if self.new_organ_win == None:
            self.new_organ_win = NewOrgan(proj = self.proj)

        #Identify parent and close it
        if parent_win == 'new_proj_win':
            self.new_proj_win.close()
        elif parent_win == 'load_proj_win':
            self.load_proj_win.close()
        else: 
            print('Other parent window?')
        print('parent_win:', parent_win)
        self.new_organ_win.show()
        self.new_organ_win.button_go_back.clicked.connect(lambda: self.show_parent(parent_win))

    
    def show_parent(self, parent:str):
        parent_win = getattr(self, parent)
        parent_win.show()

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

    def validate_params(self): 
        valid = []
        #First validate the ballooning options
        #-- Get checkboxes info
        cB_checked = {}
        for cha in self.meas_param_win.ch_all:
            for conta in ['int', 'ext']: 
                chcb = getattr(self.meas_param_win, 'cB_'+cha+'_'+conta+'_param5')
                if chcb.isEnabled() and chcb.isChecked():
                    cB_checked[cha+'_'+conta] = True
        print('cB_checked: ',cB_checked)

        #-- Get settings
        names = {}; 
        for opt in range(1,5,1):
            name_bal = getattr(self.meas_param_win, 'cB_balto'+str(opt)).currentText()
            ch_bal = getattr(self.meas_param_win, 'cB_ch_bal'+str(opt)).currentText() != '--select--'
            cont_bal = getattr(self.meas_param_win, 'cB_cont_bal'+str(opt)).currentText() != '--select--'
            if name_bal != '--select--': 
                aaa = name_bal.split('(')[1]
                bbb = aaa.split('-')
                ch_s = bbb[0].split(')')[0]
                cont_s = bbb[1]
                names[ch_s+'_'+cont_s] = {'ch': ch_bal, 
                                          'cont': cont_bal}
        print('names: ', names)
        
        #Now double check them 
        if set(list(cB_checked.keys())) != set(list(names.keys())):
            diff = set(list(cB_checked.keys())) - set(list(names.keys()))
            error_txt = "You have not selected the centreline to use for "+str(diff)
            self.meas_param_win.tE_validate.setText(error_txt)
            return 
        else: 
            for name in names: 
                if not names[name]['ch']: 
                    error_txt = "You have not selected the channel centreline to use for "+name
                    self.meas_param_win.tE_validate.setText(error_txt)
                    return 
                elif not names[name]['cont']: 
                    error_txt = "You have not selected the contour type centreline to use for "+name
                    self.meas_param_win.tE_validate.setText(error_txt)
                    return 
                else: 
                    valid.append(True)

        for opt in range(1,5,1):
            name_bal = getattr(self.meas_param_win, 'cB_balto'+str(opt)).currentText()
            if name_bal != '--select--': 
                cl_ch = getattr(self.meas_param_win, 'cB_ch_bal'+str(opt)).currentText()
                cl_cont = getattr(self.meas_param_win, 'cB_cont_bal'+str(opt)).currentText()
                
                cB_name = 'cB_'+cl_ch+'_'+cl_cont[0:3]+'_param2'
                cB_cl = getattr(self.meas_param_win, cB_name)
                if cB_cl.isChecked():
                    pass
                else: 
                    cB_cl.setChecked(True)
        
        self.meas_param_win.check_checkBoxes()
        bool_cB = [val for (_,val) in self.meas_param_win.dict_meas.items()]
        if any(bool_cB): 
            valid.append(True)
        else: 
            print('Looopppp!')
            valid.append(self.check_meas_param())

        if all(valid): 
            self.meas_param_win.tE_validate.setText('All done setting measurement parameters!')
            self.set_params()
        
    def check_meas_param(self):
        msg = "You have not selected any measurement parameters to obtain from the segmented channels. If you want to go back and select some measurement parameters, press 'Cancel', else if you are happy with this decision press 'OK'."
        title = 'No Measurement Parameters Selected'
        self.prompt_ok = Prompt_ok_cancel(msg = msg, title = title,  parent=self.meas_param_win)

        if self.prompt_ok.user_input == 'OK': 
            return True
        else: 
            print('cancel? or close?')
            error_txt = "Select measurement parameters for the channel-contours."
            self.meas_param_win.tE_validate.setText(error_txt)
            return False
        
    def set_params(self): 
        self.ballooning = {}
        for opt in range(1,5,1):
            name_bal = getattr(self.meas_param_win, 'cB_balto'+str(opt)).currentText()
            if name_bal != '--select--': 
                aaa = name_bal.split('(')[1]; bbb = aaa.split('-')
                ch_to = bbb[0].split(')')[0]
                cont_to = bbb[1]

                cl_ch = getattr(self.meas_param_win, 'cB_ch_bal'+str(opt)).currentText()
                cl_cont = getattr(self.meas_param_win, 'cB_cont_bal'+str(opt)).currentText()
                print('Opt'+str(opt)+':'+name_bal, cl_ch, cl_cont)

                self.ballooning[opt] = {'to_mesh': ch_to, 
                                        'to_mesh_type': cont_to, 
                                        'from_cl': cl_ch,
                                        'from_cl_type': cl_cont[0:3]}
                
        self.centreline = {'looped_length': getattr(self.meas_param_win, 'cB_cl_LoopLen').isChecked(),
                           'linear_length': getattr(self.meas_param_win, 'cB_cl_LinLen').isChecked()}
        
        # Toggle button and close window
        self.meas_param_win.button_set_params.setChecked(True)
        toggled(self.meas_param_win.button_set_params)
        self.meas_param_win.close()

        # Toggle button and close window
        self.new_proj_win.set_meas_param_all.setChecked(True)
        toggled(self.new_proj_win.set_meas_param_all)

        self.mH_params = self.meas_param_win.params
        self.ch_all = self.meas_param_win.ch_all
        self.mH_params[2]['measure'] = self.centreline
        self.mH_params[5]['measure'] = self.ballooning
        self.set_proj_meas_param()
    
    def set_proj_meas_param(self):
        selected_params = {}
        #First add all whole measure parameters selected
        for numa in self.meas_param_win.params: 
            selected_params[self.meas_param_win.params[numa]['s']] = {}

        print(self.meas_param_win.dict_meas)
        for cbox in self.meas_param_win.dict_meas:
            _,chf,contf,param_num = cbox.split('_')
            num_p = int(param_num.split('param')[1])
            param_name = self.meas_param_win.params[num_p]['s']
            cBox = getattr(self.meas_param_win, cbox)
            if cBox.isEnabled():
                is_checked = cBox.isChecked()
                selected_params[param_name][chf+':'+contf+':whole'] = is_checked
        
        #Add measure params from segments
        segm_dict = self.new_proj_win.mH_settings['segm']
        if isinstance(segm_dict, dict): 
            if segm_dict['cutLayersIn2Segments']: 
                cuts = [key for key in segm_dict if 'Cut' in key]
                params_segm = [param for param in segm_dict['measure'].keys() if segm_dict['measure'][param]]
                for param_a in params_segm: 
                    for cut_a in cuts: 
                        cut_semg = segm_dict[cut_a]['ch_segments']
                        no_segm = segm_dict[cut_a]['no_segments']
                        selected_params[param_a+'(segm)'] = {}
                        for ch_a in cut_semg: 
                            for cont_a in cut_semg[ch_a]:
                                for segm in range(1,no_segm+1,1):
                                    selected_params[param_a+'(segm)'][cut_a+':'+ch_a+':'+cont_a+':segm'+str(segm)] = True
        
        #Add measure params from sections
        sect_dict = self.new_proj_win.mH_settings['sect']
        if isinstance(sect_dict, dict): 
            if sect_dict['cutLayersIn2Sections']: 
                cuts = [key for key in sect_dict if 'Cut' in key]
                params_sect = [param for param in sect_dict['measure'].keys() if sect_dict['measure'][param]]
                for param_b in params_sect: 
                    for cut_b in cuts: 
                        cut_sect = sect_dict[cut_b]['ch_sections']
                        no_sect = sect_dict[cut_b]['no_sections']
                        selected_params[param_b+'(sect)'] = {}
                        for ch_b in cut_sect: 
                            for cont_b in cut_sect[ch_b]:    
                                for sect in range(1,no_sect+1,1):
                                    selected_params[param_b+'(sect)'][cut_b+':'+ch_b+':'+cont_b+':sect'+str(sect)] = True
        
        self.new_proj_win.mH_user_params = selected_params
        
    def new_proj(self):

        if self.new_proj_win.set_meas_param_all.isChecked(): 
            self.new_proj_win.button_new_proj.setChecked(True)
            toggled(self.new_proj_win.button_new_proj)
            self.new_proj_win.button_new_proj.setDisabled(True)

            proj_dict = {'name': self.new_proj_win.lineEdit_proj_name.text(), 
                        'notes' : self.new_proj_win.textEdit_ref_notes.toPlainText(),
                        'date' : str(self.new_proj_win.dateEdit.date().toPyDate()),
                        'analysis' : self.new_proj_win.checked_analysis, 
                        'dir_proj' : self.new_proj_win.proj_dir}
            
            self.proj = mHC.Project(proj_dict, new=True)

            self.new_proj_win.mH_settings['chs_all'] = self.ch_all
            self.new_proj_win.mH_settings['params'] = self.mH_params
            self.proj.set_settings(settings={'mH': {'settings':self.new_proj_win.mH_settings, 
                                                    'params': self.new_proj_win.mH_user_params},
                                             'mC': {'settings': self.new_proj_win.mC_settings,
                                                   'params': self.new_proj_win.mC_user_params}})
            
            self.proj.set_workflow()
            self.proj.create_proj_dir()
            self.proj.save_project()
            print(self.proj.__dict__)
            
        else: 
            print('not done!')






def main():
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    print('screen.name', screen.name())
    size = screen.size()
    print('screen.size: ', size.width(), size.height())
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

# import re
# r = re.compile('[+]?((\d+(\.\d*)?)|(\.\d+))([eE][+-]?\d+)?')
# if r.match('100e-5'): print ('it matches!')

# [+]?((\d+(\.\d*)?)|(\.\d+))([^a-d,f-z,A-D,F-Z][+-]?\d+)?


#https://pythex.org/
#Running example! It works!
# from PyQt6 import QtWidgets
# from PyQt6.QtCore import QRegularExpression
# from PyQt6.QtGui import QRegularExpressionValidator
# from PyQt6.QtWidgets import QWidget, QLineEdit

# import sys

# class MyWidget(QWidget):
#     def __init__(self, parent=None):
#         super(QWidget, self).__init__(parent)
#         self.le_input = QLineEdit(self)

#         reg_ex = QRegularExpression("[+]?((\d+(\.\d*)?)|(\.\d+))([^a-d,f-z,A-D,F-Z][+-]?\d+)?")
#         input_validator = QRegularExpressionValidator(reg_ex, self.le_input)
#         self.le_input.setValidator(input_validator)

# if __name__ == '__main__':
#     a = QtWidgets.QApplication(sys.argv)

#     w = MyWidget()
#     w.show()

#     a.exec()