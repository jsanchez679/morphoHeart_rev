'''
morphoHeart

Version: Apr 26, 2023
@author: Juliana Sanchez-Posada

'''
# Relative import problems: stackoverflow.com/a/14132912/8682868
#%% Imports - ########################################################
import sys
# from PyQt6 import uic
from PyQt6 import QtWidgets#, QtCore
# from pathlib import Path

#%% morphoHeart Imports - ##################################################
from src.gui.config import mH_config 
from src.gui.gui_classes import *
from src.modules import mH_classes_new as mHC
from src.modules import mH_funcBasics as fcB
from src.modules import mH_funcContours as fcC
from src.modules import mH_funcMeshes as fcM
from src import mH_api as mA

#%% API
class Controller: 
    def __init__(self):
        self.welcome_win = None
        self.new_proj_win = None
        self.meas_param_win = None
        self.load_proj_win = None
        self.new_organ_win = None
        self.main_win = None

    def show_welcome(self):
        #Close previous windows if existent
        if self.new_proj_win != None:
            self.new_proj_win.close()
        if self.load_proj_win != None:
            self.load_proj_win.close()
        #Create welcome window and show
        if self.new_proj_win == None: 
            self.welcome_win = WelcomeScreen()
        self.welcome_win.show()

        #Connect Buttons
        # -Create new project
        self.welcome_win.button_new_proj.clicked.connect(lambda: self.show_create_new_proj())
        # -Load project
        self.welcome_win.button_load_proj.clicked.connect(lambda: self.show_load_proj())
        # -Create new project from template
        self.welcome_win.button_new_proj_from_template.clicked.connect(lambda: self.button_clicked())
    
    def button_clicked(self): 
        # #Message
        # title = 'This is the title!'
        # msg = 'Message goes here!'
        # self.prompt = Prompt_ok_cancel(title, msg, parent=self.welcome_win)
        # self.prompt.exec()
        # print('output:',self.prompt.output, '\n')

        #Radio Buttons
        # items = {0: {'opt': 'Option0', 'lineEdit': True, 'regEx': 'all'}, 1: {'opt': 'Option1', 'lineEdit': False}, 2: {'opt': 'Option2', 'lineEdit': True, 'regEx': 'num'} }
        # title = 'This is the title!'
        # msg = 'Message goes here!'
        # self.prompt = Prompt_ok_cancel_radio(title, msg, items, parent=self.welcome_win)
        # self.prompt.exec()
        # print('output:',self.prompt.output, '\n')

        # #Checkboxes 
        # items = {0: {'opt': 'Option0'}, 1: {'opt': 'Option1'}, 2: {'opt': 'Option2'} }
        # title = 'This is the title!'
        # msg = 'Message goes here!'
        # title = 'Select process(ess) to re-run'
        # msg = 'Select the process(es) you want to run:'
        # # items = {0: {'opt': 'Mask Stack'}, 1: {'opt': 'Close Contours Automatically'}, 
        # #             2: {'opt': 'Close Contours manually'}, 3: {'opt': 'Close Inflow/Outflow Tract'}}
        # items = {'A-MaskChannel': {'opt': 'Mask Stack'},
        #         'A-Autom': {'opt': 'Close Contours Automatically'},
        #         'B-Manual': {'opt': 'Close Contours Manually'},
        #         'C-CloseInOut': {'opt': 'Close Inflow/Outflow Tract(s)'}}
        # self.prompt = Prompt_ok_cancel_checkbox(title, msg, items, parent=self.welcome_win)
        # self.prompt.exec()
        # print('output:',self.prompt.output, '\n')

        #Sounds
        # print(mH_config.gui_sound)
        # fcB.alert('error')
        # fcB.alert('woohoo')
        # fcB.alert('jump')
        # fcB.alert('connection')

        #Save all
        msg = ["Do you want to save the changes to this Organ and Project before closing?","If you don't save your changes will be lost."]
        self.prompt = Propmt_save_all(msg, info=[], parent=self.welcome_win)
        # self.prompt.exec()
        # print('output:',self.prompt.output, '\n')

    def show_create_new_proj(self):
        #Close welcome window
        self.sound = self.welcome_win.sound
        self.welcome_win.close()
        #Create new proj window and show
        if self.new_proj_win == None: 
            self.new_proj_win = CreateNewProj()
        self.new_proj_win.show()

        #Connect Buttons
        # -Go Back 
        self.new_proj_win.button_go_back.clicked.connect(lambda: self.show_welcome())
        # -Set Measurement Parameters 
        self.new_proj_win.set_meas_param_all.clicked.connect(lambda: self.show_meas_param())
        # -Create New Project 
        self.new_proj_win.button_new_proj.clicked.connect(lambda: self.new_proj())
        # -Show New Organ Window 
        self.new_proj_win.button_add_organ.clicked.connect(lambda: self.show_new_organ(parent_win='new_proj_win'))

    def show_meas_param(self):
        #Create meas param window and show
        if self.new_proj_win.check_to_set_params(): 
            if self.meas_param_win == None: 
                self.meas_param_win = SetMeasParam(mH_settings = self.new_proj_win.mH_settings, 
                                                parent=self.new_proj_win)
            self.meas_param_win.show()
            self.meas_param_win.button_set_params.clicked.connect(lambda: self.set_proj_meas_param())
            self.new_proj_win.set_meas_param_all.setChecked(True)
            toggled(self.new_proj_win.set_meas_param_all)
        else: 
            error_txt = "*Make sure all the 'Set' Buttons are toggle/checked to continue."
            self.new_proj_win.win_msg(error_txt)
            print('Something is wrong: show_meas_param')
            return

    def show_load_proj(self): 
        #Close welcome window
        self.welcome_win.close()
        #Create Load Project Window and show
        if self.load_proj_win == None:
            self.load_proj_win = LoadProj() 
        self.load_proj_win.show()

        #Connect buttons
        # -Go Back
        self.load_proj_win.button_go_back.clicked.connect(lambda: self.show_welcome())
        # -Browse project
        self.load_proj_win.button_browse_proj.clicked.connect(self.load_proj)
        # -Show New Organ Window 
        self.load_proj_win.button_add_organ.clicked.connect(lambda: self.show_new_organ(parent_win='load_proj_win'))
        # -Go to main_window
        self.load_proj_win.go_to_main_window.clicked.connect(lambda: self.show_main_window(parent_win='load_proj_win'))

    def show_new_organ(self, parent_win:str):
        #Identify parent and close it
        if parent_win == 'new_proj_win':
            if self.new_proj_win.button_new_proj.isChecked():
                self.new_proj_win.close()
            else: 
                error_txt = "*Please create the New Project first before adding an organ to it."
                self.new_proj_win.win_msg(error_txt)
                self.new_proj_win.button_new_proj.setChecked(False)
                toggled(self.new_proj_win.button_new_proj)
                return
        elif parent_win == 'load_proj_win':
            self.load_proj_win.close()
        else: 
            print('Other parent window?')
        print('parent_win:', parent_win)

        #Create new organ window and show
        if self.new_organ_win == None:
            self.new_organ_win = NewOrgan(proj = self.proj)
        self.new_organ_win.show()

        #Connect Buttons
        # -Go Back 
        self.new_organ_win.button_go_back.clicked.connect(lambda: self.show_parent(parent_win))
        # - Create New Organ
        self.new_organ_win.button_create_new_organ.clicked.connect(lambda: self.new_organ())
        # -Go to main_window
        self.new_organ_win.go_to_main_window.clicked.connect(lambda: self.show_main_window(parent_win='new_organ_win'))

    def show_parent(self, parent:str):
        parent_win = getattr(self, parent)
        parent_win.show()

    def show_main_window(self, parent_win:str):
        #Close new organ or load organ window window
        if parent_win == 'new_organ_win':
            if self.new_organ_win.button_create_new_organ.isChecked():
                self.new_organ_win.close()
            else: 
                error_txt = '*You need to create the organ to continue.'
                self.new_organ_win.win_msg(error_txt)
                print('Error in new proj window')
                return
            
        elif parent_win == 'load_proj_win':
            self.load_proj_win.check_unique_organ_selected(self.proj)
            if self.load_proj_win.organ_selected != None:
                self.organ_to_analyse = self.load_proj_win.organ_selected#.replace(' ', '_')
                self.load_proj_win.win_msg('Loading organ '+self.organ_to_analyse+'...')
                self.load_organ(proj = self.proj, organ_to_load = self.organ_to_analyse)
                self.load_proj_win.close()
            else: 
                if len(self.proj.organs) == 0: 
                    error_txt = "!The project selected does not contain organs. Add a new organ to this project by selecting 'Create New Organ'."
                    self.load_proj_win.win_msg(error_txt)
                else: 
                    error_txt = '*Please select one organ to analyse.'
                    self.load_proj_win.win_msg(error_txt)
                    print('Error in loading window')
                return
        else: 
            print('Other parent window?')
        print('parent_win:', parent_win)

        #Create Main Project Window and show
        if self.main_win == None:
            print('\nLoaded Project and Organ!\n >> Proj:', self.proj.__dict__.keys())
            print('>> Organ:', self.organ.__dict__.keys())
            self.main_win = MainWindow(proj = self.proj, organ = self.organ) 
        self.main_win.show()

        #Segmentation Tab
        # - Buttons inside channels
        self.main_win.ch1_closecont.clicked.connect(lambda: self.close_cont(ch_name= 'ch1'))
        self.main_win.ch1_selectcont.clicked.connect(lambda: self.select_cont(ch_name= 'ch1'))
        self.main_win.ch2_closecont.clicked.connect(lambda: self.close_cont(ch_name= 'ch2'))
        self.main_win.ch2_selectcont.clicked.connect(lambda: self.select_cont(ch_name= 'ch2'))
        self.main_win.ch3_closecont.clicked.connect(lambda: self.close_cont(ch_name= 'ch3'))
        self.main_win.ch3_selectcont.clicked.connect(lambda: self.select_cont(ch_name= 'ch3'))
        self.main_win.ch4_closecont.clicked.connect(lambda: self.close_cont(ch_name= 'ch4'))
        self.main_win.ch4_selectcont.clicked.connect(lambda: self.select_cont(ch_name= 'ch4'))

        #Process and Analyse Tab
        self.main_win.keeplargest_play.clicked.connect(lambda: self.run_keeplargest())
        self.main_win.cleanup_play.clicked.connect(lambda: self.run_cleanup())
        self.main_win.trimming_play.clicked.connect(lambda: self.run_trimming())
        self.main_win.orientation_play.clicked.connect(lambda: self.run_axis_orientation())
        self.main_win.chNS_play.clicked.connect(lambda: self.run_chNS())

        self.main_win.centreline_clean_play.clicked.connect(lambda: self.run_centreline_clean())
        self.main_win.centreline_ML_play.clicked.connect(lambda: self.run_centreline_ML())
        self.main_win.centreline_vmtk_play.clicked.connect(lambda: self.run_centreline_vmtk())
        self.main_win.centreline_select.clicked.connect(lambda: self.run_centreline_select())
        # self.main_win.centreline_play.clicked.connect(lambda: self.run_centreline())

        self.main_win.heatmaps3D_play.clicked.connect(lambda: self.run_heatmaps3D())
        #Indiv Plot buttons
        self.main_win.hm_play1.clicked.connect(lambda: self.run_heatmaps3D(btn=1))
        self.main_win.hm_play2.clicked.connect(lambda: self.run_heatmaps3D(btn=2))
        self.main_win.hm_play3.clicked.connect(lambda: self.run_heatmaps3D(btn=3))
        self.main_win.hm_play4.clicked.connect(lambda: self.run_heatmaps3D(btn=4))
        self.main_win.hm_play5.clicked.connect(lambda: self.run_heatmaps3D(btn=5))
        self.main_win.hm_play6.clicked.connect(lambda: self.run_heatmaps3D(btn=6))
        self.main_win.hm_play7.clicked.connect(lambda: self.run_heatmaps3D(btn=7))
        self.main_win.hm_play8.clicked.connect(lambda: self.run_heatmaps3D(btn=8))
        self.main_win.hm_play9.clicked.connect(lambda: self.run_heatmaps3D(btn=9))
        self.main_win.hm_play10.clicked.connect(lambda: self.run_heatmaps3D(btn=10))
        self.main_win.hm_play11.clicked.connect(lambda: self.run_heatmaps3D(btn=11))
        self.main_win.hm_play12.clicked.connect(lambda: self.run_heatmaps3D(btn=12))
        # self.main_win.heatmaps2D_play.clicked.connect(lambda: self.run_heatmaps2D())

        self.main_win.segments_play.clicked.connect(lambda: self.run_segments())
        # self.main_win.sections_play.clicked.connect(lambda: self.run_sections())

    #Functions related to API  
    # Project Related  
    def set_proj_meas_param(self):
        if self.meas_param_win.validate_params() == True: 
            self.mH_params = self.meas_param_win.params
            self.ch_all = self.meas_param_win.ch_all
            self.mH_params[2]['measure'] = self.meas_param_win.final_params['centreline']
            self.mH_params[5]['measure'] = self.meas_param_win.final_params['ballooning']
        
            selected_params = self.new_proj_win.mH_user_params 
            if selected_params == None: 
                selected_params = {}
            #First add all whole measure parameters selected
            for numa in self.meas_param_win.params: 
                selected_params[self.meas_param_win.params[numa]['s']] = {}

            for cbox in self.meas_param_win.dict_meas:
                if 'roi' not in cbox:
                    _,chf,contf,param_num = cbox.split('_')
                    num_p = int(param_num.split('param')[1])
                    param_name = self.meas_param_win.params[num_p]['s']
                    cBox = getattr(self.meas_param_win, cbox)
                    if cBox.isEnabled():
                        is_checked = cBox.isChecked()
                        selected_params[param_name][chf+'_'+contf+'_whole'] = is_checked
                else: 
                    _,roi,param_num = cbox.split('_')
                    num_p = int(param_num.split('param')[1])
                    param_name = self.meas_param_win.params[num_p]['s']
                    cBox = getattr(self.meas_param_win, cbox)
                    if cBox.isEnabled():
                        is_checked = cBox.isChecked()
                        selected_params[param_name]['roi'] = is_checked
                        
            #Add ballooning measurements
            param_name = self.meas_param_win.params[5]['s']
            selected_params[param_name] = {}
            for opt in self.mH_params[5]['measure']:
                to_mesh = self.mH_params[5]['measure'][opt]['to_mesh']
                to_mesh_type = self.mH_params[5]['measure'][opt]['to_mesh_type']
                from_cl = self.mH_params[5]['measure'][opt]['from_cl']
                from_cl_type = self.mH_params[5]['measure'][opt]['from_cl_type']
                selected_params[param_name][to_mesh+'_'+to_mesh_type+'_('+from_cl+'_'+from_cl_type+')'] = True

            #Add heatmaps 3d to 2d
            selected_params['hm3Dto2D'] = {}
            if self.meas_param_win.cB_hm3d2d.isChecked():
                hm_ch = self.meas_param_win.hm_cB_ch.currentText()
                hm_cont = self.meas_param_win.hm_cB_cont.currentText()[0:3]
                name = hm_ch+'_'+hm_cont
                selected_params['hm3Dto2D'][name] = True
            else: 
                selected_params['hm3Dto2D']['ch_cont'] = False

            self.new_proj_win.mH_user_params = selected_params
            print('Selected_params', selected_params)

            #Toogle button and close window
            self.meas_param_win.button_set_params.setChecked(True)
            toggled(self.meas_param_win.button_set_params)
            self.meas_param_win.close()
            #Toggle button in new project window
            self.new_proj_win.set_meas_param_all.setChecked(True)
            toggled(self.new_proj_win.set_meas_param_all)
            error_txt = "Well done! Continue setting up new project."
            self.new_proj_win.win_msg(error_txt)
        else: 
            # error_txt = "*Please validate selected measurement parameters first."
            # self.meas_param_win.win_msg(error_txt)
            return 
        
    def new_proj(self):
        if self.new_proj_win.validate_set_all():
            self.new_proj_win.win_msg("Creating and saving new project...")
            temp_dir = None
            if self.new_proj_win.cB_proj_as_template.isChecked():
                line_temp = self.new_proj_win.lineEdit_template_name.text()
                line_temp = line_temp.replace(' ', '_')
                temp_name = 'mH_'+line_temp+'_project.json'
                cwd = Path().absolute()
                dir_temp = cwd / 'db' / 'templates' / temp_name 
                if dir_temp.is_file():
                    self.new_proj_win.win_msg('*There is already a template with the selected name. Please give this template a new name.')
                    return
                else: 
                    print('New project template: ', dir_temp)
                    temp_dir = dir_temp

            self.new_proj_win.button_new_proj.setChecked(True)
            toggled(self.new_proj_win.button_new_proj)
            # self.new_proj_win.button_new_proj.setDisabled(True)

            proj_dict = {'name': self.new_proj_win.lineEdit_proj_name.text(), 
                        'notes' : self.new_proj_win.textEdit_ref_notes.toPlainText(),
                        'date' : str(self.new_proj_win.dateEdit.date().toPyDate()),
                        'analysis' : self.new_proj_win.checked_analysis, 
                        'dir_proj' : self.new_proj_win.proj_dir, 
                        'heart_default': self.new_proj_win.heart_analysis.isChecked()}
            
            self.proj = mHC.Project(proj_dict, new=True)

            self.new_proj_win.mH_settings['chs_all'] = self.ch_all
            self.new_proj_win.mH_settings['params'] = self.mH_params
            self.proj.set_settings(settings={'mH': {'settings':self.new_proj_win.mH_settings, 
                                                    'params': self.new_proj_win.mH_user_params},
                                            'mC': {'settings': self.new_proj_win.mC_settings,
                                                'params': self.new_proj_win.mC_user_params}})
            
            self.proj.set_workflow()
            self.proj.create_proj_dir()
            self.proj.save_project(temp_dir = temp_dir)
            print('\n>>> New Project: ',self.proj.__dict__.keys())
            self.new_proj_win.win_msg("New project '"+self.new_proj_win.lineEdit_proj_name.text()+"' has been created and saved! Continue creating an organ as part of this project. ")
    
    def load_proj(self):
        path_folder = QFileDialog.getExistingDirectory(self.load_proj_win, caption="Select the Project's directory")
        proj_name = str(Path(path_folder).name)[2:] #Removing the R_
        proj_name_us = proj_name.replace(' ', '_')
        json_name = 'mH_'+proj_name_us+'_project.json'
        proj_settings_path = Path(path_folder) / 'settings' / json_name
        if proj_settings_path.is_file(): 
            proj_dict = {'name': proj_name, 
                         'dir': path_folder}
            self.proj = mHC.Project(proj_dict, new=False)
            print('Loaded project:',self.proj.__dict__.keys())
            print('Project[organs]:',self.proj.organs)
            self.load_proj_win.proj = self.proj
            #Fill window with project info
            self.load_proj_win.fill_proj_info(proj = self.proj)
        else: 
            self.load_proj_win.button_browse_proj.setChecked(False)
            toggled(self.load_proj_win.button_browse_proj)
            self.load_proj_win.win_msg('*There is no settings file for a project within the selected directory. Please select a new directory.')

    #Organ related
    def new_organ(self): 
        if self.new_organ_win.validate_organ(self.proj): 
            self.new_organ_win.win_msg('Creating and saving new organ...')
            if self.new_organ_win.check_selection(self.proj):
                if self.new_organ_win.check_shapes(self.proj): 
                    self.new_organ_win.button_create_new_organ.setChecked(True)
                    toggled(self.new_organ_win.button_create_new_organ)
                    self.new_organ_win.win_msg('Creating organ "'+self.new_organ_win.lineEdit_organ_name.text()+'"')
                    # self.new_organ_win.button_create_new_organ.setDisabled(True)

                    name = self.new_organ_win.lineEdit_organ_name.text()
                    notes = self.new_organ_win.textEdit_ref_notes.toPlainText()
                    strain = self.new_organ_win.cB_strain.currentText()
                    stage = self.new_organ_win.cB_stage.currentText()
                    genotype = self.new_organ_win.cB_genotype.currentText()
                    manipulation = self.new_organ_win.cB_manipulation.currentText()
                    im_or = self.new_organ_win.cB_stack_orient.currentText()
                    custom_angle = self.new_organ_win.cust_angle.text()
                    res_units = self.new_organ_win.resolution
                    resolution = [res_units[axis]['scaling'] for axis in ['x','y','z']]
                    units = [res_units[axis]['units'] for axis in ['x','y','z']]
                    date = str(self.new_organ_win.dateEdit.date().toPyDate())

                    organ_settings = {'project': {'user': self.proj.user_projName,
                                                'mH': self.proj.mH_projName,
                                                'dict_dir_info': self.proj.dir_info},
                                        'user_organName': name,
                                        'user_organNotes': notes,
                                        'im_orientation': im_or,
                                        'custom_angle': custom_angle,
                                        'resolution': resolution,
                                        'im_res_units': units,
                                        'stage': stage, 
                                        'strain': strain, 
                                        'genotype': genotype,
                                        'manipulation': manipulation, 
                                        'date_created': date
                                            }
                    organ_dict = {'settings': organ_settings, 
                                'img_dirs': self.new_organ_win.img_dirs}

                    self.organ = mHC.Organ(project=self.proj, organ_dict=organ_dict, new = True)
                    self.new_organ_win.lab_filled_organ_dir.setText(str(self.organ.dir_res()))
                    print('\n>>> New Organ: ', self.organ.__dict__.keys())
                    self.proj.add_organ(self.organ)
                    self.organ.save_organ()
                    self.new_organ_win.win_msg('New organ "'+name+'" has been created as part of "'+self.proj.user_projName+'" project.')
                else: 
                    self.new_organ_win.button_create_new_organ.setChecked(False)
                    toggled(self.new_organ_win.button_create_new_organ)
                    return
            else: 
                self.new_organ_win.button_create_new_organ.setChecked(False)
                toggled(self.new_organ_win.button_create_new_organ)
                return 
        else:
            self.new_organ_win.button_create_new_organ.setChecked(False)
            toggled(self.new_organ_win.button_create_new_organ)
            return 
    
    def load_organ(self, proj, organ_to_load):
        self.organ = proj.load_organ(organ_to_load = organ_to_load)
        print('-------------Loaded Organ:-------------')
        print('organ.workflow: ', self.organ.workflow)
        if not hasattr(self.organ, 'obj_temp'):
            self.organ.obj_temp = {}
        print('self.organ.obj_temp: ',self.organ.obj_temp)
        print('self.organ.mH_settings: ',self.organ.mH_settings)
        print('self.organ.mH_settings[wf_info]: ',self.organ.mH_settings['wf_info'])

    #Channels related
    def close_cont(self, ch_name):
        mA.close_cont(controller=self, ch_name=ch_name)

    def select_cont(self, ch_name):
        mA.select_cont(controller=self, ch_name=ch_name)

    def run_keeplargest(self):
        mA.run_keeplargest(controller=self)

    def run_cleanup(self):
        mA.run_cleanup(controller=self)
    
    def run_trimming(self):
        mA.run_trimming(controller=self)

    def run_axis_orientation(self):
        mA.run_axis_orientation(controller=self)

    def run_chNS(self):
        mA.run_chNS(controller=self)

    def run_centreline_clean(self):
        mA.run_centreline_clean(controller=self)

    def run_centreline_ML(self):
        mA.run_centreline_ML(controller=self)

    def run_centreline_vmtk(self): 
        mA.run_centreline_vmtk(controller=self)
    
    def run_centreline_select(self): 
        mA.run_centreline_select(controller=self)

    # def run_centreline(self):
    #     mA.run_centreline(controller=self)

    def run_heatmaps3D(self, btn=None):
        mA.run_heatmaps3D(controller=self, btn = btn)

    # def run_heatmaps2D(self):
    #     mA.run_heatmaps2D(controller=self)

    def run_segments(self, btn=None):
        mA.run_segments(controller=self, btn = btn)

    # def run_sections(self):
    #     mA.run_sections(controller=self)
    
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

if __name__ == '__main__':
    main()

#python pyuic6 -x name.ui -o name.py
#C:\Users\bi1jsa\Desktop\pyqt6>D:\Applications\Miniconda\envs\mHpy39_qt\Scripts\pyuic6.exe -x C:\Users\bi1jsa\Desktop\pyqt6\test.ui -o C:\Users\bi1jsa\Desktop\pyqt6\test.py dragging and dropping all the files to get their path

#we defined
# the direction of insertion of the IFTs via polar coordinates in a
# local system of orthogonal axes in which the xy plane is transversal
# to the embryo, and the z axis is aligned with the embryo AP axis
# The direction of
# insertion of the IFTs is then defined by two angles: the θ angle and
# the φ angle (Fig. 5a).

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

# Create an installer
#https://build-system.fman.io/pyqt5-tutorial
# Style sheets
#https://doc.qt.io/qt-5/stylesheet.html
#https://doc.qt.io/qt-6.4/stylesheet-examples.html#customizing-qheaderview
# Images 
#https://doc.qt.io/qtdesignstudio/quick-images.html

# QDialog ButtonBox
#https://www.pythonguis.com/tutorials/pyqt-dialogs/


#https://www.color-hex.com/color-palette/96194
#https://www.color-hex.com/color-palette/96197
#https://www.color-hex.com/color-palette/1024322
# https://www.pythonguis.com/tutorials/pyqt6-bitmap-graphics/

#Theme 
#https://www.youtube.com/watch?v=ePG_t9bJQ5I
#https://raw.githubusercontent.com/NiklasWyld/Wydbid/main/Assets/stylesheet
#https://github.com/ColinDuquesnoy/QDarkStyleSheet/blob/master/qdarkstyle/dark/darkstyle.qss
# https://matiascodesal.com/blog/spice-your-qt-python-font-awesome-icons/
# https://www.geeksforgeeks.org/pyqt5-change-color-of-check-box-indicator/
# https://www.youtube.com/watch?v=ms2Ey_SzZZc
        # https://www.pythontutorial.net/pyqt/qt-style-sheets/
# https://doc.qt.io/qtforpython-6/overviews/stylesheet-examples.html
# https://doc.qt.io/qt-6/stylesheet-examples.html
# https://www.youtube.com/watch?v=ePG_t9bJQ5I
#self.cB_theme.currentIndexChanged.connect(lambda: self.theme_changed())

# https://stackoverflow.com/questions/23634241/put-an-image-on-a-qpushbutton