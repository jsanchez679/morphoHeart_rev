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
from skimage import measure, io
import copy
import json
import collections
import pprint

#%% ##### - Other Imports - ##################################################
from .mH_funcBasics import alert

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
    def __init__(self):

        def create_mHName(self):
            '''
            func - create name for a morphoHeart project
            This function will assign the newly created project a name using a
            timestamp
            '''
            now_str = datetime.now().strftime('%Y%m%d%H%M')
            self.mH_projName = 'mH_Proj-'+now_str

        create_mHName(self)
        self.organs = {}

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

        self.dict_info = {'mH_projName': self.mH_projName,
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

        self.dict_settings = settings
        self.gral_meas_keys = gral_meas_keys
        self.channels = channels
        segments_new = list(set(segments))
        self.segments = sorted(segments_new) #possible unsorted
        self.dict_info['channels'] = self.channels
        self.dict_info['segments'] = self.segments
            
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
        self.dict_params_deflt = dict_params_deflt
        #Use this two result variables to create selecting table in the GUI

    def set_measure_param(self, user_params2meas:dict, user_ball_settings:dict):
        '''
        This function will get the input of the updated selected parameters from the GUI and 
        will include those measurements in the dictionary of the project. This dictionary will then 
        be used as a workflow template for all the Organs created within the project. 
        '''
        settings_updated = copy.deepcopy(self.dict_settings)
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
        self.dict_info['gral_meas_keys'] = self.gral_meas_keys
        self.dict_info['gral_meas_param'] = self.gral_meas_param
        self.dict_info['dict_settings'] = self.dict_settings
        
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
        
        self.dict_settings = settings_updated
        self.gral_meas_param = sorted(gral_meas_param_new)

    def create_proj_dir(self, dir_proj:pathlib.WindowsPath):
        # set_dir_res()
        folder_name = 'R_'+self.user_projName
        self.dir_proj = Path(os.path.join(dir_proj,folder_name))
        self.dir_proj.mkdir(parents=True, exist_ok=True)
        self.dict_info['dir_proj'] = self.dir_proj

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
                dict_ImProc[ch] = {'A-MaskChannel': {'Status': 'NotInitialised'},
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
                dict_ImProc[ch] = {'D-S3Create':{'Status': 'NotInitialised',
                                                'Info':{'tissue':{'Status': 'NotInitialised', 
                                                            'Info':{}},
                                                        'int':{'Status': 'NotInitialised', 
                                                                    'Info':{}},
                                                        'ext':{'Status': 'NotInitialised', 
                                                                    'Info':{}}},
                                                'Settings':{'ext_mesh': self.dict_settings[ch]['general_info']['ch_ext'],
                                                            'int_mesh': self.dict_settings[ch]['general_info']['ch_int']}}} 
             
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
                            'Settings': {'from_cl': self.dict_settings[ch]['measure'][cont]['whole']['ballooning']['from_cl'],
                                        'from_cl_type': self.dict_settings[ch]['measure'][cont]['whole']['ballooning']['from_cl_type']}}

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

        self.dict_workflow = workflow
        self.dict_info['dict_workflow'] = self.dict_workflow

    def save_mHProject(self):
        jsonDict_name = 'mH_'+self.user_projName+'_project.json'
        json2save_par = self.dir_proj / 'settings'
        json2save_par.mkdir(parents=True, exist_ok=True)
        if not json2save_par.is_dir():
            print('>> Error: Settings directory could not be created!\n>> Directory: '+jsonDict_name)
            alert('error_beep')
        else: 
            json2save_dir = json2save_par / jsonDict_name
            dict_info = copy.deepcopy(self.dict_info)

            with open(str(json2save_dir), "w") as write_file:
            # with open('AAA.json', "w") as write_file:
                json.dump(dict_info, write_file, cls=NumpyArrayEncoder)

            if not json2save_dir.is_file():
                print('>> Error: Project settings file was not saved correctly!\n>> File: '+jsonDict_name)
                alert('error_beep')
            else: 
                self.info_dir = self.dir_proj / 'settings' / jsonDict_name
                print('>> Project settings file saved correctly!\n>> File: '+jsonDict_name)
                print('>> File: '+ str(json2save_dir))
                alert('countdown')
    
    def addOrgan(self, organ):
        dict_organ = copy.deepcopy(organ.dict_info)
        dict_organ.pop('project', None)
        dict_organ['dir_res'] = organ.dir_res
        self.organs[organ.mH_organName] = dict_organ

    def removeOrgan(self, organ):
        organs = copy.deepcopy(self.organs)
        organs.pop(organ.mH_organName, None)
        self.organs = organs

class Organ():
    'Organ Class'
    
    def __init__(self, project:Project, user_settings:dict, info_loadCh:dict):
        
        self.create_mHName()
        self.user_organName = user_settings['user_organName'].replace(' ', '_')
        self.parent_project = project

        self.settings = copy.deepcopy(project.dict_settings)
        self.workflow = copy.deepcopy(project.dict_workflow)
        self.dict_info = {}
        self.dict_info = user_settings

        self.checkChannels(project, info_loadCh)
                 
    def checkChannels(self, project:Project, info_loadCh:dict):
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
            print('>> Files have been checked! \n>> Images shape:')
            pprint.pprint(array_sizes)

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

    def save_organProject(self):
        jsonDict_name = 'mH_'+self.user_organName+'_organ.json'
        json2save_dir = self.settings['dirs']['settings'] / jsonDict_name
        self.all_info = {}
        self.all_info['Organ'] = self.dict_info
        self.all_info['dict_settings'] = self.settings
        self.all_info['dict_workflow'] = self.workflow

        with open(str(json2save_dir), "w") as write_file:
            json.dump(self.all_info, write_file, cls=NumpyArrayEncoder)

        if not json2save_dir.is_file():
            print('>> Error: Organ settings file was not saved correctly!\n>> File: '+jsonDict_name)
            alert('error_beep')
        else: 
            self.info_dir = self.dir_res / 'settings' / jsonDict_name
            print('>> Organ settings file saved correctly!\n>> File: '+jsonDict_name)
            print('>> Directory: '+ str(json2save_dir))
            alert('countdown')

    def create_mHName(self):
        now_str = datetime.now().strftime('%Y%m%d%H%M')
        self.mH_organName = 'mH_Organ-'+now_str

    #Get all the set mH variables in __init__
    def get_notes(self):
        return self.dict_info['user_organNotes']

    def get_orientation(self):
        return self.dict_info['im_orientation']

    def get_custom_angle(self):
        return self.dict_info['custom_angle']
    
    def get_resolution(self):
        return self.dict_info['resolution']

    def get_units_resolution(self):
        return self.dict_info['units_resolution']

    def get_stage(self):
        return self.dict_info['stage']

    def get_strain(self):
        return self.dict_info['strain']

    def get_genotype(self):
        return self.dict_info['genotype']

    def get_dir_res(self):
        return self.dir_res

    def get_direc(self, name:str):
        return self.settings['dirs'][name]

    def loadTIFF(self, ch_name:str):
        image = ImChannel(organ=self, ch_name=ch_name)
        return image

    def update_workflow(self, process):
        print('Update workflow!')

class ImChannel(): #channel
    'morphoHeart Image Channel Class'
    
    def __init__(self, organ:Organ, ch_name:str):

        dir_im = organ.settings[ch_name]['general_info']['dir_cho']
        im = io.imread(str(dir_im))
        if not isinstance(im, np.ndarray):
            print('>> Error: morphoHeart was unable to load tiff.\n>> Directory: ',str(dir_im))
            alert('error_beep')
        self.im = im
        self.parent_organ = organ
        self.channel_no = ch_name
        self.to_mask = organ.settings[ch_name]['general_info']['mask_ch']
        self.resolution = organ.dict_info['resolution']
        self.dir_cho = organ.settings[ch_name]['general_info']['dir_cho']
        if self.to_mask:
            self.dir_mk = organ.settings[ch_name]['general_info']['dir_mk']
        self.masked = False
        self.im_shape = im.shape
        
    def get_channel_no(self):
        return self.channel_no

    def get_resolution(self):
        return self.resolution

    def get_im_shape(self):
        return self.im_shape
        
    def maskIm(self):
        #Check better this function
        im_o = np.copy(self.im)
        im_mask = io.imread(str(self.dir_mk))
        if self.im_shape == im_mask.shape:
            #Check the dimensions of the mask with those of the image
            im_o[im_mask == False] = 0
            self.masked = True
            self.im_masked = im_o
        else: 
            print('>> Error: Stack could not be masked (stack shapes did not match).')
            alert('error_beep')

    def create_chS3s (self, layerDict:dict):
        s3_int = ContStack(im_channel = self, layerDict = layerDict, cont_type = 'int')
        self.s3_int = s3_int

        s3_ext = ContStack(im_channel = self, layerDict = layerDict, cont_type ='ext')
        self.s3_ext = s3_ext

        s3_tiss = ContStack(im_channel = self, layerDict = layerDict, cont_type ='all')
        self.s3_tiss = s3_tiss

    # def load_chS3s (self, organ:Organ):
    #     s3_int = ContStack(organ, self.channel_no, cont_type='int')
    #     print(s3_int.__dict__)
    #     s3_int.loadContStack(organ, self.channel_no, s3_int.cont_type)
    #     self.s3_int = s3_int

    #     s3_ext = ContStack(organ, self.channel_no, cont_type='ext')
    #     print(s3_ext.__dict__)
    #     s3_ext.loadContStack(organ, self.channel_no, s3_ext.cont_type)
    #     self.s3_ext = s3_ext

    #     s3_tiss = ContStack(organ, self.channel_no, cont_type='all')
    #     print(s3_tiss.__dict__)
    #     s3_tiss.loadContStack(organ, self.channel_no, s3_tiss.cont_type)
    #     self.s3_tiss = s3_tiss

class ContStack(): 
    'morphoHeart Contour Stack Class'
    def __init__(self, im_channel:ImChannel, layerDict:dict, cont_type:str):

        self.cont_type = cont_type
        self.im_channel = im_channel
        self.cont_name = im_channel.channel_no+'_'+self.cont_type
        self.s3 = self.s3_create(layerDict = layerDict)
        self.s3_save()
    
    def s3_create(self, layerDict:dict):
        x_dim = self.im_channel.im_shape[0]
        y_dim = self.im_channel.im_shape[1]
        z_dim = self.im_channel.im_shape[2]
        
        s3 = np.empty((x_dim,y_dim,z_dim+2))
        for pos, keySlc in enumerate(layerDict.keys()):
            if keySlc[0:3] == "slc":
                slcNum = int(keySlc[3:6])
                im_FilledCont = layerDict[keySlc][self.cont_type]
                s3[:,:,slcNum+1] = im_FilledCont
        s3 = s3.astype('uint8')
        return s3

    def s3_save(self):
        im_channel = self.im_channel
        organ = im_channel.parent_organ
        s3_name = organ.user_organName + '_s3_' + im_channel.channel_no + '_' + self.cont_type + '.npy'
        self.s3_file = s3_name
        dir2save = organ.settings['dirs']['s3_numpy'] / s3_name
        np.save(dir2save, self.s3)
        print('>> s3 files saved correctly!')
        print('>> Directory: '+ str(dir2save))
        alert('countdown')

    def loadContStack(self, organ:Organ, channel_no:int, cont_type:str):
        s3_name = organ.user_organName + '_s3_' + str(channel_no) + '_' + cont_type + '.npy'
        s3_dir = organ.dir_res / 'stacks_npy' / s3_name
        s3 = np.load(s3_dir)
        if cont_type == 'int':
            self.s3 = s3
        elif cont_type == 'ext':
            self.s3 = s3
        elif cont_type == 'all' or cont_type == 'tiss':
            self.s3 = s3

class Mesh_mH():
    'morphoHeart Mesh Class'
    
    def __init__(self, organ:Organ,imChannel:ImChannel, 
                 user_meshName:str, mesh_type:str, 
                 npy_mesh:np.ndarray, 
                 extractLargest:bool, rotateZ_90:bool):
        
        self.channel_no = imChannel.channel_no 
        self.user_meshName = user_meshName
        self.mesh_type = mesh_type
        self.mH_meshName = organ.mH_organName+'_ch0'+str(self.channel_no)+'_'+mesh_type
        
        # Attributes from ImChannel
        self.imchannel = imChannel #(resolution, mH_chName, user_chName)
        self.organ = Organ #(get_mH_organName, user_organName))
        
        self.create_mesh(npy_mesh, self.imchannel.resolution, extractLargest, rotateZ_90)
        
    def get_channel_no(self):
        return self.channel_no
    
    def get_user_meshName(self):
        return self.user_meshName
    
    def change_user_meshName(self, new_user_meshName):
        self.user_meshName = new_user_meshName
    
    def get_mesh_type(self):
        return self.mesh_type
    
    def get_mH_meshName(self):
        return self.mH_meshName
    
    def get_imchannel(self):
        return self.imchannel
    
    def get_organ(self):
        return self.organ
    
    def set_contours_source(self, contours_source):
        self.contours_source = contours_source
    
    def set_mesh_alpha(self, mesh_alpha):
        self.mesh_alpha = mesh_alpha
        self.mesh.alpha(self.mesh_alpha)
    
    def get_mesh_alpha(self):
        return self.mesh_alpha
        
    def set_mesh_color(self, mesh_color):
        self.mesh_color = mesh_color
        self.mesh.color(self.mesh_color)
        
    def get_mesh_color(self):
        return self.mesh_color
        
    def create_mesh(self, npy_mesh:np.ndarray, resolution:list, extractLargest:bool, rotateZ_90:bool) -> 'Mesh_mH':

        # Extract vertices, faces, normals and values of each mesh
        verts, faces, _, _ = measure.marching_cubes_lewiner(npy_mesh, spacing=resolution)
    
        # Create meshes
        mesh = vedo.Mesh([verts, faces])
        if extractLargest:
            mesh = mesh.extractLargestRegion()
        if rotateZ_90:
            mesh.rotateZ(-90)
        mesh.legend(self.user_meshName).wireframe()
        
        self.mesh = mesh
        #mesh = vedo.mesh.Mesh
        
    def get_mesh(self):
        try: 
            return self.mesh #confirmar con vedo
        except:
            return None
    
    def getCentreline(self): 
        pass

print('morphoHeart! - Loaded Module Classes')
