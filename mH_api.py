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

#%% GUI related
alert_all=True
heart_default=False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}
fcBasics.alert('woohoo', dict_gui['alert_all'])

partA = False
partB = True
partC = True
if partA:
    #%
    # Info coming from the gui (user's selection)
    # 1. Click: Create new project
    proj = mHC.Project()
    proj.__dict__

    #%
    # Once the project is created a new window will appear to select all the settings for the project
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
    print('>> proj.dict_projInfo: ', proj.dict_info)

    # The result of the modification of such table is shown in the dict 
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
    # print('>>proj.dict_info:', proj.dict_info)

    # And a project status dictionary is created
    proj.set_project_status()
    # print('>>proj.dict_workflow:', proj.dict_workflow)

    #%
    # Save project 
    proj.save_mHProject()

    #%
    # Having created the project an organ is created as part of the project
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
    # print('organ.settings:',organ.settings)
    # print('organ.workflow:', organ.workflow)

    #%
    # Save initial organ project
    proj.addOrgan(organ)
    organ.save_organProject()

    #%
    # CODE A ---------------------------------------------------------
    ## CHANNEL 1
    im_ch1 = organ.loadTIFF(ch_name='ch1')
    im_ch1.maskIm()
    im_ch1.saveChannel()
    organ.addChannel(im_ch1)

    im_ch1.closeContours_auto()
    im_ch1.closeContours_manual()
    im_ch1.closeInfOutf()
    im_ch1.selectContours()
    layerDict = {}
    im_ch1.create_chS3s(layerDict=layerDict)
    organ.addChannel(im_ch1)

    ## CHANNEL 2
    # im_ch2 = organ.loadTIFF(ch_name='ch2')
    # im_ch2.maskIm()
    # im_ch2.saveChannel()
    # organ.addChannel(im_ch2)
    
    #%
    # Save amended organ project 
    proj.save_mHProject()
    organ.save_organProject()

    #%
    # Delete organ and project
    # del organ
    # del proj
    # del im_ch1

if partB: 
    #% CODE B
    # Load organ and project
    projName2Load = 'Project_A-B'
    folder_name = 'R_'+projName2Load
    dir2load = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart') / folder_name
    load_dict = {'name': projName2Load, 'dir': dir2load}
    proj_new = mHC.Project(new = False, load_dict = load_dict)

    organName2Load = 'LS52_F02_V_SR_1029'
    organ_new = proj_new.loadOrgan(user_organName = organName2Load)

    #%
    im_ch1_new = mHC.ImChannel(organ=organ_new, ch_name='ch1', new=False)
    im_ch1_new.loadContStack(cont_type='int')
    im_ch1_new.loadContStack(cont_type='ext')
    






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
