'''
morphoHeart_api_B

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''

#%% ##### - Imports - ########################################################
# import pathlib
import sys
from pathlib import Path

print('package:', __package__)
print('name:', __name__)

#%% ##### - morphoHeart Imports - ##################################################
# import src.mH_exceptions as mHExcp
from src.modules import mH_funcMeshes as fcMeshes
from src.modules import mH_classes as mHC
from src.modules import mH_funcBasics as fcBasics

#%% GUI related
fcBasics.alert('woohoo')
# Setting the path to the project results
if sys.platform == 'darwin':
    dir_proj_res = Path('/Users/juliana/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/')
elif sys.platform == 'win32':
    dir_proj_res = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/')
    #dir_proj_res = Path('C://Users//pallo//Desktop//cosas juli//mh//project')
    
partA = False
partB = True
partB_vmtk = True
partC = True
print('partA:',partA,'- partB:',partB,'- partB_vmtk:',partB_vmtk,'- partC:',partC)

#%% Part A
if partA:
    #%
    # Info coming from the gui (user's selection)
    # 1. Click: Create new project
    print('\n---CREATING PROJECT----')
    proj = mHC.Project()
    proj.__dict__

    # Once the project is created a new window will appear to select all the settings for the project
    user_projName = 'Project A-B'
    user_projNotes = 'Project to compare embryos A and B'
    no_chs = 2
    name_chs = ['myocardium', 'endocardium']
    chs_relation = ['external', 'internal']
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
    ch_segments = {'ch1':['tiss', 'ext'],'ch2':['tiss', 'int'],'chNS':['tiss']}
    proj_dir = dir_proj_res

    user_proj_settings = {'project_dir': proj_dir,
                        'user_projName': user_projName,
                        'user_projNotes' : user_projNotes,
                        'no_chs': no_chs,
                        'name_chs': name_chs,
                        'chs_relation': chs_relation,
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
    print('>> proj.dict_projInfo: ', proj.info)

    # The result of the modification of such table is shown in the dict 
    # called user_params2meas.
    user_params2meas = {'ch1': {'tiss': {'whole': {'volume': True,
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
                                                'centreline': False,
                                                'centreline_linlength': False,
                                                'centreline_looplength': False},
                                            'segm1': {'volume': True, 'surf_area': True},
                                            'segm2': {'volume': True, 'surf_area': True}}},
                        'ch2': {'tiss': {'whole': {'volume': True,
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
                        #Remove cl measurements from chNS
                        'chNS': {'tiss': {'whole': {'volume': True,
                                                'surf_area': False,
                                                'thickness int>ext': True,
                                                'thickness ext>int': False,},
                                                # 'centreline': False,
                                                # 'centreline_linlength': False,
                                                # 'centreline_looplength': False},
                                            'segm1': {'volume': True,
                                                'surf_area': False,
                                                'thickness int>ext': False,
                                                'thickness ext>int': False},
                                            'segm2': {'volume': True,
                                                'surf_area': False,
                                                'thickness int>ext': False,
                                                'thickness ext>int': False}},
                                'int': {'whole': {'volume': True,
                                                'surf_area': True,}},
                                                # 'centreline': False,
                                                # 'centreline_linlength': False,
                                                # 'centreline_looplength': False}},
                                'ext': {'whole': {'volume': True,
                                                'surf_area': True,}}}}
                                                # 'centreline': False,
                                                # 'centreline_linlength': False,
                                                # 'centreline_looplength': False}}}}

    user_ball_settings = {'ballooning': True, 'ball_settings': {
                                'ball_op1': {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch2', 'from_cl_type': 'int'},
                                'ball_op2': {'to_mesh': 'ch2', 'to_mesh_type': 'ext', 'from_cl': 'ch2', 'from_cl_type': 'ext'}}}
    
    aaa = proj.gral_meas_param.copy()
    
    proj.set_measure_param(user_params2meas=user_params2meas, user_ball_settings=user_ball_settings)
    bbb = proj.gral_meas_param
    # print('>>proj.dict_info:', proj.dict_info)

    # And a project status dictionary is created
    proj.set_project_status()
    # print('>>proj.dict_workflow:', proj.dict_workflow)

    # Save project 
    proj.save_project()
    # Load project and check parameters 
    print('\n---LOADING PROJECT----')
    proj_name = 'Project_A-B'
    folder_name = 'R_'+proj_name
    proj_dir = dir_proj_res / folder_name 
    proj_new = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)

    print('>> Check Project: \n\t',fcBasics.compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))
    
    #% ------------------------------------------------------------------------------
    # Having created the project an organ is created as part of the project
    print('\n---CREATING ORGAN----')
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
                                        'dict_dir_info': proj.dir_info},
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
        # dir_cho1 = Path('C://Users//pallo//Desktop//cosas juli//mh//project//imagenes//Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch0_EDC.tif')
        # dir_mkch1 = Path('C://Users//pallo//Desktop//cosas juli//mh//project//imagenes//Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch0_mask.tif')
    mask_ch1 = True

    # mH_chName2 = 'ch2'
    if sys.platform == 'darwin':
        dir_cho2 = Path('/Users/juliana/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_EDC.tif')
        dir_mkch2 = Path('/Users/juliana/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_mask.tif')
    elif sys.platform == 'win32': 
        dir_cho2 = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_EDC.tif')
        dir_mkch2 = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_mask.tif')
        # dir_cho2 = Path('C://Users//pallo//Desktop//cosas juli//mh//project//imagenes//Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_EDC.tif')
        # dir_mkch2 = Path('C://Users//pallo//Desktop//cosas juli//mh//project//imagenes//Im_LS52_F02_V_SR_1029//LS52_F02_V_SR_1029_ch1_mask.tif')
    mask_ch2 = True

    info_loadCh = {'ch1':{'dir_cho': dir_cho1, 
                            'mask_ch': mask_ch1,
                            'dir_mk': dir_mkch1},
                    'ch2':{'dir_cho': dir_cho2, 
                            'mask_ch': mask_ch2,
                            'dir_mk': dir_mkch2}}

    organ = mHC.Organ(project=proj, user_settings = user_organ_settings,
                            info_loadCh = info_loadCh)
    # print('organ.settings:',organ.settings)
    # print('organ.workflow:', organ.workflow)

    print('\n---SAVING PROJECT AND ORGAN----')
    # Save initial organ project
    proj.add_organ(organ)
    organ.save_organ()
    
    print('\n---LOADING ORGAN----')
    organName2Load = 'LS52_F02_V_SR_1029'
    organ_new = proj.load_organ(user_organName = organName2Load)
    print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))
    del organ_new
    
    # Save project 
    proj.save_project()
    # Load project and check parameters 
    print('\n---LOADING PROJECT----')
    proj_name = 'Project_A-B'
    folder_name = 'R_'+proj_name
    proj_dir = dir_proj_res / folder_name
    proj_new = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)
    print('>> Check Project: \n',fcBasics.compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))
    del proj_new
    
    # CODE A ---------------------------------------------------------
    print('\n---CREATING CHANNELS 1 AND 2----')
    ## CHANNEL 1
    print('\n---PROCESSING CHANNEL 1----')
    im_ch1 = organ.load_TIFF(ch_name='ch1')
    im_ch1.maskIm()
    im_ch1.closeContours_auto()
    im_ch1.closeContours_manual()
    im_ch1.closeInfOutf()
    im_ch1.selectContours()
    layerDict = {}
    im_ch1.create_chS3s(layerDict=layerDict)
    
    # Save project
    proj.save_project()
    print('\n---LOADING ORGAN----')
    # Load project, organ and channel and check parameters
    proj_new = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)
    organ_new = proj_new.load_organ(user_organName = organName2Load)
    im_ch1_new = mHC.ImChannel(organ=organ_new, ch_name='ch1', new=False)
    print('>> Check Project: \n',fcBasics.compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))
    print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
    print('>> Check im_ch1: \n',fcBasics.compare_nested_dicts(im_ch1.__dict__,im_ch1_new.__dict__,'imCh1','new')) 
    del proj_new, organ_new, im_ch1_new
    
    # CHANNEL 2
    print('\n---PROCESSING CHANNEL 2----')
    im_ch2 = organ.load_TIFF(ch_name='ch2')
    im_ch2.maskIm()
    im_ch2.closeContours_auto()
    im_ch2.closeContours_manual()
    im_ch2.closeInfOutf()
    im_ch2.selectContours()
    layerDict = {}
    im_ch2.create_chS3s(layerDict=layerDict)
    
    # Save project
    proj.save_project()
    print('\n---LOADING PROJECT AND ORGAN----')
    # Load project, organ and channel and check parameters
    proj_new = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)
    organ_new = proj_new.load_organ(user_organName = organName2Load)
    im_ch2_new = mHC.ImChannel(organ=organ_new, ch_name='ch2', new=False)
    print('>> Check Project: \n',fcBasics.compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))
    print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
    print('>> Check im_ch2: \n',fcBasics.compare_nested_dicts(im_ch2.__dict__,im_ch2_new.__dict__,'imCh2','new'))
    del proj_new, organ_new, im_ch2_new
    
#%% Part B
if partB: 
    # Load project, organ and channel and check parameters
    if not partA: 
        proj_name = 'Project_A-B'
        folder_name = 'R_'+proj_name
        proj_dir = dir_proj_res / folder_name
        proj = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)
        organName2Load = 'LS52_F02_V_SR_1029'
        organ = proj.load_organ(user_organName = organName2Load)
        im_ch1 = mHC.ImChannel(organ=organ, ch_name='ch1', new=False)
        im_ch2 = mHC.ImChannel(organ=organ, ch_name='ch2', new=False)
        
    # Create s3_int, s3_ext, s3_tiss for each channel
    im_ch1.load_chS3s(cont_types=['int', 'ext', 'tiss'])
    im_ch2.load_chS3s(cont_types=['int', 'ext', 'tiss'])
        
    #% CODE B
    # First create meshes from selected contours (end part A beginning part B)
    # Load contStacks? 
    gui_keep_largest = {'ch1': {'int': False, 'ext': False, 'tiss': False}, 'ch2': {'int': False, 'ext': False, 'tiss': False}}
    print('\n---CREATING MESHES CHANNEL 1---')
    [msh1_int, msh1_ext, msh1_tiss] = im_ch1.s32Meshes(keep_largest=gui_keep_largest['ch1'],
                                                         rotateZ_90 = True, new = True)
    print('\n---CREATING MESHES CHANNEL 2---')
    [msh2_int, msh2_ext, msh2_tiss] = im_ch2.s32Meshes(keep_largest=gui_keep_largest['ch2'],
                                                         rotateZ_90 = True, new = True)
    # Save organ
    organ.save_organ()
    # Plot
    txt = [(0, organ.user_organName)]
    obj = [(msh1_ext.mesh),(msh1_int.mesh),(msh1_tiss.mesh),(msh2_ext.mesh),(msh2_int.mesh),(msh2_tiss.mesh)]
    fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
    
    # Load project, organ, channels and meshes and check parameters
    print('\n---LOADING PROJECT, ORGAN, CHANNEL AND MESHES----')
    proj_new = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)
    organ_new = proj_new.load_organ(user_organName = organName2Load)
    im_ch1_new = mHC.ImChannel(organ=organ_new, ch_name='ch1', new=False)
    im_ch2_new = mHC.ImChannel(organ=organ_new, ch_name='ch2', new=False)
    msh1_tiss2 = mHC.Mesh_mH(imChannel=im_ch1_new, mesh_type='tiss', keep_largest=True, rotateZ_90=True, new=False)
    msh2_tiss2 = mHC.Mesh_mH(imChannel=im_ch2_new, mesh_type='tiss', keep_largest=True, rotateZ_90=True, new=False)
    print('>> Check Project: \n',fcBasics.compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))
    print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
    print('>> Check im_ch1: \n',fcBasics.compare_nested_dicts(im_ch1.__dict__,im_ch1_new.__dict__,'imCh1','new'))
    print('>> Check im_ch2: \n',fcBasics.compare_nested_dicts(im_ch2.__dict__,im_ch2_new.__dict__,'imCh2','new'))
    print('>> Check msh1_tiss: \n',fcBasics.compare_nested_dicts(msh1_tiss.__dict__,msh1_tiss2.__dict__,'msh1_tiss','new'))
    print('>> Check msh2_tiss: \n',fcBasics.compare_nested_dicts(msh2_tiss.__dict__,msh2_tiss2.__dict__,'msh2_tiss','new'))
    del proj_new, organ_new, im_ch1_new, im_ch2_new, msh1_tiss2, msh2_tiss2
    
    # Clean channels
    chs = list(organ.imChannels.keys())
    if len(chs)>1 and len(chs)<3:
        for ch in chs:
            if organ.settings[ch]['general_info']['ch_relation'] == 'external':
                ch_ext = organ.obj_imChannels[ch]
            if organ.settings[ch]['general_info']['ch_relation'] == 'internal':
                ch_int = organ.obj_imChannels[ch]
                
    #check the process has not been donde even before asking if you want to clean the channel         
    clean_ch = fcBasics.ask4input('Do you want to clean the '+ch_int.user_chName+' with the '+ch_ext.user_chName+'?\n\t[0]: no, thanks\n\t[1]: yes, please! >>>:', bool)
    if clean_ch:
        inverted = fcBasics.ask4input('Select the mask you would like to use to clean the '+ch_int.user_chName+': \n\t[0]: Just the tissue layer of the '+ch_ext.user_chName+'\n\t[1]: (Recommended) The inverted internal segmentation of the '+ch_ext.user_chName+' (more profound cleaning). >>>: ', bool)
        plot = False
        ch_int.ch_clean(s3_mask=ch_ext.s3_ext, inverted=inverted, plot=plot)
        print('>> Check Ch2 vs ChInt: \n',fcBasics.compare_nested_dicts(im_ch2.__dict__,ch_int.__dict__,'ch2','int'))
        
        print('\n---RECREATING MESHES CHANNEL 2 WITH CLEANED ENDOCARDIUM---')
        [msh2_int2, msh2_ext2, msh2_tiss2] = im_ch2.s32Meshes(keep_largest=gui_keep_largest['ch2'],
                                                             rotateZ_90 = True, new = True)
        # Plot cleaned ch2
        obj = [(msh2_ext.mesh),(msh2_int.mesh),(msh2_tiss.mesh),(msh2_ext2.mesh),(msh2_int2.mesh),(msh2_tiss2.mesh)]
        txt = [(0, organ.user_organName + ' - Original'), (3,'Cleaned Meshes')]
        fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
        
        msh2_int = msh2_int2; msh2_ext = msh2_ext2; msh2_tiss = msh2_tiss2
        del msh2_int2, msh2_ext2, msh2_tiss2
            
    # Save organ
    organ.save_organ()
    # Load project, organ
    print('\n---LOADING PROJECT AND ORGAN----')
    proj_new = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)
    organ_new = proj_new.load_organ(user_organName = organName2Load)    
    print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
    del proj_new, organ_new

    # Cut meshes inflow and outflow tracts 
    obj = [(msh1_tiss.mesh),(msh2_tiss.mesh),(msh1_tiss.mesh, msh2_tiss.mesh)]
    text = organ.user_organName+"\n\nTake a closer look at both meshes and decide from which layer to cut\n the inflow and outflow. >> [0]:ch1 / [1]:ch2 / [2]:both / [3]:none.\nClose the window when done"
    txt = [(0, text)]
    fcMeshes.plot_grid(obj=obj, txt=txt, axes=5, lg_pos='bottom-right')

    # User user input to select which meshes need to be cut
    cuts = {'top':    {'chs': {'ch1': False, 'ch2': True}},
            'bottom': {'chs': {'ch1': True, 'ch2': True}}}
    meshes = [msh1_tiss, msh2_tiss]
  
    # cut_chs = 
    fcMeshes.trim_top_bottom_S3s(organ=organ, cuts=cuts, meshes=meshes)
    gui_keep_largest = {'ch1': {'int': False, 'ext': False, 'tiss': False}, 'ch2': {'int': False, 'ext': False, 'tiss': False}}

    print('\n---RECREATING MESHES CHANNEL 1 AFTER TRIMMING---')
    [msh1_int, msh1_ext, msh1_tiss] = im_ch1.createNewMeshes(keep_largest = gui_keep_largest['ch1'], 
                                            process = 'AfterTrimming',
                                            rotateZ_90 = True, new = True)
    print('\n---CREATING MESHES CHANNEL 2 AFTER TRIMMING---')
    [msh2_int, msh2_ext, msh2_tiss] = im_ch2.createNewMeshes(keep_largest = gui_keep_largest['ch2'], 
                                            process = 'AfterTrimming',
                                            rotateZ_90 = True, new = True)
    # Plot
    txt = [(0, organ.user_organName  + ' - Meshes after trimming')]
    obj = [(msh1_ext.mesh),(msh1_int.mesh),(msh1_tiss.mesh),(msh2_ext.mesh),(msh2_int.mesh),(msh2_tiss.mesh)]
    fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
    
    # Save organ
    organ.save_organ()
    # Load project, organ
    print('\n---LOADING PROJECT AND ORGAN----')
    proj_new = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)
    organ_new = proj_new.load_organ(user_organName = organName2Load)    
    print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
    del proj_new, organ_new
    
    # Create Cardiac Jelly
    if 'chNS' in organ.settings.keys():
        im_ns = mHC.ImChannelNS(organ=organ, ch_name='chNS')
        im_ns.create_chNSS3s(plot=True)
        
        gui_keep_largest = {'int': False, 'ext': False, 'tiss': False}
        [mshNS_int, mshNS_ext, mshNS_tiss] = im_ns.s32Meshes(keep_largest=gui_keep_largest,
                                                             rotateZ_90 = True, new = True)
       
        txt = [(0, organ.user_organName  + ' - Extracted ' + im_ns.user_chName)]
        obj = [(mshNS_ext.mesh),(mshNS_int.mesh),(mshNS_tiss.mesh)]
        fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
        
        txt = [(0, organ.user_organName  + ' - Final reconstructed meshes')]
        obj = [(msh1_tiss.mesh),(msh2_tiss.mesh),(mshNS_tiss.mesh),(msh1_tiss.mesh, msh2_tiss.mesh, mshNS_tiss.mesh)]
        fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
        
        # Save organ
        organ.save_organ()
        # Load project, organ
        proj_new = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)
        organ_new = proj_new.load_organ(user_organName = organName2Load)    
        print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
        del proj_new, organ_new
        
#%% Part B-vmtk
# Create meshes to extract CL
if partB_vmtk: 
    if not partA and not partB: 
        proj_name = 'Project_A-B'
        folder_name = 'R_'+proj_name
        proj_dir = dir_proj_res / folder_name
        proj = mHC.Project(new = False, proj_name = proj_name, proj_dir = proj_dir)
        organName2Load = 'LS52_F02_V_SR_1029'
        organ = proj.load_organ(user_organName = organName2Load)
        
    cl_names = [item for item in organ.parent_project.gral_meas_param if 'centreline' in item]
    msh4cl = []
    for name in cl_names: 
        mesh = organ.obj_meshes[name[0]+'_'+name[1]]
        mesh_out = mesh.mesh4CL()
        msh4cl.append(mesh_out)
    
    txt = [(0, organ.user_organName  + ' - Smoothed meshes')]
    obj = [(mesh) for mesh in msh4cl]
    fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
    
    
    
        
    
    
    
    
#%%
    

# %%
