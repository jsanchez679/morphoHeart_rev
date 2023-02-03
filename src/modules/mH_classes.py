'''
morphoHeart_classes

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
# import os
from datetime import datetime
import pathlib
from pathlib import Path
import numpy as np
import vedo as vedo
from vedo import write
from skimage import measure, io
import copy
import json
import collections
import pprint
import matplotlib.pyplot as plt
import flatdict
from typing import Union

#%% ##### - Other Imports - ##################################################
#from ...config import dict_gui
from .mH_funcBasics import alert, ask4input, make_Paths, make_tuples, get_by_path, set_by_path
from .mH_funcMeshes import unit_vector

alert_all=True
heart_default=False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}

#%% ##### - Authorship - #####################################################
__author__     = 'Juliana Sanchez-Posada'
__license__    = 'MIT'
__maintainer__ = 'J. Sanchez-Posada'
__email__      = 'julianasanchezposada@gmail.com'
__website__    = 'https://github.com/jsanchez679/morphoHeart'

#%% ##### - Class definition - ###############################################
# Definition of class to save dictionary
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pathlib.WindowsPath):
            return str(obj)
        else:
            return super(NumpyArrayEncoder, self).default(obj)

class Project(): 
    '''
    Project class: 
    A new project would include a group or groups of Organs
    that are part of the same experiment and will then be averaged and/or
    compared. From this a project can contain just one organ or 
    multiple organs with different genotypes and stages. The settings to
    process all the organs contained in a project are set up when starting a 
    new project and can be amended if needed as the organs are processed.
    '''
    def __init__(self, name=None, notes=None, analysis=None, dir_proj=None,
                             new=True, proj_name=None):

        def create_mHName(self):
            '''
            func - create name for a morphoHeart project
            This function will assign the newly created project a name using a
            timestamp
            '''
            now_str = datetime.now().strftime('%Y%m%d%H%M')
            return 'mH_Proj-'+now_str
            
        if new:
            self.mH_projName = create_mHName(self)
            self.user_projName = name.replace(' ', '_')
            self.info = {'mH_projName': self.mH_projName,
                            'user_projName': self.user_projName,
                            'user_projNotes': notes, 
                            'dirs': []}
            self.analysis = analysis
            self.dir_proj = Path(dir_proj)
            self.organs = {}
            self.cellGroups = {}
                
        else: 
            load_dict = {'name': proj_name, 'dir': dir_proj}
            self.load_project(load_dict=load_dict)
    
    def load_project(self, load_dict:dict):
        dir_res = load_dict['dir']
        jsonDict_name = 'mH_'+load_dict['name']+'_project.json'
        json2open_dir = dir_res / 'settings' / jsonDict_name
        if json2open_dir.is_file():
            with open(json2open_dir, "r") as read_file:
                print(">> "+jsonDict_name+": Opening JSON encoded data")
                load_dict = json.load(read_file)
            
            load_dict = make_Paths(load_dict)
            
            tuple_keys = [['mH_settings','chNS','general_info','ch_ext'], 
                          ['mH_settings','chNS','general_info','ch_int'], 
                          ['workflow','ImProc','chNS','D-S3Create','Settings','ext_mesh'], 
                          ['workflow','ImProc','chNS','D-S3Create','Settings','int_mesh']]
            
            load_dict = make_tuples(load_dict, tuple_keys)
           
            self.info = load_dict['info']
            self.user_projName = load_dict['info']['user_projName']
            self.mH_projName = load_dict['info']['mH_projName']
            self.analysis = load_dict['analysis']
            
            self.mH_settings = load_dict['mH_settings']
            self.mH_channels = load_dict['mH_channels']
            self.mH_segments = load_dict['mH_segments']
            self.mH_param2meas = [tuple(item) for item in load_dict['mH_param2meas']]
            
            self.mC_settings = load_dict['mC_settings']
            self.mC_channels = load_dict['mC_channels']
            self.mC_segments = load_dict['mC_segments']
            self.mC_param2meas = load_dict['mC_param2meas']
            
            self.workflow = load_dict['workflow']
            self.organs = load_dict['organs']
            self.cellGroups = load_dict['cellGroups']
          
            
            self.dir_proj = load_dict['info']['dir_proj']
            self.dir_info = load_dict['info']['dir_info']
        else: 
            print('>> Error: No project with name ',load_dict['name'],' was found!\n Directory: ',str(json2open_dir))
            alert('error_beep')

    def set_settings(self, mH_settings:dict, mC_settings:dict):
        '''
        func - Create general project settings
        This function will be called when the user creates a new project and 
        fills information regarding the workflow for such project which will get into the 
        function packed as the mH_settings dictionary. 
        The output of this function will create an attribute to the project containing 
        most of the user settings except for the selected parameters. 
        '''
    
        self.set_mH_settings(mH_settings)
        self.set_mC_settings(mC_settings)
        
    def set_mH_settings(self, mH_settings:dict):
        
        mH_set = {}
        mH_meas_keys = []
        mH_channels = []
        mH_segments = []
            
        if self.analysis['morphoHeart']:
            for ch_num in range(0, mH_settings['no_chs']):
                ch_str = 'ch'+str(ch_num+1)
                dict_info_ch = {'mH_chName':ch_str,
                                'user_chName':mH_settings['name_chs'][ch_str].replace(' ', '_'),
                                'dir_cho': None, 
                                'ch_relation': mH_settings['chs_relation'][ch_str],
                                'mask_ch': None,
                                'dir_mk': None}
                dict_setup = {}
                for cont in ['tiss', 'ext', 'int']: 
                    dict_setup[cont] = {'color': mH_settings['color_chs'][ch_str][cont], 
                                        'keep_largest' : False, 
                                        'measure': {'whole' : {}}}
                    mH_meas_keys.append((ch_str,cont,'whole'))
                    
                mH_set[ch_str] = {}
                mH_set[ch_str]['general_info'] = dict_info_ch
                mH_set[ch_str]['setup'] = dict_setup
                mH_channels.append(ch_str)
    
            if mH_settings['ns']['layer_btw_chs']:
                ch_str = 'chNS'
                mH_set['chNS']={}
                mH_set['chNS']['general_info']={'mH_chName':ch_str,
                                                'user_chName':mH_settings['ns']['user_nsChName'].replace(' ', '_'),
                                                'ch_ext': mH_settings['ns']['ch_ext'],
                                                'ch_int': mH_settings['ns']['ch_int']}
                dict_setupNS = {}
                for cont in ['tiss', 'ext', 'int']: 
                    dict_setupNS[cont] = {'color': mH_settings['ns']['color_chns'][cont], 
                                        'keep_largest' : False, 
                                        'measure': {'whole' : {}}}
                    mH_meas_keys.append((ch_str,cont,'whole'))
                
                mH_set[ch_str]['setup'] = dict_setupNS
                mH_channels.append(ch_str)
    
            if mH_settings['segments']['cutLayersIn2Segments']:
                for ch_str in mH_channels:
                    ch_segments = list(mH_settings['segments']['ch_segments'].keys())
                    if ch_str in ch_segments:
                        for s_num in range(0, mH_settings['segments']['no_segments']):
                            segm_str = 'segm'+str(s_num+1)
                            mH_segments.append(segm_str)
                            for cont in mH_settings['segments']['ch_segments'][ch_str]:
                                mH_set[ch_str]['setup'][cont]['measure'][segm_str] = {} 
                                mH_meas_keys.append((ch_str,cont,segm_str))
    
            self.info['dirs'] = {'meshes': 'NotAssigned', 
                                'csv_all': 'NotAssigned',
                                'imgs_videos': 'NotAssigned', 
                                's3_numpy': 'NotAssigned',
                                'centreline': 'NotAssigned',
                                'settings': 'NotAssigned'}
            
        self.mH_settings = mH_set
        self.mH_meas_keys = mH_meas_keys
        self.mH_channels = mH_channels
        segments_new = list(set(mH_segments))
        self.mH_segments = segments_new
        
        self.table2select_mH_meas()

    def set_mC_settings(self, mC_settings:dict): 
        
        mC_set = {}
        mC_channels = []
        mC_segments = []
        
        if self.analysis['morphoCell']:
            for ch_num in range(0, mC_settings['no_chs']):
                ch_str = 'ch'+str(ch_num+1)
                dict_info_ch = {'mH_chName':ch_str,
                                'user_chName':mC_settings['name_chs'][ch_str].replace(' ', '_'),
                                'link2mH':mC_settings['link2mH'][ch_str],
                                'dir_cho': None, 
                                'ch_relation': mC_settings['chs_relation'][ch_str],
                                'color': mC_settings['color_chs'][ch_str]}
                mC_set[ch_str] = {}
                mC_set[ch_str]['general_info'] = dict_info_ch
                mC_channels.append(ch_str)
            
            if mC_settings['segments']['cutLayersIn2Segments']:
                for ch_str in mC_channels:
                    ch_segments = list(mC_settings['segments']['ch_segments'].keys())
                    if ch_str in ch_segments:
                        for s_num in range(0, mC_settings['segments']['no_segments']):
                            segm_str = 'segm'+str(s_num+1)
                            mC_segments.append(segm_str)
                            mC_set[ch_str]['measure'][segm_str] = {} 
                            
            if self.info['dirs'] == []:
                self.info['dirs'] = {'csv_all': 'NotAssigned',
                                    'imgs_videos': 'NotAssigned',
                                    'settings': 'NotAssigned'}
            else: 
                print('>> proj.info[dirs] had already been created!')
        
        
        self.mC_settings = mC_set
        self.mC_channels = mC_channels.sort()
        self.mC_segments = mC_segments.sort()
        
        self.table2select_mC_meas()

    def table2select_mH_meas(self):
        '''
        This function will create a dictionary with all the possible measurement parameters 
        a user can get based on the settings given when setting the initial project 
        (no_ch, no_segments and the corresponding channels from which the segments will 
        be obtained, etc)
        The output of this function (dictionary with default parameters and list)
        will help to set up the GUI table for the user to select the parameters to measure. 
        '''
        channels = self.mH_channels
        conts = ['tiss', 'int', 'ext']
        mH_param2meas = []
        dict_params_deflt = {}
        
        for ch_b in channels: 
            dict_params_deflt[ch_b] = {}
            for cont_b in conts: 
                dict_params_deflt[ch_b][cont_b] = {}

        for tup in self.mH_meas_keys:
            ch, cont, segm = tup
            dict_params_deflt[ch][cont][segm] = {'volume': True, 
                                                    'surf_area': False}

            mH_param2meas.append((ch,cont,segm,'volume'))
            mH_param2meas.append((ch,cont,segm,'surf_area'))

            if cont in ['int', 'ext']:
                dict_params_deflt[ch][cont][segm]['surf_area'] = True 
            if cont == 'tiss':
                if segm == 'whole': 
                    dict_params_deflt[ch][cont][segm]['thickness int>ext'] = True
                    dict_params_deflt[ch][cont][segm]['thickness ext>int'] = False

                    mH_param2meas.append((ch,cont,segm,'thickness int>ext'))
                    mH_param2meas.append((ch,cont,segm,'thickness ext>int'))
                else: 
                    dict_params_deflt[ch][cont][segm]['thickness int>ext'] = False
                    dict_params_deflt[ch][cont][segm]['thickness ext>int'] = False

                    mH_param2meas.append((ch,cont,segm,'thickness int>ext'))
                    mH_param2meas.append((ch,cont,segm,'thickness ext>int'))
            if segm == 'whole' and ch != 'chNS':
                dict_params_deflt[ch][cont][segm]['centreline'] = True
                dict_params_deflt[ch][cont][segm]['centreline_linlength'] = True
                dict_params_deflt[ch][cont][segm]['centreline_looplength'] = True

                mH_param2meas.append((ch,cont,segm,'centreline'))
                mH_param2meas.append((ch,cont,segm,'centreline_linlength'))
                mH_param2meas.append((ch,cont,segm,'centreline_looplength'))

        self.mH_param2meas = mH_param2meas
        #Use this two result variables to create selecting table in the GUI
    
    def table2select_mC_meas(self):
        
        mC_param2meas = []
        self.mC_param2meas = mC_param2meas

    def set_mH_meas(self, user_params2meas:dict, user_ball_settings:dict):
        '''
        This function will get the input of the updated selected parameters from the GUI and 
        will include those measurements in the dictionary of the project. This dictionary will then 
        be used as a workflow template for all the Organs created within the project. 
        '''
        settings_updated = copy.deepcopy(self.mH_settings)
        mH_param2meas = copy.deepcopy(self.mH_param2meas)
        gral_struct = self.mH_meas_keys

        for tup in gral_struct: 
            ch, cont, segm = tup
            settings_updated[ch]['setup'][cont]['measure'][segm] = user_params2meas[ch][cont][segm]

        if user_ball_settings['ballooning']:
            ball_settings = user_ball_settings['ball_settings']
            for key in ball_settings.keys():
                ch = ball_settings[key]['to_mesh']
                cont = ball_settings[key]['to_mesh_type']
                from_cl = ball_settings[key]['from_cl']
                cl_type = ball_settings[key]['from_cl_type']
                settings_updated[ch]['setup'][cont]['measure']['whole']['ballooning']= {'from_cl':from_cl,
                                                                                        'from_cl_type': cl_type}
                mH_param2meas.append((ch,cont,'whole','ballooning'))

                if not settings_updated[from_cl]['setup'][cl_type]['measure']['whole']['centreline']:
                    settings_updated[from_cl]['setup'][cl_type]['measure']['whole']['centreline'] = True
                    settings_updated[from_cl]['setup'][cl_type]['measure']['whole']['centreline_linlength'] = True
                    settings_updated[from_cl]['setup'][cl_type]['measure']['whole']['centreline_looplength'] = True
                    
                if (from_cl,cl_type,'whole','centreline') not in mH_param2meas:
                    mH_param2meas.append((from_cl,cl_type,'whole','centreline'))
                    mH_param2meas.append((from_cl,cl_type,'whole','centreline_linlength'))
                    mH_param2meas.append((from_cl,cl_type,'whole','centreline_looplength'))
                    print('Added ', from_cl, cl_type)
                    
        # Note: Make sure the info being transferred from the dict to the wf is right 
        self.mH_param2meas = mH_param2meas
        self.clean_False(settings_updated=settings_updated)
        delattr(self, 'mH_meas_keys')
        
    def clean_False(self, settings_updated:dict):
        mH_param2meas = copy.deepcopy(self.mH_param2meas)
        mH_param2meas_new = []
        
        for tup in mH_param2meas:
            ch, cont, segm, var = tup
            if not settings_updated[ch]['setup'][cont]['measure'][segm][var]: 
                settings_updated[ch]['setup'][cont]['measure'][segm].pop(var, None)
                # print('deleting: ', ch, cont, segm, var)
            else: 
                mH_param2meas_new.append(tup)
        
        self.mH_settings = settings_updated
        self.mH_param2meas = sorted(mH_param2meas_new)

    def create_proj_dir(self, dir_proj:Path):
        folder_name = 'R_'+self.user_projName
        self.dir_proj = dir_proj / folder_name
        self.dir_proj.mkdir(parents=True, exist_ok=True)
        if self.dir_proj.is_dir():
            self.info['dir_proj'] = self.dir_proj
        else: 
            print('>> Error: Project directory could not be created!\n>> Dir: '+self.dir_proj)
            alert('error_beep')
            
    def set_workflow(self):
        '''
        This function will initialise the dictionary that will contain the workflow of the
        project. This workflow will be assigned to each organ that is part of the created project
        and will be updated in each organ as the user advances in the processing. 
        '''
        workflow = {}
        if self.analysis['morphoHeart']: 
            mH_channels = sorted(self.mH_channels)
            mH_segments = sorted(self.mH_segments)
    
            dict_ImProc = dict()
            dict_ImProc['Status'] = 'NotInitialised'
            dict_MeshesProc = dict()
    
             # Find the meas_param that include the extraction of a centreline
            item_centreline = [item for item in self.mH_param2meas if 'centreline' in item]
            # Find the meas_param that include the extraction of mH_segments
            segm_list = []
            for segm in mH_segments[0:1]:
                segm_list.append([item for item in self.mH_param2meas if segm in item and 'volume' in item])
            # print('segm_list:', segm_list)
            ch_segm = sorted(list(set([tup[0] for tup in segm_list[0]])))
            # print('ch_segm:', ch_segm)
            # item_segment = sorted([item for sublist in segm_list for item in sublist])
            # print(item_segment)
            
            # Find the meas_param that include the extraction of ballooning
            item_ballooning = [item for item in self.mH_param2meas if 'ballooning' in item]
            # Find the meas_param that include the extraction of thickness
            item_thickness_intext = [item for item in self.mH_param2meas if 'thickness int>ext' in item]
            item_thickness_extint = [item for item in self.mH_param2meas if 'thickness ext>int' in item]
    
            dict_MeshesProc = {'Status' : 'NotInitialised',
                               'A-Create3DMesh': {'Status': 'NotInitialised'},
                               'B-TrimMesh': {'Status': 'NotInitialised'},
                               'C-Centreline': {'Status': 'NotInitialised'},
                               'D-Ballooning': {'Status': 'NotInitialised'}, 
                               'D-Thickness_int>ext': {'Status': 'NotInitialised'},
                               'D-Thickness_ext>int': {'Status': 'NotInitialised'},
                               'E-Segments': {'Status': 'NotInitialised'}}
                               
            # Project status
            for ch in mH_channels:
                if 'NS' not in ch:
                    dict_ImProc[ch] = {'Status': 'NotInitialised',
                                        'A-MaskChannel': {'Status': 'NotInitialised'},
                                        'B-CloseCont':{'Status': 'NotInitialised',
                                                        'Steps':{'A-Autom': {'Status': 'NotInitialised'},
                                                                'B-Manual': {'Status': 'NotInitialised'},
                                                                'C-CloseInOut': {'Status': 'NotInitialised'}}},
    
                                        'C-SelectCont':{'Status': 'NotInitialised'},
    
                                        'D-S3Create':{'Status': 'NotInitialised',
                                                    'Info': {'tiss':{'Status': 'NotInitialised'}, 
                                                            'int':{'Status': 'NotInitialised'}, 
                                                            'ext':{'Status': 'NotInitialised'}}}}
                    
                    #Check the external channel
                    if self.mH_settings[ch]['general_info']['ch_relation'] == 'external':
                        dict_ImProc[ch]['E-TrimS3'] = {'Status': 'NotInitialised',
                                                         'Info':{'tiss':{'Status': 'NotInitialised'}, 
                                                                 'int':{'Status': 'NotInitialised'},
                                                                 'ext':{'Status': 'NotInitialised'}}, 
                                                         'Planes':{}}
                    else: 
                        dict_ImProc[ch]['E-CleanCh'] = {'Status': 'NotInitialised',
                                                          'Info': {'tiss':{'Status': 'NotInitialised'}, 
                                                                  'int':{'Status': 'NotInitialised'}, 
                                                                  'ext':{'Status': 'NotInitialised'}}}
                        dict_ImProc[ch]['E-TrimS3'] = {'Status': 'NotInitialised',
                                                         'Info':{'tiss':{'Status': 'NotInitialised'}, 
                                                                 'int':{'Status': 'NotInitialised'},
                                                                 'ext':{'Status': 'NotInitialised'}}, 
                                                         'Planes':{}}
                else: 
                    dict_ImProc[ch] = {'Status': 'NotInitialised',
                                        'D-S3Create':{'Status': 'NotInitialised',
                                                    'Settings':{'ext_mesh': self.mH_settings[ch]['general_info']['ch_ext'],
                                                                'int_mesh': self.mH_settings[ch]['general_info']['ch_int']}}} 
                 
    
                for process in ['A-Create3DMesh','B-TrimMesh','C-Centreline']:
                    if 'NS' not in ch:
                        dict_MeshesProc[process][ch] = {}
                        for cont in ['tiss', 'int', 'ext']:
                            if process == 'A-Create3DMesh':
                                dict_MeshesProc[process][ch][cont] = {'Status': 'NotInitialised'}
                                # dict_MeshesProc[process][ch][cont]['stack_dir'] = None
                                # if cont == 'tiss':
                                #     dict_MeshesProc[process][ch][cont]['keep_largest'] = False
                                # else: 
                                #     dict_MeshesProc[process][ch][cont]['keep_largest'] = None
                            if process == 'B-TrimMesh':
                                dict_MeshesProc[process][ch][cont] = {'Status': 'NotInitialised'}
                                # dict_MeshesProc[process][ch][cont]['stack_dir'] = None
                                # if cont == 'tiss':
                                #     dict_MeshesProc[process][ch][cont]['keep_largest'] = False
                                # else: 
                                #     dict_MeshesProc[process][ch][cont]['keep_largest'] = None
                            
                            if process == 'C-Centreline':
                                if (ch,cont,'whole','centreline') in item_centreline:
                                    dict_MeshesProc[process][ch][cont] = {'Status': 'NotInitialised',
                                                                           'dir_cleanMesh': None, 
                                                                           'dir_meshLabMesh': None, 
                                                                           'vmtk_cl': {'Status': 'NotInitialised',
                                                                                       'vmtktxt': 'NotInitialised'},
                                                                           'connect_cl': {'Status': 'NotInitialised',
                                                                                       'Settings': 'NotInitialised'},
                                                                           'measure':{'Status': 'NotInitialised',
                                                                                       'parameters': []}}
                    else: 
                        if process == 'A-Create3DMesh':
                            dict_MeshesProc[process][ch] = {'Status': 'NotInitialised', 
                                                            'keep_largest': False}
    
                for cont in ['tiss', 'int', 'ext']:
                    if (ch,cont,'whole','ballooning') in item_ballooning:
                        dict_MeshesProc['D-Ballooning'][ch] = {}
                        from_cl = self.mH_settings[ch]['setup'][cont]['measure']['whole']['ballooning']['from_cl']
                        from_cl_type = self.mH_settings[ch]['setup'][cont]['measure']['whole']['ballooning']['from_cl_type']
                        dict_MeshesProc['D-Ballooning'][ch][cont] =  {'Status': 'NotInitialised',
                                                                       'Settings': {'from_cl': from_cl, 
                                                                                   'from_cl_type': from_cl_type}}
    
                    if (ch,cont,'whole','thickness int>ext') in item_thickness_intext:
                        dict_MeshesProc['D-Thickness_int>ext'][ch] = {}
                        dict_MeshesProc['D-Thickness_int>ext'][ch][cont] = {'Status': 'NotInitialised',
                                                                     'Parameters': {'actual_values' : {'min_val': None,
                                                                                                     'max_val': None}}}    
                    if (ch,cont,'whole','thickness ext>int') in item_thickness_extint:
                         dict_MeshesProc['D-Thickness_ext>int'][ch] = {}
                         dict_MeshesProc['D-Thickness_ext>int'][ch][cont] = {'Status': 'NotInitialised',
                                                                     'Parameters': {'actual_values' : {'min_val': None,
                                                                                                 'max_val': None}}}                                                       
            # Project status
            for ch in ch_segm:
                dict_MeshesProc['E-Segments'][ch] = {}
                for cont in ['tiss', 'int', 'ext']:
                    if (ch, cont,'segm1','volume') in segm_list[0]:
                        dict_MeshesProc['E-Segments'][ch][cont] = {'Status': 'NotInitialised',
                                                                   'Segments': {}}
                        for segm in ['whole']+mH_segments:
                            dict_MeshesProc['E-Segments'][ch][cont]['Segments'][segm]={'Status': 'NotInitialised',
                                                                                        'measure': {'Status': 'NotInitialised',
                                                                                                    'parameters': []}}
            workflow['ImProc'] = dict_ImProc
            workflow['MeshesProc'] = dict_MeshesProc
        
        if self.analysis['morphoCell']:
            
            dict_cell = {}
            workflow['CellProc'] = dict_cell
            
        self.workflow = workflow

    def save_project(self):
        #Create a new dictionary that contains all the settings
        jsonDict_name = 'mH_'+self.user_projName+'_project.json'
        json2save_par = self.dir_proj / 'settings'
        json2save_par.mkdir(parents=True, exist_ok=True)
        
        self.dir_info = self.dir_proj / 'settings' / jsonDict_name
        self.info['dir_info'] = self.dir_info
        
        all_info = {}
        all_info['info'] = self.info
        all_info['analysis'] = self.analysis
        all_info['mH_settings'] = self.mH_settings
        all_info['mH_channels'] = self.mH_channels
        all_info['mH_segments'] = self.mH_segments
        all_info['mH_param2meas'] = self.mH_param2meas
        
        all_info['mC_settings'] = self.mC_settings
        all_info['mC_channels'] = self.mC_channels
        all_info['mC_segments'] = self.mC_segments
        all_info['mC_param2meas'] = self.mC_param2meas
        
        all_info['workflow'] = self.workflow
        all_info['organs'] = self.organs
        all_info['cellGroups'] = self.cellGroups
        
        if not json2save_par.is_dir():
            print('>> Error: Settings directory could not be created!\n>> Directory: '+jsonDict_name)
            alert('error_beep')
        else: 
            json2save_dir = json2save_par / jsonDict_name
            with open(str(json2save_dir), "w") as write_file:
                json.dump(all_info, write_file, cls=NumpyArrayEncoder)

            if not json2save_dir.is_file():
                print('>> Error: Project settings file was not saved correctly!\n>> File: '+jsonDict_name)
                alert('error_beep')
            else: 
                print('>> Project settings file saved correctly!\n>> File: '+jsonDict_name)
                print('>> File: '+ str(json2save_dir)+'\n')
                alert('countdown')
        
    
    def add_organ(self, organ):
        dict_organ = copy.deepcopy(organ.info)
        dict_organ.pop('project', None)
        dict_organ['dir_res'] = organ.dir_res
        
        self.organs[organ.user_organName] = dict_organ
        self.save_project()

    def remove_organ(self, organ):
        organs = copy.deepcopy(self.organs)
        organs.pop(organ.user_organName, None)
        self.organs = organs
        self.save_project()

    def load_organ(self, user_organName:str):
        dir_res = self.organs[user_organName]['dir_res']
        jsonDict_name = 'mH_'+self.organs[user_organName]['user_organName']+'_organ.json'
        json2open_dir = Path(dir_res) / 'settings' / jsonDict_name
        if json2open_dir.is_file():
            with open(json2open_dir, "r") as read_file:
                print(">> "+jsonDict_name+": Opening JSON encoded data")
                dict_out = json.load(read_file)
            organ = Organ(project=self, user_settings={}, info_loadCh={}, 
                            new=False, load_dict=dict_out)
        else: 
            organ = None
            print('>> Error: No organ name with name ',user_organName,' was found!\n Directory: ',str(json2open_dir))
            alert('error_beep')
            
        return organ

class Organ():
    'Organ Class'
    
    def __init__(self, project:Project, user_settings:dict, info_loadCh:dict, new=True, load_dict={}):
        
        self.parent_project = project
        
        if new:
            self.user_organName = user_settings['user_organName'].replace(' ', '_')
            self.info = user_settings
            self.info['dirs'] = project.info['dirs']
            self.info_loadCh = info_loadCh
            self.create_mHName()
            self.analysis = copy.deepcopy(project.analysis)
            if self.analysis['morphoHeart']:
                self.mH_settings = copy.deepcopy(project.mH_settings)
                self.imChannels = {}
                self.obj_imChannels = {}
                self.imChannelNS = {}
                self.obj_imChannelNS = {}
                self.meshes = {}
                self.obj_meshes = {}
                self.objects = {}
            if self.analysis['morphoCell']:
                self.mC_settings = copy.deepcopy(project.mC_settings)
            self.workflow = copy.deepcopy(project.workflow)
        else: 
            self.load_organ(load_dict=load_dict)
        
        self.check_channels(project)

    def load_organ(self, load_dict:dict):
        
        load_dict = make_Paths(load_dict)
        
        # user_settings = dict_out['Organ']
        self.info = load_dict['Organ']
        self.user_organName = self.info['user_organName'].replace(' ', '_')
        # info_loadCh = dict_out['info_loadCh']
        self.info_loadCh = load_dict['info_loadCh']
        self.analysis = load_dict['analysis']
        
        tuple_keys = [['mH_settings','chNS','general_info','ch_ext'],
                      ['mH_settings','chNS','general_info','ch_int'], 
                      ['workflow','ImProc','chNS','D-S3Create','Settings','ext_mesh'], 
                      ['workflow','ImProc','chNS','D-S3Create','Settings','int_mesh']]
        
        for ch in load_dict['imChannels'].keys():
            tuple_keys.append(['imChannels', ch, 'shape'])
            tuple_keys.append(['imChannels', ch, 'shape_s3'])
            for cont in load_dict['imChannels'][ch]['contStack'].keys():
                tuple_keys.append(['imChannels', ch, 'contStack',cont,'shape_s3'])
        
        load_dict = make_tuples(load_dict, tuple_keys)
     
        self.objects = load_dict['objects']
        if self.analysis['morphoHeart']:
            # mH_Settings
            self.mH_settings = load_dict['mH_settings']
            # imChannels
            self.imChannels = load_dict['imChannels']
            self.load_objImChannels()
            # imChannelNS
            self.imChannelNS = load_dict['imChannelNS']
            self.load_objImChannelNS()
            # meshes
            self.meshes = load_dict['meshes']
            self.load_objMeshes()
            
        if self.analysis['morphoCell']:
            # mC_Settings
            self.mC_settings = load_dict['mC_settings']
        # Workflow
        self.workflow = load_dict['workflow']
       
        self.dir_info = Path(load_dict['dir_info'])
        self.mH_organName = load_dict['mH_organName']
        
    def load_objImChannels(self):
        self.obj_imChannels = {}
        if len(self.imChannels) > 0:
            for imCh in self.imChannels:
                im_ch = ImChannel(organ=self, ch_name=imCh, new=False)
                self.obj_imChannels[imCh] = im_ch
        
    def load_objImChannelNS(self):
        self.obj_imChannelNS = {}
        if len(self.imChannelNS) > 0: 
            for imCh in self.imChannelNS:
                im_ch = ImChannelNS(organ=self, ch_name=imCh, new=False)
                self.obj_imChannelNS[imCh] = im_ch
        
    def load_objMeshes(self):
        self.obj_meshes = {}
        if len(self.meshes) > 0: 
            for mesh in self.meshes:
                ch_no = self.meshes[mesh]['channel_no']
                if 'NS' in mesh: 
                    imCh = self.obj_imChannelNS[ch_no]
                else: 
                    imCh = self.obj_imChannels[ch_no]
                mesh_type = self.meshes[mesh]['mesh_type']
                keep_largest = self.meshes[mesh]['keep_largest']
                rotateZ_90 = self.meshes[mesh]['rotateZ_90'] 
                msh = Mesh_mH(imChannel = imCh, mesh_type = mesh_type, 
                              keep_largest = keep_largest, rotateZ_90 = rotateZ_90,
                              new = False)
                self.obj_meshes[mesh] = msh

    def create_mHName(self):
        now_str = datetime.now().strftime('%Y%m%d%H%M')
        self.mH_organName = 'mH_Organ-'+now_str
                 
    def check_channels(self, project:Project):
        info_loadCh = self.info_loadCh
        chs = [x for x in project.mH_channels if x != 'chNS']    
        array_sizes = {}
        sizes = []
        for ch in chs:
            try:
                images_o = io.imread(str(info_loadCh[ch]['dir_cho']))
                array_sizes[ch]= {'cho': images_o.shape}
                sizes.append(images_o.shape)
            except: 
                print('>> Error: Something went wrong opening the file -',ch)
                alert('error_beep')
            
            if info_loadCh[ch]['mask_ch']:
                try:
                    images_mk = io.imread(str(info_loadCh[ch]['dir_mk']))
                    array_sizes[ch]['mask']= images_mk.shape
                    sizes.append(images_mk.shape)
                except: 
                    print('>> Error: Something went wrong opening the mask -',ch)
                    alert('error_beep')
            
        unique_size = list(set(sizes))
        if len(unique_size) != 1: 
            counter = collections.defaultdict(int)
            for elem in unique_size:
                counter[elem] += 1
            print('>> Error: Dimensions of imported images do not match! Please check! \n Imported Data: ')
            pprint.pprint(array_sizes)
            alert('error_beep')
        
        else:      
            for ch in chs:
                for param in ['dir_cho','mask_ch','dir_mk']:
                    self.mH_settings[ch]['general_info'][param] = info_loadCh[ch][param]
            # print('>> Files have been checked! \n>> Images shape:')
            # pprint.pprint(array_sizes)

        self.create_folders()

    def create_folders(self):
        dirResults = ['meshes', 'csv_all', 'imgs_videos', 's3_numpy', 'centreline', 'settings']
        organ_folder = self.user_organName
        for direc in dirResults:
            dir2create = self.parent_project.dir_proj / organ_folder / direc
            dir2create.mkdir(parents=True, exist_ok=True)
            if dir2create.is_dir():
                self.info['dirs'][direc] = dir2create
            else: 
                print('Error: Directory ', self.user_organName, '/', direc, ' could not be created!')
                alert('error_beep')
        self.dir_res = self.parent_project.dir_proj / organ_folder

    def add_channel(self, imChannel):
        # Check first if the channel has been already added to the organ
        new = False
        if imChannel.channel_no not in self.imChannels.keys():
            new = True
            
        if new: 
            print('adding Channel')
            channel_dict = {}
            channel_dict['parent_organ_name'] = imChannel.parent_organ_name
            channel_dict['channel_no'] = imChannel.channel_no
            channel_dict['user_chName'] = imChannel.user_chName
            channel_dict['ch_relation'] = imChannel.ch_relation
            channel_dict['to_mask'] = imChannel.to_mask
            channel_dict['resolution'] = imChannel.resolution
            channel_dict['dir_cho'] = imChannel.dir_cho
            if imChannel.to_mask:
                channel_dict['dir_mk'] = imChannel.dir_mk
            channel_dict['masked'] = imChannel.masked
            channel_dict['shape'] = imChannel.shape
            channel_dict['process'] = imChannel.process
            channel_dict['contStack'] = imChannel.contStack
            channel_dict['dir_stckproc'] = imChannel.dir_stckproc
            
            self.imChannels[imChannel.channel_no] = channel_dict
            
        else: # just update im_proc 
            self.imChannels[imChannel.channel_no]['process'] = imChannel.process
            self.imChannels[imChannel.channel_no]['contStack'] = imChannel.contStack
            if imChannel.dir_stckproc.is_file():
                self.imChannels[imChannel.channel_no]['dir_stckproc'] = imChannel.dir_stckproc
            if hasattr(imChannel, 'shape_s3'):
                self.imChannels[imChannel.channel_no]['shape_s3'] = imChannel.shape_s3
        self.obj_imChannels[imChannel.channel_no] = imChannel
        
    def add_channelNS(self, imChannelNS):
        # Check first if the channel has been already added to the organ
        new = False
        if imChannelNS.channel_no not in self.imChannelNS.keys():
            new = True
            
        if new: 
            print('adding ChannelNS')
            channel_dict = {}
            channel_dict['parent_organ_name'] = imChannelNS.parent_organ_name
            channel_dict['channel_no'] = imChannelNS.channel_no
            channel_dict['user_chName'] = imChannelNS.user_chName
            channel_dict['ch_relation'] = imChannelNS.ch_relation
            channel_dict['resolution'] = imChannelNS.resolution
            channel_dict['process'] = imChannelNS.process
            channel_dict['contStack'] = imChannelNS.contStack
            channel_dict['setup'] = imChannelNS.setup
            self.imChannelNS[imChannelNS.channel_no] = channel_dict
            
        else: # just update im_proc 
            self.imChannelNS[imChannelNS.channel_no]['process'] = imChannelNS.process
            self.imChannelNS[imChannelNS.channel_no]['contStack'] = imChannelNS.contStack
           
        self.obj_imChannelNS[imChannelNS.channel_no] = imChannelNS

    def add_mesh(self, mesh): # mesh: Mesh_mH
        new = False
        if mesh.name not in self.meshes.keys():
            new = True
            print('New mesh!')
        if new: 
            self.meshes[mesh.name] = {}
            self.meshes[mesh.name]['parent_organ'] = mesh.parent_organ.user_organName
            self.meshes[mesh.name]['channel_no'] = mesh.imChannel.channel_no
            self.meshes[mesh.name]['user_meshName'] = mesh.user_meshName
            self.meshes[mesh.name]['mesh_type'] = mesh.mesh_type
            self.meshes[mesh.name]['legend'] = mesh.legend
            self.meshes[mesh.name]['name'] = mesh.name
            self.meshes[mesh.name]['resolution'] = mesh.resolution
            self.meshes[mesh.name]['color'] = mesh.color
            self.meshes[mesh.name]['alpha'] = mesh.alpha
            self.meshes[mesh.name]['keep_largest'] = mesh.keep_largest
            self.meshes[mesh.name]['rotateZ_90'] = mesh.rotateZ_90
            if hasattr(mesh,'dir_out'):
                self.meshes[mesh.name]['dir_out'] = mesh.dir_out
        self.obj_meshes[mesh.name] = mesh

    def load_TIFF(self, ch_name:str):
        print('---- Loading TIFF! ----')
        image = ImChannel(organ=self, ch_name=ch_name)
        return image

    def save_organ(self):
        all_info = {}
        all_info['Organ'] = self.info
        all_info['info_loadCh'] = self.info_loadCh
        all_info['analysis'] = self.analysis
        
        jsonDict_name = 'mH_'+self.user_organName+'_organ.json'
        json2save_dir = self.info['dirs']['settings'] / jsonDict_name
        if self.analysis['morphoHeart']:
            all_info['mH_settings'] = self.mH_settings
            
            image_dict = copy.deepcopy(self.imChannels)
            for ch in image_dict.keys():
                image_dict[ch].pop('parent_organ', None)
            all_info['imChannels'] = image_dict
            
            imageNS_dict = copy.deepcopy(self.imChannelNS)
            for chNS in imageNS_dict.keys():
                imageNS_dict[chNS].pop('parent_organ', None)
            all_info['imChannelNS'] = imageNS_dict

            all_info['meshes'] = self.meshes
            all_info['objects'] = self.objects
            
        if self.analysis['morphoCell']:
            all_info['mC_settings'] = self.mC_settings
        
        all_info['workflow'] = self.workflow
    
        self.dir_info = self.dir_res / 'settings' / jsonDict_name
        all_info['dir_info'] = self.dir_info
        all_info['mH_organName'] = self.mH_organName

        with open(str(json2save_dir), "w") as write_file:
            json.dump(all_info, write_file, cls=NumpyArrayEncoder)

        if not json2save_dir.is_file():
            print('>> Error: Organ settings file was not saved correctly!\n>> File: '+jsonDict_name)
            alert('error_beep')
        else: 
            print('\n>> Organ settings file saved correctly! - '+jsonDict_name)
            #print('>> Directory: '+ str(json2save_dir)+'\n')
            alert('countdown')
            

    def check_status(self, process:str):
 
        if process=='ImProc':
            ch_done = []
            for ch in self.imChannels.keys():
                # First check close contours
                close_done = []
                for key_a in ['A-Autom', 'B-Manual', 'C-CloseInOut']:
                    close_done.append(self.workflow[process][ch]['B-CloseCont']['Steps'][key_a]['Status'])
                print('channel:',ch, '-CloseCont:', close_done)
                if all(flag == 'DONE' for flag in close_done):
                    self.workflow[process][ch]['B-CloseCont']['Status'] = 'DONE'

                # Now update all the workflow
                proc_done = []
                for key_b in self.workflow[process][ch].keys():
                    if key_b != 'Status':
                        proc_done.append(self.workflow[process][ch][key_b]['Status'])
                print('channel:',ch, '-ImProc:', proc_done)
                if all(flag == 'DONE' for flag in proc_done):
                    self.workflow[process][ch]['Status'] = 'DONE'
                ch_done.append(self.workflow[process][ch]['Status'])
            
            if all(flag == 'DONE' for flag in ch_done):
                self.workflow[process]['Status'] = 'DONE'

    def update_workflow(self, process, update):
        workflow = self.workflow
        set_by_path(workflow, process, update)
    
    #Get all the set mH variables in __init__
    def get_notes(self):
        
        return self.info['user_organNotes']

    def get_orientation(self):
        return self.info['im_orientation']

    def get_custom_angle(self):
        return self.info['custom_angle']
    
    def get_resolution(self):
        return self.info['resolution']

    def get_units_resolution(self):
        return self.info['units_resolution']

    def get_stage(self):
        return self.info['stage']

    def get_strain(self):
        return self.info['strain']

    def get_genotype(self):
        return self.info['genotype']

    def get_dir_res(self):
        return self.dir_res

    def get_direc(self, name:str):
        return self.info['dirs'][name]

class ImChannel(): #channel
    'morphoHeart Image Channel Class (this class will be used to contain the images as tiffs that have been'
    'closed and the resulting s3s that come up from each channel'
    
    def __init__(self, organ:Organ, ch_name:str, new=True):

        self.parent_organ = organ
        self.parent_organ_name = organ.user_organName
        self.channel_no = ch_name
        self.user_chName = organ.mH_settings[ch_name]['general_info']['user_chName']
        self.ch_relation = organ.mH_settings[ch_name]['general_info']['ch_relation']
        if new:       
            self.new_ImChannel()
        else: 
            self.load_channel()

    def new_ImChannel(self):
        organ = self.parent_organ
        ch_name = self.channel_no
        
        self.to_mask = organ.mH_settings[ch_name]['general_info']['mask_ch']
        self.resolution = organ.info['resolution']
        self.dir_cho = organ.mH_settings[ch_name]['general_info']['dir_cho']            
        if self.to_mask:
            self.dir_mk = organ.mH_settings[ch_name]['general_info']['dir_mk']
        self.masked = False
        self.shape = self.im().shape
        self.process = ['Init']
        self.contStack = {}
        self.save_channel(im_proc=self.im_proc())
        organ.add_channel(imChannel=self)
        organ.save_organ()
        
    def im(self):
        im = io.imread(str(self.dir_cho))
        if not isinstance(im, np.ndarray):
            print('>> Error: morphoHeart was unable to load tiff.\n>> Directory: ',str(self.dir_cho))
            alert('error_beep')
        return im
    
    def im_proc(self, new=True):
        if new: 
            im_proc =  np.copy(self.im())  
        else: 
            if hasattr(self, 'dir_stckproc'):
                im_proc = io.imread(str(self.dir_stckproc))
                if not isinstance(im_proc, np.ndarray):
                    print('>> Error: morphoHeart was unable to load processed tiff.\n>> Directory: ',str(self.dir_stckproc))
                    alert('error_beep')
            else: 
                im_proc =  np.copy(self.im())      
        return im_proc
        
    def load_channel(self):
        organ = self.parent_organ
        ch_name = self.channel_no
        
        self.to_mask = organ.imChannels[ch_name]['to_mask']
        self.resolution = organ.imChannels[ch_name]['resolution']
        self.dir_cho = Path(organ.imChannels[ch_name]['dir_cho'])
        if self.to_mask:
                self.dir_mk = Path(organ.imChannels[ch_name]['dir_mk'])
        self.masked = organ.imChannels[ch_name]['masked']
        self.shape = tuple(organ.imChannels[ch_name]['shape'])
        if 'shape_s3' in organ.imChannels[ch_name].keys():
            self.shape_s3 = tuple(organ.imChannels[ch_name]['shape_s3'])
        self.process = organ.imChannels[ch_name]['process']
        contStack_dict = organ.imChannels[ch_name]['contStack']
        for cont in contStack_dict.keys():
            contStack_dict[cont]['s3_dir'] = Path(contStack_dict[cont]['s3_dir'])
        self.contStack = contStack_dict
        self.dir_stckproc = organ.imChannels[ch_name]['dir_stckproc']

    def get_channel_no(self):
        return self.channel_no

    def get_resolution(self):
        return self.resolution

    def get_shape(self):
        return self.shape
    
    def add_contStack(self, contStack):
        # Check first if the contStack has been already added to the channel
        new = False
        if contStack.cont_type not in self.contStack.keys():
            new = True
            
        if new: 
            contStack_dict = copy.deepcopy(contStack.__dict__)
            contStack_dict.pop('im_channel', None)
            self.contStack[contStack.cont_type] = contStack_dict
        else: # just update im_proc 
            self.contStack[contStack.cont_type]['process'] = contStack.process
     
    def maskIm(self):
        #Check workflow status
        workflow = self.parent_organ.workflow
        process = ['ImProc', self.channel_no, 'A-MaskChannel','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE':
            q = 'You already masked this channel ('+ self.user_chName+'). Do you want to re-run it?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
                
        if proceed: 
            #Load images
            im_o = np.copy(self.im())
            im_mask = io.imread(str(self.dir_mk))
            #Process
            print('---- Masking! ----')
            if self.shape == im_mask.shape:
                #Check the dimensions of the mask with those of the image
                im_o[im_mask == False] = 0
                self.masked = True
                self.save_channel(im_proc=im_o)
                
                #Update organ workflow
                self.parent_organ.update_workflow(process, update = 'DONE')
                
                #self.parent_organ.workflow['ImProc'][self.channel_no]['A-MaskChannel']['Status'] = 'DONE'
                process_up = ['ImProc', self.channel_no,'Status']
                if get_by_path(workflow, process_up) == 'NotInitialised':
                    self.parent_organ.update_workflow(process_up, update = 'Initialised')
                
                #Update channel process
                self.process.append('Masked')
                
                #Update organ imChannels
                self.parent_organ.imChannels[self.channel_no]['masked'] = True
                self.parent_organ.add_channel(self)
                self.parent_organ.save_organ()
                
            else: 
                print('>> Error: Stack could not be masked (stack shapes did not match).')
                alert('error_beep')
                
            process_up2 = ['ImProc','Status']
            if get_by_path(workflow, process_up2) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up2, update = 'Initialised')
            
    def closeContours_auto(self):
        #Check workflow status
        workflow = self.parent_organ.workflow
        process = ['ImProc', self.channel_no,'B-CloseCont','Steps','A-Autom','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE':
            q = 'You already closed automatically the contours of this channel ('+ self.user_chName+'). Do you want to re-run it?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
                
        if proceed: 
            # Load image
            im_proc = self.im_proc()
            self.save_channel(im_proc=im_proc)
            workflow = self.parent_organ.workflow
            
            #Process
            print('---- Closing Contours Auto! ----')
            
            #Update organ workflow
            self.parent_organ.update_workflow(process, update = 'DONE')

            process_up = ['ImProc',self.channel_no,'B-CloseCont','Status']
            if get_by_path(workflow, process_up) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up, update = 'Initialised')
            
            #Update channel process
            self.process.append('ClosedCont-Auto')
            
            #Update organ imChannels
            self.parent_organ.add_channel(self)
            self.parent_organ.save_organ()
            
            process_up2 = ['ImProc','Status']
            if get_by_path(workflow, process_up2) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up2, update = 'Initialised')
                
            #Update
            # 'B-CloseCont':{'Status': 'NotInitialised',
            #                 'Steps':{'A-Autom': {'Status': 'NotInitialised'},
            #                                     # 'Range': None, 
            #                                     # 'Range_completed': None}, 
        
    def closeContours_manual(self):
        #Check workflow status
        workflow = self.parent_organ.workflow
        process = ['ImProc', self.channel_no,'B-CloseCont','Steps','B-Manual','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE':
            q = 'You already finished closing manually the contours of this channel ('+ self.user_chName+'). Do you want to re-run this process and close some more?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
                
        if proceed: 
            # Load image
            im_proc = self.im_proc()
            self.save_channel(im_proc=im_proc)
            
            #Process
            print('---- Closing Contours Manually! ----')
            
                    
            #Update organ workflow
            self.parent_organ.update_workflow(process, update = 'DONE')
            
            process_up = ['ImProc',self.channel_no,'B-CloseCont','Status']
            if get_by_path(workflow, process_up) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up, update = 'Initialised')
            
            
            #Update channel process
            self.process.append('ClosedCont-Manual')
                    
            #Update organ imChannels
            self.parent_organ.add_channel(self)
            self.parent_organ.save_organ()
            
            process_up2 = ['ImProc','Status']
            if get_by_path(workflow, process_up2) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up2, update = 'Initialised')
            
            #Update
            # 'B-CloseCont':{'Status': 'NotInitialised',
            #                         'B-Manual': {'Status': 'NotInitialised'},
            #                                     # 'Range': None, 
            #                                     # 'Range_completed': None}, 
            
    def closeInfOutf(self):
        #Check workflow status
        workflow = self.parent_organ.workflow
        process = ['ImProc', self.channel_no,'B-CloseCont','Steps','C-CloseInOut','Status']
        check_proc = get_by_path(workflow, process)
        if dict_gui['heart_default']:
            txt_pr = 'inflow/outflow'
        else: 
            txt_pr = 'bottom/top'
        if check_proc == 'DONE':
            q = 'You already closed the '+txt_pr+' contours of this channel ('+ self.user_chName+'). Do you want to re-run this process and close some more?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
                
        if proceed: 
            # Load image
            im_proc = self.im_proc()
            self.save_channel(im_proc=im_proc)
            
            #Process
            print('---- Closing Inf/Ouft! ----')
            
            #Update organ workflow
            self.parent_organ.update_workflow(process, update = 'DONE')
            
            process_up = ['ImProc',self.channel_no,'B-CloseCont','Status']
            if get_by_path(workflow, process_up) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up, update = 'Initialised')
            
            # Update channel process
            self.process.append('ClosedInfOutf')
            
            #Update organ imChannels
            self.parent_organ.add_channel(self)
            
            #TO DO: Update general status of B-CloseCont to Done when confirmed
            self.parent_organ.check_status(process = 'ImProc')
            self.parent_organ.save_organ()
            
            process_up2 = ['ImProc','Status']
            if get_by_path(workflow, process_up2) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up2, update = 'Initialised')
                
            #Update 
            # 'B-CloseCont':{'Status': 'NotInitialised',
            #                         'C-CloseInOut': {'Status': 'NotInitialised'}}},

    def selectContours(self):
        #Check workflow status
        workflow = self.parent_organ.workflow
        process = ['ImProc', self.channel_no,'C-SelectCont','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE':
            q = 'You already selected the contours for this channel ('+ self.user_chName+'). Do you want to re-select them?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
                
        if proceed: 
            # Load image
            im_proc = self.im_proc()
            self.save_channel(im_proc=im_proc)
            
            #Process
            print('---- Selecting Contours! ----')
            
            #Update organ workflow
            self.parent_organ.update_workflow(process, update = 'DONE')

            #Update channel process
            self.process.append('SelectCont')
                    
            #Update organ imChannels
            self.parent_organ.add_channel(self)
            self.parent_organ.save_organ()
            
            process_up2 = ['ImProc','Status']
            if get_by_path(workflow, process_up2) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up2, update = 'Initialised')
                
            #Update
            # 'C-SelectCont':{'Status': 'NotInitialised'},
            #                 # 'Info': {'tuple_slices': None,
            #                 #         'number_contours': None,
            #                 #         'range': None}},

    def create_chS3s (self, layerDict:dict):
        #Check workflow status
        workflow = self.parent_organ.workflow
        process = ['ImProc', self.channel_no, 'D-S3Create','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE':
            q = 'You already created the contour stacks (S3s) of this channel ('+ self.user_chName+'). Do you want to re-create them?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
                
        if proceed: 
            dirs_cont = []; shapes_s3 = []
            for cont in ['int', 'ext', 'tiss']:
                s3 = ContStack(im_channel=self, cont_type=cont, new=True, layerDict=layerDict)
                self.add_contStack(s3)
                dirs_cont.append(s3.s3_dir.is_file())
                shapes_s3.append(s3.shape_s3)
                #Update organ workflow
                process_cont = ['ImProc',self.channel_no,'D-S3Create','Info',cont,'Status']
                self.parent_organ.update_workflow(process_cont, update = 'DONE')
            
            #Update organ workflow
            if all(flag for flag in dirs_cont):
                if shapes_s3.count(shapes_s3[0]) == len(shapes_s3):
                    self.shape_s3 = s3.shape_s3
                else: 
                    print('self.shape_s3 = s3.shape')
                self.parent_organ.update_workflow(process, update = 'DONE')

            #Update channel process
            self.process.append('CreateS3')
            
            #Update organ imChannel
            self.parent_organ.add_channel(self)
            self.parent_organ.save_organ()
            
            process_up2 = ['ImProc','Status']
            if get_by_path(workflow, process_up2) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up2, update = 'Initialised')
            
    def load_chS3s (self, cont_types:list):
        for cont in ['int', 'ext', 'tiss']:
            if cont in cont_types:
                s3 = ContStack(im_channel=self, cont_type=cont, new=False)
                setattr(self, 's3_'+cont, s3)
                self.add_contStack(s3)
        
        #Update channel process
        self.process.append('LoadS3')
        
        #Update organ imChannel
        self.parent_organ.add_channel(self)
        self.parent_organ.save_organ()

    def trimS3(self, cuts, cuts_out): 
        #Check workflow status
        workflow = self.parent_organ.workflow
        process = ['ImProc', self.channel_no, 'E-TrimS3','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE':
            q = 'You already masked this channel ('+ self.user_chName+'). Do you want to re-run it?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
                
        if proceed: 
            #Load s3s
            self.load_chS3s(cont_types=['int', 'ext', 'tiss'])
            
            #Process
            print('---- Trimming S3s! ----')                             
            if len(cuts) == 1:
                pl = cuts_out[cuts[0]]['plane_info_image']
                plm = cuts_out[cuts[0]]['plane_info_mesh']
                for s3 in [self.s3_int, self.s3_ext, self.s3_tiss]:
                    s3.cutW1Plane(pl, cuts[0])
                    process_cont = ['ImProc',self.channel_no,'E-TrimS3','Info',s3.cont_type,'Status']
                    self.parent_organ.update_workflow(process_cont, update = 'DONE')
                    planes_up = ['ImProc',self.channel_no,'E-TrimS3','Planes',cuts[0]]
                    self.parent_organ.update_workflow(planes_up, update = {'cut_image' : pl,'cut_mesh' : plm})
                    
            if len(cuts) == 2:
                for s3 in [self.s3_int, self.s3_ext, self.s3_tiss]:
                    pl1 = cuts_out['bottom']['plane_info_image']
                    pl1m = cuts_out['bottom']['plane_info_mesh']
                    pl2 = cuts_out['top']['plane_info_image']
                    pl2m = cuts_out['top']['plane_info_mesh']
                    s3.cutW2Planes(pl1, pl2)
                    process_cont = ['ImProc',self.channel_no,'E-TrimS3','Info',s3.cont_type,'Status']
                    self.parent_organ.update_workflow(process_cont, update = 'DONE')
                    planes_bot = ['ImProc',self.channel_no,'E-TrimS3','Planes','bottom']
                    self.parent_organ.update_workflow(planes_bot, update = {'cut_image' : pl1,'cut_mesh' : pl1m})
                    planes_top = ['ImProc',self.channel_no,'E-TrimS3','Planes','top']
                    self.parent_organ.update_workflow(planes_top, update = {'cut_image' : pl2,'cut_mesh' : pl2m})
            
            #Update organ workflow 
            self.parent_organ.update_workflow(process, update = 'DONE')
            
            #Update channel process
            self.process.append('TrimS3')
            
            #Update organ imChannels
            self.parent_organ.add_channel(self)
            
            process_up2 = ['ImProc','Status']
            if get_by_path(workflow, process_up2) == 'NotInitialised':
                self.parent_organ.update_workflow(process_up2, update = 'Initialised')
            
            # Save organ
            self.parent_organ.save_organ()
            # Update status 
            self.parent_organ.check_status(process = 'ImProc')
        
    def s32Meshes(self, cont_types:list, keep_largest, rotateZ_90, new):
        
        meshes_out = []
        for mesh_type in ['int', 'ext', 'tiss']:
            # if not new: 
            #     keep_largest = workflow['MeshesProc']['A-Create3DMesh'][self.channel_no]['mesh_type']
            mesh = Mesh_mH(self, mesh_type, keep_largest[mesh_type], rotateZ_90, new)
            meshes_out.append(mesh)
            
        return meshes_out
    
    def createNewMeshes(self, keep_largest:dict, process:str, rotateZ_90:bool, new:bool):
        
        workflow = self.parent_organ.workflow
        ch_no = self.channel_no
        meshes_out = self.s32Meshes(keep_largest, rotateZ_90, new)
        if process == 'AfterTrimming':
            for mesh_type in ['int', 'ext', 'tiss']:
                workflow['MeshesProc']['B-TrimMesh'][ch_no][mesh_type]['Status'] = 'DONE'
                workflow['MeshesProc']['B-TrimMesh'][ch_no][mesh_type]['stack_dir'] = self.contStack[mesh_type]['s3_dir']
                workflow['MeshesProc']['B-TrimMesh'][ch_no][mesh_type]['keep_largest'] = keep_largest[mesh_type]
                # workflow['MeshesProc']['B-TrimMesh'][ch_no][mesh_type]['trim_settings'] = info[ch_no]
            
                workflow['MeshesProc']['B-TrimMesh'][ch_no]['trim_settings'] = {}
                dict_pl = workflow['ImProc'][ch_no]['E-TrimS3']['Planes']
                workflow['MeshesProc']['B-TrimMesh'][ch_no]['trim_settings'] = dict_pl
                
        # Save organ
        self.parent_organ.save_organ()   
        
        return meshes_out

    def save_channel(self, im_proc):
        im_name = self.parent_organ.user_organName + '_StckProc_' + self.channel_no + '.npy'
        im_dir = self.parent_organ.info['dirs']['s3_numpy'] / im_name
        np.save(im_dir, im_proc)
        if not im_dir.is_file():
            print('>> Error: Processed channel was not saved correctly!\n>> File: '+im_name)
            alert('error_beep')
        else: 
            print('>> Processed channel saved correctly! - ', im_name)
            # print('>> Directory: '+ str(im_dir)+'\n')
            alert('countdown')
            self.dir_stckproc = im_dir
    
    def ch_clean (self, s3_mask, inverted=True, plot=False, im_every=25): 
        """
        Function to clean channel using the other as a mask
        """
        workflow = self.parent_organ.workflow
    
        s3s = [self.s3_int, self.s3_ext, self.s3_tiss]
        if workflow['ImProc'][self.channel_no]['E-CleanCh']['Status'] != 'DONE':
            proceed = True
        else: 
            proceed = ask4input('You had already run this process. Do you want to re-run it?\n\t[0]: no, continue with next step\n\t[1]: yes, re-run it! >>>:', bool)
    
        if proceed: 
            for s3 in s3s:
                print('- Cleaning '+self.user_chName+' ('+ self.channel_no + '-' + s3.cont_type +')')
                    
                # What happens if the s3() are None? 
                s3_s = s3.s3()
                if not isinstance(s3_s, np.ndarray): 
                    print(' not isinstance(s3_s, np.array)')
                    continue
                s3_mask_s = s3_mask.s3()
                if not isinstance(s3_mask_s, np.ndarray): 
                    print('not isinstance(s3_mask_s, np.array)')
                    continue
                s3_bits = np.zeros_like(s3_s, dtype='uint8')
                s3_new =  np.zeros_like(s3_s, dtype='uint8')
        
                index = list(s3.shape_s3).index(min(s3.shape_s3))
                if index == 2:
                    for slc in range(s3.shape_s3[2]):
                        mask_slc = s3_mask_s[:,:,slc]
                        toClean_slc = s3_s[:,:,slc]
        
                        if inverted:
                            # Invert ch to use as mask 
                            inv_slc = np.where((mask_slc==0)|(mask_slc==1), mask_slc^1, mask_slc)
                        else: 
                            # Keep ch to use as mask as it is
                            inv_slc = np.copy(mask_slc)
        
                        # inverted_mask or mask AND ch1_2clean
                        toRemove_slc = np.logical_and(toClean_slc, inv_slc)
                        # Keep only the clean bit
                        cleaned_slc = np.logical_xor(toClean_slc, toRemove_slc)
        
                        if plot and slc in list(range(0,s3.shape_s3[0],im_every)):
                            self.slc_plot(slc, inv_slc, toClean_slc, toRemove_slc, cleaned_slc, inverted)
        
                        s3_bits[:,:,slc] = toRemove_slc
                        s3_new[:,:,slc] = cleaned_slc
                        
                    s3_new = s3_new.astype('uint8')
                    s3.s3_save(s3_new)
                    alert('whistle')   
                    
                else:
                    print('>> Index different to 2, check!')
                    alert('error_beep')
                
                workflow['ImProc'][self.channel_no]['E-CleanCh']['Info'][s3.cont_type]['Status'] = 'DONE'
                workflow['ImProc'][self.channel_no]['E-CleanCh']['Settings'] = {'s3_mask': s3_mask.cont_name, 'inverted': inverted}
                workflow['ImProc'][self.channel_no]['E-CleanCh']['Status'] = 'DONE'
                
                  
    def slc_plot (self, slc, mask_slc, toClean_slc, toRemove_slc, cleaned_slc, inverted):
        """
        Function to plot mask, original image and result
        """
        if self.channel_no != 'chNS':#option == 'clean':
            if inverted: 
                txt = ['ch0_inv','ch1','ch0_inv AND ch1','ch0_inv AND ch1\nxOR ch1']
            else: 
                txt = ['ch0','ch1','ch0 AND ch1','ch0 AND ch1\nxOR ch1']
        else:
            txt = ['ch0_int','ch1_ext','ch0_int AND ch1_ext','layer in between']

        #Plot
        fig, ax = plt.subplots(1, 4, figsize = (10,2.5))
        fig.suptitle("Slice:"+str(slc), y=1.05, weight="semibold")
        ax[0].imshow(mask_slc)
        ax[1].imshow(toClean_slc)
        ax[2].imshow(toRemove_slc)
        ax[3].imshow(cleaned_slc)
        for num in range(0,4,1):
            ax[num].set_title(txt[num])
            ax[num].set_xticks([])
            ax[num].set_yticks([])

        plt.show()
        
class ImChannelNS(): #channel

    'morphoHeart Image Channel Negative Space'
    
    def __init__(self, organ:Organ, ch_name:str, new=True):

        self.parent_organ = organ
        self.parent_organ_name = organ.user_organName
        self.channel_no = ch_name
        self.user_chName = organ.mH_settings[ch_name]['general_info']['user_chName']
        self.ch_relation = 'negative-space'
        if new:
            self.new_ImChannelNS()
        else: 
            self.load_channel()
    
    def new_ImChannelNS (self):
        
        organ = self.parent_organ
        ch_name = self.channel_no
        
        self.resolution = organ.info['resolution']
        self.process = ['Init']
        self.contStack = {}
        
        # external contour
        ext_s3_name = organ.mH_settings[ch_name]['general_info']['ch_ext'][0]
        ext_s3_type = organ.mH_settings[ch_name]['general_info']['ch_ext'][1]
        
        #internal contour
        int_s3_name = organ.mH_settings[ch_name]['general_info']['ch_int'][0]
        int_s3_type = organ.mH_settings[ch_name]['general_info']['ch_int'][1]
        
        self.setup = {'ext':{'name': ext_s3_name, 'type': ext_s3_type}, 
                      'int':{'name': int_s3_name, 'type': int_s3_type}}
        
        organ.add_channelNS(imChannelNS=self)
        organ.check_status(process='ImProc')
        organ.save_organ()
    
    def load_channel(self):
        
        organ = self.parent_organ
        ch_name = self.channel_no
        
        self.resolution = organ.imChannelNS[ch_name]['resolution']
        self.process = organ.imChannelNS[ch_name]['process']
        contStack_dict = organ.imChannelNS[ch_name]['contStack']
        for cont in contStack_dict.keys():
            contStack_dict[cont]['s3_dir'] = Path(contStack_dict[cont]['s3_dir'])
            contStack_dict[cont]['shape_s3'] = tuple(contStack_dict[cont]['shape_s3'])
        self.contStack = contStack_dict
        
        # organ.add_channel(imChannel=self)
        
    def create_chNSS3s(self, plot=False):
        organ = self.parent_organ
        ext_s3_name = self.setup['ext']['name']
        ext_s3_type = self.setup['ext']['type']
        ext_s3 = ContStack(im_channel=organ.obj_imChannels[ext_s3_name], 
                           cont_type=ext_s3_type, new=False)
        self.s3_ext = ext_s3
        self.add_contStack(ext_s3)
        
        int_s3_name = self.setup['int']['name']
        int_s3_type = self.setup['int']['type']
        int_s3 = ContStack(im_channel=organ.obj_imChannels[int_s3_name], 
                           cont_type=int_s3_type, new=False)
        self.s3_int = int_s3
        self.add_contStack(int_s3)
        
        tiss_s3 = ContStack(im_channel = self, cont_type = 'tiss', new = True, 
                            layerDict=plot)
        self.s3_tiss = tiss_s3
        self.add_contStack(tiss_s3)
     
    def get_channel_no(self):
        return self.channel_no

    def get_resolution(self):
        return self.resolution
    
    def add_contStack(self, contStack):
        # Check first if the contStack has been already added to the channel
        new = False
        if contStack.cont_type not in self.contStack.keys():
            new = True
            
        if new: 
            contStack_dict = {}
            contStack_dict['cont_type'] = contStack.cont_type
            contStack_dict['imfilled_name'] = contStack.imfilled_name
            contStack_dict['cont_name'] = contStack.cont_name
            contStack_dict['s3_file'] = contStack.s3_file
            contStack_dict['s3_dir'] = contStack.s3_dir
            contStack_dict['shape_s3'] = contStack.shape_s3
            contStack_dict['process'] = contStack.process
            self.contStack[contStack.cont_type] = contStack_dict
        else: # just update process 
            self.contStack[contStack.cont_type]['process'] = contStack.process

    
    def create_s3_tiss (self, plot=False, im_every=25): 
        """
        Function to extract the negative space channel
        """
        workflow = self.parent_organ.workflow
        
        print('- Extracting '+self.user_chName+'!')
        if workflow['ImProc'][self.channel_no]['D-S3Create']['Status'] != 'DONE':
            proceed = True
        else: 
            proceed = ask4input('You had already run this process. Do you want to re-run it?\n\t[0]: no, continue with next step\n\t[1]: yes, re-run it! >>>:', bool)

        if proceed: 
            s3 = self.s3_ext.s3()
            s3_mask = self.s3_int.s3()
            
            s3_bits = np.zeros_like(s3, dtype='uint8')
            s3_new =  np.zeros_like(s3, dtype='uint8')
    
            index = list(s3.shape).index(min(s3.shape))
            if index == 2:
                for slc in range(s3.shape[2]):
                    mask_slc = s3_mask[:,:,slc]
                    toClean_slc = s3[:,:,slc]
                    # Keep ch to use as mask as it is
                    inv_slc = np.copy(mask_slc)
    
                    # inverted_mask or mask AND ch1_2clean
                    toRemove_slc = np.logical_and(toClean_slc, inv_slc)
                    # Keep only the clean bit
                    cleaned_slc = np.logical_xor(toClean_slc, toRemove_slc)
    
                    if plot and slc in list(range(0,s3.shape[0],im_every)):
                        self.slc_plot(slc, inv_slc, toClean_slc, toRemove_slc, cleaned_slc, inverted=False)
    
                    s3_bits[:,:,slc] = toRemove_slc
                    s3_new[:,:,slc] = cleaned_slc
                    
                s3_new = s3_new.astype('uint8')
                alert('whistle')   
                
            else:
                print('>> Index different to 2, check!')
                alert('error_beep')

        workflow['ImProc'][self.channel_no]['Status'] = 'DONE'
        workflow['ImProc'][self.channel_no]['D-S3Create']['Status'] = 'DONE'
        
        return s3_new
    
    def slc_plot (self, slc, mask_slc, toClean_slc, toRemove_slc, cleaned_slc, inverted):
        """
        Function to plot mask, original image and result
        """
        if self.channel_no != 'chNS':#option == 'clean':
            if inverted: 
                txt = ['ch0_inv','ch1','ch0_inv AND ch1','ch0_inv AND ch1\nxOR ch1']
            else: 
                txt = ['ch0','ch1','ch0 AND ch1','ch0 AND ch1\nxOR ch1']
        else:
            txt = ['ch0_int','ch1_ext','ch0_int AND ch1_ext','layer in between']

        #Plot
        fig, ax = plt.subplots(1, 4, figsize = (10,2.5))
        fig.suptitle("Slice:"+str(slc), y=1.05, weight="semibold")
        ax[0].imshow(mask_slc)
        ax[1].imshow(toClean_slc)
        ax[2].imshow(toRemove_slc)
        ax[3].imshow(cleaned_slc)
        for num in range(0,4,1):
            ax[num].set_title(txt[num])
            ax[num].set_xticks([])
            ax[num].set_yticks([])

        plt.show()
        
    # func - s32Meshes
    def s32Meshes(self, keep_largest, rotateZ_90, new):
        
        meshes_out = []
        for mesh_type in ['int', 'ext', 'tiss']:
            mesh = Mesh_mH(self, mesh_type, keep_largest[mesh_type], rotateZ_90, new)
            meshes_out.append(mesh)
            
        return meshes_out
        
class ContStack(): 
    'morphoHeart Contour Stack Class'
    
    def __init__(self, im_channel:Union[ImChannel,ImChannelNS], 
                             cont_type:str, new=True, layerDict={}):
        
        cont_types = ['int', 'ext', 'tiss']
        names = ['imIntFilledCont', 'imExtFilledCont', 'imAllFilledCont']

        index = cont_types.index(cont_type)
        self.cont_type = cont_type
        self.imfilled_name = names[index]
        self.im_channel = im_channel
        self.cont_name = im_channel.channel_no+'_'+self.cont_type
        
        parent_organ = im_channel.parent_organ
        self.s3_file = parent_organ.user_organName + '_s3_' + im_channel.channel_no + '_' + self.cont_type + '.npy'
        self.s3_dir = parent_organ.dir_res / 's3_numpy' / self.s3_file
        
        if new: 
            if im_channel.channel_no == 'chNS':
                s3 = im_channel.create_s3_tiss(plot=layerDict)
            else: 
                s3 = self.s3_create(layerDict = layerDict)
            self.s3_save(s3)
            self.shape_s3 = s3.shape
            self.process = ['Init']
        else: 
            s3 = self.s3()
            self.shape_s3 = s3.shape
            self.process = im_channel.contStack[cont_type]['process']
            self.process.append('Loaded')
    
    def s3_create(self, layerDict:dict):
        x_dim = self.im_channel.shape[0]
        y_dim = self.im_channel.shape[1]
        z_dim = self.im_channel.shape[2]
        
        s3 = np.empty((x_dim,y_dim,z_dim+2))
        for pos, keySlc in enumerate(layerDict.keys()):
            if keySlc[0:3] == "slc":
                slcNum = int(keySlc[3:6])
                im_FilledCont = layerDict[keySlc][self.cont_type]
                s3[:,:,slcNum+1] = im_FilledCont
        s3 = s3.astype('uint8')
        parent_organ = self.im_channel.parent_organ
        parent_organ.workflow['ImProc'][self.im_channel.channel_no]['D-S3Create']['Status'] = 'DONE'
        
        return s3
    
    def s3(self):
        if self.s3_dir.is_file():
            s3 = np.load(self.s3_dir)
        else: 
            print('>> Error: s3 file does not exist!\n>> File: '+self.s3_file)
            alert('error_beep')
            s3 = None
            
        return s3

    def s3_save(self, s3):
        organ = self.im_channel.parent_organ
        dir2save = organ.info['dirs']['s3_numpy'] / self.s3_file
        np.save(dir2save, s3)
        if not dir2save.is_file():
            print('>> Error: s3 file was not saved correctly!\n>> File: '+self.s3_file)
            alert('error_beep')
        else: 
            print('>> s3 file saved correctly! - ', self.im_channel.channel_no, '-', self.cont_type)
            # print('>> Directory: '+ str(dir2save)+'\n')
            alert('countdown')
            
        
    def cutW2Planes(self, pl1, pl2):
        """
        Function used to cut inflow AND outflow tract of the s3 mask (s3_cut) given as input
    
        """
        #Load s3 and resolution
        s32cut = self.s3()
        resolution = self.im_channel.resolution
        
        # Get dimensions of external stack
        xdim, ydim, zdim = s32cut.shape
        # Reshape stacks as a vector
        s3_cut_v = s32cut.reshape(-1)
    
        # Get vectors of x,y and z positions
        pix_coord_pos = np.where(s32cut >= 0)
        del s32cut
        # Trasform coordinate positions to um using resolution
        pix_um = np.transpose(np.asarray([pix_coord_pos[i]*resolution[i] for i in range(len(resolution))]))
        del pix_coord_pos
    
        normal_inf = unit_vector(pl1['pl_normal'])#pls_normal[0])
        normal_outf = unit_vector(pl2['pl_normal'])#pls_normal[1])
    
        # Find all the d values of pix_um
        d_pix_um_Inf = np.dot(np.subtract(pix_um,np.array(pl1['pl_centre'])),np.array(normal_inf))
        d_pix_um_Outf = np.dot(np.subtract(pix_um,np.array(pl2['pl_centre'])),np.array(normal_outf))
        del pix_um
    
        # Clear vector d_pix_um using only those that are 1 in stack
        d_pve_pix_um_Inf = s3_cut_v*d_pix_um_Inf
        d_pve_pix_um_Outf = s3_cut_v*d_pix_um_Outf
        del d_pix_um_Inf, d_pix_um_Outf
    
        # Duplicate s3f_v to initialise stacks without inflow
        s3f_all_v = np.copy(s3_cut_v)
        s3f_all_v.astype('uint8')
        del s3_cut_v
    
        # Find all positions in d_pve_pix_um that are at either side of the planes (outside of mesh)
        pos_outside_inf = np.where(d_pve_pix_um_Inf < 0)[0]
        pos_outside_outf = np.where(d_pve_pix_um_Outf > 0)[0]
        del d_pve_pix_um_Inf, d_pve_pix_um_Outf
    
        # Remove the points that are outside of the mesh (inflow)
        s3f_all_v[pos_outside_inf] = 0
        del pos_outside_inf
    
        # Remove the points that are outside of the mesh (ouflow)
        s3f_all_v[pos_outside_outf] = 0
        del pos_outside_outf
    
        # Reshape vector into matrix/stack
        s3f_cut = s3f_all_v.reshape((xdim, ydim, zdim))
        
        # Save new s3
        self.s3_save(s3f_cut)
        alert('woohoo')
    
        # return s3f_cut
    
    # func - cutInfOrOutfOptMx
    def cutW1Plane (self, pl, cut):
        """
        Function used to cut inflow OR outflow tract of the s3 mask (s3_cut) given as input
    
        """
    
        # print('- Cutting s3 - ' + option+' '+mesh_name)
        #Load s3 and resolution
        s32cut = self.s3()
        resolution = self.im_channel.resolution
    
        # Get dimensions of external stack
        xdim, ydim, zdim = s32cut.shape
        # Reshape stacks as a vector
        s3_cut_v = s32cut.reshape(-1)
    
        # Get vectors of x,y and z positions
        pix_coord_pos = np.where(s32cut >= 0)
        del s32cut
        # Trasform coordinate positions to um using resolution
        pix_um = np.transpose(np.asarray([pix_coord_pos[i]*resolution[i] for i in range(len(resolution))]))
        del pix_coord_pos
    
        normal  = unit_vector(pl['pl_normal'])
        # Find all the d values of pix_um
        d_pix_um = np.dot(np.subtract(pix_um,np.array(pl['pl_centre'])),np.array(normal))
    
        # Clear vector d_pix_um using only those that are 1 in stack
        d_pve_pix_um = s3_cut_v*d_pix_um
        del pix_um
    
        # Duplicate s3f_v to initialise stacks without inflow/outflow
        s3f_all_v = np.copy(s3_cut_v)
        s3f_all_v.astype('uint8')
        del s3_cut_v
    
        # Find all positions in d_pve_pix_um that are at either side of the planes (outside of mesh)
        if cut == 'inflow tract' or cut == 'bottom':
            pos_outside = np.where(d_pve_pix_um < 0)[0]
        elif cut == 'outflow tract' or cut == 'top':
            pos_outside = np.where(d_pve_pix_um > 0)[0]
        del d_pve_pix_um
    
        # Remove the points that are outside of the mesh (inflow/outflow)
        s3f_all_v[pos_outside] = 0
        del pos_outside
    
        # Reshape vector into matrix/stack
        s3f_cut = s3f_all_v.reshape((xdim, ydim, zdim))
        del s3f_all_v
        
        # Save new s3
        self.s3_save(s3f_cut)
        alert('woohoo')

   
class Mesh_mH():
    'morphoHeart Mesh Class'
    
    def __init__(self, imChannel:ImChannel, mesh_type:str, 
                 keep_largest:bool, rotateZ_90=True, new=True):
        
        self.parent_organ = imChannel.parent_organ
        self.imChannel = imChannel
        self.channel_no = imChannel.channel_no
        self.user_meshName = self.parent_organ.mH_settings[self.channel_no]['general_info']['user_chName']
        self.mesh_type = mesh_type
        self.legend = self.user_meshName+'_'+self.mesh_type
        self.name = self.channel_no +'_'+self.mesh_type
        self.resolution = imChannel.get_resolution()

        wf = ['MeshesProc','A-Create3DMesh', imChannel.channel_no, mesh_type] 
        if new: 
            self.keep_largest = keep_largest
            self.rotateZ_90 = rotateZ_90
            self.create_mesh(keep_largest = keep_largest, rotateZ_90 = rotateZ_90)
            self.color = self.parent_organ.mH_settings[self.channel_no]['general_info']['colorCh_'+self.mesh_type]
            self.alpha = 0.05
            
            # Update workflow
            self.parent_organ.update_workflow(wf+['Status'], update = 'DONE')
            if 'NS' not in imChannel.channel_no:
                self.parent_organ.update_workflow(wf+['Stack_dir'], update = imChannel.contStack[self.mesh_type]['s3_dir'])
                self.parent_organ.update_workflow(wf+['keep_largest'], update = keep_largest)
                mH_settings = self.parent_organ.mH_settings
                items = [imChannel.channel_no,'setup',self.mesh_type,'keep_largest']
                set_by_path(mH_settings, items, keep_largest)
            # else:  
        
        else: 
            self.load_mesh()
            workflow = self.parent_organ.workflow
            self.keep_largest = get_by_path(workflow, wf+['keep_largest'])
            self.rotateZ_90 = rotateZ_90
            self.color = self.parent_organ.meshes[self.name]['color']
            self.alpha = self.parent_organ.meshes[self.name]['alpha']
            
        self.mesh.color(self.color)
        self.mesh.alpha(self.alpha)
        
        if new: 
            self.parent_organ.add_mesh(self)
            self.save_mesh()
    
    def create_mesh(self, keep_largest:bool, rotateZ_90:bool):
        # Extract vertices, faces, normals and values of each mesh
        s3_type = 's3_'+self.mesh_type
        s3 = getattr(self.imChannel, s3_type)
        s3s3 = s3.s3()
        # if self.mesh_type == 'int':
        #     s3 = self.imChannel.s3_int.s3()
        # elif self.mesh_type == 'ext':
        #     s3 = self.imChannel.s3_ext.s3()
        # elif self.mesh_type == 'tiss':
        #     s3 = self.imChannel.s3_tiss.s3()
        # print(s3)
        verts, faces, _, _ = measure.marching_cubes_lewiner(s3s3, spacing=self.resolution)
    
        # Create meshes
        mesh = vedo.Mesh([verts, faces])
        if keep_largest:
            mesh = mesh.extractLargestRegion()
        if rotateZ_90:
            mesh.rotateZ(-90)
        mesh.legend(self.legend).wireframe()
        self.mesh = mesh
    
    def load_mesh(self):
        parent_organ = self.parent_organ
        mesh_name = parent_organ.user_organName+'_'+self.legend+'.vtk'
        mesh_dir = parent_organ.info['dirs']['meshes'] / mesh_name
        mesh_out = vedo.load(str(mesh_dir))
        self.dir_out = mesh_dir
        self.mesh = mesh_out

    def save_mesh(self):
        parent_organ = self.parent_organ
        mesh_name = parent_organ.user_organName+'_'+self.legend+'.vtk'
        mesh_dir = parent_organ.info['dirs']['meshes'] / mesh_name
        self.dir_out = mesh_dir
        mesh_out = self.mesh
        mesh_out.write(str(mesh_dir))
        print('>> Mesh '+mesh_name+' has been saved!')
        alert('countdown')        
        self.parent_organ.add_mesh(self)
        
    def mesh4CL(self):
        """
        Function that cleans and smooths meshes given as input to get centreline using VMTK
    
        """
        
        mesh4cl = self.mesh.clone()
        print('- Cleaning mesh '+self.legend)
        print("\t- Original number of points making up mesh: ", mesh4cl.NPoints())
        # Reduce the number of points that make up the mesh
        mesh4cl.subsample(fraction = 0.005)#tol=0.005)
        print("\t- Number of points after cleaning surface: ",mesh4cl.NPoints(),'\n- Smoothing mesh...', self.legend)
        
        # vp = vedo.Plotter(N=1, axes=5)
        # vp.show(mesh4cl, at=0, interactive=True)
        
        # Smooth mesh
        mesh4cl_cut = mesh4cl.clone().smooth_mls_2d(f=0.2)
        mesh4cl_cut.legend(self.legend+"-C&S").color(self.color)
        print('- Mesh smoothed!')
        alert('woohoo')

        return mesh4cl_cut

    def get_channel_no(self):
        return self.channel_no
    
    def get_user_meshName(self):
        return self.user_meshName
    
    def get_legend(self):
        return self.mesh.legend
    
    def change_user_meshName(self, new_user_meshName):
        self.user_meshName = new_user_meshName
    
    def get_mesh_type(self):
        return self.mesh_type
    
    def get_imChannel(self):
        return self.imChannel
    
    def get_organ(self):
        return self.parent_organ
    
    def set_alpha(self, mesh_alpha):
        self.alpha = mesh_alpha
        self.mesh.alpha(self.alpha)
        self.parent_organ.meshes[self.name]['alpha'] = self.alpha
        self.parent_organ.save_organ()
    
    def get_alpha(self):
        return self.mesh_alpha
        
    def set_color(self, mesh_color):
        self.color = mesh_color
        self.mesh.color(self.color)
        self.parent_organ.meshes[self.name]['color'] = self.color
        self.parent_organ.save_organ()
        
    def get_color(self):
        return self.mesh_color   
        
    def get_mesh(self):
        try: 
            return self.mesh 
        except:
            self.load_mesh()
            return self.mesh
    
    def getCentreline(self): 
        pass

#%%
print('morphoHeart! - Loaded Module Classes')
