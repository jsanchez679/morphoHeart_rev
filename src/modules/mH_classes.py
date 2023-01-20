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
import vedo as vedo
from vedo import write
from skimage import measure, io
import copy
import json
import collections
import pprint
import matplotlib.pyplot as plt

#%% ##### - Other Imports - ##################################################
from .mH_funcBasics import alert, ask4input

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
    def __init__(self, new=True, proj_name=None, proj_dir=None):

        def create_mHName(self):
            '''
            func - create name for a morphoHeart project
            This function will assign the newly created project a name using a
            timestamp
            '''
            now_str = datetime.now().strftime('%Y%m%d%H%M')
            self.mH_projName = 'mH_Proj-'+now_str
        if new:
            create_mHName(self)
            self.organs = {}
        else: 
            load_dict = {'name': proj_name, 'dir': proj_dir}
            self.load_project(load_dict=load_dict)
    
    
    def load_project(self, load_dict:dict):
        dir_res = load_dict['dir']
        jsonDict_name = 'mH_'+load_dict['name']+'_project.json'
        json2open_dir = dir_res / 'settings' / jsonDict_name
        with open(json2open_dir, "r") as read_file:
            print(">> "+jsonDict_name+": Opening JSON encoded data")
            dict_out = json.load(read_file)
        self.info = dict_out['info']
        self.user_projName = dict_out['info']['user_projName']
        self.mH_projName = dict_out['info']['mH_projName']
        self.info['dir_proj'] = Path(self.info['dir_proj'])
        self.info['dir_info'] = Path(self.info['dir_info'])
        
        if 'chNS' in dict_out['settings'].keys():
            dict_out['settings']['chNS']['general_info']['ch_ext'] = tuple(dict_out['settings']['chNS']['general_info']['ch_ext'])
            dict_out['settings']['chNS']['general_info']['ch_int'] = tuple(dict_out['settings']['chNS']['general_info']['ch_int'])
        
        if 'chNS' in dict_out['workflow']['ImProc'].keys():
            dict_out['workflow']['ImProc']['chNS']['D-S3Create']['Settings']['ext_mesh'] = tuple(dict_out['workflow']['ImProc']['chNS']['D-S3Create']['Settings']['ext_mesh'])
            dict_out['workflow']['ImProc']['chNS']['D-S3Create']['Settings']['int_mesh'] = tuple(dict_out['workflow']['ImProc']['chNS']['D-S3Create']['Settings']['int_mesh'])
         
        self.settings = dict_out['settings']
        self.workflow = dict_out['workflow']
        self.channels = dict_out['channels']
        self.segments = dict_out['segments']
        self.organs = dict_out['organs']
        try: 
            for key in self.organs.keys():
                self.organs[key]['dir_res'] = Path(self.organs[key]['dir_res'])
        except: 
            pass
        # self.gral_meas_keys = dict_out['tuples']['gral_meas_keys']
        
        self.gral_meas_param = [tuple(item) for item in dict_out['gral_meas_param']]
        self.dir_proj = Path(dict_out['info']['dir_proj'])
        self.dir_info = Path(dict_out['info']['dir_info'])
        #self.all_info = dict_out

    def create_gralprojWF(self, user_proj_settings:dict):
        '''
        func - Create general project workflow
        This function will be called when the user creates a new project and 
        fills information regarding the workflow for such project which will get into the 
        function packed as the user_proj_settings dictionary. 
        The output of this function will create an attribute to the project containing 
        most of the user settings except for the selected parameters. 
        '''

        self.user_projName = user_proj_settings['user_projName'].replace(' ', '_')
        self.info = {}
        self.info = {'mH_projName': self.mH_projName,
                            'user_projName': self.user_projName,
                            'user_projNotes': user_proj_settings['user_projNotes'], 
                            }

        settings = {}
        gral_meas_keys = []
        channels = []

        for ch_num in range(0, user_proj_settings['no_chs']):
            ch_str = 'ch'+str(ch_num+1)
            dict_info_ch = {'mH_chName':ch_str,
                            'user_chName':user_proj_settings['name_chs'][ch_num].replace(' ', '_'),
                            'dir_cho': None, 
                            'colorCh_tiss': user_proj_settings['color_chs'][ch_num][0],
                            'colorCh_ext': user_proj_settings['color_chs'][ch_num][1],
                            'colorCh_int': user_proj_settings['color_chs'][ch_num][2],
                            'mask_ch': None,
                            'dir_mk': None}
            settings[ch_str] = {}
            settings[ch_str]['general_info'] = dict_info_ch
            settings[ch_str]['measure'] = {}
            for cont in ['tissue', 'int', 'ext']:
                settings[ch_str]['measure'][cont] = {}
                settings[ch_str]['measure'][cont]['whole'] ={} 
                gral_meas_keys.append((ch_str,cont,'whole'))
            channels.append(ch_str)

        if user_proj_settings['ns']['layer_btw_chs']:
            ch_str = 'chNS'
            settings['chNS']={}
            settings['chNS']['general_info']={'mH_chName':ch_str,
                                            'user_chName':user_proj_settings['ns']['user_nsChName'].replace(' ', '_'),
                                            'ch_ext': user_proj_settings['ns']['ch_ext'],
                                            'ch_int': user_proj_settings['ns']['ch_int'],
                                            'colorCh_tiss': user_proj_settings['ns']['color_chns'][0],
                                            'colorCh_ext': user_proj_settings['ns']['color_chns'][1],
                                            'colorCh_int': user_proj_settings['ns']['color_chns'][2]}
            settings[ch_str]['measure'] = {}
            for cont in ['tissue', 'int', 'ext']:
                settings[ch_str]['measure'][cont] = {}
                settings[ch_str]['measure'][cont]['whole'] = {} 
                gral_meas_keys.append((ch_str,cont,'whole'))
            channels.append(ch_str)

        segments = []
        if user_proj_settings['segments']['cutLayersIn2Segments']:
            for ch_str in channels:
                ch_segments = list(user_proj_settings['segments']['ch_segments'].keys())
                if ch_str in ch_segments:
                    for s_num in range(0, user_proj_settings['segments']['no_segments']):
                        segm_str = 'segm'+str(s_num+1)
                        segments.append(segm_str)
                        for cont in user_proj_settings['segments']['ch_segments'][ch_str]:
                            settings[ch_str]['measure'][cont][segm_str] = {} 
                            gral_meas_keys.append((ch_str,cont,segm_str))

        settings['dirs'] = {'meshes': 'NotAssigned', 
                            'csv_all': 'NotAssigned',
                            'imgs_videos': 'NotAssigned', 
                            's3_numpy': 'NotAssigned',
                            'centreline': 'NotAssigned',
                            'settings': 'NotAssigned'}

        self.settings = settings
        self.gral_meas_keys = gral_meas_keys
        self.channels = channels
        segments_new = list(set(segments))
        self.segments = sorted(segments_new) 
        # self.info['channels'] = self.channels
        # self.info['segments'] = self.segments
        # self.info['organs'] = {}
            
        self.create_table2select_meas_param()

    def create_table2select_meas_param(self):
        '''
        This function will create a dictionary with all the possible measurement parameters 
        a user can get based on the settings given when setting the initial project 
        (no_ch, no_segments and the corresponding channels from which the segments will 
        be obtained, etc)
        The output of this function (dictionary with default parameters and list)
        will help to set up the GUI table for the user to select the parameters to measure. 
        '''
        channels = self.channels
        conts = ['tissue', 'int', 'ext']
        gral_meas_param = []
        dict_params_deflt = {}
        for ch_b in channels: 
            dict_params_deflt[ch_b] = {}
            for cont_b in conts: 
                dict_params_deflt[ch_b][cont_b] = {}

        for tup in self.gral_meas_keys:
            ch, cont, segm = tup
            dict_params_deflt[ch][cont][segm] = {'volume': True, 
                                                    'surf_area': False}

            gral_meas_param.append((ch,cont,segm,'volume'))
            gral_meas_param.append((ch,cont,segm,'surf_area'))

            if cont in ['int', 'ext']:
                dict_params_deflt[ch][cont][segm]['surf_area'] = True 
            if cont == 'tissue':
                if segm == 'whole': 
                    dict_params_deflt[ch][cont][segm]['thickness int>ext'] = True
                    dict_params_deflt[ch][cont][segm]['thickness ext>int'] = False

                    gral_meas_param.append((ch,cont,segm,'thickness int>ext'))
                    gral_meas_param.append((ch,cont,segm,'thickness ext>int'))
                else: 
                    dict_params_deflt[ch][cont][segm]['thickness int>ext'] = False
                    dict_params_deflt[ch][cont][segm]['thickness ext>int'] = False

                    gral_meas_param.append((ch,cont,segm,'thickness int>ext'))
                    gral_meas_param.append((ch,cont,segm,'thickness ext>int'))
            if segm == 'whole':
                dict_params_deflt[ch][cont][segm]['centreline'] = True
                dict_params_deflt[ch][cont][segm]['centreline_linlength'] = True
                dict_params_deflt[ch][cont][segm]['centreline_looplength'] = True

                gral_meas_param.append((ch,cont,segm,'centreline'))
                gral_meas_param.append((ch,cont,segm,'centreline_linlength'))
                gral_meas_param.append((ch,cont,segm,'centreline_looplength'))

        self.gral_meas_param = gral_meas_param
        #self.dict_params_deflt = dict_params_deflt
        #Use this two result variables to create selecting table in the GUI

    def set_measure_param(self, user_params2meas:dict, user_ball_settings:dict):
        '''
        This function will get the input of the updated selected parameters from the GUI and 
        will include those measurements in the dictionary of the project. This dictionary will then 
        be used as a workflow template for all the Organs created within the project. 
        '''
        settings_updated = copy.deepcopy(self.settings)
        gral_meas_param = copy.deepcopy(self.gral_meas_param)
        gral_struct = self.gral_meas_keys

        for tup in gral_struct: 
            ch, cont, segm = tup
            settings_updated[ch]['measure'][cont][segm] = user_params2meas[ch][cont][segm]

        if user_ball_settings['ballooning']:
            ball_settings = user_ball_settings['ball_settings']
            for key in ball_settings.keys():
                ch = ball_settings[key]['to_mesh']
                cont = ball_settings[key]['to_mesh_type']
                from_cl = ball_settings[key]['from_cl']
                cl_type = ball_settings[key]['from_cl_type']
                # print(ch, cont, from_cl, cl_type)
                settings_updated[ch]['measure'][cont]['whole']['ballooning']= {'from_cl':from_cl,
                                                                               'from_cl_type': cl_type}
                gral_meas_param.append((ch,cont,'whole','ballooning'))

                if not settings_updated[from_cl]['measure'][cl_type]['whole']['centreline']:
                    settings_updated[from_cl]['measure'][cl_type]['whole']['centreline'] = True
                    settings_updated[from_cl]['measure'][cl_type]['whole']['centreline_linlength'] = True
                    settings_updated[from_cl]['measure'][cl_type]['whole']['centreline_looplength'] = True
                    # print('Added ('+from_cl+','+cl_type+',whole,centreline)')

                if (from_cl,cl_type,'whole','centreline') not in gral_meas_param:
                    gral_meas_param.append((from_cl,cl_type,'whole','centreline'))
                    gral_meas_param.append((from_cl,cl_type,'whole','centreline_linlength'))
                    gral_meas_param.append((from_cl,cl_type,'whole','centreline_looplength'))
                    # print('Added to list ('+from_cl+','+cl_type+',whole,centreline)')

        # Note: Make sure the info being transferred from the dict to the wf is right 
        self.gral_meas_param = gral_meas_param
        self.clean_False(settings_updated=settings_updated)
        delattr(self, 'gral_meas_keys')
        
    def clean_False(self, settings_updated:dict):
        gral_meas_param = copy.deepcopy(self.gral_meas_param)
        gral_meas_param_new = []
        
        for tup in gral_meas_param:
            ch, cont, segm, var = tup
            if not settings_updated[ch]['measure'][cont][segm][var]:
                remove_var = settings_updated[ch]['measure'][cont][segm].pop(var, None)
                # if remove_var != None:
                #     print('Tuple: '+str(tup)+' was removed!')
            else: 
                gral_meas_param_new.append(tup)
        
        self.settings = settings_updated
        self.gral_meas_param = sorted(gral_meas_param_new)

    def create_proj_dir(self, dir_proj:Path):
        # set_dir_res()
        folder_name = 'R_'+self.user_projName
        self.dir_proj = dir_proj / folder_name
        self.dir_proj.mkdir(parents=True, exist_ok=True)
        self.info['dir_proj'] = self.dir_proj

    def set_project_status(self):
        '''
        This function will initialise the dictionary that will contain the workflow of the
        project. This workflow will be assigned to each organ that is part of the created project
        and will be updated in each organ as the user advances in the processing. 
        '''
        channels = self.channels
        segments = self.segments

        workflow = {'ImProc': {},
                    'MeshesProc': {}}

        dict_ImProc = dict()
        dict_ImProc['Status'] = 'NotInitialised'
        dict_MeshesProc = dict()

         # Find the meas_param that include the extraction of a centreline
        item_centreline = [item for item in self.gral_meas_param if 'centreline' in item]
        # Find the meas_param that include the extraction of segments
        segm_list = []
        for segm in self.segments:
            segm_list.append([item for item in self.gral_meas_param if segm in item])
        item_segment = sorted([item for sublist in segm_list for item in sublist])
        # print('item_segment:', item_segment)
        # Find the meas_param that include the extraction of ballooning
        item_ballooning = [item for item in self.gral_meas_param if 'ballooning' in item]
        # Find the meas_param that include the extraction of thickness
        item_thickness_intext = [item for item in self.gral_meas_param if 'thickness int>ext' in item]
        item_thickness_extint = [item for item in self.gral_meas_param if 'thickness ext>int' in item]

        # Project status
        for ch in channels:
            if 'NS' not in ch:
                dict_ImProc[ch] = {'Status': 'NotInitialised',
                                    'A-MaskChannel': {'Status': 'NotInitialised'},
                                    'B-CloseCont':{'Status': 'NotInitialised',
                                                    'Steps':{'A-Autom': {'Status': 'NotInitialised',
                                                                        'Range': None, 
                                                                        'Range_completed': None}, 
                                                            'B-Manual': {'Status': 'NotInitialised',
                                                                        'Range': None, 
                                                                        'Range_completed': None}, 
                                                            'C-CloseInOut': {'Status': 'NotSet'}}},

                                    'C-SelectCont':{'Status': 'NotInitialised',
                                                    'Info': {'tuple_slices': None,
                                                            'number_contours': None,
                                                            'range': None}},

                                    'D-S3Create':{'Status': 'NotInitialised',
                                                'Info': {'tissue':{'Status': 'NotInitialised', 
                                                                    'Info':{}},
                                                        'int':{'Status': 'NotInitialised', 
                                                                    'Info':{}},
                                                        'ext':{'Status': 'NotInitialised', 
                                                                    'Info':{}}}}, 

                                    'E-TrimS3': {'Status': 'NotInitialised',
                                                'Info':{'tissue':{'Status': 'NotInitialised', 
                                                            'Info':{}},
                                                'int':{'Status': 'NotInitialised', 
                                                            'Info':{}},
                                                'ext':{'Status': 'NotInitialised', 
                                                            'Info':{}}}}}
            else: 
                dict_ImProc[ch] = {'Status': 'NotInitialised',
                                    'D-S3Create':{'Status': 'NotInitialised',
                                                'Info':{'tissue':{'Status': 'NotInitialised', 
                                                            'Info':{}},
                                                        'int':{'Status': 'NotInitialised', 
                                                                    'Info':{}},
                                                        'ext':{'Status': 'NotInitialised', 
                                                                    'Info':{}}},
                                                'Settings':{'ext_mesh': self.settings[ch]['general_info']['ch_ext'],
                                                            'int_mesh': self.settings[ch]['general_info']['ch_int']}}} 
             
            dict_MeshesProc[ch] = {}
            for cont in ['tissue', 'int', 'ext']:
                if 'NS' not in ch:
                    dict_MeshesProc[ch][cont]={'A-Create3DMesh': {'Status': 'NotInitialised',
                                                                'original_stack_dir':None,
                                                                'keep_largest': None,
                                                                'mesh_dir': None},
                                                'B-TrimMesh': {'Status': 'NotInitialised',
                                                                'original_stack_dir':None,
                                                                'keep_largest': None,
                                                                'trim-settings': {'no_cuts': 0},
                                                                'mesh_dir': None},
                                                'C-Centreline': {}
                                                }
                else: 
                    dict_MeshesProc[ch][cont]={'A-Create3DMesh': {'Status': 'NotInitialised',
                                                                'original_stack_dir':None,
                                                                'keep_largest': True,
                                                                'mesh_dir': None},
                                                }
                if cont == 'tissue' and 'NS' in ch:
                    dict_MeshesProc[ch][cont]['A-Create3DMesh']['keep_largest'] = False

                if (ch,cont,'whole','centreline') in item_centreline:
                     dict_MeshesProc[ch][cont]['C-Centreline'] = {'Status': 'NotInitialised',
                                                                    'dir_cleanMesh': None, 
                                                                    'dir_meshLabMesh': None, 
                                                                    'vmtk_cl': {'Status': 'NotInitialised',
                                                                                'Settings': 'NotInitialised'},
                                                                    'connect_cl': {'Status': 'NotInitialised',
                                                                                'Settings': 'NotInitialised'},
                                                                    'measure':{'Status': 'NotInitialised',
                                                                                'Settings': 'NotInitialised'}}
                if (ch,cont,'whole','ballooning') in item_ballooning:
                     dict_MeshesProc[ch][cont]['D-Ballooning'] = {'Status': 'NotInitialised',
                            'Settings': {'from_cl': self.settings[ch]['measure'][cont]['whole']['ballooning']['from_cl'],
                                        'from_cl_type': self.settings[ch]['measure'][cont]['whole']['ballooning']['from_cl_type']}}

                if (ch,cont,'whole','thickness int>ext') in item_thickness_intext:
                     dict_MeshesProc[ch][cont]['D-Thickness'] = {'Status': 'NotInitialised',
                                                                        'Settings': {}}    
                if (ch,cont,'whole','thickness ext>int') in item_thickness_extint:
                     dict_MeshesProc[ch][cont]['D-Thickness'] = {'Status': 'NotInitialised',
                                                                        'Settings': {}}                                                       
                                                                    
                if len(self.segments) > 0:
                    # print('IN!!', ch, cont)
                    if (ch,cont,'segm1','volume') in item_segment:
                        # print('In2!',ch,cont)
                        dict_MeshesProc[ch][cont]['E-Segments'] = {'Status': 'NotInitialised',
                                                                    'Settings': {},
                                                                    'Segments': {}}

                        for segm in ['whole']+segments:
                            dict_MeshesProc[ch][cont]['E-Segments']['Segments'][segm]={'Status': 'NotInitialised',
                                                                                        'measure': None}

        workflow['ImProc'] = dict_ImProc
        workflow['MeshesProc'] = dict_MeshesProc
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
        all_info['settings'] = self.settings
        all_info['workflow'] = self.workflow
        all_info['channels'] = self.channels
        all_info['segments'] = self.segments
        # self.info['organs'] = {}
        all_info['organs'] = self.organs
        all_info['gral_meas_param'] = self.gral_meas_param
        # all_info['tuples'] = {}
        # all_info['tuples']['gral_meas_keys'] = self.gral_meas_keys
        # all_info['tuples']['gral_meas_param'] = self.gral_meas_param
        # self.all_info = all_info
        
        if not json2save_par.is_dir():
            print('>> Error: Settings directory could not be created!\n>> Directory: '+jsonDict_name)
            alert('error_beep')
        else: 
            json2save_dir = json2save_par / jsonDict_name
            with open(str(json2save_dir), "w") as write_file:
            # with open('AAA.json', "w") as write_file:
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

        dict_organ = {'user_organName': organ.user_organName, 
                        'parent_projectName': organ.parent_project.user_projName,
                        'info': organ.info,
                        }
        dict_organ['user_organName']
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
        with open(json2open_dir, "r") as read_file:
            print(">> "+jsonDict_name+": Opening JSON encoded data")
            dict_out = json.load(read_file)
        user_settings = dict_out['Organ']
        info_loadCh = dict_out['info_loadCh']
        organ = Organ(project=self, user_settings= user_settings, info_loadCh=info_loadCh, 
                        new=False, load_dict=dict_out)
        return organ

class Organ():
    'Organ Class'
    
    def __init__(self, project:Project, user_settings:dict, info_loadCh:dict, new=True, load_dict={}):
        
        self.user_organName = user_settings['user_organName'].replace(' ', '_')
        self.parent_project = project
        self.info = user_settings
        self.info_loadCh = info_loadCh

        if new:
            self.create_mHName()
            self.settings = copy.deepcopy(project.settings)
            self.workflow = copy.deepcopy(project.workflow)
            self.imChannels = {}
            self.meshes = {}
            self.objects = {}
        else: 
            self.load_organ(load_dict=load_dict)

        self.check_channels(project, info_loadCh)

    def load_organ(self, load_dict:dict):
        self.info['project']['dict_dir_info'] = Path(self.info['project']['dict_dir_info'])
        for ch in self.info_loadCh:
            for key_a in self.info_loadCh[ch]:
                if 'dir' in key_a:
                    self.info_loadCh[ch][key_a] = Path(self.info_loadCh[ch][key_a])  
                    
        if 'chNS' in load_dict['settings'].keys():
            load_dict['settings']['chNS']['general_info']['ch_ext'] = tuple(load_dict['settings']['chNS']['general_info']['ch_ext'])
            load_dict['settings']['chNS']['general_info']['ch_int'] = tuple(load_dict['settings']['chNS']['general_info']['ch_int'])
        
        if 'chNS' in load_dict['workflow']['ImProc'].keys():
            load_dict['workflow']['ImProc']['chNS']['D-S3Create']['Settings']['ext_mesh'] = tuple(load_dict['workflow']['ImProc']['chNS']['D-S3Create']['Settings']['ext_mesh'])
            load_dict['workflow']['ImProc']['chNS']['D-S3Create']['Settings']['int_mesh'] = tuple(load_dict['workflow']['ImProc']['chNS']['D-S3Create']['Settings']['int_mesh'])
         
        self.settings = load_dict['settings']
        for ch in self.settings:
            for key_b in self.settings[ch]:
                if 'dir' in key_b:
                    self.settings[ch][key_b] = Path(self.settings[ch][key_b])
        for key_c in self.settings['dirs']:
            self.settings['dirs'][key_c] = Path(self.settings['dirs'][key_c])
        self.workflow = load_dict['workflow']
        self.imChannels = load_dict['imChannels']
        for ch in self.imChannels.keys():
            for key_d in self.imChannels[ch].keys():
                if 'dir' in key_d:
                    self.imChannels[ch][key_d] = Path(self.imChannels[ch][key_d])
            self.imChannels[ch]['shape'] = tuple(self.imChannels[ch]['shape'])
            if 'shape_s3' in self.imChannels[ch].keys():
                self.imChannels[ch]['shape_s3'] = tuple(self.imChannels[ch]['shape_s3'])
            
            for key_e in self.imChannels[ch]['contStack'].keys():
                self.imChannels[ch]['contStack'][key_e]['shape_s3'] = tuple(self.imChannels[ch]['contStack'][key_e]['shape_s3'])
        self.meshes = load_dict['meshes']
        self.objects = load_dict['objects']
        self.dir_info = Path(load_dict['dir_info'])
        self.mH_organName = load_dict['mH_organName']
        
        #Create all imChannels 
        
        
        #Create all contStacks
        

    def create_mHName(self):
        now_str = datetime.now().strftime('%Y%m%d%H%M')
        self.mH_organName = 'mH_Organ-'+now_str
                 
    def check_channels(self, project:Project, info_loadCh:dict):
        chs = [x for x in project.channels if x != 'chNS']    
        array_sizes = {}
        sizes = []
        for ch in chs:
            try:
                images_o = io.imread(str(info_loadCh[ch]['dir_cho']))
                array_sizes[ch]= {'cho': images_o.shape}
                # print(ch,',cho-',str(images_o.shape))
                sizes.append(images_o.shape)
            except: 
                print('>> Error: Something went wrong opening the file -',ch)
                alert('error_beep')
            
            if info_loadCh[ch]['mask_ch']:
                try:
                    images_mk = io.imread(str(info_loadCh[ch]['dir_mk']))
                    array_sizes[ch]['mask']= images_mk.shape
                    # print(ch,',mask-',str(images_mk.shape))
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
                    self.settings[ch]['general_info'][param] = info_loadCh[ch][param]
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
                self.settings['dirs'][direc] = dir2create
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
            channel_dict = copy.deepcopy(imChannel.__dict__)
            channel_dict.pop('parent_organ', None)
            self.imChannels[imChannel.channel_no] = channel_dict
        else: # just update im_proc 
            self.imChannels[imChannel.channel_no]['process'] = imChannel.process
            self.imChannels[imChannel.channel_no]['contStack'] = imChannel.contStack
            if imChannel.dir_stckproc.is_file():
                self.imChannels[imChannel.channel_no]['dir_stckproc'] = imChannel.dir_stckproc
            if hasattr(imChannel, 'shape_s3'):
                self.imChannels[imChannel.channel_no]['shape_s3'] = imChannel.shape_s3

    def add_mesh(self, mesh, new:bool): # mesh: Mesh_mH
        if new: 
            self.meshes[mesh.legend] = {}
            self.meshes[mesh.legend]['parent_organ'] = mesh.parent_organ.user_organName
            self.meshes[mesh.legend]['channel_no'] = mesh.imChannel.channel_no
            self.meshes[mesh.legend]['user_meshName'] = mesh.user_meshName
            self.meshes[mesh.legend]['mesh_type'] = mesh.mesh_type
            self.meshes[mesh.legend]['legend'] = mesh.legend
            self.meshes[mesh.legend]['resolution'] = mesh.resolution
            self.meshes[mesh.legend]['color'] = mesh.color
            self.meshes[mesh.legend]['alpha'] = mesh.alpha
            if hasattr(mesh,'dir_out'):
                self.meshes[mesh.legend]['dir_out'] = mesh.dir_out
            
        # else: # just update im_proc 
        #     self.imChannels[imChannel.channel_no]['im_proc'] = imChannel.im_proc
        #     self.imChannels[imChannel.channel_no]['process'] = imChannel.process
        #     if imChannel.dir_stckproc.is_file():
        #         self.imChannels[imChannel.channel_no]['dir_stckproc'] = imChannel.dir_stckproc

    def load_TIFF(self, ch_name:str):
        print('---- Loading TIFF! ----')
        image = ImChannel(organ=self, ch_name=ch_name)
        return image

    def save_organ(self):
        jsonDict_name = 'mH_'+self.user_organName+'_organ.json'
        json2save_dir = self.settings['dirs']['settings'] / jsonDict_name
        all_info = {}
        all_info['Organ'] = self.info
        all_info['info_loadCh'] = self.info_loadCh
        all_info['settings'] = self.settings
        all_info['workflow'] = self.workflow
    
        image_dict = copy.deepcopy(self.imChannels)
        for ch in image_dict.keys():
            image_dict[ch].pop('parent_organ', None)
        all_info['imChannels'] = image_dict
    
        all_info['meshes'] = self.meshes
        all_info['objects'] = self.objects
        self.dir_info = self.dir_res / 'settings' / jsonDict_name
        all_info['dir_info'] = self.dir_info
        all_info['mH_organName'] = self.mH_organName

        with open(str(json2save_dir), "w") as write_file:
            json.dump(all_info, write_file, cls=NumpyArrayEncoder)

        if not json2save_dir.is_file():
            print('>> Error: Organ settings file was not saved correctly!\n>> File: '+jsonDict_name)
            alert('error_beep')
        else: 
            print('>> Organ settings file saved correctly! - '+jsonDict_name)
            #print('>> Directory: '+ str(json2save_dir)+'\n')
            alert('countdown')

    def check_status(self, process:str):
        keys_wf = {'ImProc': ['A-MaskChannel', 'B-CloseCont','C-SelectCont','D-S3Create','E-TrimS3'], 
                    'MeshesProc': ['A-Create3DMesh','B-TrimMesh','C-Centreline','D-Thickness','E-Segments']}

        if process=='ImProc':
            for ch in self.imChannels.keys():
                # First check close contours
                close_done = []
                for key_a in ['A-Autom', 'B-Manual']:
                    close_done.append(self.workflow[process][ch]['B-CloseCont']['Steps'][key_a]['Status'])
                print('channel:',ch, '-CloseCont:', close_done)
                if all(flag == 'DONE' for flag in close_done):
                    self.workflow[process][ch]['B-CloseCont']['Status'] = 'DONE'

                # Now update all the workflow
                proc_done = []
                for key_b in keys_wf[process]:
                    proc_done.append(self.workflow[process][ch][key_b]['Status'])
                print('channel:',ch, '-ImProc:', proc_done)
                if all(flag == 'DONE' for flag in proc_done):
                    self.workflow[process][ch]['Status'] = 'DONE'

        
    def update_workflow(self, process, update):
        # updated_workflow = copy.deepcopy(self.workflow)
        # wf = copy.deepcopy(self.workflow)
        # count = 0
        # while count < len(process):
        #     wf = wf[process[count]]
        #     print(wf)
        # self.workflow['ImProc'][self.channel_no]['A-MaskChannel']['Status'] = 'DONE'
        print('Update workflow!')
    
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
        return self.settings['dirs'][name]

class ImChannel(): #channel
    'morphoHeart Image Channel Class (this class will be used to contain the images as tiffs that have been'
    'closed and the resulting s3s that come up from each channel'
    
    def __init__(self, organ:Organ, ch_name:str, new=True):

        self.parent_organ = organ
        self.parent_organ_name = organ.user_organName
        self.channel_no = ch_name
        if new:            
            self.to_mask = organ.settings[ch_name]['general_info']['mask_ch']
            self.resolution = organ.info['resolution']
            self.dir_cho = organ.settings[ch_name]['general_info']['dir_cho']            
            if self.to_mask:
                self.dir_mk = organ.settings[ch_name]['general_info']['dir_mk']
            self.masked = False
            self.shape = self.im().shape
            self.process = ['Init']
            self.contStack = {}
            self.save_channel(im_proc=self.im_proc())
            organ.add_channel(imChannel=self)
            organ.save_organ()
        else: 
            self.load_channel(organ=organ, ch_name=ch_name)

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
        
    def load_channel(self, organ:Organ, ch_name:str):
        
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

        # organ.add_channel(imChannel=self)

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
            self.parent_organ.update_workflow(process = ('ImProc', self.channel_no, 'A-MaskChannel','Status'), update = 'DONE')
            self.parent_organ.workflow['ImProc'][self.channel_no]['A-MaskChannel']['Status'] = 'DONE'
            if self.parent_organ.workflow['ImProc'][self.channel_no]['Status'] == 'NotInitialised':
                self.parent_organ.workflow['ImProc'][self.channel_no]['Status'] = 'Initialised'
            
            #Update channel process
            self.process.append('Masked')
            
            #Update organ imChannels
            self.parent_organ.imChannels[self.channel_no]['masked'] = True
            self.parent_organ.add_channel(self)
            self.parent_organ.save_organ()
            
        else: 
            print('>> Error: Stack could not be masked (stack shapes did not match).')
            alert('error_beep')
            
        if self.parent_organ.workflow['ImProc']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc']['Status'] = 'Initialised'
    
    def closeContours_auto(self):
        # Load image
        im_proc = self.im_proc()
        self.save_channel(im_proc=im_proc)
        
        #Process
        print('---- Closing Contours Auto! ----')
        
        #Update organ workflow
        self.parent_organ.update_workflow(process = (), update = 'DONE')
        self.parent_organ.workflow['ImProc'][self.channel_no]['B-CloseCont']['Steps']['A-Autom']['Status'] = 'DONE'
        if self.parent_organ.workflow['ImProc'][self.channel_no]['B-CloseCont']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc'][self.channel_no]['B-CloseCont']['Status'] = 'Initialised'
        
        #Update channel process
        self.process.append('ClosedCont-Auto')
        
        #Update organ imChannels
        self.parent_organ.add_channel(self)
        self.parent_organ.save_organ()
        
        if self.parent_organ.workflow['ImProc']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc']['Status'] = 'Initialised'
        
    def closeContours_manual(self):
        # Load image
        im_proc = self.im_proc()
        self.save_channel(im_proc=im_proc)
        
        #Process
        print('---- Closing Contours Manually! ----')
        
                
        #Update organ workflow
        self.parent_organ.update_workflow(process = (), update = 'DONE')
        self.parent_organ.workflow['ImProc'][self.channel_no]['B-CloseCont']['Steps']['B-Manual']['Status'] = 'DONE'
        if self.parent_organ.workflow['ImProc'][self.channel_no]['B-CloseCont']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc'][self.channel_no]['B-CloseCont']['Status'] = 'Initialised'
        
        #Update channel process
        self.process.append('ClosedCont-Manual')
                
        #Update organ imChannels
        self.parent_organ.add_channel(self)
        self.parent_organ.save_organ()
        
        if self.parent_organ.workflow['ImProc']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc']['Status'] = 'Initialised'
        
    def closeInfOutf(self):
        # Load image
        im_proc = self.im_proc()
        self.save_channel(im_proc=im_proc)
        
        #Process
        print('---- Closing Inf/Ouft! ----')
        
        
        #Update organ workflow
        self.parent_organ.update_workflow(process = (), update = 'DONE')
        self.parent_organ.workflow['ImProc'][self.channel_no]['B-CloseCont']['Steps']['C-CloseInOut']['Status'] = 'DONE'
        if self.parent_organ.workflow['ImProc'][self.channel_no]['B-CloseCont']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc'][self.channel_no]['B-CloseCont']['Status'] = 'Initialised'
        
        # Update channel process
        self.process.append('ClosedInfOutf')
        
        #Update organ imChannels
        self.parent_organ.add_channel(self)
        
        #TO DO: Update general status of B-CloseCont to Done when confirmed
        self.parent_organ.check_status(process = 'ImProc')
        self.parent_organ.save_organ()
        
        if self.parent_organ.workflow['ImProc']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc']['Status'] = 'Initialised'

    def selectContours(self):
        # Load image
        im_proc = self.im_proc()
        self.save_channel(im_proc=im_proc)
        
        #Process
        print('---- Selecting Contours! ----')
        
        #Update organ workflow
        self.parent_organ.update_workflow(process = (), update = 'DONE')
        self.parent_organ.workflow['ImProc'][self.channel_no]['C-SelectCont']['Status'] = 'DONE'
        
        #Update channel process
        self.process.append('SelectCont')
                
        #Update organ imChannels
        self.parent_organ.add_channel(self)
        self.parent_organ.save_organ()
        
        if self.parent_organ.workflow['ImProc']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc']['Status'] = 'Initialised'

    def create_chS3s (self, layerDict:dict):
        s3_int = ContStack(im_channel=self, cont_type='int', new=True, layerDict=layerDict)
        #self.s3_int = s3_int
        self.add_contStack(s3_int)
        #Update organ workflow
        self.parent_organ.workflow['ImProc'][self.channel_no]['D-S3Create']['Info']['int']['Status'] = 'DONE'
        
        s3_ext = ContStack(im_channel=self, cont_type='ext', new=True, layerDict=layerDict)
        #self.s3_ext = s3_ext
        self.add_contStack(s3_ext)
        #Update organ workflow
        self.parent_organ.workflow['ImProc'][self.channel_no]['D-S3Create']['Info']['ext']['Status'] = 'DONE'
        
        s3_tiss = ContStack(im_channel=self, cont_type='tiss', new=True, layerDict=layerDict)
        #self.s3_tiss = s3_tiss
        self.add_contStack(s3_tiss)
        #Update organ workflow
        self.parent_organ.workflow['ImProc'][self.channel_no]['D-S3Create']['Info']['tissue']['Status'] = 'DONE'
      
        #Update organ workflow
        if s3_int.s3_dir.is_file() and s3_ext.s3_dir.is_file() and s3_tiss.s3_dir.is_file():
            if s3_int.shape_s3 == s3_ext.shape_s3 == s3_tiss.shape_s3:
                self.shape_s3 = s3_int.shape_s3
            else: 
                print('self.shape_s3 = s3_int.shape')
            self.parent_organ.update_workflow(process = (), update = 'DONE')
            self.parent_organ.workflow['ImProc'][self.channel_no]['D-S3Create']['Status'] = 'DONE'
            # self.parent_organ.workflow['ImProc'][self.channel_no]['Status'] = 'DONE'
        
        if self.parent_organ.workflow['ImProc']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc']['Status'] = 'Initialised'
            
        #Update channel process
        self.process.append('CreateS3')
        
        #Update organ imChannel
        self.parent_organ.add_channel(self)
        self.parent_organ.save_organ()
        
    def load_chS3s (self, cont_types:list):
        if 'int' in cont_types:
            s3_int = ContStack(im_channel=self, cont_type='int', new=False)
            self.s3_int = s3_int
            self.add_contStack(s3_int)
        
        if 'ext' in cont_types:
            s3_ext = ContStack(im_channel=self, cont_type='ext', new=False)
            self.s3_ext = s3_ext
            self.add_contStack(s3_ext)
            
        if 'tiss' in cont_types:
            s3_tiss = ContStack(im_channel=self, cont_type='tiss', new=False)
            self.s3_tiss = s3_tiss
            self.add_contStack(s3_tiss)
        
        #Update channel process
        self.process.append('LoadS3')
        
        #Update organ imChannel
        self.parent_organ.add_channel(self)
        self.parent_organ.save_organ()
        
        return

    def trimS3(self): # Not sure what this is! Check if it is part of the process
        #Load s3s
        
        #Process
        print('---- Trimming S3s! ----')
        
        #Update organ workflow        
        self.parent_organ.update_workflow(process = (), update = 'DONE')
        self.parent_organ.workflow['ImProc'][self.channel_no]['E-TrimS3']['Status'] = 'DONE'
        
        #Update channel process
        self.process.append('TrimS3')
        
        #Update organ imChannels
        self.parent_organ.add_channel(self)
        self.parent_organ.save_organ()
        
        if self.parent_organ.workflow['ImProc']['Status'] == 'NotInitialised':
            self.parent_organ.workflow['ImProc']['Status'] = 'Initialised'

    def save_channel(self, im_proc):
        im_name = self.parent_organ.user_organName + '_StckProc_' + self.channel_no + '.npy'
        im_dir = self.parent_organ.settings['dirs']['s3_numpy'] / im_name
        np.save(im_dir, im_proc)
        if not im_dir.is_file():
            print('>> Error: Processed channel was not saved correctly!\n>> File: '+im_name)
            alert('error_beep')
        else: 
            print('>> Processed channel saved correctly! - ', im_name)
            # print('>> Directory: '+ str(im_dir)+'\n')
            alert('countdown')
            self.dir_stckproc = im_dir
    
    def ch_clean (self, s3, s3_mask, option, inverted=True, plot=False, im_every=25): 
        """
        Function to clean channel using the other as a mask
        """
        
        if option == "cj":
            print('- Extracting cardiac jelly')
        elif option == "clean":
            print('- Cleaning endocardium ('+ self.channel_no + '-' + s3.cont_type +')')

        s3_s = s3.s3()
        s3_mask_s = s3_mask.s3()
        
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
                    self.slc_plot(slc, inv_slc, toClean_slc, toRemove_slc, cleaned_slc, option, inverted)

                s3_bits[:,:,slc] = toRemove_slc
                s3_new[:,:,slc] = cleaned_slc
                
            s3_new = s3_new.astype('uint8')
            s3.s3_save(s3_new)
            alert('whistle')            
        
        else:
            print('>> Index different to 2, check!')
            alert('error_beep')

    def slc_plot (self, slc, mask_slc, toClean_slc, toRemove_slc, cleaned_slc, option, inverted):
        """
        Function to plot mask, original image and result
        """
        if option == 'clean':
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

class ContStack(): 
    'morphoHeart Contour Stack Class'
    def __init__(self, im_channel:ImChannel, cont_type:str, new=False, layerDict={}):
        
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
        dir2save = organ.settings['dirs']['s3_numpy'] / self.s3_file
        np.save(dir2save, s3)
        if not dir2save.is_file():
            print('>> Error: s3 file was not saved correctly!\n>> File: '+self.s3_file)
            alert('error_beep')
        else: 
            print('>> s3 file saved correctly! - ', self.cont_type)
            # print('>> Directory: '+ str(dir2save)+'\n')
            alert('countdown')

   
class Mesh_mH():
    'morphoHeart Mesh Class'
    
    def __init__(self, imChannel:ImChannel, mesh_type:str, 
                 extractLargest:bool, rotateZ_90:bool, new=True):
        
        self.parent_organ = imChannel.parent_organ
        self.imChannel = imChannel
        self.channel_no = imChannel.channel_no
        self.user_meshName = self.parent_organ.settings[self.channel_no]['general_info']['user_chName']
        self.mesh_type = mesh_type
        self.legend = self.user_meshName+'_'+self.mesh_type
        self.resolution = imChannel.get_resolution()
        if new: 
            self.create_mesh(extractLargest = extractLargest, rotateZ_90 = rotateZ_90)
        else: 
            self.load_mesh()
        self.color = self.parent_organ.settings[self.channel_no]['general_info']['colorCh_'+self.mesh_type]
        self.set_color(self.color)
        self.alpha = 1
        self.set_alpha(self.alpha)
        self.parent_organ.add_mesh(self, new=True)
        if new: 
            self.save_mesh()
    
    def create_mesh(self, extractLargest:bool, rotateZ_90:bool):
        # Extract vertices, faces, normals and values of each mesh
        if self.mesh_type == 'int':
            s3 = self.imChannel.s3_int.s3()
        elif self.mesh_type == 'ext':
            s3 = self.imChannel.s3_ext.s3()
        elif self.mesh_type == 'tiss':
            s3 = self.imChannel.s3_tiss.s3()
        # print(s3)
        verts, faces, _, _ = measure.marching_cubes_lewiner(s3, spacing=self.resolution)
    
        # Create meshes
        mesh = vedo.Mesh([verts, faces])
        if extractLargest:
            mesh = mesh.extractLargestRegion()
        if rotateZ_90:
            mesh.rotateZ(-90)
        mesh.legend(self.legend).wireframe()
        self.mesh = mesh
    
    def load_mesh(self):
        parent_organ = self.parent_organ
        mesh_name = parent_organ.user_organName+'_'+self.legend+'.vtk'
        mesh_dir = parent_organ.settings['dirs']['meshes'] / mesh_name
        mesh_out = vedo.load(str(mesh_dir))
        self.mesh = mesh_out

    def save_mesh(self):
        parent_organ = self.parent_organ
        mesh_name = parent_organ.user_organName+'_'+self.legend+'.vtk'
        mesh_dir = parent_organ.settings['dirs']['meshes'] / mesh_name
        self.dir_out = mesh_dir
        mesh_out = self.mesh
        mesh_out.write(str(mesh_dir))
        print('>> Mesh '+mesh_name+' has been saved!')
        alert('countdown')        
        self.parent_organ.add_mesh(self, new=True)

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
    
    def get_alpha(self):
        return self.mesh_alpha
        
    def set_color(self, mesh_color):
        self.color = mesh_color
        self.mesh.color(self.color)
        
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

print('morphoHeart! - Loaded Module Classes')
