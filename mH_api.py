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
from src.modules import mH_classes as mHC
from src.modules import mH_funcBasics as fcBasics
from src.modules import mH_funcContours as fcCont
from src.modules import mH_funcMeshes as fcMeshes

#%% GUI related
fcBasics.alert('woohoo')
# Setting the path to the project results
if sys.platform == 'darwin':
    dir_proj_res = Path('/Users/juliana/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/')
elif sys.platform == 'win32':
    dir_proj_res = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/')
    #dir_proj_res = Path('C://Users//pallo//Desktop//cosas juli//mh//project')
    
partA = False
partB = False
partB_vmtk = False
partC = True
print('partA:',partA,'- partB:',partB,'- partB_vmtk:',partB_vmtk,'- partC:',partC)

user_projName = 'TestAll'
proj_name = user_projName
user_organName = 'LS52_F02_V_SR_1029'
organName2Load = user_organName
folder_name = 'R_'+proj_name
dir_proj = dir_proj_res / folder_name
# user_organName = 'LS52_F02_V_SR_1029'
# organName2Load = 'LS52_F02_V_SR_1029'

#%% Part A - Create Project
if partA:
    #%
    # Info coming from the gui (user's selection)
    # 1. Click: Create new project
    print('\n---CREATING PROJECT----')
    # user_projName = 'Project B-C'
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
        color_chNS = {'tiss':'darkorange','ext':'powderblue', 'int':'greenyellow'}
        # By default the volume and surface area of the segments per tissue selected will be measured
        cutLayersIn2Segments = True
        no_segments = 2
        name_segments = {'segm1': 'atrium', 'segm2': 'ventricle'}
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
                                                'thickness ext>int': False},
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
                                                'thickness ext>int': False},
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
    # proj_name = 'Project_B-C'
    folder_name = 'R_'+proj_name
    dir_proj = dir_proj_res / folder_name 
    proj_new = mHC.Project(name = proj_name, dir_proj = dir_proj)
    print('>> Check Project: \n\t',fcBasics.compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))

#%% Part A - Create Organ
if partA:
    #% ------------------------------------------------------------------------------
    # Having created the project an organ is created as part of the project
    print('\n---CREATING ORGAN----')
    # user_organName = 'LS52_F02_V_SR_1029'
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

    # - Set path to images
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
    # Load project, organ
    fcBasics.check_gral_loading(proj, organ, proj_name, dir_proj, organName2Load)
    
    
    # CODE A ---------------------------------------------------------
    print('\n---CREATING CHANNELS 1 AND 2----')
    ## CHANNEL 1
    print('\n---PROCESSING CHANNEL 1----')
    im_ch1 = fcCont.closeContours(organ=organ, ch_name='ch1')
    im_ch1 = fcCont.selectContours(organ=organ, im_ch = im_ch1)

    # Save project
    proj.save_project()
    # Load project, organ
    fcBasics.check_gral_loading(proj, organ, proj_name, dir_proj, organName2Load)
    
    # CHANNEL 2
    print('\n---PROCESSING CHANNEL 2----')
    im_ch2 = fcCont.closeContours(organ=organ, ch_name='ch2')
    im_ch2 = fcCont.selectContours(organ=organ, im_ch = im_ch2)
    
    # Save project
    proj.save_project()
    # Load project, organ
    fcBasics.check_gral_loading(proj, organ, proj_name, dir_proj, organName2Load)
    
    
#%% Part B
if partB: 
    # Load project, organ and channel and check parameters
    if not partA: 
        proj = mHC.Project(name = proj_name, dir_proj = dir_proj)
        organ = proj.load_organ(user_organName = organName2Load)

    #% CODE B
    # Create meshes after processing images
    gui_keep_largest = {'ch1': {'int': True, 'ext': True, 'tiss': False}, 
                        'ch2': {'int': True, 'ext': True, 'tiss': False}}
    rotateZ_90 = True
    fcMeshes.s32Meshes(organ, gui_keep_largest, rotateZ_90=rotateZ_90)
    
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, organ, proj_name, dir_proj, organName2Load)
    
    # Clean channels
    plot = True
    fcMeshes.clean_intCh(organ, plot)
     
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, organ, proj_name, dir_proj, organName2Load)
  
    # Cut meshes inflow and outflow tracts 
    # Function to decide which meshes to cut
    fcMeshes.select_meshes2trim(organ=organ)
    # meshes = [msh1_tiss, msh2_tiss]
    # User user input to select which meshes need to be cut
    cuts = {'top':    {'chs': {'ch1': False, 'ch2': True}},
            'bottom': {'chs': {'ch1': True, 'ch2': True}}}

    fcMeshes.trim_top_bottom_S3s(organ=organ, cuts=cuts)
    # fcMeshes.plot_all_organ(organ)
    
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, organ, proj_name, dir_proj, organName2Load)
  
    # Create Cardiac Jelly
    plot = True
    fcMeshes.extractNSCh(organ, plot)
        
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, organ, proj_name, dir_proj, organName2Load)
  
#%% Part B-vmtk
# Create meshes to extract CL and extract CL
if partB_vmtk: 
    if not partA and not partB: 
        proj = mHC.Project(name = proj_name, dir_proj = dir_proj)
        organ = proj.load_organ(user_organName = organName2Load)
        fcMeshes.plot_all_organ(organ)
    
    # Create meshes to extract CL
    plot = True; tol=2
    fcMeshes.cutMeshes4CL(organ, tol=tol, plot=plot)
    fcMeshes.extractCL(organ)
    nPoints = 300
    fcMeshes.createCLs(organ, nPoints = nPoints)
    
    # Get CL measurements
    fcMeshes.measure_centreline(organ, nPoints=nPoints)
    
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, organ, proj_name, dir_proj, organName2Load)
    
#%% Part C - Measure
if partC: 
    if not partA and not partB and not partB_vmtk: 
        # proj_name = proj_name
        folder_name = 'R_'+proj_name
        dir_proj = dir_proj_res / folder_name
        proj = mHC.Project(name = proj_name, dir_proj = dir_proj)
        # organName2Load = 'LS52_F02_V_SR_1029'
        organ = proj.load_organ(user_organName = organName2Load)
        fcMeshes.plot_all_organ(organ)

    plot = False
    fcMeshes.extractThickness(organ, color_map='turbo', plot=plot)
    fcMeshes.extractBallooning(organ, color_map='turbo', plot=plot)
    
    fcMeshes.plot_meas_meshes(organ, meas=['thickness int>ext']) 
    fcMeshes.plot_meas_meshes(organ, meas=['thickness ext>int']) 
    fcMeshes.plot_meas_meshes(organ, meas=['ballooning']) 
    
    for obj in organ.obj_meshes:
        pp = organ.obj_meshes[obj].mesh_meas
        if pp != {}:
            print(obj,':',pp)
            
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, organ, proj_name, dir_proj, organName2Load)
    
#%%
#%% To do: 
    # update workflow when maesuring centrelines
    # update workflow when measuring volumes
    # revise segment creation in the workflow
    # see if there can be an easier way to create workflow dict
    # ask user if the project already exists if he/she wants to change some of the settings
    # run it again to check if the changes from 'NotInitialised' to 'NI' works
    # create a kspline ribbon using the kspline
    # add to the workflow - measurements if to divide meshes l/R with CL
    # which name?
    # which process would that be included in? - measure?
    # see whether to ask the user to select the cl to use to divide meshes L/R 
    # When creating the disk to cut meshes A/V how many discs to create and cut?
    # save the stacks for the disks?
    # save the stacks for the L/R
    # how to call l/r 
    
    
#%%
    # # Divide heart layers into chambers and save data
    # cyl_Chambers, num_pt, m_atr, m_vent, dict_shapes, dict_pts, s3_cyl = fcMeshes.getRing2CutChambers(filename = filename, 
    #                                                                               kspl_CL = kspl_CL[0], mesh2cut = m_myoc, 
    #                                                                               resolution = res, dir_stl = directories[2], 
    #                                                                               dir_txtNnpy = directories[1],
    #                                                                               dict_pts = dict_pts, 
    #                                                                               dict_shapes = dict_shapes)
    

# %%
#%% pip freeze > requirements.txt