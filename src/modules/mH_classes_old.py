'''
morphoHeart_classes

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
import os
from datetime import datetime
import pathlib
from pathlib import Path
import numpy as np
from skimage import measure, io
import copy
import json
import collections
import pprint
import matplotlib.pyplot as plt
import flatdict
from typing import Union
from time import perf_counter
import vedo as vedo
from vedo import write
from scipy.interpolate import splprep, splev, interpn
from itertools import count
import random
from skimage.draw import line_aa
import seaborn as sns

path_fcMeshes = os.path.abspath(__file__)
path_mHImages = Path(path_fcMeshes).parent.parent.parent / 'images'

#%% ##### - Other Imports - ##################################################
#from ...config import dict_gui
from .mH_funcBasics import alert, ask4input, make_Paths, make_tuples, get_by_path, set_by_path
from .mH_funcMeshes import unit_vector, plot_organCLs, find_angle_btw_pts, classify_segments_from_ext, create_asign_subsg

alert_all=True
heart_default=False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}

#%% Set default fonts and sizes for plots
txt_font = 'Dalim'
leg_font = 'LogoType' # 'Quikhand' 'LogoType'  'Dalim'
leg_width = 0.18
leg_height = 0.2
txt_size = 0.7
txt_color = '#696969'
txt_slider_size = 0.8

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
    def __init__(self, proj_dict:dict, new:bool):
        
        # if dir_proj.is_dir():
        #     print(">> There is already a directory with the new project's name!")
        #     settings_name = 'mH_'+name+'_project.json'
        #     dir_settings = dir_proj / 'settings' / settings_name
        #     if dir_settings.is_file():
        #         print('>> There is already a project settings file within this !')
        #         new = False
        #     else: 
        #         print('>> New Project! (if2)')
        #         new = True
        # else: 
        #     print('>> New Project! (if1)')
        #     new = True
            
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
            self.user_projName = proj_dict['name'].replace(' ', '_')
            self.info = {'mH_projName': self.mH_projName,
                            'user_projName': self.user_projName,
                            'user_projNotes': proj_dict['notes'], 
                            'date_created' : proj_dict['date'],
                            'dirs': []}
            self.analysis = proj_dict['analysis']
            self.dir_proj = Path(proj_dict['dir_proj'])
            self.organs = {}
            self.cellGroups = {}
                
        else: 
            load_dict = {'name': proj_dict['name'], 'dir': proj_dict['dir_proj']}
            self.load_project(load_dict=load_dict)
    
    def load_project(self, load_dict:dict):
        print('Loading project:', load_dict)
#         dir_res = load_dict['dir']
#         jsonDict_name = 'mH_'+load_dict['name']+'_project.json'
#         json2open_dir = dir_res / 'settings' / jsonDict_name
#         if json2open_dir.is_file():
#             with open(json2open_dir, "r") as read_file:
#                 print(">> "+jsonDict_name+": Opening JSON encoded data")
#                 load_dict = json.load(read_file)
            
#             load_dict = make_Paths(load_dict)
            
#             tuple_keys = [['mH_settings','general_info','chNS','ch_ext'], 
#                           ['mH_settings','general_info','chNS','ch_int'], 
#                          ]
            
#             load_dict = make_tuples(load_dict, tuple_keys)
           
#             self.info = load_dict['info']
#             self.user_projName = load_dict['info']['user_projName']
#             self.mH_projName = load_dict['info']['mH_projName']
#             self.analysis = load_dict['analysis']
            
#             self.mH_settings = load_dict['mH_settings']
#             self.mH_channels = load_dict['mH_channels']
#             self.mH_segments = load_dict['mH_segments']
#             self.mH_sections = load_dict['mH_sections']
#             self.mH_param2meas = [tuple(item) for item in load_dict['mH_param2meas']]
            
#             self.mC_settings = load_dict['mC_settings']
#             self.mC_channels = load_dict['mC_channels']
#             self.mC_segments = load_dict['mC_segments']
#             self.mC_param2meas = load_dict['mC_param2meas']
            
#             self.workflow = load_dict['workflow']
#             self.mH_methods = load_dict['mH_methods']
#             self.organs = load_dict['organs']
#             self.cellGroups = load_dict['cellGroups']
          
#             self.dir_proj = load_dict['info']['dir_proj']
#             self.dir_info = load_dict['info']['dir_info']
#         else: 
#             print('>> Error: No project with name ',load_dict['name'],' was found!\n Directory: ',str(json2open_dir))
#             alert('error_beep')

#     def set_settings(self, mH_settings:dict, mC_settings:dict):
#         '''
#         func - Create general project settings
#         This function will be called when the user creates a new project and 
#         fills information regarding the workflow for such project which will get into the 
#         function packed as the mH_settings dictionary. 
#         The output of this function will create an attribute to the project containing 
#         most of the user settings except for the selected parameters. 
#         '''
    
#         self.set_mH_settings(mH_settings)
#         self.set_mC_settings(mC_settings)
        
#     def set_mH_settings(self, mH_settings:dict):
        
#         mH_set = {'general_info':{}, 'setup': {}, 'measure': {}, 'wf_info': {}}
#         mH_meas_keys = []
#         mH_channels = []
#         mH_segments = []
#         mH_sections = []
            
#         if self.analysis['morphoHeart']:
            
#             if mH_settings['segm'] != False: 
#                 if mH_settings['segm']['cutLayersIn2Segments']:
#                     for cut in [key for key in mH_settings['segm'] if key != 'cutLayersIn2Segments' and key!= 'measure']:
#                         dict_segments[cut] = mH_settings['segm'][cut]
#                     dict_segments['measure'] = mH_settings['segm']['measure']
#                         # dict_segments = {'no_segments': mH_settings['segments']['no_segments'],
#                         #                 'no_cuts_4segments': mH_settings['segments']['no_cuts_4segments'],
#                         #                 'name_segments': mH_settings['segments']['name_segments'],
#                         #                 'ch_segments': mH_settings['segments']['ch_segments']}
                
#             if mH_settings['sect'] != False: 
#                 if mH_settings['sect']['cutLayersIn2Sections']:
#                     for cut in [key for key in mH_settings['sect'] if key != 'cutLayersIn2Sections' and key!= 'measure']:
#                         dict_sections[cut] = mH_settings['sect'][cut]
#                     dict_sections['measure'] = mH_settings['sect']['measure']
#                         # dict_sections = {'no_sections': mH_settings['sections']['no_sections'],
#                         #                 'name_sections': mH_settings['sections']['name_sections'],
#                         #                 'ch_sections': mH_settings['sections']['ch_sections']}
                
#             for ch_num in range(0, mH_settings['no_chs']):
#                 ch_str = 'ch'+str(ch_num+1)
#                 dict_info_ch = {'mH_chName':ch_str,
#                                 'user_chName':mH_settings['name_chs'][ch_str].replace(' ', '_'),
#                                 'dir_cho': None, 
#                                 'ch_relation': mH_settings['chs_relation'][ch_str],
#                                 'mask_ch': mH_settings['mask_ch'][ch_str],
#                                 'dir_mk': None}
                
#                 if mH_settings['segments']['cutLayersIn2Segments']:   
#                     if ch_str in mH_settings['segments']['ch_segments'].keys():
#                         dict_info_ch['ch_segments'] = mH_settings['segments']['ch_segments'][ch_str]
                    
#                 if mH_settings['sections']['cutLayersIn2Sections']:   
#                     if ch_str in mH_settings['sections']['ch_sections'].keys():
#                         dict_info_ch['ch_sections'] = mH_settings['sections']['ch_sections'][ch_str]
            
#                 dict_setup = {}
#                 dict_meas = {}
#                 for cont in ['tiss', 'ext', 'int']: 
#                     dict_setup[cont] = {'color': mH_settings['color_chs'][ch_str][cont], 
#                                         'keep_largest' : False, 
#                                         'rotateZ_90': False, 
#                                         'alpha': 0.05}
#                     dict_meas[cont] = {'whole': {}}
#                     mH_meas_keys.append((ch_str,cont,'whole'))
                    
#                 mH_set['general_info'][ch_str] = dict_info_ch
#                 mH_set['setup'][ch_str] = dict_setup
#                 mH_set['measure'][ch_str] = dict_meas
#                 mH_channels.append(ch_str)
            
#             mH_set['general_info']['segments'] = dict_segments
#             mH_set['general_info']['sections'] = dict_sections
#             mH_set['general_info']['rotateZ_90'] = mH_settings['rotateZ_90']
    
#             if mH_settings['ns']['layer_btw_chs']:
#                 ch_str = 'chNS'
#                 mH_set['general_info']['chNS']={'mH_chName':ch_str,
#                                                 'user_chName':mH_settings['ns']['user_nsChName'].replace(' ', '_'),
#                                                 'ch_ext': mH_settings['ns']['ch_ext'],
#                                                 'ch_int': mH_settings['ns']['ch_int']}
                
#                 if mH_settings['segments']['cutLayersIn2Segments']:   
#                     if ch_str in mH_settings['segments']['ch_segments'].keys():
#                         mH_set['general_info']['chNS']['ch_segments'] = mH_settings['segments']['ch_segments'][ch_str]
                        
#                 dict_setupNS = {}
#                 dict_measNS = {}
#                 for cont in ['tiss', 'ext', 'int']: 
#                     dict_setupNS[cont] = {'color': mH_settings['ns']['color_chns'][cont], 
#                                         'keep_largest' : False,
#                                         'rotateZ_90': False}
#                     dict_measNS[cont] = {'whole': {}}
#                     mH_meas_keys.append((ch_str,cont,'whole'))
                
#                 mH_set['setup'][ch_str] = dict_setupNS
#                 mH_set['measure'][ch_str] = dict_measNS
#                 mH_set['orientation'] = {}
#                 mH_channels.append(ch_str)
    
#             if mH_settings['segments']['cutLayersIn2Segments']:
#                 for ch_str in mH_channels:
#                     ch_segments = list(mH_settings['segments']['ch_segments'].keys())
#                     if ch_str in ch_segments:
#                         for s_num in range(0, mH_settings['segments']['no_segments']):
#                             segm_str = 'segm'+str(s_num+1)
#                             mH_segments.append(segm_str)
#                             for cont in mH_settings['segments']['ch_segments'][ch_str]:
#                                 mH_set['measure'][ch_str][cont][segm_str] = {} 
#                                 mH_meas_keys.append((ch_str,cont,segm_str))
            
#             if mH_settings['sections']['cutLayersIn2Sections']:
#                 for ch_str in mH_channels:
#                     ch_sections = list(mH_settings['sections']['ch_sections'].keys())
#                     if ch_str in ch_sections:
#                         for s_num in range(0, mH_settings['sections']['no_sections']):
#                             sect_str = 'sect'+str(s_num+1)
#                             mH_sections.append(sect_str)
#                             for cont in mH_settings['sections']['ch_sections'][ch_str]:
#                                 mH_set['measure'][ch_str][cont][sect_str] = {} 
#                                 mH_meas_keys.append((ch_str,cont,sect_str))
                                
#         self.mH_settings = mH_set
#         self.mH_meas_keys = mH_meas_keys
#         self.mH_channels = mH_channels
#         segments_new = list(set(mH_segments))
#         self.mH_segments = segments_new
#         sections_new = list(set(mH_sections))
#         self.mH_sections = sections_new
        
#         self.table2select_mH_meas()

#     def set_mC_settings(self, mC_settings:dict): 
        
#         mC_set = {}
#         mC_channels = []
#         mC_segments = []
        
#         if self.analysis['morphoCell']:
#             for ch_num in range(0, mC_settings['no_chs']):
#                 ch_str = 'ch'+str(ch_num+1)
#                 dict_info_ch = {'mH_chName':ch_str,
#                                 'user_chName':mC_settings['name_chs'][ch_str].replace(' ', '_'),
#                                 'link2mH':mC_settings['link2mH'][ch_str],
#                                 'dir_cho': None, 
#                                 'ch_relation': mC_settings['chs_relation'][ch_str],
#                                 'color': mC_settings['color_chs'][ch_str]}
#                 mC_set[ch_str] = {}
#                 mC_set[ch_str]['general_info'] = dict_info_ch
#                 mC_channels.append(ch_str)
            
#             if mC_settings['segments']['cutLayersIn2Segments']:
#                 for ch_str in mC_channels:
#                     ch_segments = list(mC_settings['segments']['ch_segments'].keys())
#                     if ch_str in ch_segments:
#                         for s_num in range(0, mC_settings['segments']['no_segments']):
#                             segm_str = 'segm'+str(s_num+1)
#                             mC_segments.append(segm_str)
#                             mC_set[ch_str]['measure'][segm_str] = {} 
                            
#             else: 
#                 print('>> proj.info[dirs] had already been created!')
        
#         self.mC_settings = mC_set
#         self.mC_channels = mC_channels.sort()
#         self.mC_segments = mC_segments.sort()
        
#         self.table2select_mC_meas()

#     def table2select_mH_meas(self):
#         '''
#         This function will create a dictionary with all the possible measurement parameters 
#         a user can get based on the settings given when setting the initial project 
#         (no_ch, no_segments and the corresponding channels from which the segments will 
#         be obtained, etc)
#         The output of this function (dictionary with default parameters and list)
#         will help to set up the GUI table for the user to select the parameters to measure. 
#         '''
#         channels = self.mH_channels
#         conts = ['tiss', 'int', 'ext']
#         mH_param2meas = []
#         dict_params_deflt = {}
        
#         for ch_b in channels: 
#             dict_params_deflt[ch_b] = {}
#             for cont_b in conts: 
#                 dict_params_deflt[ch_b][cont_b] = {}

#         for tup in self.mH_meas_keys:
#             ch, cont, segm = tup
#             if 'segm' in segm or 'whole' in segm: 
#                 dict_params_deflt[ch][cont][segm] = {'volume': True, 
#                                                         'surf_area': False}
#                 mH_param2meas.append((ch,cont,segm,'volume'))
#                 mH_param2meas.append((ch,cont,segm,'surf_area'))
#             else: 
#                 dict_params_deflt[ch][cont][segm] = {'volume': True}
#                 mH_param2meas.append((ch,cont,segm,'volume'))


#             if cont in ['int', 'ext']:
#                 dict_params_deflt[ch][cont][segm]['surf_area'] = True 
#             if cont == 'tiss':
#                 if segm == 'whole': 
#                     dict_params_deflt[ch][cont][segm]['thickness int>ext'] = True
#                     dict_params_deflt[ch][cont][segm]['thickness ext>int'] = False

#                     mH_param2meas.append((ch,cont,segm,'thickness int>ext'))
#                     mH_param2meas.append((ch,cont,segm,'thickness ext>int'))
#                 elif 'segm' in segm: 
#                     dict_params_deflt[ch][cont][segm]['thickness int>ext'] = False
#                     dict_params_deflt[ch][cont][segm]['thickness ext>int'] = False

#                     mH_param2meas.append((ch,cont,segm,'thickness int>ext'))
#                     mH_param2meas.append((ch,cont,segm,'thickness ext>int'))
                    
#             if segm == 'whole' and cont in ['ext','int'] and ch != 'chNS':
#                 dict_params_deflt[ch][cont][segm]['centreline'] = True
#                 dict_params_deflt[ch][cont][segm]['centreline_linlength'] = True
#                 dict_params_deflt[ch][cont][segm]['centreline_looplength'] = True

#                 mH_param2meas.append((ch,cont,segm,'centreline'))
#                 mH_param2meas.append((ch,cont,segm,'centreline_linlength'))
#                 mH_param2meas.append((ch,cont,segm,'centreline_looplength'))

#         self.mH_param2meas = mH_param2meas
#         #Use this two result variables to create selecting table in the GUI
    
#     def table2select_mC_meas(self):
        
#         mC_param2meas = []
#         self.mC_param2meas = mC_param2meas

#     def set_mH_meas(self, user_params2meas:dict, user_ball_settings:dict):
#         '''
#         This function will get the input of the updated selected parameters from the GUI and 
#         will include those measurements in the dictionary of the project. This dictionary will then 
#         be used as a workflow template for all the Organs created within the project. 
#         '''
#         settings_updated = copy.deepcopy(self.mH_settings)
#         mH_param2meas = copy.deepcopy(self.mH_param2meas)
#         gral_struct = self.mH_meas_keys
        
#         for tup in gral_struct: 
#             ch, cont, segm = tup
#             settings_updated['measure'][ch][cont][segm] = user_params2meas[ch][cont][segm]

#         if user_ball_settings['ballooning']:
#             ball_settings = user_ball_settings['ball_settings']
#             for key in ball_settings.keys():
#                 ch = ball_settings[key]['to_mesh']
#                 cont = ball_settings[key]['to_mesh_type']
#                 from_cl = ball_settings[key]['from_cl']
#                 cl_type = ball_settings[key]['from_cl_type']
#                 settings_updated['measure'][ch][cont]['whole']['ballooning']= {'from_cl':from_cl,
#                                                                                'from_cl_type': cl_type, 
#                                                                                'range': {}}
#                 mH_param2meas.append((ch,cont,'whole','ballooning'))

#                 if not settings_updated['measure'][from_cl][cl_type]['whole']['centreline']:
#                     settings_updated['measure'][from_cl][cl_type]['whole']['centreline'] = True
#                     settings_updated['measure'][from_cl][cl_type]['whole']['centreline_linlength'] = True
#                     settings_updated['measure'][from_cl][cl_type]['whole']['centreline_looplength'] = True
                    
#                 if (from_cl,cl_type,'whole','centreline') not in mH_param2meas:
#                     mH_param2meas.append((from_cl,cl_type,'whole','centreline'))
#                     mH_param2meas.append((from_cl,cl_type,'whole','centreline_linlength'))
#                     mH_param2meas.append((from_cl,cl_type,'whole','centreline_looplength'))
#                     print('>> Added ', from_cl, cl_type)
                    
#         # Note: Make sure the info being transferred from the dict to the wf is right 
#         self.mH_param2meas = mH_param2meas
#         self.clean_False(settings_updated=settings_updated)
#         delattr(self, 'mH_meas_keys')
#         self.set_mH_methods()
#         self.update_mH_settings()
        
#     def clean_False(self, settings_updated:dict):
#         mH_param2meas = copy.deepcopy(self.mH_param2meas)
#         mH_param2meas_new = []
        
#         for tup in mH_param2meas:
#             ch, cont, segm, var = tup
#             if not settings_updated['measure'][ch][cont][segm][var]: 
#                 settings_updated['measure'][ch][cont][segm].pop(var, None)
#                 # print('deleting: ', ch, cont, segm, var)
#             else: 
#                 mH_param2meas_new.append(tup)
        
#         self.mH_settings = settings_updated
#         self.mH_param2meas = sorted(mH_param2meas_new)
    
#     def set_mH_methods(self):
#         mH_param2meas = self.mH_param2meas

#         if len(mH_param2meas)>0: 
#             methods = ['A-Create3DMesh','B-TrimMesh']
        
#         if any(flag == 'ballooning' for (_,_,_,flag) in mH_param2meas):
#             methods.append('C-Centreline')
#             methods.append('D-Ballooning')
#         elif any(flag == 'centreline' for (_,_,_,flag) in mH_param2meas):
#             methods.append('C-Centreline')
#         if any(flag == 'thickness int>ext' for (_,_,_,flag) in mH_param2meas):
#             methods.append('D-Thickness_int>ext')
#         if any(flag == 'thickness ext>int' for (_,_,_,flag) in mH_param2meas):
#                 methods.append('D-Thickness_ext>int')
#         if any('segm' in flag for (_,_,flag,_) in mH_param2meas):
#             methods.append('E-Segments')
#         if any('sect' in flag for (_,_,flag,_) in mH_param2meas):
#             methods.append('E-Sections')
        
#         self.mH_methods = methods
    
#     def update_mH_settings(self):
#         methods = self.mH_methods
#         mH_settings = self.mH_settings
#         mH_params = self.mH_param2meas
#         if len(methods)>0:
#             mH_settings['wf_info']={'ImProc':{'E-CleanCh': {'Settings': {'ch':None,
#                                                                          's3_mask': None,
#                                                                          'inverted': False}},
#                                               'E-TrimS3': {'Planes': None}},
#                                     'MeshesProc': {'B-TrimMesh': {'Planes': None}}}
#         if 'C-Centreline' in methods:
#             centreline = True
#             item_centreline = [item for item in mH_params if 'centreline' in item]
#             mH_settings['wf_info']['MeshesProc']['C-Centreline'] = {}
#             mH_settings['wf_info']['MeshesProc']['C-Centreline']['Planes'] = {'bottom': None, 'top': None}
#             # mH_settings['wf_info']['MeshesProc']['C-Centreline']['KSplines'] = {}
#             for tup in item_centreline:
#                 ch, cont, _, _ = tup
#                 if ch not in mH_settings['wf_info']['MeshesProc']['C-Centreline'].keys():
#                     mH_settings['wf_info']['MeshesProc']['C-Centreline'][ch] = {}
#                 mH_settings['wf_info']['MeshesProc']['C-Centreline'][ch][cont] = {'dir_cleanMesh': None, 
#                                                                                    'dir_meshLabMesh': None, 
#                                                                                    'vmtktxt': None,
#                                                                                    'connect_cl': None}
                
#         if 'D-Ballooning' in methods:
#             item_ball = [item for item in mH_params if 'ballooning' in item]
#             mH_settings['wf_info']['MeshesProc']['D-Ballooning'] = {}
#             for tup in item_ball:
#                 ch, cont, _, _ = tup
#                 if ch not in mH_settings['wf_info']['MeshesProc']['D-Ballooning'].keys():
#                     mH_settings['wf_info']['MeshesProc']['D-Ballooning'][ch] = {}
#                 mH_settings['wf_info']['MeshesProc']['D-Ballooning'][ch][cont] = self.mH_settings['measure'][ch][cont]['whole']['ballooning']
            
#         if 'D-Thickness_int>ext' in methods:
#             item_th = [item for item in mH_params if 'thickness int>ext' in item]
#             mH_settings['wf_info']['MeshesProc']['D-Thickness_int>ext'] = {}
#             for tup in item_th:
#                 ch, cont, _, _ = tup
#                 if ch not in mH_settings['wf_info']['MeshesProc']['D-Thickness_int>ext'].keys():
#                     mH_settings['wf_info']['MeshesProc']['D-Thickness_int>ext'][ch] = {}
#                 mH_settings['wf_info']['MeshesProc']['D-Thickness_int>ext'][ch][cont] = {'range' : {}}
                
#         if 'D-Thickness_ext>int' in methods:
#             item_th = [item for item in mH_params if 'thickness ext>int' in item]
#             mH_settings['wf_info']['MeshesProc']['D-Thickness_ext>int'] = {}
#             for tup in item_th:
#                 ch, cont, _, _ = tup
#                 if ch not in mH_settings['wf_info']['MeshesProc']['D-Thickness_ext>int'].keys():
#                     mH_settings['wf_info']['MeshesProc']['D-Thickness_ext>int'][ch] = {}
#                 mH_settings['wf_info']['MeshesProc']['D-Thickness_ext>int'][ch][cont] = {'range' : {}}
                
#         if self.analysis['morphoHeart']:
#             self.info['dirs'] = {'meshes': 'NotAssigned', 
#                                 'csv_all': 'NotAssigned',
#                                 'imgs_videos': 'NotAssigned', 
#                                 's3_numpy': 'NotAssigned',
#                                 'settings': 'NotAssigned'}
#             if centreline:
#                 self.info['dirs']['centreline'] = 'NotAssigned'
#         elif self.analysis['morphoCell']:
#             self.info['dirs'] = {'csv_all': 'NotAssigned',
#                                 'imgs_videos': 'NotAssigned', 
#                                 'settings': 'NotAssigned'}

#     def create_proj_dir(self, dir_proj:Path):
#         folder_name = 'R_'+self.user_projName
#         self.dir_proj = dir_proj / folder_name
#         self.dir_proj.mkdir(parents=True, exist_ok=True)
#         if self.dir_proj.is_dir():
#             self.info['dir_proj'] = self.dir_proj
#         else: 
#             print('>> Error: Project directory could not be created!\n>> Dir: '+self.dir_proj)
#             alert('error_beep')
            
#     def set_workflow(self):
#         '''
#         This function will initialise the dictionary that will contain the workflow of the
#         project. This workflow will be assigned to each organ that is part of the created project
#         and will be updated in each organ as the user advances in the processing. 
#         '''
#         workflow = {}
#         if self.analysis['morphoHeart']: 
#             mH_channels = sorted(self.mH_channels)
#             mH_segments = sorted(self.mH_segments)
#             mH_sections = sorted(self.mH_sections)
    
#             dict_ImProc = dict()
#             dict_ImProc['Status'] = 'NI'
#             dict_MeshesProc = dict()
    
#             # Find the meas_param that include the extraction of a centreline
#             item_centreline = [item for item in self.mH_param2meas if 'centreline' in item]
#             # Find the meas_param that include the extraction of mH_segments
#             segm_list = []
#             for segm in mH_segments[0:1]:
#                 segm_list.append([item for item in self.mH_param2meas if segm in item and 'volume' in item])
#             ch_segm = sorted(list(set([tup[0] for tup in segm_list[0]])))
            
#             # Find the meas_param that include the extraction of mH_sections
#             sect_list = []
#             for sect in mH_sections[0:1]:
#                 sect_list.append([item for item in self.mH_param2meas if sect in item and 'volume' in item])
#             ch_sect = sorted(list(set([tup[0] for tup in sect_list[0]])))

#             # Find the meas_param that include the extraction of ballooning
#             item_ballooning = [item for item in self.mH_param2meas if 'ballooning' in item]
#             # Find the meas_param that include the extraction of thickness
#             item_thickness_intext = [item for item in self.mH_param2meas if 'thickness int>ext' in item]
#             item_thickness_extint = [item for item in self.mH_param2meas if 'thickness ext>int' in item]
    
#             dict_MeshesProc = {'Status' : 'NI'}
#             for met in self.mH_methods:
#                 dict_MeshesProc[met] =  {'Status': 'NI'}
                               
#             # Project status
#             for ch in mH_channels:
#                 if 'A-Create3DMesh' in dict_MeshesProc.keys():
#                     if 'NS' not in ch:
#                         dict_ImProc[ch] = {'Status': 'NI',
#                                             'A-MaskChannel': {'Status': 'NI'},
#                                             'B-CloseCont':{'Status': 'NI',
#                                                             'Steps':{'A-Autom': {'Status': 'NI'},
#                                                                     'B-Manual': {'Status': 'NI'},
#                                                                     'C-CloseInOut': {'Status': 'NI'}}},
#                                             'C-SelectCont':{'Status': 'NI'},
#                                             'D-S3Create':{'Status': 'NI',
#                                                         'Info': {'tiss':{'Status': 'NI'}, 
#                                                                 'int':{'Status': 'NI'}, 
#                                                                 'ext':{'Status': 'NI'}}}}
#                         #Check the external channel
#                         if self.mH_settings['general_info'][ch]['ch_relation'] == 'external':
#                             dict_ImProc[ch]['E-TrimS3'] = {'Status': 'NI',
#                                                              'Info':{'tiss':{'Status': 'NI'}, 
#                                                                      'int':{'Status': 'NI'},
#                                                                      'ext':{'Status': 'NI'}}}
#                         else: 
#                             dict_ImProc[ch]['E-CleanCh'] = {'Status': 'NI',
#                                                               'Info': {'tiss':{'Status': 'NI'}, 
#                                                                       'int':{'Status': 'NI'}, 
#                                                                       'ext':{'Status': 'NI'}}}
#                             dict_ImProc[ch]['E-TrimS3'] = {'Status': 'NI',
#                                                              'Info':{'tiss':{'Status': 'NI'}, 
#                                                                      'int':{'Status': 'NI'},
#                                                                      'ext':{'Status': 'NI'}}}
#                     else: 
#                         dict_ImProc[ch] = {'Status': 'NI',
#                                             'D-S3Create':{'Status': 'NI'}} 
                 
#             for nn, ch in enumerate(mH_channels):
#                 for process in ['A-Create3DMesh','B-TrimMesh','C-Centreline']:
#                     if 'NS' not in ch:
#                         if process != 'C-Centreline':
#                             dict_MeshesProc[process][ch] = {}
#                         for nnn, cont in enumerate(['tiss', 'int', 'ext']):
#                             if process == 'A-Create3DMesh' or process == 'B-TrimMesh':
#                                 dict_MeshesProc[process][ch][cont] = {'Status': 'NI'}
                         
#                             if process == 'C-Centreline' and 'C-Centreline' in dict_MeshesProc.keys():
#                                 # print('nn:', nn, 'nnn:', nnn)
#                                 if nn == 0 and nnn == 0: 
#                                     dict_MeshesProc[process]['Status'] = 'NI'
#                                     dict_MeshesProc[process]['SimplifyMesh'] = {'Status':'NI'}
#                                     dict_MeshesProc[process]['vmtk_CL'] = {'Status':'NI'}
#                                     dict_MeshesProc[process]['buildCL'] = {'Status':'NI'}
                                    
#                                 if (ch,cont,'whole','centreline') in item_centreline:
#                                     # print(ch,cont)
#                                     if ch not in dict_MeshesProc[process]['SimplifyMesh'].keys(): 
#                                         dict_MeshesProc[process]['SimplifyMesh'][ch] = {}
#                                         dict_MeshesProc[process]['vmtk_CL'][ch] = {}
#                                         dict_MeshesProc[process]['buildCL'][ch] = {}
#                                     dict_MeshesProc[process]['SimplifyMesh'][ch][cont] = {'Status': 'NI'}
#                                     dict_MeshesProc[process]['vmtk_CL'][ch][cont] = {'Status': 'NI'}
#                                     dict_MeshesProc[process]['buildCL'][ch][cont] = {'Status': 'NI'}
                                    
#                     else: 
#                         if process == 'A-Create3DMesh':
#                             dict_MeshesProc[process][ch] = {'Status': 'NI'}
    
#                 for cont in ['tiss', 'int', 'ext']:
#                     if (ch,cont,'whole','ballooning') in item_ballooning:
#                         dict_MeshesProc['D-Ballooning'][ch] = {}
#                         dict_MeshesProc['D-Ballooning'][ch][cont] =  {'Status': 'NI'}
    
#                     if (ch,cont,'whole','thickness int>ext') in item_thickness_intext:
#                         dict_MeshesProc['D-Thickness_int>ext'][ch] = {}
#                         dict_MeshesProc['D-Thickness_int>ext'][ch][cont] = {'Status': 'NI'}
                        
#                     if (ch,cont,'whole','thickness ext>int') in item_thickness_extint:
#                          dict_MeshesProc['D-Thickness_ext>int'][ch] = {}
#                          dict_MeshesProc['D-Thickness_ext>int'][ch][cont] = {'Status': 'NI'}
                                                       
#             # Project status
#             for ch in ch_segm:
#                 dict_MeshesProc['E-Segments'][ch] = {}
#                 for cont in ['tiss', 'int', 'ext']:
#                     if (ch, cont,'segm1','volume') in segm_list[0]:
#                         dict_MeshesProc['E-Segments'][ch][cont] = {'Status': 'NI'}
#                         for segm in mH_segments:
#                             dict_MeshesProc['E-Segments'][ch][cont][segm]={'Status': 'NI'}
            
#             for ch in ch_sect:
#                 dict_MeshesProc['E-Sections'][ch] = {}
#                 for cont in ['tiss', 'int', 'ext']:
#                     if (ch, cont,'sect1','volume') in sect_list[0]:
#                         dict_MeshesProc['E-Sections'][ch][cont] = {'Status': 'NI'}
#                         for sect in mH_sections:
#                             dict_MeshesProc['E-Sections'][ch][cont][sect]={'Status': 'NI'}
            
#             # Measure Dictionary
#             dict_meas = flatdict.FlatDict({})
#             rows = self.mH_param2meas
#             dict_meas['Status'] = 'NI'
#             for ch, cont, segm, param in rows:
#                 key = ":".join([ch, cont, segm, param])
#                 dict_meas[key] = 'NI'
            
#             dict_MeshesProc['F-Measure'] = dict_meas.as_dict()
                                                                                       
#             workflow['ImProc'] = dict_ImProc
#             workflow['MeshesProc'] = dict_MeshesProc
        
#         if self.analysis['morphoCell']:
            
#             dict_cell = {}
#             workflow['CellProc'] = dict_cell
            
#         self.workflow = workflow

#     def save_project(self):
#         #Create a new dictionary that contains all the settings
#         jsonDict_name = 'mH_'+self.user_projName+'_project.json'
#         json2save_par = self.dir_proj / 'settings'
#         json2save_par.mkdir(parents=True, exist_ok=True)
        
#         self.dir_info = self.dir_proj / 'settings' / jsonDict_name
#         self.info['dir_info'] = self.dir_info
        
#         all_info = {}
#         all_info['info'] = self.info
#         all_info['analysis'] = self.analysis
#         all_info['mH_methods'] = self.mH_methods
#         all_info['mH_settings'] = self.mH_settings
#         all_info['mH_channels'] = self.mH_channels
#         all_info['mH_segments'] = self.mH_segments
#         all_info['mH_sections'] = self.mH_sections
#         all_info['mH_param2meas'] = self.mH_param2meas
        
#         all_info['mC_settings'] = self.mC_settings
#         all_info['mC_channels'] = self.mC_channels
#         all_info['mC_segments'] = self.mC_segments
#         all_info['mC_param2meas'] = self.mC_param2meas
        
#         all_info['workflow'] = self.workflow
#         all_info['mH_methods'] = self.mH_methods
#         all_info['organs'] = self.organs
#         all_info['cellGroups'] = self.cellGroups
        
#         if not json2save_par.is_dir():
#             print('>> Error: Settings directory could not be created!\n>> Directory: '+jsonDict_name)
#             alert('error_beep')
#         else: 
#             json2save_dir = json2save_par / jsonDict_name
#             with open(str(json2save_dir), "w") as write_file:
#                 json.dump(all_info, write_file, cls=NumpyArrayEncoder)

#             if not json2save_dir.is_file():
#                 print('>> Error: Project settings file was not saved correctly!\n>> File: '+jsonDict_name)
#                 alert('error_beep')
#             else: 
#                 print('>> Project settings file saved correctly!\n>> File: '+jsonDict_name)
#                 # print('>> File: '+ str(json2save_dir)+'\n')
#                 alert('countdown')
        
    
#     def add_organ(self, organ):
#         dict_organ = copy.deepcopy(organ.info)
#         dict_organ.pop('project', None)
#         dict_organ['dir_res'] = organ.dir_res
        
#         self.organs[organ.user_organName] = dict_organ
#         self.save_project()

#     def remove_organ(self, organ):
#         organs = copy.deepcopy(self.organs)
#         organs.pop(organ.user_organName, None)
#         self.organs = organs
#         self.save_project()

#     def load_organ(self, user_organName:str):
#         dir_res = self.organs[user_organName]['dir_res']
#         jsonDict_name = 'mH_'+self.organs[user_organName]['user_organName']+'_organ.json'
#         json2open_dir = Path(dir_res) / 'settings' / jsonDict_name
#         if json2open_dir.is_file():
#             with open(json2open_dir, "r") as read_file:
#                 print(">> "+jsonDict_name+": Opening JSON encoded data")
#                 dict_out = json.load(read_file)
#             organ = Organ(project=self, user_settings={}, info_loadCh={}, 
#                             new=False, load_dict=dict_out)
#         else: 
#             organ = None
#             print('>> Error: No organ name with name ',user_organName,' was found!\n Directory: ',str(json2open_dir))
#             alert('error_beep')
            
#         return organ

# class Organ():
#     'Organ Class'
    
#     def __init__(self, project:Project, user_settings:dict, info_loadCh:dict, 
#                  new=True, load_dict={}):
        
#         self.parent_project = project
#         if new:
#             self.user_organName = user_settings['user_organName'].replace(' ', '_')
#             self.info = user_settings
#             self.info['dirs'] = project.info['dirs']
#             self.info_loadCh = info_loadCh
#             self.create_mHName()
#             self.analysis = copy.deepcopy(project.analysis)
#             if self.analysis['morphoHeart']:
#                 self.mH_settings = copy.deepcopy(project.mH_settings)
#                 self.imChannels = {}
#                 self.obj_imChannels = {}
#                 self.imChannelNS = {}
#                 self.obj_imChannelNS = {}
#                 self.meshes = {}
#                 self.submeshes = {}
#                 self.obj_meshes = {}
#                 self.objects = {'KSplines': {}, 'Spheres': {}}
#                 if 'C-Centreline' in self.parent_project.mH_methods:
#                     self.objects['KSplines']['cut4cl'] = {'bottom': {}, 'top':{}}
#                     self.objects['Spheres']['cut4cl'] = {'bottom': {}, 'top':{}}
#                     self.objects['Centreline'] = {}
#             if self.analysis['morphoCell']:
#                 self.mC_settings = copy.deepcopy(project.mC_settings)
#             self.workflow = copy.deepcopy(project.workflow)
#         else: 
#             self.load_organ(load_dict=load_dict)
        
#         self.check_channels(project)

#     def load_organ(self, load_dict:dict):
        
#         load_dict = make_Paths(load_dict)
        
#         # user_settings = dict_out['Organ']
#         self.info = load_dict['Organ']
#         self.user_organName = self.info['user_organName'].replace(' ', '_')
#         # info_loadCh = dict_out['info_loadCh']
#         self.info_loadCh = load_dict['info_loadCh']
#         self.analysis = load_dict['analysis']
        
#         tuple_keys = [['mH_settings','general_info','chNS','ch_ext'],
#                       ['mH_settings','general_info','chNS','ch_int']]
        
#         for ch in load_dict['imChannels'].keys():
#             tuple_keys.append(['imChannels', ch, 'shape'])
#             tuple_keys.append(['imChannels', ch, 'shape_s3'])
#             for cont in load_dict['imChannels'][ch]['contStack'].keys():
#                 tuple_keys.append(['imChannels', ch, 'contStack',cont,'shape_s3'])
        
#         load_dict = make_tuples(load_dict, tuple_keys)
        
#         # Workflow
#         self.workflow = load_dict['workflow']
#         self.dir_info = Path(load_dict['dir_info'])
#         self.mH_organName = load_dict['mH_organName']
        
#         self.objects = load_dict['objects']
#         if self.analysis['morphoHeart']:
#             # mH_Settings
#             self.mH_settings = load_dict['mH_settings']
#             # imChannels
#             self.imChannels = load_dict['imChannels']
#             self.load_objImChannels()
#             # imChannelNS
#             self.imChannelNS = load_dict['imChannelNS']
#             self.load_objImChannelNS()
#             # meshes
#             self.meshes = load_dict['meshes']
#             self.load_objMeshes()
#             # submeshes
#             if 'submeshes' in load_dict.keys():
#                 submeshes_dict = load_dict['submeshes']
#                 flat_subm_dict = flatdict.FlatDict(submeshes_dict)
#                 list_colors = [key.split(':') for key in flat_subm_dict if 'color' in key]
#                 submeshes_dict_new = make_tuples(submeshes_dict, list_colors)
#                 self.submeshes = submeshes_dict_new
#             else: 
#                 self.submeshes = {}
#             # objects
#             self.objects = load_dict['objects']
            
#         if self.analysis['morphoCell']:
#             # mC_Settings
#             self.mC_settings = load_dict['mC_settings']
        
#     def load_objImChannels(self):
#         self.obj_imChannels = {}
#         if len(self.imChannels) > 0:
#             for imCh in self.imChannels:
#                 im_ch = ImChannel(organ=self, ch_name=imCh)#, new=False)
#                 self.obj_imChannels[imCh] = im_ch
        
#     def load_objImChannelNS(self):
#         self.obj_imChannelNS = {}
#         if len(self.imChannelNS) > 0: 
#             for imCh in self.imChannelNS:
#                 im_ch = ImChannelNS(organ=self, ch_name=imCh)#, new=False)
#                 self.obj_imChannelNS[imCh] = im_ch
        
#     def load_objMeshes(self):
#         self.obj_meshes = {}
#         if len(self.meshes) > 0: 
#             for mesh in self.meshes:
#                 ch_no = self.meshes[mesh]['channel_no']
#                 if 'NS' in mesh: 
#                     imCh = self.obj_imChannelNS[ch_no]
#                 else: 
#                     imCh = self.obj_imChannels[ch_no]
#                 mesh_type = self.meshes[mesh]['mesh_type']
#                 keep_largest = self.meshes[mesh]['keep_largest']
#                 rotateZ_90 = self.meshes[mesh]['rotateZ_90'] 
#                 msh = Mesh_mH(imChannel = imCh, mesh_type = mesh_type, 
#                               keep_largest = keep_largest, rotateZ_90 = rotateZ_90)#,
#                               # new = False)
#                 self.obj_meshes[mesh] = msh

#     def create_mHName(self):
#         now_str = datetime.now().strftime('%Y%m%d%H%M')
#         self.mH_organName = 'mH_Organ-'+now_str
                 
#     def check_channels(self, project:Project):
#         info_loadCh = self.info_loadCh
#         chs = [x for x in project.mH_channels if x != 'chNS']    
#         array_sizes = {}
#         sizes = []
#         for ch in chs:
#             try:
#                 images_o = io.imread(str(info_loadCh[ch]['dir_cho']))
#                 array_sizes[ch]= {'cho': images_o.shape}
#                 sizes.append(images_o.shape)
#             except: 
#                 print('>> Error: Something went wrong opening the file -',ch)
#                 alert('error_beep')
            
#             if info_loadCh[ch]['mask_ch']:
#                 try:
#                     images_mk = io.imread(str(info_loadCh[ch]['dir_mk']))
#                     array_sizes[ch]['mask']= images_mk.shape
#                     sizes.append(images_mk.shape)
#                 except: 
#                     print('>> Error: Something went wrong opening the mask -',ch)
#                     alert('error_beep')
            
#         unique_size = list(set(sizes))
#         if len(unique_size) != 1: 
#             counter = collections.defaultdict(int)
#             for elem in unique_size:
#                 counter[elem] += 1
#             print('>> Error: Dimensions of imported images do not match! Please check! \n Imported Data: ')
#             pprint.pprint(array_sizes)
#             alert('error_beep')
        
#         else:      
#             for ch in chs:
#                 for param in ['dir_cho','mask_ch','dir_mk']:
#                     self.mH_settings['general_info'][ch][param] = info_loadCh[ch][param]
#             # print('>> Files have been checked! \n>> Images shape:')
#             # pprint.pprint(array_sizes)

#         self.create_folders()

#     def create_folders(self):
#         dirResults = ['meshes', 'csv_all', 'imgs_videos', 's3_numpy', 'centreline', 'settings']
#         organ_folder = self.user_organName
#         for direc in dirResults:
#             dir2create = self.parent_project.dir_proj / organ_folder / direc
#             dir2create.mkdir(parents=True, exist_ok=True)
#             if dir2create.is_dir():
#                 self.info['dirs'][direc] = dir2create
#             else: 
#                 print('>> Error: Directory ', self.user_organName, '/', direc, ' could not be created!')
#                 alert('error_beep')
#         self.dir_res = self.parent_project.dir_proj / organ_folder

#     def add_channel(self, imChannel):
#         # Check first if the channel has been already added to the organ
#         new = False
#         if imChannel.channel_no not in self.imChannels.keys():
#             new = True
            
#         if new: 
#             print('>> Adding Channel - ', imChannel.channel_no)
#             channel_dict = {}
#             channel_dict['parent_organ_name'] = imChannel.parent_organ_name
#             channel_dict['channel_no'] = imChannel.channel_no
#             channel_dict['user_chName'] = imChannel.user_chName
#             channel_dict['ch_relation'] = imChannel.ch_relation
#             channel_dict['to_mask'] = imChannel.to_mask
#             channel_dict['resolution'] = imChannel.resolution
#             channel_dict['dir_cho'] = imChannel.dir_cho
#             if imChannel.to_mask:
#                 channel_dict['dir_mk'] = imChannel.dir_mk
#             channel_dict['masked'] = imChannel.masked
#             channel_dict['shape'] = imChannel.shape
#             channel_dict['process'] = imChannel.process
#             channel_dict['contStack'] = imChannel.contStack
#             channel_dict['dir_stckproc'] = imChannel.dir_stckproc
            
#             self.imChannels[imChannel.channel_no] = channel_dict
#             self.info['shape_s3'] = imChannel.shape
            
#         else: # just update im_proc 
#             self.imChannels[imChannel.channel_no]['process'] = imChannel.process
#             self.imChannels[imChannel.channel_no]['contStack'] = imChannel.contStack
#             if imChannel.dir_stckproc.is_file():
#                 self.imChannels[imChannel.channel_no]['dir_stckproc'] = imChannel.dir_stckproc
#             if hasattr(imChannel, 'shape_s3'):
#                 self.imChannels[imChannel.channel_no]['shape_s3'] = imChannel.shape_s3
#         self.obj_imChannels[imChannel.channel_no] = imChannel
        
#     def add_channelNS(self, imChannelNS):
#         # Check first if the channel has been already added to the organ
#         new = False
#         if imChannelNS.channel_no not in self.imChannelNS.keys():
#             new = True
            
#         if new: 
#             print('>> Adding ChannelNS - ', imChannelNS.channel_no)
#             channel_dict = {}
#             channel_dict['parent_organ_name'] = imChannelNS.parent_organ_name
#             channel_dict['channel_no'] = imChannelNS.channel_no
#             channel_dict['user_chName'] = imChannelNS.user_chName
#             channel_dict['ch_relation'] = imChannelNS.ch_relation
#             channel_dict['resolution'] = imChannelNS.resolution
#             channel_dict['process'] = imChannelNS.process
#             channel_dict['contStack'] = imChannelNS.contStack
#             channel_dict['setup_NS'] = imChannelNS.setup_NS
#             self.imChannelNS[imChannelNS.channel_no] = channel_dict
            
#         else: # just update im_proc 
#             self.imChannelNS[imChannelNS.channel_no]['process'] = imChannelNS.process
#             self.imChannelNS[imChannelNS.channel_no]['contStack'] = imChannelNS.contStack
           
#         self.obj_imChannelNS[imChannelNS.channel_no] = imChannelNS

#     def add_mesh(self, mesh): # mesh: Mesh_mH
    
#         new = False
#         if mesh.name not in self.meshes.keys():
#             new = True
#         if new: 
#             print('>> Adding Mesh - ', mesh.name)
#             self.meshes[mesh.name] = {}
#             self.meshes[mesh.name]['parent_organ'] = mesh.parent_organ.user_organName
#             self.meshes[mesh.name]['channel_no'] = mesh.imChannel.channel_no
#             self.meshes[mesh.name]['user_meshName'] = mesh.user_meshName
#             self.meshes[mesh.name]['mesh_type'] = mesh.mesh_type
#             self.meshes[mesh.name]['legend'] = mesh.legend
#             self.meshes[mesh.name]['name'] = mesh.name
#             self.meshes[mesh.name]['resolution'] = mesh.resolution
#             self.meshes[mesh.name]['color'] = mesh.color
#             self.meshes[mesh.name]['alpha'] = mesh.alpha
#             self.meshes[mesh.name]['keep_largest'] = mesh.keep_largest
#             self.meshes[mesh.name]['rotateZ_90'] = mesh.rotateZ_90
#             self.meshes[mesh.name]['s3_dir'] = mesh.s3_dir
#             if hasattr(mesh,'dir_out'):
#                 self.meshes[mesh.name]['dir_out'] = mesh.dir_out
#             self.obj_meshes[mesh.name] = mesh
#         else: #Just updating things that could change
#             self.meshes[mesh.name]['color'] = mesh.color
#             self.meshes[mesh.name]['alpha'] = mesh.alpha
#             self.meshes[mesh.name]['keep_largest'] = mesh.keep_largest
#             self.obj_meshes[mesh.name] = mesh
#             if hasattr(mesh, 'dirs'):
#                 self.meshes[mesh.name]['dirs'] = mesh.dirs
#             print('>> Mesh data updated!')
    
#     def add_submesh(self, submesh):
#         new = False
#         if submesh.sub_name_all not in self.submeshes.keys():
#             new = True
#         if new:
#             print('>> Adding SubMesh - ', submesh.sub_name_all)
#             self.submeshes[submesh.sub_name_all] = {}
#             #New to submesh
#             self.submeshes[submesh.sub_name_all]['sub_name'] = submesh.sub_name
#             self.submeshes[submesh.sub_name_all]['sub_name_all'] = submesh.sub_name_all
#             self.submeshes[submesh.sub_name_all]['parent_mesh'] = submesh.parent_mesh.name
#             self.submeshes[submesh.sub_name_all]['sub_mesh_type'] = submesh.sub_mesh_type
#             self.submeshes[submesh.sub_name_all]['sub_legend'] = submesh.sub_legend
#             self.submeshes[submesh.sub_name_all]['sub_user_name'] = submesh.sub_user_name
#             #Mesh related
#             self.submeshes[submesh.sub_name_all]['resolution'] = submesh.resolution
#             self.submeshes[submesh.sub_name_all]['color'] = submesh.color
#             self.submeshes[submesh.sub_name_all]['alpha'] = submesh.alpha
#             self.submeshes[submesh.sub_name_all]['keep_largest'] = submesh.keep_largest
#             self.submeshes[submesh.sub_name_all]['rotateZ_90'] = submesh.rotateZ_90
#             #Inherited from parent_mesh
#             self.submeshes[submesh.sub_name_all]['parent_mesh'] = {}
#             self.submeshes[submesh.sub_name_all]['parent_mesh']['legend'] = submesh.parent_mesh.legend
#             self.submeshes[submesh.sub_name_all]['parent_mesh']['name'] = submesh.parent_mesh.name
#             self.submeshes[submesh.sub_name_all]['parent_mesh']['imChannel'] = submesh.parent_mesh.imChannel.channel_no

#         else: #Just updating things that could change
#             self.submeshes[submesh.sub_name_all]['color'] = submesh.color
#             self.submeshes[submesh.sub_name_all]['alpha'] = submesh.alpha
#             self.submeshes[submesh.sub_name_all]['keep_largest'] = submesh.keep_largest
#             print('>> SubMesh data updated!')
            
#         if submesh.sub_mesh_type == 'Section':
#             self.submeshes[submesh.sub_name_all]['s3_invert'] = submesh.s3_invert
#             self.submeshes[submesh.sub_name_all]['s3_mask_dir'] = submesh.s3_mask_dir
#         elif submesh.sub_mesh_type == 'Segment':
#             if hasattr(submesh, 'dict_segm'):
#                 self.submeshes[submesh.sub_name_all]['dict_segm'] = submesh.dict_segm
       
            

#     def add_object(self, obj, proc:str, class_name:Union[list,str], name):
        
#         if isinstance(obj, vedo.shapes.KSpline):# or name == 'KSpline':
#             if proc != 'Centreline': 
#                 if isinstance(class_name, list):
#                     classif, mesh_name = class_name
#                     self.objects['KSplines'][proc][classif][mesh_name] = {'points': obj.points(), 
#                                                                        'color': obj.color()}
#                 else: 
#                     self.objects['KSplines'][proc][class_name] = {'points': obj.points(), 
#                                                                        'color': obj.color()}
#             else: 
#                 self.objects[proc][class_name] = {'points': obj.points(), 
#                                                   'color': obj.color()}
            
#         if isinstance(obj, vedo.shapes.Sphere):# or name == 'Sphere':
#             if isinstance(class_name, list):
#                 classif, mesh_name = class_name
#                 self.objects['Spheres'][proc][classif][mesh_name] = {'center': obj.center, 
#                                                                    'color': obj.color()}
#             else: 
#                 self.objects['Spheres'][proc][class_name] = {'center': obj.center, 
#                                                                    'color': obj.color()}
                
                    
#     def load_TIFF(self, ch_name:str):
#         print('---- Loading TIFF! ----')
#         image = ImChannel(organ=self, ch_name=ch_name)#,new=True
#         return image

#     def save_organ(self):
#         all_info = {}
#         all_info['Organ'] = self.info
#         all_info['info_loadCh'] = self.info_loadCh
#         all_info['analysis'] = self.analysis
        
#         jsonDict_name = 'mH_'+self.user_organName+'_organ.json'
#         json2save_dir = self.info['dirs']['settings'] / jsonDict_name
#         if self.analysis['morphoHeart']:
#             all_info['mH_settings'] = self.mH_settings
            
#             image_dict = copy.deepcopy(self.imChannels)
#             for ch in image_dict.keys():
#                 image_dict[ch].pop('parent_organ', None)
#             all_info['imChannels'] = image_dict
            
#             imageNS_dict = copy.deepcopy(self.imChannelNS)
#             for chNS in imageNS_dict.keys():
#                 imageNS_dict[chNS].pop('parent_organ', None)
#             all_info['imChannelNS'] = imageNS_dict

#             all_info['meshes'] = self.meshes
#             all_info['submeshes'] = self.submeshes
#             all_info['objects'] = self.objects
            
#         if self.analysis['morphoCell']:
#             all_info['mC_settings'] = self.mC_settings
        
#         all_info['workflow'] = self.workflow
    
#         self.dir_info = self.dir_res / 'settings' / jsonDict_name
#         all_info['dir_info'] = self.dir_info
#         all_info['mH_organName'] = self.mH_organName

#         with open(str(json2save_dir), "w") as write_file:
#             json.dump(all_info, write_file, cls=NumpyArrayEncoder)

#         if not json2save_dir.is_file():
#             print('>> Error: Organ settings file was not saved correctly!\n>> File: '+jsonDict_name)
#             alert('error_beep')
#         else: 
#             print('\n>> Organ settings file saved correctly! - '+jsonDict_name)
#             #print('>> Directory: '+ str(json2save_dir)+'\n')
#             alert('countdown')
            
#     def check_status(self, process:str):
 
#         if process=='ImProc':
#             ch_done = []
#             for ch in self.imChannels.keys():
#                 # First check close contours
#                 close_done = []
#                 for key_a in ['A-Autom', 'B-Manual', 'C-CloseInOut']:
#                     val = get_by_path(self.workflow, [process,ch,'B-CloseCont','Steps',key_a,'Status'])
#                     close_done.append(val)
#                    # close_done.append(self.workflow[process][ch]['B-CloseCont']['Steps'][key_a]['Status'])
#                 print('-> channel:',ch, '-CloseCont:', close_done)
#                 if all(flag == 'DONE' for flag in close_done):
#                     self.update_workflow([process,ch,'B-CloseCont','Status'], 'DONE')
#                     # self.workflow[process][ch]['B-CloseCont']['Status'] = 'DONE'

#                 # Now update all the workflow
#                 proc_done = []
#                 for key_b in self.workflow[process][ch].keys():
#                     if key_b != 'Status':
#                         val_b = get_by_path(self.workflow, [process,ch,key_b,'Status'])
#                         proc_done.append(val_b)
#                         # proc_done.append(self.workflow[process][ch][key_b]['Status'])
#                 print('-> channel:',ch, '-ImProc:', proc_done)
#                 if all('DONE' in flag for flag in proc_done):
#                     self.update_workflow([process,ch,'Status'], 'DONE')
#                     # self.workflow[process][ch]['Status'] = 'DONE'
#                 val_c = get_by_path(self.workflow, [process,ch,'Status'])
#                 ch_done.append(val_c)
#                 # ch_done.append(self.workflow[process][ch]['Status'])
            
#             if all(flag == 'DONE' for flag in ch_done):
#                 self.update_workflow([process,'Status'], 'DONE')
#                 # self.workflow[process]['Status'] = 'DONE'
                
#         if process == 'MeshesProc':
#             proc_done = []
#             flat_dict = flatdict.FlatDict(self.workflow[process])
#             for key_f in [proc for proc in self.workflow[process].keys() if proc != 'Status']:
#                 proc_done.append(self.workflow[process][key_f]['Status'])
#                 if key_f != 'E-Segments':
#                     dict_proc = [item for item in flat_dict.keys() if key_f in item]
#                     ch_cont_done = [flat_dict[item] for item in dict_proc[1:]]
#                     print('->',key_f, ch_cont_done)
#                     if all(flag == 'DONE' for flag in ch_cont_done):
#                         self.update_workflow([process,key_f,'Status'], 'DONE')
            
#             if all(flag == 'DONE' for flag in proc_done):
#                 self.update_workflow([process,'Status'], 'DONE')

#     def update_workflow(self, process, update):
#         workflow = self.workflow
#         set_by_path(workflow, process, update)
        
#     def update_settings(self, process, update, mH='mH'):
#         if mH =='mH':
#             settings = self.mH_settings
#         else:  #=='mC'
#             settings = self.mC_settings
#         set_by_path(settings, process, update)
    
#     def get_ext_int_chs(self): 
#         chs = list(self.imChannels.keys())
#         ch_ext = []; ch_int = []
#         if len(chs)>1:# and len(chs)<3:
#             for ch in chs:
#                 if self.mH_settings['general_info'][ch]['ch_relation'] == 'external':
#                     ch_ext = self.obj_imChannels[ch]
#                 if self.mH_settings['general_info'][ch]['ch_relation'] == 'internal':
#                     ch_int = self.obj_imChannels[ch]
                    
#         return ch_ext, ch_int
    
#     def check_method(self, method:str):
#         if method in self.parent_project.mH_methods:
#             return True
#         else:
#             return False  
    
#     def get_stack_orientation(self, views, 
#                               colors=[[255,215,0,200],[0,0,205,200],[255,0,0,200]],):
#         #Check if the orientation has alredy been stablished
#         # if 'orientation' in self.mH_settings.keys(): 
#         if 'stack' in self.mH_settings['orientation'].keys():
#             q = 'You already selected the stack orientation of this organ. Do you want to re-assign it?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-assign it!'}
#             proceed = ask4input(q, res, bool)
#         else: 
#             proceed = True
#         # else: 
#         #     proceed = True
                
#         if proceed: 
#             im_orient = self.info['im_orientation']
#             rotateY = False
#             if im_orient == 'custom': 
#                 cust_angle = self.info['custom_angle']
#                 rotateY = True
            
#             ext_ch, _ = self.get_ext_int_chs()
#             mesh_ext = self.obj_meshes[ext_ch.channel_no+'_tiss']
            
#             pos = mesh_ext.mesh.center_of_mass()
#             side = max(self.get_maj_bounds())
#             color_o = [152,251,152,255]
#             orient_cube = vedo.Cube(pos=pos, side=side, c=color_o[:-1])
#             orient_cube.linewidth(1).force_opaque()
            
#             if rotateY: 
#                 orient_cube.rotate_y(cust_angle)
            
#             orient_cube.pos(pos)
#             orient_cube_clear = orient_cube.clone().alpha(0.5)
#             txt0 = vedo.Text2D(self.user_organName+' - Reference cube and mesh to select planar views in STACK...', c=txt_color, font=txt_font, s=txt_size)
            
#             mks = []; sym = ['o']*len(views)
#             for n, view, col in zip(count(), views, colors):
#                 mks.append(vedo.Marker('*').c(col[0:-1]).legend(view))
#             lb = vedo.LegendBox(mks, markers=sym, font=txt_font, 
#                                 width=leg_width/1.5, height=leg_height/1.5)
            
#             path_logo = path_mHImages / 'logo-07.jpg'
#             logo = vedo.Picture(str(path_logo))
            
#             vpt = MyFaceSelectingPlotter(N=2, axes=1,colors=colors, color_o=color_o, 
#                                          views=views)
#             vpt.add_icon(logo, pos=(0.1,1), size=0.25)
#             vpt.add_callback("key press", vpt.on_key_press)
#             vpt.add_callback("mouse click", vpt.select_cube_face)
#             vpt.show(mesh_ext.mesh, orient_cube_clear,txt0, at=0)
#             vpt.show(orient_cube, lb, vpt.msg, vpt.msg_face, at=1, azimuth=45, elevation=30, zoom=0.8, interactive=True)
               
#             print('vpt.planar_views:',vpt.planar_views)
#             print('vpt.selected_faces:',vpt.selected_faces)
            
#             stack_dict = {'planar_views': vpt.planar_views}
#             proc = ['orientation', 'stack']
#             self.update_settings(proc, update = stack_dict, mH = 'mH')
            
#     def get_ROI_orientation(self, views, colors, plane:str, ref_vect='Y+'):
#         #Check if the orientation has alredy been stablished
#         if 'orientation' in self.mH_settings.keys(): 
#             if 'ROI' in self.mH_settings['orientation'].keys():
#                 q = 'You already selected the ROI (organ) orientation for this organ. Do you want to re-assign it?'
#                 res = {0: 'no, continue with next step', 1: 'yes, re-assign it!'}
#                 proceed = ask4input(q, res, bool)
#             else: 
#                 proceed = True
#         else: 
#             proceed = True
                
#         if proceed: 
#             q = 'How do you want to define the Organ (ROI) orientation?:'
#             res = {0: 'I want to use the centreline (project linLine, measure angle and define ROI orientation', 
#                    1: 'I want to use the same images orientation defined',
#                    2: 'Other...'}
#             opt = ask4input(q, res, int)
            
#             if opt == 0: 
#                 self.orient_by_cl(views, colors, plane, ref_vect)
#             elif opt == 1: 
#                 print('Opt1: Code under development!')
#             elif opt == 2: 
#                 print('Opt2: Code under development!')
        
#     def orient_by_cl(self, views, colors, plane:str, ref_vect='Y+'):
        
#         # Select the mesh to use to measure organ orientation
#         dict_cl = plot_organCLs(self)
#         q = 'Select the centreline you want to use to measure organ orientation:'
#         extend_dir = ask4input(q, dict_cl, int)
        
#         ch_cont_cl = dict_cl[extend_dir].split(' (')[1].split('-')
#         ch = ch_cont_cl[0]
#         cont = ch_cont_cl[1]
        
#         cl_mesh = self.obj_meshes[ch+'_'+cont]
#         linLine = cl_mesh.get_linLine()
#         pts = linLine.points()
        
#         plane_coord = {'XY': 2, 'YZ': 0, 'XZ': 1}
#         if isinstance(ref_vect, str):
#             ref_vectAll = {'X+': np.array([[1,0,0],[0,0,0]]),
#                            'Y+': np.array([[0,1,0],[0,0,0]]),
#                            'Z+': np.array([[0,0,1],[0,0,0]])}
#             ref_vectF = ref_vectAll[ref_vect]
            
#         coord = plane_coord[plane]
#         for pt in pts: 
#             pt[coord] = 0
        
#         angle = find_angle_btw_pts(pts, ref_vectF)
        
#         pos = cl_mesh.mesh.center_of_mass()
#         side = max(self.get_maj_bounds())  
#         color_o = [152,251,152,255]
#         orient_cube = vedo.Cube(pos=pos, side=side, c=color_o[:-1])
#         orient_cube.linewidth(1).force_opaque()
        
#         if angle != 0: 
#             if coord == 0: 
#                 orient_cube.rotate_x(angle)
#             elif coord == 1: 
#                 orient_cube.rotate_y(angle)
#             elif coord == 2: 
#                 orient_cube.rotate_z(angle)
        
#         orient_cube.pos(pos)
#         orient_cube_clear = orient_cube.clone().alpha(0.5)
        
#         txt0 = vedo.Text2D(self.user_organName+' - Reference cube and mesh to select planar views in RIO (organ)...', c=txt_color, font=txt_font, s=txt_size)
        
#         mks = []; sym = ['o']*len(views)
#         for n, view, col in zip(count(), views, colors):
#             mks.append(vedo.Marker('*').c(col[0:-1]).legend(view))
#         lb = vedo.LegendBox(mks, markers=sym, font=txt_font, 
#                             width=leg_width/1.5, height=leg_height/1.5)
#         # Load logo
#         path_logo = path_mHImages / 'logo-07.jpg'
#         logo = vedo.Picture(str(path_logo))
        
#         vpt = MyFaceSelectingPlotter(N=2, axes=1,colors=colors, color_o=color_o, 
#                                      views=views)
#         vpt.add_icon(logo, pos=(0.1,1), size=0.25)
#         vpt.add_callback("key press", vpt.on_key_press)
#         vpt.add_callback("mouse click", vpt.select_cube_face)
#         vpt.show(cl_mesh.mesh, orient_cube_clear, txt0, at=0)
#         vpt.show(orient_cube, lb, vpt.msg, vpt.msg_face, at=1, azimuth=45, elevation=30, zoom=0.8, interactive=True)
           
#         print('vpt.planar_views:',vpt.planar_views)
#         print('vpt.selected_faces:',vpt.selected_faces)
        
#         roi_dict = {'planar_views': vpt.planar_views, 
#                     'proj_plane': plane, 
#                     'ref_vect': ref_vect,
#                     'ref_vectF': ref_vectF,
#                     'orient_vect': pts,
#                     'angle_deg': angle}
        
#         proc = ['orientation', 'ROI']
#         self.update_settings(proc, update = roi_dict, mH = 'mH')
        
#         # if 'orientation' not in list(self.mH_settings.keys()): 
#         #     self.mH_settings['orientation'] = {'ROI': roi_dict}
#         # else: 
#         #     self.mH_settings['orientation']['ROI'] = roi_dict

#     def get_maj_bounds(self):
#         x_b = 0; y_b = 0; z_b = 0
#         for mesh_o in self.obj_meshes:
#             m_mesh = self.obj_meshes[mesh_o].mesh
#             x1,x2,y1,y2,z1,z2 = m_mesh.bounds()
#             if x2-x1 > x_b:
#                 x_b = x2-x1
#             if y2-y1 > y_b:
#                 y_b = y2-y1
#             if z2-z1 > z_b:
#                 z_b = z2-z1   
                
#         return [x_b, y_b, z_b]
        
#     #Get all the set mH variables in __init__
#     def get_notes(self):
#         return self.info['user_organNotes']

#     def get_custom_angle(self):
#         return self.info['custom_angle']
    
#     def get_resolution(self):
#         return self.info['resolution']

#     def get_units_resolution(self):
#         return self.info['units_resolution']

#     def get_stage(self):
#         return self.info['stage']

#     def get_strain(self):
#         return self.info['strain']

#     def get_genotype(self):
#         return self.info['genotype']

#     def get_dir_res(self):
#         return self.dir_res

#     def get_direc(self, name:str):
#         return self.info['dirs'][name]

# class ImChannel(): #channel
#     'morphoHeart Image Channel Class (this class will be used to contain the images as tiffs that have been'
#     'closed and the resulting s3s that come up from each channel'
    
#     def __init__(self, organ:Organ, ch_name:str): #, new=True):
        
#         self.parent_organ = organ
#         self.parent_organ_name = organ.user_organName
#         self.channel_no = ch_name
#         self.user_chName = organ.mH_settings['general_info'][ch_name]['user_chName']
#         self.ch_relation = organ.mH_settings['general_info'][ch_name]['ch_relation']
        
#         if self.channel_no not in organ.imChannels.keys():   
#             print('>> New Channel-', self.channel_no)
#             self.new_ImChannel()
#         else: 
#             print('>> Loading Channel-', self.channel_no)
#             self.load_channel()

#     def new_ImChannel(self):
#         organ = self.parent_organ
#         ch_name = self.channel_no
        
#         self.to_mask = organ.mH_settings['general_info'][ch_name]['mask_ch']
#         self.resolution = organ.info['resolution']
#         self.dir_cho = organ.mH_settings['general_info'][ch_name]['dir_cho']            
#         if self.to_mask:
#             self.dir_mk = organ.mH_settings['general_info'][ch_name]['dir_mk']
#         self.masked = False
#         self.shape = self.im().shape
#         self.process = ['Init']
#         self.contStack = {}
#         self.save_channel(im_proc=self.im_proc())
#         organ.add_channel(imChannel=self)
#         organ.save_organ()
        
#     def im(self):
#         im = io.imread(str(self.dir_cho))
#         if not isinstance(im, np.ndarray):
#             print('>> Error: morphoHeart was unable to load tiff.\n>> Directory: ',str(self.dir_cho))
#             alert('error_beep')
#         return im
    
#     def im_proc(self, new=True):
#         if new: 
#             im_proc =  np.copy(self.im())  
#         else: 
#             if hasattr(self, 'dir_stckproc'):
#                 im_proc = io.imread(str(self.dir_stckproc))
#                 if not isinstance(im_proc, np.ndarray):
#                     print('>> Error: morphoHeart was unable to load processed tiff.\n>> Directory: ',str(self.dir_stckproc))
#                     alert('error_beep')
#             else: 
#                 im_proc =  np.copy(self.im())      
#         return im_proc
        
#     def load_channel(self):
#         organ = self.parent_organ
#         ch_name = self.channel_no
        
#         self.to_mask = organ.imChannels[ch_name]['to_mask']
#         self.resolution = organ.imChannels[ch_name]['resolution']
#         self.dir_cho = Path(organ.imChannels[ch_name]['dir_cho'])
#         if self.to_mask:
#                 self.dir_mk = Path(organ.imChannels[ch_name]['dir_mk'])
#         self.masked = organ.imChannels[ch_name]['masked']
#         self.shape = tuple(organ.imChannels[ch_name]['shape'])
#         if 'shape_s3' in organ.imChannels[ch_name].keys():
#             self.shape_s3 = tuple(organ.imChannels[ch_name]['shape_s3'])
#         self.process = organ.imChannels[ch_name]['process']
#         contStack_dict = organ.imChannels[ch_name]['contStack']
#         for cont in contStack_dict.keys():
#             contStack_dict[cont]['s3_dir'] = Path(contStack_dict[cont]['s3_dir'])
#         self.contStack = contStack_dict
#         self.dir_stckproc = organ.imChannels[ch_name]['dir_stckproc']

#     def get_channel_no(self):
#         return self.channel_no

#     def get_resolution(self):
#         return self.resolution

#     def get_shape(self):
#         return self.shape
    
#     def add_contStack(self, contStack):
#         # Check first if the contStack has been already added to the channel
#         new = False
#         if contStack.cont_type not in self.contStack.keys():
#             new = True
            
#         if new: 
#             contStack_dict = copy.deepcopy(contStack.__dict__)
#             contStack_dict.pop('im_channel', None)
#             self.contStack[contStack.cont_type] = contStack_dict
#         else: # just update im_proc 
#             self.contStack[contStack.cont_type]['process'] = contStack.process
     
#     def maskIm(self):
#         #Check workflow status
#         workflow = self.parent_organ.workflow
#         process = ['ImProc', self.channel_no, 'A-MaskChannel','Status']
#         check_proc = get_by_path(workflow, process)
#         if check_proc == 'DONE':
#             q = 'You already masked this channel ('+ self.user_chName+'). Do you want to re-run it?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
#             proceed = ask4input(q, res, bool)
#         else: 
#             proceed = True
                
#         if proceed: 
#             #Load images
#             im_o = np.copy(self.im())
#             im_mask = io.imread(str(self.dir_mk))
#             #Process
#             print('\n---- Masking! ----')
#             if self.shape == im_mask.shape:
#                 #Check the dimensions of the mask with those of the image
#                 im_o[im_mask == False] = 0
#                 self.masked = True
#                 self.save_channel(im_proc=im_o)
                
#                 #Update organ workflow
#                 self.parent_organ.update_workflow(process, update = 'DONE')
                
#                 #self.parent_organ.workflow['ImProc'][self.channel_no]['A-MaskChannel']['Status'] = 'DONE'
#                 process_up = ['ImProc', self.channel_no,'Status']
#                 if get_by_path(workflow, process_up) == 'NI':
#                     self.parent_organ.update_workflow(process_up, update = 'Initialised')
                
#                 #Update channel process
#                 self.process.append('Masked')
                
#                 #Update organ imChannels
#                 self.parent_organ.imChannels[self.channel_no]['masked'] = True
#                 self.parent_organ.add_channel(self)
#                 self.parent_organ.save_organ()
                
#             else: 
#                 print('>> Error: Stack could not be masked (stack shapes did not match).')
#                 alert('error_beep')
                
#             process_up2 = ['ImProc','Status']
#             if get_by_path(workflow, process_up2) == 'NI':
#                 self.parent_organ.update_workflow(process_up2, update = 'Initialised')
            
#     def closeContours_auto(self):
#         #Check workflow status
#         workflow = self.parent_organ.workflow
#         process = ['ImProc', self.channel_no,'B-CloseCont','Steps','A-Autom','Status']
#         check_proc = get_by_path(workflow, process)
#         if check_proc == 'DONE':
#             q = 'You already closed automatically the contours of this channel ('+ self.user_chName+'). Do you want to re-run it?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
#             proceed = ask4input(q, res, bool)
#         else: 
#             proceed = True
                
#         if proceed: 
#             # Load image
#             im_proc = self.im_proc()
#             self.save_channel(im_proc=im_proc)
#             workflow = self.parent_organ.workflow
            
#             #Process
#             print('\n---- Closing Contours Auto! ----')
            
#             #Update organ workflow
#             self.parent_organ.update_workflow(process, update = 'DONE')

#             process_up = ['ImProc',self.channel_no,'B-CloseCont','Status']
#             if get_by_path(workflow, process_up) == 'NI':
#                 self.parent_organ.update_workflow(process_up, update = 'Initialised')
            
#             #Update channel process
#             self.process.append('ClosedCont-Auto')
            
#             #Update organ imChannels
#             self.parent_organ.add_channel(self)
#             self.parent_organ.save_organ()
            
#             process_up2 = ['ImProc','Status']
#             if get_by_path(workflow, process_up2) == 'NI':
#                 self.parent_organ.update_workflow(process_up2, update = 'Initialised')
                
#             #Update
#             # 'B-CloseCont':{'Status': 'NI',
#             #                 'Steps':{'A-Autom': {'Status': 'NI'},
#             #                                     # 'Range': None, 
#             #                                     # 'Range_completed': None}, 
        
#     def closeContours_manual(self):
#         #Check workflow status
#         workflow = self.parent_organ.workflow
#         process = ['ImProc', self.channel_no,'B-CloseCont','Steps','B-Manual','Status']
#         check_proc = get_by_path(workflow, process)
#         if check_proc == 'DONE':
#             q = 'You already finished closing manually the contours of this channel ('+ self.user_chName+'). Do you want to re-run this process and close some more?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
#             proceed = ask4input(q, res, bool)
#         else: 
#             proceed = True
                
#         if proceed: 
#             # Load image
#             im_proc = self.im_proc()
#             self.save_channel(im_proc=im_proc)
            
#             #Process
#             print('\n---- Closing Contours Manually! ----')
            
                    
#             #Update organ workflow
#             self.parent_organ.update_workflow(process, update = 'DONE')
            
#             process_up = ['ImProc',self.channel_no,'B-CloseCont','Status']
#             if get_by_path(workflow, process_up) == 'NI':
#                 self.parent_organ.update_workflow(process_up, update = 'Initialised')
            
            
#             #Update channel process
#             self.process.append('ClosedCont-Manual')
                    
#             #Update organ imChannels
#             self.parent_organ.add_channel(self)
#             self.parent_organ.save_organ()
            
#             process_up2 = ['ImProc','Status']
#             if get_by_path(workflow, process_up2) == 'NI':
#                 self.parent_organ.update_workflow(process_up2, update = 'Initialised')
            
#             #Update
#             # 'B-CloseCont':{'Status': 'NI',
#             #                         'B-Manual': {'Status': 'NI'},
#             #                                     # 'Range': None, 
#             #                                     # 'Range_completed': None}, 
            
#     def closeInfOutf(self):
#         #Check workflow status
#         workflow = self.parent_organ.workflow
#         process = ['ImProc', self.channel_no,'B-CloseCont','Steps','C-CloseInOut','Status']
#         check_proc = get_by_path(workflow, process)
#         if dict_gui['heart_default']:
#             txt_pr = 'inflow/outflow'
#         else: 
#             txt_pr = 'bottom/top'
#         if check_proc == 'DONE':
#             q = 'You already closed the '+txt_pr+' contours of this channel ('+ self.user_chName+'). Do you want to re-run this process and close some more?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
#             proceed = ask4input(q, res, bool)
#         else: 
#             proceed = True
                
#         if proceed: 
#             # Load image
#             im_proc = self.im_proc()
#             self.save_channel(im_proc=im_proc)
            
#             #Process
#             print('\n---- Closing Inf/Ouft! ----')
            
#             #Update organ workflow
#             self.parent_organ.update_workflow(process, update = 'DONE')
            
#             process_up = ['ImProc',self.channel_no,'B-CloseCont','Status']
#             if get_by_path(workflow, process_up) == 'NI':
#                 self.parent_organ.update_workflow(process_up, update = 'Initialised')
            
#             # Update channel process
#             self.process.append('ClosedInfOutf')
            
#             #Update organ imChannels
#             self.parent_organ.add_channel(self)
            
#             #TO DO: Update general status of B-CloseCont to Done when confirmed
#             self.parent_organ.check_status(process = 'ImProc')
#             self.parent_organ.save_organ()
            
#             process_up2 = ['ImProc','Status']
#             if get_by_path(workflow, process_up2) == 'NI':
#                 self.parent_organ.update_workflow(process_up2, update = 'Initialised')
                
#             #Update 
#             # 'B-CloseCont':{'Status': 'NI',
#             #                         'C-CloseInOut': {'Status': 'NI'}}},

#     def selectContours(self):
#         #Check workflow status
#         workflow = self.parent_organ.workflow
#         process = ['ImProc', self.channel_no,'C-SelectCont','Status']
#         check_proc = get_by_path(workflow, process)
#         if check_proc == 'DONE':
#             q = 'You already selected the contours for this channel ('+ self.user_chName+'). Do you want to re-select them?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
#             proceed = ask4input(q, res, bool)
#         else: 
#             proceed = True
                
#         if proceed: 
#             # Load image
#             im_proc = self.im_proc()
#             self.save_channel(im_proc=im_proc)
            
#             #Process
#             print('\n---- Selecting Contours! ----')
            
#             #Update organ workflow
#             self.parent_organ.update_workflow(process, update = 'DONE')

#             #Update channel process
#             self.process.append('SelectCont')
                    
#             #Update organ imChannels
#             self.parent_organ.add_channel(self)
#             self.parent_organ.save_organ()
            
#             process_up2 = ['ImProc','Status']
#             if get_by_path(workflow, process_up2) == 'NI':
#                 self.parent_organ.update_workflow(process_up2, update = 'Initialised')
                
#             #Update
#             # 'C-SelectCont':{'Status': 'NI'},
#             #                 # 'Info': {'tuple_slices': None,
#             #                 #         'number_contours': None,
#             #                 #         'range': None}},
#             layerDict = {}
#             return layerDict
        
#         else: 
#             layerDict = {}
#             return layerDict
            

#     def create_chS3s (self, layerDict:dict):
#         #Check workflow status
#         workflow = self.parent_organ.workflow
#         process = ['ImProc', self.channel_no, 'D-S3Create','Status']
#         check_proc = get_by_path(workflow, process)
#         if check_proc == 'DONE':
#             q = 'You already created the contour stacks (S3s) of this channel ('+ self.user_chName+'). Do you want to re-create them?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
#             proceed = ask4input(q, res, bool)
#         else: 
#             proceed = True
                
#         if proceed: 
#             dirs_cont = []; shapes_s3 = []
#             for cont in ['int', 'ext', 'tiss']:
#                 s3 = ContStack(im_channel=self, cont_type=cont, layerDict=layerDict)#new=True,
#                 self.add_contStack(s3)
#                 dirs_cont.append(s3.s3_dir.is_file())
#                 shapes_s3.append(s3.shape_s3)
#                 #Update organ workflow
#                 process_cont = ['ImProc',self.channel_no,'D-S3Create','Info',cont,'Status']
#                 self.parent_organ.update_workflow(process_cont, update = 'DONE')
            
#             #Update organ workflow
#             if all(flag for flag in dirs_cont):
#                 if shapes_s3.count(shapes_s3[0]) == len(shapes_s3):
#                     self.shape_s3 = s3.shape_s3
#                 else: 
#                     print('>> Error: self.shape_s3 = s3.shape')
#                 self.parent_organ.update_workflow(process, update = 'DONE')

#             #Update channel process
#             self.process.append('CreateS3')
            
#             #Update organ imChannel
#             self.parent_organ.add_channel(self)
#             self.parent_organ.save_organ()
            
#             process_up2 = ['ImProc','Status']
#             if get_by_path(workflow, process_up2) == 'NI':
#                 self.parent_organ.update_workflow(process_up2, update = 'Initialised')
            
#     def load_chS3s (self, cont_types:list):
#         for cont in cont_types:
#             # print(cont)
#             s3 = ContStack(im_channel=self, cont_type=cont)#, new=False)
#             setattr(self, 's3_'+cont, s3)
#             self.add_contStack(s3)
        
#         #Update channel process
#         self.process.append('LoadS3')
        
#         #Update organ imChannel
#         self.parent_organ.add_channel(self)
#         self.parent_organ.save_organ()

#     def trimS3(self, cuts, cuts_out): 
#         #Check workflow status
#         workflow = self.parent_organ.workflow
#         process = ['ImProc', self.channel_no, 'E-TrimS3','Status']
#         check_proc = get_by_path(workflow, process)
#         if check_proc == 'DONE':
#             q = 'You already trimmed this channel ('+ self.user_chName+'). Do you want to re-run it?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
#             proceed = ask4input(q, res, bool)
#         else: 
#             proceed = True
                
#         if proceed: 
#             #Load s3s
#             self.load_chS3s(cont_types=['int', 'ext', 'tiss'])
            
#             #Process
#             print('\n---- Trimming S3s! ----')                             
#             if len(cuts) == 1:
#                 pl = cuts_out[cuts[0]]['plane_info_image']
#                 plm = cuts_out[cuts[0]]['plane_info_mesh']
#                 for s3 in [self.s3_int, self.s3_ext, self.s3_tiss]:
#                     s3.cutW1Plane(pl, cuts[0])
#                     #Update organ workflow
#                     process_cont = ['ImProc',self.channel_no,'E-TrimS3','Info',s3.cont_type,'Status']
#                     self.parent_organ.update_workflow(process_cont, update = 'DONE')
                    
#                 #Update mH_settings
#                 # Image
#                 proc_im = ['wf_info', 'ImProc', 'E-TrimS3','Planes', self.channel_no, 'cut_image']
#                 update_im = {cuts[0]:pl}
#                 self.parent_organ.update_settings(proc_im, update = update_im, mH='mH')
#                 # Mesh
#                 proc_mesh = ['wf_info', 'MeshesProc', 'B-TrimMesh','Planes', self.channel_no, 'cut_mesh']
#                 update_mesh = {cuts[0]:plm}
#                 self.parent_organ.update_settings(proc_mesh, update = update_mesh, mH='mH')
                
#             if len(cuts) == 2:
#                 for s3 in [self.s3_int, self.s3_ext, self.s3_tiss]:
#                     pl1 = cuts_out['bottom']['plane_info_image']
#                     pl1m = cuts_out['bottom']['plane_info_mesh']
#                     pl2 = cuts_out['top']['plane_info_image']
#                     pl2m = cuts_out['top']['plane_info_mesh']
#                     s3.cutW2Planes(pl1, pl2)
#                     #Update organ workflow
#                     process_cont = ['ImProc',self.channel_no,'E-TrimS3','Info',s3.cont_type,'Status']
#                     self.parent_organ.update_workflow(process_cont, update = 'DONE')
                
#                 #Update mH_settings   
#                 # Image
#                 proc_im = ['wf_info', 'ImProc', 'E-TrimS3','Planes', self.channel_no, 'cut_image']
#                 update_im =  {'bottom': pl1, 'top': pl2}
#                 self.parent_organ.update_settings(proc_im, update = update_im, mH = 'mH')
#                 # Mesh
#                 proc_mesh = ['wf_info', 'MeshesProc', 'B-TrimMesh','Planes', self.channel_no, 'cut_mesh']
#                 update_mesh = {'bottom': pl1m, 'top': pl2m}
#                 self.parent_organ.update_settings(proc_mesh, update = update_mesh, mH = 'mH')
  
              
#             #Update organ workflow 
#             self.parent_organ.update_workflow(process, update = 'DONE')
            
#             #Update channel process
#             self.process.append('TrimS3')
            
#             #Update organ imChannels
#             self.parent_organ.add_channel(self)
            
#             process_up2 = ['ImProc','Status']
#             if get_by_path(workflow, process_up2) == 'NI':
#                 self.parent_organ.update_workflow(process_up2, update = 'Initialised')
            
#             # Save organ
#             self.parent_organ.save_organ()
#             # Update status 
#             self.parent_organ.check_status(process = 'ImProc')
        
#     def s32Meshes(self, cont_types:list, keep_largest=False, rotateZ_90=True, new_set=False):

#         meshes_out = []
#         for mesh_type in cont_types:
#             name = self.channel_no + '_' + mesh_type
#             if name not in self.parent_organ.meshes.keys():
#                 keep_largest_f = keep_largest[mesh_type]
#                 print('>> New Mesh!')
#             else: 
#                 if new_set: 
#                     print('>> New_set = True')
#                     try: 
#                         keep_largest_f = keep_largest[mesh_type]
#                         print('>> New keep_largest')
#                     except:
#                         print('>> Old keep_largest')
#                         keep_largest_f = self.parent_organ.mH_settings['setup'][self.channel_no][mesh_type]['keep_largest']
#                     print('recreating mesh with new settings -keep largest')
#                 else: 
#                     keep_largest_f = keep_largest
#                     print('>> Recreating mesh with same settings as original')
#             mesh = Mesh_mH(self, mesh_type, keep_largest_f, rotateZ_90, new_set=new_set)#, new=True)
#             meshes_out.append(mesh)
            
#         return meshes_out
    
#     def createNewMeshes(self, cont_types:list, process:str, new_set = False):
                         
#         ch_no = self.channel_no
#         if process == 'AfterTrimming':
#             meshes_out = self.s32Meshes(cont_types, new_set=True)
#             for mesh_type in ['int', 'ext', 'tiss']:
#                 proc = ['MeshesProc', 'B-TrimMesh', ch_no, mesh_type,'Status']
#                 self.parent_organ.update_workflow(proc, 'DONE')
                
#             process_up = ['MeshesProc','B-TrimMesh','Status']
#             if get_by_path(self.parent_organ.workflow, process_up) == 'NI':
#                 self.parent_organ.update_workflow(process_up, update = 'Initialised')
                
#             self.parent_organ.check_status(process = 'MeshesProc')
                
#         # Save organ
#         self.parent_organ.save_organ()   
        
#         return meshes_out

#     def save_channel(self, im_proc):
#         im_name = self.parent_organ.user_organName + '_StckProc_' + self.channel_no + '.npy'
#         im_dir = self.parent_organ.info['dirs']['s3_numpy'] / im_name
#         np.save(im_dir, im_proc)
#         if not im_dir.is_file():
#             print('>> Error: Processed channel was not saved correctly!\n>> File: '+im_name)
#             alert('error_beep')
#         else: 
#             print('>> Processed channel saved correctly! - ', im_name)
#             # print('>> Directory: '+ str(im_dir)+'\n')
#             alert('countdown')
#             self.dir_stckproc = im_dir
    
#     def ch_clean (self, s3_mask, inverted=True, plot=False, im_every=25, proceed=None): 
#         """
#         Function to clean channel using the other as a mask
#         """
        
#         if proceed: #== None: 
#             workflow = self.parent_organ.workflow
#             s3s = [self.s3_int, self.s3_ext, self.s3_tiss]
#             process = ['ImProc',self.channel_no,'E-CleanCh', 'Status']
#             check_proc = get_by_path(workflow, process)
#             if check_proc == 'DONE':
#                 q = 'You already cleanes the '+ self.user_chName+' with the '+s3_mask.im_channel.user_chName+'. Do you want to re-run this process?'
#                 res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
#                 proceed2 = ask4input(q, res, bool)
#             else: 
#                 proceed2 = True
            
#         if proceed2: 
#             for s3 in s3s:
#                 print('>> Cleaning '+self.user_chName+' ('+ self.channel_no + '-' + s3.cont_type +')')
                    
#                 # What happens if the s3() are None? 
#                 s3_s = s3.s3()
#                 if not isinstance(s3_s, np.ndarray): 
#                     print('>> Error: Not isinstance(s3_s, np.array)')
#                     alert('clown')
#                     continue
#                 s3_mask_s = s3_mask.s3()
#                 if not isinstance(s3_mask_s, np.ndarray): 
#                     print('>> Error: not isinstance(s3_mask_s, np.array)')
#                     alert('clown')
#                     continue
#                 s3_bits = np.zeros_like(s3_s, dtype='uint8')
#                 s3_new =  np.zeros_like(s3_s, dtype='uint8')
        
#                 index = list(s3.shape_s3).index(min(s3.shape_s3))
#                 if index == 2:
#                     for slc in range(s3.shape_s3[2]):
#                         mask_slc = s3_mask_s[:,:,slc]
#                         toClean_slc = s3_s[:,:,slc]
        
#                         if inverted:
#                             # Invert ch to use as mask 
#                             inv_slc = np.where((mask_slc==0)|(mask_slc==1), mask_slc^1, mask_slc)
#                         else: 
#                             # Keep ch to use as mask as it is
#                             inv_slc = np.copy(mask_slc)
        
#                         # inverted_mask or mask AND ch1_2clean
#                         toRemove_slc = np.logical_and(toClean_slc, inv_slc)
#                         # Keep only the clean bit
#                         cleaned_slc = np.logical_xor(toClean_slc, toRemove_slc)
        
#                         if plot and slc in list(range(0,s3.shape_s3[0],im_every)):
#                             self.slc_plot(slc, inv_slc, toClean_slc, toRemove_slc, cleaned_slc, inverted)
        
#                         s3_bits[:,:,slc] = toRemove_slc
#                         s3_new[:,:,slc] = cleaned_slc
                        
#                     s3_new = s3_new.astype('uint8')
#                     s3.s3_save(s3_new)
#                     alert('whistle')   
                    
#                 else:
#                     print('>> Index different to 2, check!')
#                     alert('error_beep')
                
#                 #Update workflow 
#                 proc_up = ['ImProc',self.channel_no,'E-CleanCh','Info',s3.cont_type, 'Status']
#                 self.parent_organ.update_workflow(proc_up, 'DONE')
                
            
#             # Update organ workflow
#             self.parent_organ.update_workflow(process, 'DONE')
#             # Update mH_settings
#             proc_set = ['wf_info','ImProc','E-CleanCh','Settings']
#             self.parent_organ.update_settings(proc_set+['ch'], self.user_chName, 'mH')
#             self.parent_organ.update_settings(proc_set+['s3_mask'], s3_mask.cont_name, 'mH')
#             self.parent_organ.update_settings(proc_set+['inverted'],inverted, 'mH')
                
                  
#     def slc_plot (self, slc, mask_slc, toClean_slc, toRemove_slc, cleaned_slc, inverted):
#         """
#         Function to plot mask, original image and result
#         """
        
#         if inverted: 
#             txt = ['ch0_inv','ch1','ch0_inv AND ch1','ch0_inv AND ch1\nxOR ch1']
#         else: 
#             txt = ['ch0','ch1','ch0 AND ch1','ch0 AND ch1\nxOR ch1']
       
#         #Plot
#         fig, ax = plt.subplots(1, 4, figsize = (10,2.5))
#         fig.suptitle("Slice:"+str(slc), y=1.05, weight="semibold")
#         ax[0].imshow(mask_slc)
#         ax[1].imshow(toClean_slc)
#         ax[2].imshow(toRemove_slc)
#         ax[3].imshow(cleaned_slc)
#         for num in range(0,4,1):
#             ax[num].set_title(txt[num])
#             ax[num].set_xticks([])
#             ax[num].set_yticks([])

#         plt.show()
        
# class ImChannelNS(): #channel

#     'morphoHeart Image Channel Negative Space'
    
#     def __init__(self, organ:Organ, ch_name:str):#, new=True):

#         self.parent_organ = organ
#         self.parent_organ_name = organ.user_organName
#         self.channel_no = ch_name
#         self.user_chName = organ.mH_settings['general_info'][ch_name]['user_chName']
#         self.ch_relation = 'negative-space'
#         if self.channel_no not in organ.imChannelNS.keys():
#             print('>> New ChannelNS')
#             self.new_ImChannelNS()
#         else: 
#             print('>> Loading ChannelNS')
#             self.load_channel()
    
#     def new_ImChannelNS (self):
#         organ = self.parent_organ
#         ch_name = self.channel_no
        
#         self.resolution = organ.info['resolution']
#         self.process = ['Init']
#         self.contStack = {}
        
#         # external contour
#         ext_s3_name = organ.mH_settings['general_info'][ch_name]['ch_ext'][0]
#         ext_s3_type = organ.mH_settings['general_info'][ch_name]['ch_ext'][1]
#         # internal contour
#         int_s3_name = organ.mH_settings['general_info'][ch_name]['ch_int'][0]
#         int_s3_type = organ.mH_settings['general_info'][ch_name]['ch_int'][1]
        
#         self.setup_NS = {'ext':{'name': ext_s3_name, 'type': ext_s3_type}, 
#                       'int':{'name': int_s3_name, 'type': int_s3_type}}
        
#         organ.add_channelNS(imChannelNS=self)
#         organ.check_status(process='ImProc')
#         organ.save_organ()
    
#     def load_channel(self):
        
#         organ = self.parent_organ
#         ch_name = self.channel_no
        
#         self.resolution = organ.imChannelNS[ch_name]['resolution']
#         self.process = organ.imChannelNS[ch_name]['process']
#         contStack_dict = organ.imChannelNS[ch_name]['contStack']
#         for cont in contStack_dict.keys():
#             contStack_dict[cont]['s3_dir'] = Path(contStack_dict[cont]['s3_dir'])
#             contStack_dict[cont]['shape_s3'] = tuple(contStack_dict[cont]['shape_s3'])
#         self.contStack = contStack_dict
#         self.setup_NS = organ.imChannelNS[ch_name]['setup_NS']
        
#         # organ.add_channel(imChannel=self)
        
#     def create_chNSS3s(self, plot=False):
#         organ = self.parent_organ
#         ext_s3_name = self.setup_NS['ext']['name']
#         ext_s3_type = self.setup_NS['ext']['type']
#         ext_s3 = ContStack(im_channel=organ.obj_imChannels[ext_s3_name], 
#                            cont_type=ext_s3_type)#, new=False)
#         self.s3_ext = ext_s3
#         self.add_contStack(ext_s3, cont_type = 'ext')
        
#         int_s3_name = self.setup_NS['int']['name']
#         int_s3_type = self.setup_NS['int']['type']
#         int_s3 = ContStack(im_channel=organ.obj_imChannels[int_s3_name], 
#                            cont_type=int_s3_type)#, new=False)
#         self.s3_int = int_s3
#         self.add_contStack(int_s3, cont_type = 'int')
        
#         tiss_s3 = ContStack(im_channel = self, cont_type = 'tiss',
#                             layerDict=plot)#,  new = True)
#         self.s3_tiss = tiss_s3
#         self.add_contStack(tiss_s3, cont_type = 'tiss')
        
#     def load_chS3s (self, cont_types:list):
#         for cont in cont_types:
#             # print(cont)
#             s3 = ContStack(im_channel=self, cont_type=cont)#, new=False)
#             setattr(self, 's3_'+cont, s3)
#             self.add_contStack(s3, cont)
        
#         #Update channel process
#         self.process.append('LoadS3')
        
#         #Update organ imChannel
#         self.parent_organ.add_channelNS(imChannelNS=self)
#         self.parent_organ.save_organ()
     
#     def get_channel_no(self):
#         return self.channel_no

#     def get_resolution(self):
#         return self.resolution
    
#     def add_contStack(self, contStack, cont_type):
#         # Check first if the contStack has been already added to the channel
#         new = False
#         if cont_type not in self.contStack.keys():
#             new = True
            
#         if new: 
#             contStack_dict = {}
#             contStack_dict['cont_type'] = cont_type
#             contStack_dict['imfilled_name'] = contStack.imfilled_name
#             contStack_dict['cont_name'] = contStack.cont_name
#             contStack_dict['s3_file'] = contStack.s3_file
#             contStack_dict['s3_dir'] = contStack.s3_dir
#             contStack_dict['shape_s3'] = contStack.shape_s3
#             contStack_dict['process'] = contStack.process
#             self.contStack[cont_type] = contStack_dict
#         else: # just update process 
#             self.contStack[cont_type]['process'] = contStack.process

    
#     def create_s3_tiss (self, plot=False, im_every=25): 
#         """
#         Function to extract the negative space channel
#         """        
#         #Check workflow status
#         workflow = self.parent_organ.workflow
#         process = ['ImProc', self.channel_no,'D-S3Create','Status']
#         check_proc = get_by_path(workflow, process)
#         if check_proc == 'DONE':
#             q = 'You already extracted the '+ self.user_chName+' from the negative space. Do you want to re-run this process?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
#             proceed = ask4input(q, res, bool)
#         else: 
#             proceed = True
                
#         if proceed: 
#             print('>> Extracting '+self.user_chName+'!')
#             s3 = self.s3_ext.s3()
#             s3_mask = self.s3_int.s3()
            
#             s3_bits = np.zeros_like(s3, dtype='uint8')
#             s3_new =  np.zeros_like(s3, dtype='uint8')
    
#             index = list(s3.shape).index(min(s3.shape))
#             if index == 2:
#                 for slc in range(s3.shape[2]):
#                     mask_slc = s3_mask[:,:,slc]
#                     toClean_slc = s3[:,:,slc]
#                     # Keep ch to use as mask as it is
#                     inv_slc = np.copy(mask_slc)
    
#                     # inverted_mask or mask AND ch1_2clean
#                     toRemove_slc = np.logical_and(toClean_slc, inv_slc)
#                     # Keep only the clean bit
#                     cleaned_slc = np.logical_xor(toClean_slc, toRemove_slc)
    
#                     if plot and slc in list(range(0,s3.shape[0],im_every)):
#                         self.slc_plot(slc, inv_slc, toClean_slc, toRemove_slc, cleaned_slc, inverted=False)
    
#                     s3_bits[:,:,slc] = toRemove_slc
#                     s3_new[:,:,slc] = cleaned_slc
                    
#                 s3_new = s3_new.astype('uint8')
#                 alert('whistle')   
                
#             else:
#                 print('>> Index different to 2, check!')
#                 alert('error_beep')

#         workflow['ImProc'][self.channel_no]['Status'] = 'DONE'
#         workflow['ImProc'][self.channel_no]['D-S3Create']['Status'] = 'DONE'
        
#         return s3_new
    
#     def slc_plot (self, slc, mask_slc, toClean_slc, toRemove_slc, cleaned_slc, inverted):
#         """
#         Function to plot mask, original image and result
#         """
       
#         txt = ['ch0_int','ch1_ext','ch0_int AND ch1_ext','layer in between']

#         #Plot
#         fig, ax = plt.subplots(1, 4, figsize = (10,2.5))
#         fig.suptitle("Slice:"+str(slc), y=1.05, weight="semibold")
#         ax[0].imshow(mask_slc)
#         ax[1].imshow(toClean_slc)
#         ax[2].imshow(toRemove_slc)
#         ax[3].imshow(cleaned_slc)
#         for num in range(0,4,1):
#             ax[num].set_title(txt[num])
#             ax[num].set_xticks([])
#             ax[num].set_yticks([])

#         plt.show()
        
#     # func - s32Meshes
#     def s32Meshes(self, cont_types:list, keep_largest=False, rotateZ_90=True, new_set=False):
#         meshes_out = []
#         for mesh_type in cont_types:
#             name = self.channel_no + '_' + mesh_type
#             if name not in self.parent_organ.meshes.keys():
#                 keep_largest_f = keep_largest[mesh_type]
#                 print('>> New mesh NS!')
#             else: 
#                 if new_set: 
#                     print('>> New_set = True')
#                     try: 
#                         keep_largest_f = keep_largest[mesh_type]
#                         print('>> New keep_largest')
#                     except: 
#                         print('>> Old keep_largest')
#                         keep_largest_f = self.parent_organ.mH_settings['setup'][self.channel_no][mesh_type]['keep_largest']
#                     print('>> Recreating mesh with new settings -keep largest')
#                 else: 
#                     keep_largest_f = keep_largest
#                     print('>> Recreating mesh with same settings as original')
#             mesh = Mesh_mH(self, mesh_type, keep_largest_f, rotateZ_90, new_set=new_set)#, new=True)
#             meshes_out.append(mesh)
            
#         return meshes_out
        
# class ContStack(): 
#     'morphoHeart Contour Stack Class'
    
#     def __init__(self, im_channel:Union[ImChannel,ImChannelNS], 
#                              cont_type:str, layerDict={}):#new=True,
        
#         cont_types = ['int', 'ext', 'tiss']
#         names = ['imIntFilledCont', 'imExtFilledCont', 'imAllFilledCont']

#         index = cont_types.index(cont_type)
#         self.cont_type = cont_type
#         self.imfilled_name = names[index]
#         self.im_channel = im_channel
#         self.cont_name = im_channel.channel_no+'_'+self.cont_type
        
#         parent_organ = im_channel.parent_organ
#         self.s3_file = parent_organ.user_organName + '_s3_' + im_channel.channel_no + '_' + self.cont_type + '.npy'
#         self.s3_dir = parent_organ.dir_res / 's3_numpy' / self.s3_file
        
#         if self.cont_type not in self.im_channel.contStack.keys():
#         # if new: 
#             if im_channel.channel_no == 'chNS':
#                 s3 = im_channel.create_s3_tiss(plot=layerDict)
#             else: 
#                 s3 = self.s3_create(layerDict = layerDict)
#             self.s3_save(s3)
#             self.shape_s3 = s3.shape
#             self.process = ['Init']
#         else: 
#             s3 = self.s3()
#             self.shape_s3 = s3.shape
#             self.process = im_channel.contStack[cont_type]['process']
#             self.process.append('Loaded')
    
#     def s3_create(self, layerDict:dict):
#         x_dim = self.im_channel.shape[0]
#         y_dim = self.im_channel.shape[1]
#         z_dim = self.im_channel.shape[2]
        
#         s3 = np.empty((x_dim,y_dim,z_dim+2))
#         for pos, keySlc in enumerate(layerDict.keys()):
#             if keySlc[0:3] == "slc":
#                 slcNum = int(keySlc[3:6])
#                 im_FilledCont = layerDict[keySlc][self.cont_type]
#                 s3[:,:,slcNum+1] = im_FilledCont
#         s3 = s3.astype('uint8')
#         parent_organ = self.im_channel.parent_organ
#         parent_organ.workflow['ImProc'][self.im_channel.channel_no]['D-S3Create']['Status'] = 'DONE'
        
#         return s3
    
#     def s3(self):
#         if self.s3_dir.is_file():
#             s3 = np.load(self.s3_dir)
#         else: 
#             print('>> Error: s3 file does not exist!\n>> File: '+self.s3_file)
#             alert('error_beep')
#             s3 = None
            
#         return s3

#     def s3_save(self, s3):
#         organ = self.im_channel.parent_organ
#         dir2save = organ.info['dirs']['s3_numpy'] / self.s3_file
#         np.save(dir2save, s3)
#         if not dir2save.is_file():
#             print('>> Error: s3 file was not saved correctly!\n>> File: '+self.s3_file)
#             alert('error_beep')
#         else: 
#             print('>> s3 file saved correctly! - ', self.im_channel.channel_no, '-', self.cont_type)
#             # print('>> Directory: '+ str(dir2save)+'\n')
#             alert('countdown')
            
        
#     def cutW2Planes(self, pl1, pl2):
#         """
#         Function used to cut inflow AND outflow tract of the s3 mask (s3_cut) given as input
    
#         """
#         #Load s3 and resolution
#         s32cut = self.s3()
#         resolution = self.im_channel.resolution
        
#         # Get dimensions of external stack
#         xdim, ydim, zdim = s32cut.shape
#         # Reshape stacks as a vector
#         s3_cut_v = s32cut.reshape(-1)
    
#         # Get vectors of x,y and z positions
#         pix_coord_pos = np.where(s32cut >= 0)
#         del s32cut
#         # Trasform coordinate positions to um using resolution
#         pix_um = np.transpose(np.asarray([pix_coord_pos[i]*resolution[i] for i in range(len(resolution))]))
#         del pix_coord_pos
    
#         normal_inf = unit_vector(pl1['pl_normal'])#pls_normal[0])
#         normal_outf = unit_vector(pl2['pl_normal'])#pls_normal[1])
    
#         # Find all the d values of pix_um
#         d_pix_um_Inf = np.dot(np.subtract(pix_um,np.array(pl1['pl_centre'])),np.array(normal_inf))
#         d_pix_um_Outf = np.dot(np.subtract(pix_um,np.array(pl2['pl_centre'])),np.array(normal_outf))
#         del pix_um
    
#         # Clear vector d_pix_um using only those that are 1 in stack
#         d_pve_pix_um_Inf = s3_cut_v*d_pix_um_Inf
#         d_pve_pix_um_Outf = s3_cut_v*d_pix_um_Outf
#         del d_pix_um_Inf, d_pix_um_Outf
    
#         # Duplicate s3f_v to initialise stacks without inflow
#         s3f_all_v = np.copy(s3_cut_v)
#         s3f_all_v.astype('uint8')
#         del s3_cut_v
    
#         # Find all positions in d_pve_pix_um that are at either side of the planes (outside of mesh)
#         pos_outside_inf = np.where(d_pve_pix_um_Inf < 0)[0]
#         pos_outside_outf = np.where(d_pve_pix_um_Outf > 0)[0]
#         del d_pve_pix_um_Inf, d_pve_pix_um_Outf
    
#         # Remove the points that are outside of the mesh (inflow)
#         s3f_all_v[pos_outside_inf] = 0
#         del pos_outside_inf
    
#         # Remove the points that are outside of the mesh (ouflow)
#         s3f_all_v[pos_outside_outf] = 0
#         del pos_outside_outf
    
#         # Reshape vector into matrix/stack
#         s3f_cut = s3f_all_v.reshape((xdim, ydim, zdim))
        
#         # Save new s3
#         self.s3_save(s3f_cut)
#         alert('woohoo')
    
#         # return s3f_cut
    
#     # func - cutInfOrOutfOptMx
#     def cutW1Plane (self, pl, cut):
#         """
#         Function used to cut inflow OR outflow tract of the s3 mask (s3_cut) given as input
    
#         """
    
#         # print('- Cutting s3 - ' + option+' '+mesh_name)
#         #Load s3 and resolution
#         s32cut = self.s3()
#         resolution = self.im_channel.resolution
    
#         # Get dimensions of external stack
#         xdim, ydim, zdim = s32cut.shape
#         # Reshape stacks as a vector
#         s3_cut_v = s32cut.reshape(-1)
    
#         # Get vectors of x,y and z positions
#         pix_coord_pos = np.where(s32cut >= 0)
#         del s32cut
#         # Trasform coordinate positions to um using resolution
#         pix_um = np.transpose(np.asarray([pix_coord_pos[i]*resolution[i] for i in range(len(resolution))]))
#         del pix_coord_pos
    
#         normal  = unit_vector(pl['pl_normal'])
#         # Find all the d values of pix_um
#         d_pix_um = np.dot(np.subtract(pix_um,np.array(pl['pl_centre'])),np.array(normal))
    
#         # Clear vector d_pix_um using only those that are 1 in stack
#         d_pve_pix_um = s3_cut_v*d_pix_um
#         del pix_um
    
#         # Duplicate s3f_v to initialise stacks without inflow/outflow
#         s3f_all_v = np.copy(s3_cut_v)
#         s3f_all_v.astype('uint8')
#         del s3_cut_v
    
#         # Find all positions in d_pve_pix_um that are at either side of the planes (outside of mesh)
#         if cut == 'inflow tract' or cut == 'bottom':
#             pos_outside = np.where(d_pve_pix_um < 0)[0]
#         elif cut == 'outflow tract' or cut == 'top':
#             pos_outside = np.where(d_pve_pix_um > 0)[0]
#         del d_pve_pix_um
    
#         # Remove the points that are outside of the mesh (inflow/outflow)
#         s3f_all_v[pos_outside] = 0
#         del pos_outside
    
#         # Reshape vector into matrix/stack
#         s3f_cut = s3f_all_v.reshape((xdim, ydim, zdim))
#         del s3f_all_v
        
#         # Save new s3
#         self.s3_save(s3f_cut)
#         alert('woohoo')

   
# class Mesh_mH():
#     'morphoHeart Mesh Class'
    
#     def __init__(self, imChannel:ImChannel, mesh_type:str, 
#                  keep_largest:bool, rotateZ_90=True, new_set=False):#, new=True):
        
#         self.parent_organ = imChannel.parent_organ
#         self.imChannel = imChannel
#         self.channel_no = imChannel.channel_no
#         self.user_meshName = self.parent_organ.mH_settings['general_info'][self.channel_no]['user_chName']
#         self.mesh_type = mesh_type
#         self.legend = self.user_meshName+'_'+self.mesh_type
#         self.name = self.channel_no +'_'+self.mesh_type
#         self.resolution = imChannel.get_resolution()
        
#         wf = ['MeshesProc','A-Create3DMesh', imChannel.channel_no, mesh_type] 
#         if self.name not in self.parent_organ.meshes.keys():
#             print('>> New mesh -', self.name)
#             new = True
#             self.keep_largest = keep_largest
#             self.rotateZ_90 = rotateZ_90
            
#             self.create_mesh(keep_largest = keep_largest, rotateZ_90 = rotateZ_90)
#             self.color = self.parent_organ.mH_settings['setup'][self.channel_no][self.mesh_type]['color']
#             self.alpha = 0.05
            
#             #Update settings
#             set_proc = ['setup', self.channel_no, self.mesh_type]
#             self.parent_organ.update_settings(set_proc+['keep_largest'], self.keep_largest, 'mH')
#             self.parent_organ.update_settings(set_proc+['rotateZ_90'], self.rotateZ_90, 'mH')
#             self.parent_organ.update_settings(set_proc+['alpha'], self.alpha, 'mH')
            
#             # Update workflow
#             if 'NS' not in self.channel_no:
#                 self.parent_organ.update_workflow(wf+['Status'], update = 'DONE')
#             else: 
#                 self.parent_organ.update_workflow(wf[0:3]+['Status'], update = 'DONE')
            
#             process_up = ['MeshesProc','A-Create3DMesh','Status']
#             if get_by_path(self.parent_organ.workflow, process_up) == 'NI':
#                 self.parent_organ.update_workflow(process_up, update = 'Initialised')
            
#             process_up2 = ['MeshesProc','Status']
#             if get_by_path(self.parent_organ.workflow, process_up2) == 'NI':
#                 self.parent_organ.update_workflow(process_up2, update = 'Initialised')
                
#             self.dirs = {'mesh': None, 'arrays': None}
#             self.parent_organ.check_status(process = 'MeshesProc')
#             self.mesh_meas = {}
        
#         else: 
#             new = False
#             self.color = self.parent_organ.mH_settings['setup'][self.channel_no][self.mesh_type]['color']
#             self.alpha = self.parent_organ.mH_settings['setup'][self.channel_no][self.mesh_type]['alpha']
#             self.s3_dir = self.imChannel.contStack[self.mesh_type]['s3_dir']
#             if new_set: 
#                 self.keep_largest = keep_largest
#                 self.rotateZ_90 = rotateZ_90
#                 print('>> Re-creating mesh -', self.name)
#                 self.create_mesh(keep_largest = keep_largest, rotateZ_90 = rotateZ_90)
#             else: 
#                 self.keep_largest = self.parent_organ.mH_settings['setup'][self.channel_no][self.mesh_type]['keep_largest']
#                 self.rotateZ_90 = self.parent_organ.mH_settings['setup'][self.channel_no][self.mesh_type]['rotateZ_90']
#                 print('>> Loading mesh-', self.name)
#                 self.load_mesh()
#                 if self.name in self.parent_organ.objects['Centreline'].keys():
#                     if self.parent_organ.workflow['MeshesProc']['C-Centreline']['buildCL']['Status'] == 'DONE':
#                         self.set_centreline()
#             self.dirs = self.parent_organ.meshes[self.name]['dirs']
#             if self.dirs['mesh'] != None: 
#                 for n, meas_mesh in enumerate(self.dirs['mesh'].keys()):
#                     if n == 0:
#                         self.mesh_meas = {}
#                     if 'ball' in meas_mesh:
#                         n_type = meas_mesh.split('(')[1][:-1]
#                         m_ball = self.balloon_mesh(n_type = n_type)
#                         self.mesh_meas[meas_mesh] = m_ball
#                     elif 'thck' in meas_mesh: 
#                         n_type = meas_mesh.split('(')[1][:-1]
#                         m_thck = self.thickness_mesh(n_type = n_type)
#                         self.mesh_meas[meas_mesh] = m_thck
#             else: 
#                 self.mesh_meas = {}
            
#         self.mesh.color(self.color)
#         self.mesh.alpha(self.alpha)
#         if new or new_set: 
#             self.parent_organ.add_mesh(self)
#             self.save_mesh()

    
#     def create_mesh(self, keep_largest:bool, rotateZ_90:bool):
#         # Extract vertices, faces, normals and values of each mesh
#         s3_type = 's3_'+self.mesh_type
#         try: 
#             s3 = getattr(self.imChannel, s3_type)
#         except: 
#             self.imChannel.load_chS3s(cont_types=[self.mesh_type])
#             s3 = getattr(self.imChannel, s3_type)
            
#         self.s3_dir = s3.s3_dir
#         s3s3 = s3.s3()
#         verts, faces, _, _ = measure.marching_cubes(s3s3, spacing=self.resolution, method='lewiner')
    
#         # Create meshes
#         mesh = vedo.Mesh([verts, faces])
#         if keep_largest:
#             mesh = mesh.extractLargestRegion()
#         if rotateZ_90:
#             mesh.rotateZ(-90)
#         mesh.legend(self.legend).wireframe()
#         self.mesh = mesh
    
#     def load_mesh(self):
#         parent_organ = self.parent_organ
#         # mesh_name = parent_organ.user_organName+'_'+self.legend+'.vtk'
#         mesh_name = parent_organ.user_organName+'_'+self.name+'.vtk'
#         mesh_dir = parent_organ.info['dirs']['meshes'] / mesh_name
#         mesh_out = vedo.load(str(mesh_dir))
#         mesh_out.legend(self.legend).wireframe()
#         self.dir_out = mesh_dir
#         self.mesh = mesh_out

#     def save_mesh(self, m_type='self', ext='.vtk'):
#         parent_organ = self.parent_organ
#         if m_type == 'self':
#             if ext != '.vtk':
#                 mesh_name = parent_organ.user_organName+'_'+self.legend+ext
#             else: #== .vtk
#                 mesh_name = parent_organ.user_organName+'_'+self.name+ext
#             mesh_dir = parent_organ.info['dirs']['meshes'] / mesh_name
#             self.dir_out = mesh_dir
#             mesh_out = self.mesh
            
#         elif 'ball' in m_type or 'thck' in m_type: 
#             if ext != '.vtk':
#                 mesh_name = parent_organ.user_organName+'_'+self.legend+'_CM'+m_type+ext
#             else: #== .vtk
#                 mesh_name = parent_organ.user_organName+'_'+self.name+'_CM'+m_type+ext
#             mesh_dir = parent_organ.info['dirs']['meshes'] / mesh_name
#             mesh_out = self.mesh_meas[m_type]
#             if self.dirs['mesh'] == None: 
#                 self.dirs['mesh'] = {m_type: mesh_dir}
#             else:
#                 self.dirs['mesh'][m_type] = mesh_dir
            
#         mesh_out.write(str(mesh_dir))
#         print('>> Mesh '+mesh_name+' has been saved!')
#         alert('countdown')        
#         self.parent_organ.add_mesh(self)
    
#     def save_array(self, array, m_type):
        
#         parent_organ = self.parent_organ        
#         # title = parent_organ.user_organName+'_'+self.legend+'--'+m_type
#         title = parent_organ.user_organName+'_'+self.name+'_CM'+m_type
#         np2save_dir = self.parent_organ.info['dirs']['csv_all'] / title
#         np.save(np2save_dir, array)
#         if self.dirs['arrays'] == None: 
#             self.dirs['arrays'] = {m_type: np2save_dir}
#         else:
#             self.dirs['arrays'][m_type] = np2save_dir
            
#         np2save_dirf = Path(str(np2save_dir)+'.npy')
#         if not np2save_dirf.is_file():
#             print('>> Error: Array was not saved correctly!\n>> File: '+title)
#             alert('error_beep')
#         else: 
#             print('>> Project settings file saved correctly!\n>> File: '+title)
#             alert('countdown')
            
#     def mesh4CL(self):
#         """
#         Function that cleans and smooths meshes given as input to get centreline using VMTK
    
#         """
#         mesh4cl = self.mesh.clone()
#         print('>> Cleaning mesh '+self.legend)
#         print("\t- Original number of points making up mesh: ", mesh4cl.NPoints())
#         # Reduce the number of points that make up the mesh
#         mesh4cl.subsample(fraction = 0.005)#tol=0.005)
#         print("\t- Number of points after cleaning surface: ",mesh4cl.NPoints(),'\n- Smoothing mesh...', self.legend)
                
#         # Smooth mesh
#         mesh4cl_cut = mesh4cl.clone().smooth_mls_2d(f=0.2)
#         mesh4cl_cut.legend(self.legend+"-C&S").color(self.color)
#         print('>> Mesh smoothed!')
#         alert('woohoo')

#         return mesh4cl_cut
    
#     def set_centreline(self):
#         try: 
#             cl_info = self.parent_organ.objects['Centreline'][self.name]
#             self.centreline_info = cl_info
#             print('>> Centerline has been set for ', self.name)
#         except: 
#             print('>> No centreline has been created for this mesh - ', self.name)

#     def get_channel_no(self):
#         return self.channel_no
    
#     def get_user_meshName(self):
#         return self.user_meshName
    
#     def get_legend(self):
#         return self.mesh.legend
    
#     def change_user_meshName(self, new_user_meshName):
#         self.user_meshName = new_user_meshName
    
#     def get_mesh_type(self):
#         return self.mesh_type
    
#     def get_imChannel(self):
#         return self.imChannel
    
#     def get_organ(self):
#         return self.parent_organ
    
#     def set_alpha(self, mesh_alpha):      
#         self.mesh.alpha(mesh_alpha)
#         self.alpha = mesh_alpha
#         #Update settings
#         set_proc = ['setup', self.channel_no, self.mesh_type]
#         self.parent_organ.update_settings(set_proc+['alpha'], self.alpha, 'mH')
        
#         self.parent_organ.meshes[self.name]['alpha'] = self.alpha
#         self.parent_organ.save_organ()
    
#     def get_alpha(self):
#         return self.mesh_alpha
        
#     def set_color(self, mesh_color):
#         self.mesh.color(mesh_color)
#         self.color = mesh_color
#         #Update settings
#         set_proc = ['setup', self.channel_no, self.mesh_type]
#         self.parent_organ.update_settings(set_proc+['color'], self.color, 'mH')
        
#         self.parent_organ.meshes[self.name]['color'] = self.color
#         self.parent_organ.save_organ()
        
#     def get_color(self):
#         return self.mesh_color   
        
#     def get_mesh(self):
#         try: 
#             return self.mesh 
#         except:
#             self.load_mesh()
#             return self.mesh
    
#     def thickness_mesh(self, n_type, color_map = 'turbo', alpha=1):
#         try: 
#             mesh_out = self.mesh_meas['thck('+n_type+')']
#             print('>> Extracting mesh from mesh_meas attribute')
#             return mesh_out.alpha(alpha)
#         except: 
#             dir_mesh = self.dirs['mesh']['thck('+n_type+')']
#             dir_npy = Path(str(self.dirs['arrays']['thck('+n_type+')'])+'.npy')
#             # print(dir_mesh, dir_npy)
#             if dir_mesh.is_file() and dir_npy.is_file():
#                 name = 'Thickness'
#                 # title = self.legend+'\n'+name+' [um]\n('+n_type+')'
#                 title = self.legend+'\n'+name+' [um]\n('+n_type.replace('TO','>')+')'
#                 mesh_out = self.load_meas_mesh(dir_mesh, dir_npy, title, 
#                                                color_map=color_map, alpha=alpha)
#                 return mesh_out.alpha(alpha)
#             else: 
#                 print('>> Error: Unable to load mesh', self.name,'-',n_type)
#                 alert('error_beep')
#                 return None
        
#     def balloon_mesh(self, n_type, color_map = 'turbo', alpha=1):
#         try: 
#             mesh_out = self.mesh_meas['ballCL('+n_type+')']
#             print('>> Extracting mesh from mesh_meas attribute')
#             return mesh_out.alpha(alpha)
#         except: 
#             dir_mesh = self.dirs['mesh']['ballCL('+n_type+')']
#             dir_npy = Path(str(self.dirs['arrays']['ballCL('+n_type+')'])+'.npy')
#             # print(dir_mesh, dir_npy)
#             if dir_mesh.is_file() and dir_npy.is_file():
#                 name = 'Ballooning'
#                 # title = self.legend+'\n'+name+' [um]\n('+n_type+')'
#                 title = self.legend+'\n'+name+' [um]\n('+n_type+')'
#                 mesh_out = self.load_meas_mesh(dir_mesh, dir_npy, title, 
#                                                color_map=color_map, alpha=alpha)
#                 return mesh_out.alpha(alpha)
#             else: 
#                 print('>> Error: Unable to load mesh', self.name,'-',n_type)
#                 alert('error_beep')
#                 return None
        
#     def load_meas_mesh(self, dir_mesh, dir_npy, title, color_map, alpha):
#         title_print = title.replace('\n', ' ')
#         print('>> Loading mesh '+title_print)
#         mesh_out = vedo.load(str(dir_mesh))
#         npy_colour = np.load(dir_npy)
        
#         # Assign colour
#         mesh_out.pointdata['Distance'] = npy_colour
#         vmin, vmax = np.min(npy_colour),np.max(npy_colour)
#         mesh_out.cmap(color_map)
#         mesh_out.alpha(alpha)
#         mesh_out.add_scalarbar(title=title, pos=(0.8, 0.05))
#         mesh_out.mapper().SetScalarRange(vmin,vmax)
#         mesh_out.legend(title)
        
#         return mesh_out
        
#     def get_centreline(self, nPoints=300, color='deepskyblue'): 
#         try: 
#             points = self.centreline_info['points']
#             kspl = vedo.KSpline(points, res = nPoints).color(color).lw(5).legend('CL_'+self.name)
#             return kspl
#         except: 
#             print('>> No centreline has been created for this mesh - ', self.name)
#             return None
        
#     def get_linLine(self, color='aqua'):
#         cl_final =  self.get_centreline()
#         cl_points = cl_final.points()
#         cl_pt0 = cl_points[0]
#         cl_ptm1 = cl_points[-1]
         
#         #Create linear line
#         linLine = vedo.Line(cl_pt0, cl_ptm1, c=color, lw=5)
        
#         return linLine

#     def get_clRibbon(self, nPoints, nRes, pl_normal, clRib_type):
#         """
#         Function that creates dorso-ventral extended centreline ribbon
#         """
        
#         cl = self.get_centreline(nPoints)
#         pts_cl = cl.points()
        
#         # Extended centreline
#         nn = -20
#         inf_ext_normal = (pts_cl[nn]+(pts_cl[-1]-pts_cl[nn])*5)#*70
#         outf_ext_normal = (pts_cl[0]+(pts_cl[0]-pts_cl[1])*100)#*70 (test for LnR cut Jun14.22)
      
#         pts_cl_ext = np.insert(pts_cl,0,np.transpose(outf_ext_normal), axis=0)
#         pts_cl_ext = np.insert(pts_cl_ext,len(pts_cl_ext),np.transpose(inf_ext_normal), axis=0)
    
#         # Increase the resolution of the extended centreline and interpolate to unify sampling
#         xd = np.diff(pts_cl_ext[:,0])
#         yd = np.diff(pts_cl_ext[:,1])
#         zd = np.diff(pts_cl_ext[:,2])
#         dist = np.sqrt(xd**2+yd**2+zd**2)
#         u = np.cumsum(dist)
#         u = np.hstack([[0],u])
#         t = np.linspace(0, u[-1], nRes)#601
#         resamp_pts = interpn((u,), pts_cl_ext, t)
#         kspl_ext = vedo.KSpline(resamp_pts, res=nRes).color('purple').legend('ExtendedCL')#601
    
#         pl_linLine_unitNormal = unit_vector(pl_normal)
#         pl_linLine_unitNormal120 = pl_linLine_unitNormal*120
    
#         if clRib_type == 'ext2sides': # Names are switched but it works
#             x_cl, y_cl, z_cl = pl_linLine_unitNormal120
#             kspl_ext_D = kspl_ext.clone().x(x_cl).y(y_cl).z(z_cl).legend('kspl_CLExt1')
#             kspl_ext_V = kspl_ext.clone().x(-x_cl).y(-y_cl).z(-z_cl).legend('kspl_CLExt2')
#             cl_ribbon = vedo.Ribbon(kspl_ext_D, kspl_ext_V, alpha=0.2, res=(1500, 1500))
#             cl_ribbon = cl_ribbon.wireframe(True).legend("rib_ExtCL(2-sides)")
    
#         elif clRib_type == 'ext1side':
#             x_ucl, y_ucl, z_ucl = pl_linLine_unitNormal*15
#             cl_ribbon = []
#             for i in range(10):
#                 kspl_ext_DA = kspl_ext.clone().x(i*x_ucl).y(i*y_ucl).z(i*z_ucl)
#                 kspl_ext_DB = kspl_ext.clone().x((i+1)*x_ucl).y((i+1)*y_ucl).z((i+1)*z_ucl)
#                 cl_ribbon2un = vedo.Ribbon(kspl_ext_DA, kspl_ext_DB, alpha=0.2, res=(220, 5))
#                 cl_ribbon.append(cl_ribbon2un)
#             cl_ribbon = vedo.merge(cl_ribbon)
#             cl_ribbon.legend('rib_ExtCL(1-side)').wireframe(True)
    
#         elif clRib_type == 'HDStack':
#             x_ul, y_ul, z_ul = pl_linLine_unitNormal*2
#             x_cl, y_cl, z_cl = pl_linLine_unitNormal120
#             cl_ribbon = []
#             for i in range(100):
#                 kspl_ext_D = kspl_ext.clone().x(x_cl-i*x_ul).y(y_cl-i*y_ul).z(z_cl-i*z_ul)
#                 kspl_ext_V = kspl_ext.clone().x(-x_cl+i*x_ul).y(-y_cl+i*y_ul).z(-z_cl+i*z_ul)
#                 cl_ribbon2un = vedo.Ribbon(kspl_ext_D, kspl_ext_V, alpha=0.2, res=(220, 20))
#                 if i == 0:
#                     rib_pts = cl_ribbon2un.points()
#                 else:
#                     rib_pts = np.concatenate((rib_pts,cl_ribbon2un.points()))
#                 cl_ribbon.append(cl_ribbon2un)
#             cl_ribbon = vedo.merge(cl_ribbon)
#             cl_ribbon.legend('HDStack').wireframe(True)
            
#         return cl_ribbon
        
#     def get_volume(self): 
#         mesh_vol = self.mesh.volume()
#         return mesh_vol
        
#     def get_area(self): 
#         mesh_area = self.mesh.area()
#         return mesh_area
    
#     def create_section(self, name, color, alpha=0.05):
           
#         sect_info = self.parent_organ.mH_settings['general_info']['sections']['name_sections']
#         if name == 'sect1':
#             invert = True
#         else: 
#             invert = False
#         # print('name:', name, '- invert:', invert)
            
#         submesh = SubMesh(parent_mesh = self, sub_mesh_type='Section', 
#                           name = name, user_name = sect_info[name],
#                           color = color, alpha = alpha)#,
        
#         submesh.s3_invert = invert
#         name2save = self.parent_organ.user_organName + '_mask_sect.npy'
#         submesh.s3_mask_dir = self.parent_organ.info['dirs']['s3_numpy'] / name2save
        
#         segments_info = self.parent_organ.mH_settings['general_info']['sections']
#         submesh.sub_user_name = segments_info['name_sections'][submesh.sub_name]
        
#         self.parent_organ.add_submesh(submesh)
        
#         return submesh
        
#     def mask_segments(self):
          
#         # Get segments info
#         no_discs = self.parent_organ.mH_settings['general_info']['segments']['no_cuts_4segments']

#         # Mask im_channel
#         im_ch = self.imChannel
#         im_ch.load_chS3s([self.mesh_type])
#         cont_tiss = getattr(im_ch, 's3_'+self.mesh_type)
#         s3 = cont_tiss.s3()
#         masked_s3 = s3.copy()
        
#         for nn in range(no_discs):
#             name_s3 = self.parent_organ.user_organName + '_mask_DiscNo'+str(nn)+'.npy'
#             s3_dir = self.parent_organ.info['dirs']['s3_numpy'] / name_s3
#             s3_mask = np.load(str(s3_dir))
#             s3_mask = s3_mask.astype('bool')
#             masked_s3 = mask_disc(self.parent_organ.info['shape_s3'], masked_s3, s3_mask)
        
#         rotateZ_90=self.rotateZ_90
#         # print('rotateZ_90:', rotateZ_90)
#         masked_mesh = create_submesh(masked_s3, self.resolution, keep_largest=False, rotateZ_90=self.rotateZ_90)
#         cut_masked = masked_mesh.split(maxdepth=100)
#         print('> Meshes making up tissue: ', len(cut_masked))
#         alert('frog')
       
#         palette = sns.color_palette("Set2", len(cut_masked))
#         cut_masked_rot = []
#         if rotateZ_90:
#             for n, mesh, color in zip(count(), cut_masked, palette):
#                 cut_masked_rot.append(mesh.rotate_z(-90).alpha(0.1).color(color).legend('No.'+str(n)))
        
#         return cut_masked_rot
        

#     def create_segment(self, name, color):
        
#         segm_info = self.parent_organ.mH_settings['general_info']['segments']['name_segments']
#         alpha = self.alpha

#         submesh = SubMesh(parent_mesh = self, sub_mesh_type='Segment', 
#                           name = name, user_name = segm_info[name], 
#                           color=color, alpha = alpha)
        
#         segments_info = self.parent_organ.mH_settings['general_info']['segments']
#         submesh.sub_user_name = segments_info['name_segments'][submesh.sub_name]
        
#         self.parent_organ.add_submesh(submesh)
            
#         return submesh
    
    
# class SubMesh():
    
#     def __init__(self, parent_mesh: Mesh_mH, sub_mesh_type:str, name: str,
#                  user_name='', color='gold', alpha=0.05):
        
#         self.parent_mesh = parent_mesh
#         self.sub_name = name # ch_cont_segm/sect
#         self.sub_name_all = parent_mesh.name + '_' + name
#         self.sub_mesh_type = sub_mesh_type # Section, Segment
#         self.keep_largest = False#keep_largest
        
#         parent_organ = self.parent_mesh.parent_organ
        
#         if self.sub_name_all not in parent_organ.submeshes.keys():
#             print('>> New submesh - ', self.sub_name_all)
#             # new = True
#             self.sub_name = name # ch_cont_segm/sect
#             self.sub_legend = parent_mesh.legend + '_' + user_name # e.g. myoc_ext_atrium
#             self.color = color
#             self.alpha = alpha
#             self.rotateZ_90 = parent_mesh.rotateZ_90
#             self.imChannel = parent_mesh.imChannel
#             self.mesh_type = parent_mesh.mesh_type
#             self.resolution = parent_mesh.resolution
#         else: 
#             # new = False
#             print('>> Recreating submesh - ', self.sub_name_all)
#             #Get data from submesh dict
#             submesh_dict = parent_organ.submeshes[self.sub_name_all]
#             self.sub_legend = submesh_dict['sub_legend']
#             self.color = submesh_dict['color']
#             self.alpha = submesh_dict['alpha']
#             self.rotateZ_90 = submesh_dict['rotateZ_90']
#             self.imChannel = parent_mesh.imChannel
#             self.mesh_type = parent_mesh.mesh_type
#             self.resolution = submesh_dict['resolution']
#             for attr in ['s3_invert', 's3_mask_dir', 'dict_segm', 'sub_user_name']:
#                 if attr in submesh_dict.keys():
#                     value = submesh_dict[attr]
#                     setattr(self, attr, value)
                    
#     def get_sect_mesh(self):
        
#         s3_mask = np.load(str(self.s3_mask_dir))
#         s3_mask = s3_mask.astype('bool')
#         if self.s3_invert: 
#             maskF = np.invert(s3_mask)
#         else: 
#             maskF = s3_mask
            
#         im_ch = self.imChannel      
#         cont = self.mesh_type
#         im_ch.load_chS3s([cont])
#         cont_tiss = getattr(im_ch, 's3_'+cont)
#         s3 = cont_tiss.s3()
#         masked_s3 = s3.copy()
    
#         masked_s3[maskF] = 0
#         mesh = create_submesh(masked_s3, self.resolution, self.keep_largest, self.rotateZ_90)
#         mesh.legend(self.sub_legend).wireframe()
#         mesh.alpha(self.alpha)
#         mesh.color(self.color)

#         return mesh

#     def get_segm_mesh(self):
        
#         parent_organ = self.parent_mesh.parent_organ
#         dict_ext_segm = parent_organ.mH_settings['general_info']['segments']['ext_segm']
#         organ_ext_meshes = [dict_ext_segm[key]['name'] for key in dict_ext_segm.keys()]
#         if self.sub_name_all in organ_ext_meshes: 
#             mesh_name = parent_organ.user_organName+'_'+self.sub_name_all+'.vtk'
#             mesh_dir = parent_organ.info['dirs']['meshes'] / mesh_name
#             if mesh_dir.is_file():
#                 # print('> '+self.sub_name_all+' is an external segment mesh!')
#                 segm_mesh = vedo.load(str(mesh_dir))
#                 segm_mesh.legend(self.sub_legend).wireframe()
#                 segm_mesh.color(self.color).alpha(self.alpha)
#                 self.mesh = segm_mesh
#         else: 
#             mesh = self.parent_mesh
#             cut_masked = mesh.mask_segments()
        
#             #Get the name of the ext_ext mesh and load it
#             name_ext_mesh = parent_organ.mH_settings['general_info']['segments']['ext_ext']
#             # print('name_ext_mesh:', name_ext_mesh)
#             mesh_ext = parent_organ.obj_meshes[name_ext_mesh]
            
#             # Get the name of the corresponding ext_ext_segm
#             # name_ext_mesh_segm = parent_organ.mH_settings['general_info']['segments']['ext_segm'][self.sub_name]
#             # Create the submesh
#             ext_sub = mesh_ext.create_segment(name = self.sub_name, color = '')
            
#             #Recreating dict_segm
#             # segments_info = parent_organ.mH_settings['general_info']['segments']
#             sp_dict_segm = {'user_name': self.sub_user_name,#segments_info['name_segments'][self.sub_name],
#                             'color': self.color, 
#                             'meshes_number': []}
#             # print('sp_dict_segm - get_segm_mesh', sp_dict_segm)
            
#             # Classify resulting segments using ext_ext submesh
#             sp_dict_segm = classify_segments_from_ext(meshes = cut_masked, 
#                                                    dict_segm = sp_dict_segm,
#                                                    ext_sub = ext_sub)
#             # Assign meshes to submesh
#             _, segm_mesh = create_asign_subsg(parent_organ, mesh, 
#                                                     cut_masked, self.sub_name, 
#                                                     sp_dict_segm, self.color)
            
#         return segm_mesh
    
#     def set_alpha(self, mesh_alpha):      
#         self.alpha = mesh_alpha
#         #Update settings
#         self.parent_mesh.parent_organ.submeshes[self.sub_name_all]['alpha'] = self.alpha
#         self.parent_mesh.parent_organ.save_organ()
    
#     def get_alpha(self):
#         return self.parent_mesh.parent_organ.submeshes[self.sub_name_all]['alpha']
        
#     def set_color(self, mesh_color):
#         self.color = mesh_color
#         #Update settings
#         self.parent_mesh.parent_organ.submeshes[self.sub_name_all]['color'] = self.color
#         self.parent_mesh.parent_organ.save_organ()
        
#     def get_color(self):
#         return self.parent_mesh.parent_organ.submeshes[self.sub_name_all]['color'] 

# class MyFaceSelectingPlotter(vedo.Plotter):
#     def __init__(self, colors, color_o, views, **kwargs):
        
#         # Create planar_views dictionary
#         planar_views = {}
#         for n, view, color in zip(count(), views, colors): 
#             planar_views[view] = {'color': color}
            
#         self.planar_views = planar_views
#         self.views = views
#         self.color_o = color_o
#         self.done = False
        
#         # Create message that displays instructions
#         self.msg = vedo.Text2D("", pos="top-center", c=txt_color, bg='white', font=txt_font, alpha=0.8, s=0.7)
#         self.msg_face = vedo.Text2D("", pos="bottom-center", c=txt_color, bg='red', font=txt_font, alpha=0.2, s=0.7)
        
#         # Initialise plotter with current planar view
#         self.active_n = 0
#         self.selected_faces = []
#         self.active_color = self.planar_views[self.current_view()]['color']
#         self.get_msg()
#         vedo.printc('Selecting '+self.current_view().upper()+'...', c="g", invert=True)

#         #Initialise Plotter 
#         super().__init__(**kwargs)
    
#     def current_view(self):
#         return self.views[self.active_n]
        
#     def get_msg(self):
#         if self.active_n < len(self.views)-1:
#             msg1 = 'Instructions: Select (click) the cube face that represents the '+self.current_view().upper()+' face'
#             msg2 = '\n press -c- and then click to continue.'
#             self.msg.text(msg1+msg2)
#         else:
#             if self.check_full():
#                 msg_close = 'Instructions: You are done selecting planar views. Close the window to continue.'
#                 self.msg.text(msg_close)
#             else: 
#                 msg1 = 'Instructions: Select (click) the cube face that represents the '+self.current_view().upper()+' face'
#                 msg2 = '\n press -c- and then click to continue.'
#                 self.msg.text(msg1+msg2)
    
#     def check_full(self):
#         check = []
#         for pv in self.planar_views:
#             if 'pl_normal' in self.planar_views[pv].keys():
#                 check.append(isinstance(self.planar_views[pv]['pl_normal'], np.ndarray))
#             else: 
#                 check.append(False)
#         # print('\n')
#         return all(check)
        
#     def on_key_press(self, evt):
#         if not self.done: 
#             if evt.keypress == "c":
#                 planar_view = self.current_view()
#                 if 'idcell' in self.planar_views[planar_view].keys():
#                     self.selected_faces.append(self.planar_views[planar_view]['idcell'])
#                     self.get_msg()
#                     vedo.printc('>> n:'+str(self.active_n)+'-'+str(len(self.views)), c='orange', invert=True)
#                     if self.active_n < len(self.views)-1:
#                         self.active_n += 1
#                         planar_view = self.current_view()
#                         self.active_color = self.planar_views[planar_view]['color']
#                         vedo.printc('Now selecting '+planar_view.upper()+'...', c="g", invert=True)
#                         self.get_msg()
#                     else: 
#                         # print('BBB')
#                         self.get_msg()
#                         if self.check_full(): 
#                             self.done = True
#                             vedo.printc('You are done, now close the window!', c='orange', invert=True)
#                     vedo.printc('n:'+str(self.active_n), c='orange', invert=True)
#                 else: 
#                     msg_warning = "You need to select a cube's face for the "+planar_view.upper()+" face to continue."
#                     self.msg_face.text(msg_warning)
#                     vedo.printc('No cell has been selected',c='r', invert=True)
#         else: 
#             vedo.printc('You are done, now close the window!', c='orange', invert=True)
        
#     def select_cube_face(self, evt):
#         if not self.done: 
#             if isinstance(evt.actor, vedo.shapes.Cube):
#                 orient_cube = evt.actor
#                 if not orient_cube:
#                     return
#                 pt = evt.picked3d
#                 idcell = orient_cube.closest_point(pt, return_cell_id=True)
#                 vedo.printc('You clicked (idcell):', idcell, c='y', invert=True)
#                 if set(orient_cube.cellcolors[idcell]) == set(self.color_o):
#                     orient_cube.cellcolors[idcell] = self.active_color #RGBA 
#                     for cell_no in range(len(orient_cube.cells())):
#                         if cell_no != idcell and cell_no not in self.selected_faces: 
#                             orient_cube.cellcolors[cell_no] = self.color_o #RGBA 
#                 planar_view =  self.current_view()
#                 self.msg_face.text("You selected cube's face number "+str(idcell)+" as the "+planar_view.upper()+" face")
#                 self.planar_views[planar_view]['idcell'] = idcell
#                 cells = orient_cube.cells()[idcell]
#                 points = [orient_cube.points()[cell] for cell in cells]
#                 plane_fit = vedo.fit_plane(points, signed=True)
#                 self.planar_views[planar_view]['pl_normal'] = plane_fit.normal
#         else: 
#             vedo.printc('You are done, now close the window!', c='orange', invert=True)
        
# #%% - Drawing Functions
# #%% func - draw_line
# def draw_line (clicks, myIm, color_draw):
#     """
#     Function that draws white or black line connecting all the clicks received as input
#     """
#     for num, click in enumerate(clicks):
#         if num < len(clicks)-1:
#             pt1x, pt1y = click
#             pt2x, pt2y = clicks[num+1]
#             rr, cc, val = line_aa(int(pt1x), int(pt1y),
#                                   int(pt2x), int(pt2y))
#             rr1, cc1, val1 = line_aa(int(pt1x)+1, int(pt1y),
#                                      int(pt2x)+1, int(pt2y))
#             rr2, cc2, val2 = line_aa(int(pt1x)-1, int(pt1y),
#                                      int(pt2x)-1, int(pt2y))
#             if color_draw == "white" or color_draw == "":
#                 myIm[rr, cc] = val * 50000
#             elif color_draw == "1":
#                 myIm[rr, cc] = 1
#                 myIm[rr1, cc1] = 1
#                 myIm[rr2, cc2] = 1
#             elif color_draw == "0":
#                 myIm[rr, cc] = 0
#                 myIm[rr1, cc1] = 0
#                 myIm[rr2, cc2] = 0
#             else: #"black"
#                 myIm[rr, cc] = val * 0
#                 myIm[rr1, cc1] = val1 * 0
                
#     return myIm

# #%% - Masking
# #%% func - mask_disc
# def mask_disc(shape_s3, s3, s3_cyl):
    
#     #Load stack shape
#     zdim, xdim, ydim = shape_s3
#     s3_mask = copy.deepcopy(s3)
    
#     for slc in range(zdim):
#         im_cyl =s3_cyl[:,:,slc]
#         pos_pts = np.where(im_cyl == 1)
#         clicks = [(pos_pts[0][i], pos_pts[1][i]) for i in range(pos_pts[0].shape[0])]
#         if len(clicks+clicks) > 200:
#             clicks_random = random.sample(clicks+clicks, 200)#2*len(clicks))
#         else:
#             clicks_random = random.sample(clicks+clicks, 2*len(clicks))
            
#         im = s3_mask[:,:,slc]
#         myIm = draw_line(clicks_random, im, '0')
#         s3_mask[:,:,slc] = myIm

#     return s3_mask

# #%% - Mesh functions
# #%% func - create_mesh
# def create_submesh(masked_s3, resolution, keep_largest:bool, rotateZ_90:bool):
    
#     verts, faces, _, _ = measure.marching_cubes(masked_s3, spacing=resolution, method='lewiner')
   
#     # Create meshes
#     mesh = vedo.Mesh([verts, faces])
#     if keep_largest:
#         mesh = mesh.extract_largest_region()
#     if rotateZ_90:
#         mesh.rotate_z(-90)
        
#     alert('woohoo')
    
#     return mesh
 
#%%
print('morphoHeart! - Loaded Module Classes')
