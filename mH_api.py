'''
morphoHeart_api_B

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''

#%% ##### - Imports - ########################################################
# import pathlib
import sys

from pathlib import Path
import numpy as np
import os
import vedo as vedo


print('package:', __package__)
print('name:', __name__)

#%% ##### - morphoHeart Imports - ##################################################
# import src.mH_exceptions as mHExcp
from src.modules import mH_classes as mHC
from src.modules import mH_funcBasics as fcBasics
from src.modules import mH_funcMeshes as fcMeshes

#%% Info coming from the gui (user's selection)
# 1. Click: Create new project
proj = mHC.Project()
proj.__dict__

#%% 
# 2. Once the project is created a new window will appear to select all the 
# settings for the project
if sys.platform == 'darwin':
    dir_proj_res = Path('/Users/juliana/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/')
elif sys.platform == 'win32':
    dir_proj_res = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/')

user_projName = 'Project A-B'
user_projNotes = 'Project to compare embryos A and B'
no_chs = 2
name_chs = ['myocardium', 'endocardium']
color_chs_tiss_ext_int = [['lightseagreen','gold','crimson'],['darkmagenta','deepskyblue','deeppink']]
layer_btw_chs = True
ch_ext = ('ch1', 'int')
ch_int = ('ch2', 'ext')
user_nsChName = 'cardiac jelly'
color_chns_tiss_ext_int = ['darkorange','crimson','deepskyblue']
# By default the volume and surface area of the segments per tissue selected will be measured
cutLayersIn2Segments = True
no_segments = 2
name_segments = ['atrium', 'ventricle']
# channels/meshes that will be divided into segments 
ch_segments = {'ch1':['tissue', 'ext'],'ch2':['tissue', 'int'],'chNS':['tissue']}
proj_dir = dir_proj_res

user_proj_settings = {'project_dir': proj_dir,
                    'user_projName': user_projName,
                    'user_projNotes' : user_projNotes,
                    'no_chs': no_chs,
                    'name_chs': name_chs,
                    'color_chs': color_chs_tiss_ext_int,
                    'ns': 
                        {'layer_btw_chs': layer_btw_chs,
                        'ch_ext': ch_ext,
                        'ch_int': ch_int,
                        'user_nsChName': user_nsChName,
                        'color_chns': color_chns_tiss_ext_int},
                    'segments': 
                        {'cutLayersIn2Segments': cutLayersIn2Segments,
                        'no_segments': no_segments,
                        'name_segments': name_segments,
                        'ch_segments': ch_segments}, 
                        }

# This will create attributes within the instance of the project
# containing information of the settings selected by the user
# Additionally, based on the number of segments and channels selected, 
# a dictionary with predefined measurement parameters is created with 
# which a table in the GUI will be created for the user to modify
proj.create_gralprojWF(user_proj_settings=user_proj_settings)
# Create project directory
proj.create_proj_dir(dir_proj_res)
print('>>proj.dict_projInfo: ', proj.dict_info)

#%% The result of the modification of such table is shown in the dict 
# called user_params2meas.
user_params2meas = {'ch1': {'tissue': {'whole': {'volume': True,
                                            'surf_area': False,
                                            'thickness int>ext': True,
                                            'thickness ext>int': False,
                                            'centreline': True,
                                            'centreline_linlength': True,
                                            'centreline_looplength': True},
                                        'segm1': {'volume': True,
                                            'surf_area': False,
                                            'thickness int>ext': False,
                                            'thickness ext>int': False},
                                        'segm2': {'volume': True,
                                            'surf_area': False,
                                            'thickness int>ext': False,
                                            'thickness ext>int': False}},
                            'int':    {'whole': {'volume': True,
                                            'surf_area': True,
                                            'centreline': True,
                                            'centreline_linlength': True,
                                            'centreline_looplength': True}},
                            'ext':    {'whole': {'volume': True,
                                            'surf_area': True,
                                            'centreline': True,
                                            'centreline_linlength': True,
                                            'centreline_looplength': True},
                                        'segm1': {'volume': True, 'surf_area': True},
                                        'segm2': {'volume': True, 'surf_area': True}}},
                    'ch2': {'tissue': {'whole': {'volume': True,
                                            'surf_area': False,
                                            'thickness int>ext': True,
                                            'thickness ext>int': False,
                                            'centreline': True,
                                            'centreline_linlength': True,
                                            'centreline_looplength': True},
                                        'segm1': {'volume': True,
                                            'surf_area': False,
                                            'thickness int>ext': False,
                                            'thickness ext>int': False},
                                        'segm2': {'volume': True,
                                            'surf_area': False,
                                            'thickness int>ext': False,
                                            'thickness ext>int': False}},
                            'int':    {'whole': {'volume': True,
                                            'surf_area': True,
                                            'centreline': False,
                                            'centreline_linlength': False,
                                            'centreline_looplength': False},
                                        'segm1': {'volume': True, 'surf_area': True},
                                        'segm2': {'volume': True, 'surf_area': True}},
                            'ext': {'whole': {'volume': True,
                                            'surf_area': True,
                                            'centreline': True,
                                            'centreline_linlength': True,
                                            'centreline_looplength': True}}},
                    'chNS': {'tissue': {'whole': {'volume': True,
                                            'surf_area': False,
                                            'thickness int>ext': True,
                                            'thickness ext>int': False,
                                            'centreline': False,
                                            'centreline_linlength': False,
                                            'centreline_looplength': False},
                                        'segm1': {'volume': True,
                                            'surf_area': False,
                                            'thickness int>ext': False,
                                            'thickness ext>int': False},
                                        'segm2': {'volume': True,
                                            'surf_area': False,
                                            'thickness int>ext': False,
                                            'thickness ext>int': False}},
                            'int': {'whole': {'volume': True,
                                            'surf_area': True,
                                            'centreline': False,
                                            'centreline_linlength': False,
                                            'centreline_looplength': False}},
                            'ext': {'whole': {'volume': True,
                                            'surf_area': True,
                                            'centreline': False,
                                            'centreline_linlength': False,
                                            'centreline_looplength': False}}}}

user_ball_settings = {'ballooning': True, 'ball_settings': {
                            'ball_op1': {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch2', 'from_cl_type': 'int'},
                            'ball_op2': {'to_mesh': 'ch2', 'to_mesh_type': 'ext', 'from_cl': 'ch2', 'from_cl_type': 'ext'}}}

proj.set_measure_param(user_params2meas=user_params2meas, user_ball_settings=user_ball_settings)
print('>>proj.dict_info:', proj.dict_info)

# And a project status dictionary is created
proj.set_project_status()
print('>>proj.dict_workflow:', proj.dict_workflow)

#%% Save project 
proj.save_mHProject()

#%% Having created the project an organ is created as part of the project
user_organName = 'LS52_F02_V_SR_1029'
user_organNotes = 'Wild-type heart 1'
im_orientation = 'ventral'
custom_angle = 0
pix_x = 0.22832596445005054
pix_y = 0.22832596445005054
pix_z = 0.652961
units_x = 'um'
units_y = 'um'
units_z = 'um'

# non essential info
stage = '72-74hpf'
strain = 'myl7:lifeActGFP, fli1a:AcTag-RFP'
genotype = 'wt'

user_organ_settings = {'project': {'user': proj.user_projName,
                                    'mH': proj.mH_projName,
                                    'dict_info_dir': proj.info_dir},
                        'user_organName': user_organName,
                        'user_organNotes': user_organNotes,
                        'im_orientation': im_orientation,
                        'custom_angle': custom_angle,
                        'resolution': [pix_x, pix_y, pix_z],
                        'units_resolution': [units_x, units_y, units_z],
                        'stage': stage, 
                        'strain': strain, 
                        'genotype': genotype,
                        }

# - Load Channels
# mH_chName1 = 'ch1'
if sys.platform == 'darwin':
    dir_cho1 = Path('/Users/juliana/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch0_EDC.tif')
    dir_mkch1 = Path('/Users/juliana/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch0_mask.tif')
elif sys.platform == 'win32':
    dir_cho1 = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch0_EDC.tif')
    dir_mkch1 = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch0_mask.tif')

mask_ch1 = True

# mH_chName2 = 'ch2'
if sys.platform == 'darwin':
    dir_cho2 = Path('/Users/juliana/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_EDC.tif')
    dir_mkch2 = Path('/Users/juliana/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_mask.tif')
elif sys.platform == 'win32': 
    dir_cho2 = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_EDC.tif')
    dir_mkch2 = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_mask.tif')

mask_ch2 = True

info_loadCh = {'ch1':{'dir_cho': dir_cho1, 
                        'mask_ch': mask_ch1,
                        'dir_mk': dir_mkch1},
                'ch2':{'dir_cho': dir_cho2, 
                        'mask_ch': mask_ch2,
                        'dir_mk': dir_mkch2},   
               }

organ = mHC.Organ(project=proj, user_settings = user_organ_settings,
                        info_loadCh = info_loadCh)


# Try loading files of dictLoadChannels before creating dict
import pathlib
from skimage import io

def loadTIF(dir_in:pathlib.PosixPath, test=False):
    if test: 
        try: 
            images_o = io.imread(str(dir_in))
            success = True
        except FileNotFoundError:
            success = False
            print(f'Error: Invalid file {dir_in}')
        return success

errors = []
for ch in ['ch1', 'ch2']: 
    for name in ['cho', 'mk']:
        dir_in = dict_loadCh[ch]['dir_'+name]
        print(dir_in)
        success = loadTIF(dir_in = dir_in, test=True)
        errors.append((dir_in, success))

# - Analsysis Pipeline
# -- segment layer between channels
layer_btw_chs = True
ch_ext = 'ch1-myocardium'
ch_int = 'ch2-endocardium'
mH_nsChName = 'chNS'
user_nsChName = 'cardiac jelly'

# -- cut layers into segments
cutLayersIn2Segments = True
segments_no = 2
user_segName1 = 'atrium'
mH_segName1 = 'segm1'
user_segName2 = 'ventricle'
mH_segName2 = 'segm2'

# -- parameters to measure
params2measure = {'ch1':
                    {'tiss': 
                        {'all':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True, 
                            'cutIn2Segments': True},
                        'segm1':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True, 
                            'ballooning': True},
                        'segm2':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'ballooning': True, 
                            'thck_ext2int': True,
                            'ballooning': True}
                        },
                    'int': 
                        {'all':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True, 
                            'ballooning': True, 
                            'cutIn2Segments': True},
                        'segm1':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True},
                        'segm2':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True, }
                        },                      
                    'ext': 
                        {'all':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True, 
                            'ballooning': True, 
                            'cutIn2Segments': True},
                        'segm1':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True},
                        'segm2':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True}
                        }
                    }, 
                'ch2':
                    {'tiss': 
                        {'all':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True, 
                            'cutIn2Segments': True},
                        'segm1':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True, 
                            'ballooning': True},
                        'segm2':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'ballooning': True, 
                            'thck_ext2int': True,
                            'ballooning': True}
                        },
                    'int': 
                        {'all':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True, 
                            'ballooning': True, 
                            'cutIn2Segments': True},
                        'segm1':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True},
                        'segm2':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True, }
                        },                      
                    'ext': 
                        {'all':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True, 
                            'ballooning': True, 
                            'cutIn2Segments': True},
                        'segm1':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True},
                        'segm2':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True}
                        }
                    }, 
                'chNS':
                    {'tiss': 
                        {'all':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True, 
                            'cutIn2Segments': True},
                        'segm1':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True, 
                            'ballooning': True},
                        'segm2':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'ballooning': True, 
                            'thck_ext2int': True,
                            'ballooning': True}
                        },
                    'int': 
                        {'all':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True, 
                            'ballooning': True, 
                            'cutIn2Segments': True},
                        'segm1':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True},
                        'segm2':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True, }
                        },                      
                    'ext': 
                        {'all':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True, 
                            'ballooning': True, 
                            'cutIn2Segments': True},
                        'segm1':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True},
                        'segm2':
                            {'surf_area' : True, 
                            'volume': True, 
                            'centreline': True, 
                            'centreline_legnth': True,
                            'linear_length': True,
                            'thck_int2ext': True,
                            'thck_ext2int': True,
                            'ballooning': True}
                        }
                    }, 
                }

dict_AnPipeline = {'ns': 
                        {'layer_btw_chs': layer_btw_chs,
                        'ch_ext': ch_ext,
                        'ch_int': ch_int,
                        'mH_nsChName': mH_nsChName,
                        'user_nsChName': user_nsChName},
                    'segments': 
                        {'cutLayersIn2Segments':cutLayersIn2Segments,
                        'segments_no': segments_no, 
                        'user_segName1': user_segName1, 
                        'mH_segName1': mH_segName1,
                        'user_segName2': user_segName2,
                        'mH_segName2': mH_segName2,},
                    'params2measure': params2measure,
                    }

#%% GUI related
alert_all=True
heart_default=False

dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}

# Analysis Progress Dict
# ADDD!!!
#%% 
# connection = 24
fcBasics.alert('woohoo', dict_gui['alert_all'])

#%% Create instances of classes based on initial set-up
organ1 = mHC.Organ(user_name_in=dict_projInfo['mH_projName'],
                   dir_channels=dict_projInfo['dir_channels'],
                   dir_res=dict_projInfo['dir_res'], 
                   no_chs = dict_loadCh['no_chs'],
                   stage=dict_projInfo['stage'],
                   strain=dict_projInfo['strain'], 
                   genotype=dict_projInfo['genotype'])

print(organ1.__dict__)

#%%
fcBasics.save_mHProject(dicts={'dict_projInfo':dict_projInfo, 'dict_loadCh':dict_loadCh,
                                'dict_AnPipeline':dict_AnPipeline, 'dict_gui':dict_gui}, organ= organ1)


#%%  Create Channel 1 - Myocardium (external)
ch01 = mHC.ImChannel(channel_no=dict_loadCh['ch1']['mH_chName'], 
                      organ=organ1,
                      user_chName=dict_loadCh['ch1']['user_chName'], 
                      resolution= dict_projInfo['resolution'],
                      im_orientation=dict_projInfo['im_orientation'], 
                      to_mask=dict_loadCh['ch1']['mask_ch'], 
                      dir_cho=dict_loadCh['ch1']['dir_cho'])
print(ch01.__dict__)
ch01.load_chS3s(organ=organ1)

#%%  Create Channel 2 - Endocardium (internal)
ch02 = mHC.ImChannel(channel_no=dict_loadCh['ch2']['mH_chName'], 
                      organ=organ1,
                      user_chName=dict_loadCh['ch2']['user_chName'], 
                      resolution= dict_projInfo['resolution'],
                      im_orientation=dict_projInfo['im_orientation'], 
                      to_mask=dict_loadCh['ch2']['mask_ch'], 
                      dir_cho=dict_loadCh['ch2']['dir_cho'])
print(ch02.__dict__)
ch02.load_chS3s(organ=organ1)

#%% Clean endocardium
clean_ch2wch1 = True
if clean_ch2wch1:
    pass

#%%
user_meshName = 'myocardium'
mesh_type = 'tissue'
mesh_color = 'teal'
mesh_alpha = 0.1
contours_source = np.array(range(10))

extractLargest = False
npy_mesh = np.load(os.path.join(str(organ1.dir_res), 'stacks_npy','LS52_F02_V_SR_1029_s3_ch0_all.npy'))
rotateZ_90 = True
chMyoc = 'AA'
m_Myoc = mHC.Mesh_mH(organ=organ1, 
                     imChannel=chMyoc,
                     user_meshName = user_meshName,
                     mesh_type=mesh_type, 
                     npy_mesh=npy_mesh,
                     extractLargest=extractLargest, 
                     rotateZ_90=rotateZ_90)

print(m_Myoc.__dict__)

vp = vedo.Plotter(N=1, axes=1)
vp.show(m_Myoc.mesh, at=0, zoom=1.2, interactive=True)

# m_Myoc.set_mesh_alpha(0.1)
m_Myoc.set_mesh_color('Teal')
m_Myoc.set_mesh_alpha(0.1)
        
vp = vedo.Plotter(N=1, axes=1)
vp.show(m_Myoc.mesh, at=0, zoom=1.2, interactive=True)

myoc = m_Myoc.mesh
m_Myoc.mesh.volume()
m_Myoc.mesh.area()


# %%
