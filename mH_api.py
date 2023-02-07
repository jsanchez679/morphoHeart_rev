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

alert_all=True
heart_default=False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}

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
    
partA = True
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
    user_projName = 'Project B-C'
    user_projNotes = 'Project to compare embryos B and C'
    # Morphological analysis - morphoHeart
    mH_analysis = True
    # Cellular analysis - morphoCell
    mC_analysis = False
    user_analysis = {'morphoHeart': mH_analysis, 'morphoCell': mC_analysis}
    dir_proj = dir_proj_res
    
    proj = mHC.Project(name=user_projName, notes=user_projNotes, 
                               analysis=user_analysis, dir_proj = dir_proj)
    proj.__dict__

    # Once the project is created a new window will appear to select all the 
    # settings for the project
    # >> Settings for morphological analysis
    if proj.analysis['morphoHeart']: 
        print('>> Setting up morphoHeart')
        # Ask for settings the settings for morphoHeart
        no_chs = 2
        name_chs = {'ch1': 'myocardium', 'ch2': 'endocardium'}
        chs_relation =  {'ch1': 'external', 'ch2': 'internal'}
        color_chs = {'ch1':{'tiss':'lightseagreen','int':'gold','ext':'crimson'}, 
                     'ch2':{'tiss':'darkmagenta','int':'deepskyblue','ext':'deeppink'}}
        layer_btw_chs = True
        ch_ext = ('ch1', 'int')
        ch_int = ('ch2', 'ext')
        user_nsChName = 'cardiac jelly'
        color_chNS = {'tiss':'darkorange','ext':'crimson', 'int':'deepskyblue'}
        # By default the volume and surface area of the segments per tissue selected will be measured
        cutLayersIn2Segments = True
        no_segments = 2
        name_segments = {'ch1': 'atrium', 'ch2': 'ventricle'}
        # channels/meshes that will be divided into segments 
        ch_segments = {'ch1':['tiss', 'ext'],'ch2':['tiss', 'int'],'chNS':['tiss']}
        
        mH_settings = {'no_chs': no_chs,
                        'name_chs': name_chs,
                        'chs_relation': chs_relation,
                        'color_chs': color_chs,
                        'ns': 
                            {'layer_btw_chs': layer_btw_chs,
                            'ch_ext': ch_ext,
                            'ch_int': ch_int,
                            'user_nsChName': user_nsChName,
                            'color_chns': color_chNS},
                        'segments': 
                            {'cutLayersIn2Segments': cutLayersIn2Segments,
                            'no_segments': no_segments,
                            'name_segments': name_segments,
                            'ch_segments': ch_segments}}
    else: 
        mH_settings = {}
            
    if proj.analysis['morphoCell']:  
        # Ask for settings the settings for morphoCell
        print('>> Setting up morphoCell')
        if not proj.analysis['morphoHeart']:
            # Ask for settings of the myocardial channel to use as guidance 
            # when positioning cells
            print('set-up process only analysis of cells')
            no_chs = 2
            name_chs = {'ch1':'myocardium', 'ch2':'myoc_nuclei'}
            link2mH = {'ch1': False, 'ch2': False}
            chs_relation =  {'ch1': 'tissue', 'ch2': 'cells'}
            color_chs = {'ch1':'lightseagreen', 
                         'ch2':'darkmagenta'}
            cutLayersIn2Segments = True
            no_segments = 3
            name_segments = {'ch1': 'atrium', 'ch2': 'ventricle'}
            mC_settings = {'no_chs': no_chs,
                           'name_chs': name_chs,
                           'link2mH': link2mH,
                           'chs_relation': chs_relation,
                           'color_chs': color_chs,
                           'segments': 
                               {'cutLayersIn2Segments': cutLayersIn2Segments,
                               'no_segments': no_segments,
                               'name_segments': name_segments}}
        else: 
            # Ask if cells are from one of the channels processed in
            # morphoHeart, if so, link them to the tissue? 
            print('link cells to channel')
            no_chs = 2
            name_chs = {'ch1':'myocardium', 'ch2':'myoc_nuclei'}
            link2mH = {'ch1': True, 'ch2': False}
            chs_relation =  {'ch1': 'tissue', 'ch2': 'cells'}
            color_chs = {'ch1':'lightseagreen', 
                         'ch2':'darkmagenta'}
            cutLayersIn2Segments = True
            no_segments = 3
            name_segments = {'ch1': 'atrium', 'ch2': 'ventricle'}
            mC_settings = {'no_chs': no_chs,
                           'name_chs': name_chs,
                           'link2mH': link2mH,
                           'chs_relation': chs_relation,
                           'color_chs': color_chs,
                           'segments': 
                               {'cutLayersIn2Segments': cutLayersIn2Segments,
                               'no_segments': no_segments,
                               'name_segments': name_segments}}
    else: 
        mC_settings = {}
        
    # This will create attributes within the instance of the project
    # containing information of the settings selected by the user
    # Additionally, based on the number of segments and channels selected, 
    # a dictionary with predefined measurement parameters is created with 
    # which a table in the GUI will be created for the user to modify
    proj.set_settings(mH_settings=mH_settings, mC_settings=mC_settings)
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
                                                'thickness ext>int': False},
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
                                'ext': {'whole': {'volume': True,
                                                'surf_area': True,}}}}

    user_ball_settings = {'ballooning': True, 'ball_settings': {
                                'ball_op1': {'to_mesh': 'ch1', 'to_mesh_type': 'int',
                                             'from_cl': 'ch2', 'from_cl_type': 'int'},
                                'ball_op2': {'to_mesh': 'ch2', 'to_mesh_type': 'ext', 
                                             'from_cl': 'ch2', 'from_cl_type': 'ext'}}}

    proj.set_mH_meas(user_params2meas=user_params2meas, user_ball_settings=user_ball_settings)

    # And a project status dictionary is created
    proj.set_workflow()

    # Save project 
    proj.save_project()
    # Load project and check parameters 
    print('\n---LOADING PROJECT----')
    proj_name = 'Project_B-C'
    folder_name = 'R_'+proj_name
    dir_proj = dir_proj_res / folder_name 
    proj_new = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
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

    print('\n---SAVING PROJECT AND ORGAN----')
    # Save initial organ project
    proj.add_organ(organ)
    organ.save_organ()
    
    # Save project 
    proj.save_project()
    # Load project and check parameters 
    print('\n---LOADING PROJECT AND ORGAN----')
    proj_name = 'Project_B-C'
    folder_name = 'R_'+proj_name
    dir_proj = dir_proj_res / folder_name
    proj_new = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
    organName2Load = 'LS52_F02_V_SR_1029'
    organ_new = proj.load_organ(user_organName = organName2Load)
    print('>> Check Project: \n',fcBasics.compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))
    print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))
    del proj_new, organ_new
    
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
    proj_new = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
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
    proj_new = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
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
        proj_name = 'Project_B-C'
        folder_name = 'R_'+proj_name
        dir_proj = dir_proj_res / folder_name
        proj = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
        organName2Load = 'LS52_F02_V_SR_1029'
        organ = proj.load_organ(user_organName = organName2Load)
        im_ch1 = mHC.ImChannel(organ=organ, ch_name='ch1', new=False)
        im_ch2 = mHC.ImChannel(organ=organ, ch_name='ch2', new=False)
        
    # Create s3_int, s3_ext, s3_tiss for each channel
    # im_ch1.load_chS3s(cont_types=['int', 'ext', 'tiss'])
    # im_ch2.load_chS3s(cont_types=['int', 'ext', 'tiss'])
        
    #% CODE B
    # First create meshes from selected contours (end part A beginning part B)
    # Load contStacks? 
    gui_keep_largest = {'ch1': {'int': True, 'ext': True, 'tiss': False}, 'ch2': {'int': True, 'ext': True, 'tiss': False}}
    print('\n---CREATING MESHES CHANNEL 1---')
    [msh1_int, msh1_ext, msh1_tiss] = im_ch1.s32Meshes(cont_types=['int', 'ext', 'tiss'],
                                                       keep_largest=gui_keep_largest['ch1'],
                                                       rotateZ_90 = True, new_set = True)
    print('\n---CREATING MESHES CHANNEL 2---')
    [msh2_int, msh2_ext, msh2_tiss] = im_ch2.s32Meshes(cont_types=['int', 'ext', 'tiss'],
                                                       keep_largest=gui_keep_largest['ch2'],
                                                         rotateZ_90 = True, new_set = True)
    # Save organ
    organ.save_organ()
    # Plot
    txt = [(0, organ.user_organName)]
    obj = [(msh1_ext.mesh),(msh1_int.mesh),(msh1_tiss.mesh),(msh2_ext.mesh),(msh2_int.mesh),(msh2_tiss.mesh)]
    fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
    
    # Load project, organ, channels and meshes and check parameters
    print('\n---LOADING PROJECT, ORGAN, CHANNEL AND MESHES----')
    proj_new = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
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
    msh2_int, msh2_ext, msh2_tiss = fcMeshes.clean_intCh(organ)
            
    # Save organ
    organ.save_organ()
    # Load project, organ
    print('\n---LOADING PROJECT AND ORGAN----')
    proj_new = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
    organ_new = proj_new.load_organ(user_organName = organName2Load)    
    print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
    del proj_new, organ_new

    # Cut meshes inflow and outflow tracts 
    obj = [(msh1_tiss.mesh),(msh2_tiss.mesh),(msh1_tiss.mesh, msh2_tiss.mesh)]
    text = organ.user_organName+"\n\nTake a closer look at both meshes and decide from which layer to cut\n the inflow and outflow. \nClose the window when done"
    txt = [(0, text)]
    fcMeshes.plot_grid(obj=obj, txt=txt, axes=5, lg_pos='bottom-right')

    # User user input to select which meshes need to be cut
    cuts = {'top':    {'chs': {'ch1': False, 'ch2': True}},
            'bottom': {'chs': {'ch1': True, 'ch2': True}}}
    meshes = [msh1_tiss, msh2_tiss]
  
    fcMeshes.trim_top_bottom_S3s(organ=organ, cuts=cuts, meshes=meshes)
    print('\n---RECREATING MESHES CHANNEL 1 AFTER TRIMMING---')
    [msh1_int, msh1_ext, msh1_tiss] = im_ch1.createNewMeshes(cont_types=['int', 'ext', 'tiss'],
                                            process = 'AfterTrimming')
    print('\n---CREATING MESHES CHANNEL 2 AFTER TRIMMING---')
    [msh2_int, msh2_ext, msh2_tiss] = im_ch2.createNewMeshes(cont_types=['int', 'ext', 'tiss'],
                                            process = 'AfterTrimming')
    # Plot
    txt = [(0, organ.user_organName  + ' - Meshes after trimming')]
    obj = [(msh1_ext.mesh),(msh1_int.mesh),(msh1_tiss.mesh),(msh2_ext.mesh),(msh2_int.mesh),(msh2_tiss.mesh)]
    fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
    
    # Save organ
    organ.save_organ()
    # Load project, organ
    print('\n---LOADING PROJECT AND ORGAN----')
    proj_new = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
    organ_new = proj_new.load_organ(user_organName = organName2Load)    
    print('>> Check Project: \n',fcBasics.compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))
    print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
    del proj_new, organ_new
    
    # Create Cardiac Jelly
    if 'chNS' in organ.mH_settings['general_info'].keys():
        im_ns = mHC.ImChannelNS(organ=organ, ch_name='chNS')
        im_ns.create_chNSS3s(plot=True)
        
        gui_keep_largest = {'int': True, 'ext': True, 'tiss': False}
        [mshNS_int, mshNS_ext, mshNS_tiss] = im_ns.s32Meshes(cont_types=['int', 'ext', 'tiss'],
                                                             keep_largest=gui_keep_largest,
                                                             rotateZ_90 = True, new_set = True)
       
        txt = [(0, organ.user_organName  + ' - Extracted ' + im_ns.user_chName)]
        obj = [(mshNS_ext.mesh),(mshNS_int.mesh),(mshNS_tiss.mesh)]
        fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
        
        txt = [(0, organ.user_organName  + ' - Final reconstructed meshes')]
        obj = [(msh1_tiss.mesh),(msh2_tiss.mesh),(mshNS_tiss.mesh),(msh1_tiss.mesh, msh2_tiss.mesh, mshNS_tiss.mesh)]
        fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
        
        # Save organ
        organ.save_organ()
        # Load project, organ
        proj_new = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
        organ_new = proj_new.load_organ(user_organName = organName2Load)    
        print('>> Check Project: \n',fcBasics.compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))
        print('>> Check Organ: \n',fcBasics.compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
        del proj_new, organ_new
        
#%% Part B-vmtk
# Create meshes to extract CL and extract CL
if partB_vmtk: 
    if not partA and not partB: 
        proj_name = 'Project_B-C'
        folder_name = 'R_'+proj_name
        dir_proj = dir_proj_res / folder_name
        proj = mHC.Project(new = False, proj_name = proj_name, dir_proj = dir_proj)
        organName2Load = 'LS52_F02_V_SR_1029'
        organ = proj.load_organ(user_organName = organName2Load)
    
    # Create meshes to extract CL
    plot = True
    fcMeshes.cutMeshes4CL(organ, plot=plot)
    
   
    

    
    
    
    
#%%
    

# %%
