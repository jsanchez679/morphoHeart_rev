
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
partC_thk = False
partC = True

print('partA:',partA,'- partB:',partB,'- partB_vmtk:',partB_vmtk,'- partC_thk:',partC_thk, '- partC:',partC)

user_projName = 'TestAll2'
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
    dir_proj = dir_proj
    
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
        cutLayersIn2Sections = True
        no_sections = 2
        name_sections = {'sect1': 'left', 'sect2': 'right'}
        ch_sections = {'ch1':['tiss'],'ch2':['tiss'],'chNS':['tiss']}
       
        
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
                            'ch_segments': ch_segments},
                        'sections': 
                            {'cutLayersIn2Sections': cutLayersIn2Sections,
                            'no_sections': no_sections,
                            'name_sections': name_sections,
                            'ch_sections': ch_sections}}
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
                                                'thickness ext>int': False},
                                            'sect1': {'volume': True},
                                            'sect2': {'volume': True}},
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
                                                'thickness ext>int': False},
                                            'sect1': {'volume': True},
                                            'sect2': {'volume': True}},
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
                                                'thickness ext>int': False},
                                            'sect1': {'volume': True},
                                            'sect2': {'volume': True}},
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
    fcBasics.check_gral_loading(proj, proj_name, dir_proj)
    
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
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
    
    
    # CODE A ---------------------------------------------------------
    print('\n---CREATING CHANNELS 1 AND 2----')
    ## CHANNEL 1
    print('\n---PROCESSING CHANNEL 1----')
    im_ch1 = fcCont.closeContours(organ=organ, ch_name='ch1')
    im_ch1 = fcCont.selectContours(organ=organ, im_ch = im_ch1)

    # Save project
    proj.save_project()
    # Load project, organ
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
    
    # CHANNEL 2
    print('\n---PROCESSING CHANNEL 2----')
    im_ch2 = fcCont.closeContours(organ=organ, ch_name='ch2')
    im_ch2 = fcCont.selectContours(organ=organ, im_ch = im_ch2)
    
    # Save project
    proj.save_project()
    # Load project, organ
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
    
    
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
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
    
    # Clean channels
    plot = True
    fcMeshes.clean_intCh(organ, plot)
     
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
  
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
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
  
    # Create Cardiac Jelly
    plot = True
    fcMeshes.extractNSCh(organ, plot)
        
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
  

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
    fcMeshes.measure_orientation(organ)
    
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
    
#%% Part C-thkness - Measure
if partC_thk: 
    if not partA and not partB and not partB_vmtk: 
        # proj_name = proj_name
        folder_name = 'R_'+proj_name
        dir_proj = dir_proj_res / folder_name
        proj = mHC.Project(name = proj_name, dir_proj = dir_proj)
        # organName2Load = 'LS52_F02_V_SR_1029'
        organ = proj.load_organ(user_organName = organName2Load)
        fcMeshes.plot_all_organ(organ)

    # 3D Thickness and Ballooning Heatmaps 
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
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
    
#%%
if partC: 
    if not partA and not partB and not partB_vmtk and not partC_thk: 
        # proj_name = proj_name
        folder_name = 'R_'+proj_name
        dir_proj = dir_proj_res / folder_name
        proj = mHC.Project(name = proj_name, dir_proj = dir_proj)
        # organName2Load = 'LS52_F02_V_SR_1029'
        organ = proj.load_organ(user_organName = organName2Load)
        fcMeshes.plot_all_organ(organ)

    # Get volume measurements
    fcMeshes.measure_volume(organ)
    fcMeshes.measure_area(organ)
    
    from itertools import count
    colors = [[255,215,0,200],[0,0,205,200],[255,0,0,200]]
    views = ['top', 'ventral', 'left']
    planar_views = {}
    for n, view, color in zip(count(), views, colors): 
        planar_views[view] = {'color': color}
    
    organ.get_stack_orientation(planar_views)
    
    # Get organ orientation
    plane = 'YZ'
    ref_vect = 'Y+'
    planar_views = {}
    for n, view, color in zip(count(), views, colors): 
        planar_views[view] = {'color': color}
    organ.get_ROI_orientation(planar_views, plane='YZ',ref_vect=ref_vect)
    
    # Get organ centreline ribbon 
    nRes = 601; nPoints = 300; clRib_type = 'ext2sides'
    fcMeshes.get_organ_ribbon(organ, nRes, nPoints, clRib_type)
    # organ.info['shape_s3'] = organ.imChannels['ch1']['shape']
    fcMeshes.get_cube_clRibbon(organ, plotshow=True)
    
    # Cut organ into sections
    subms = fcMeshes.get_sections(organ, plotshow=True)
    
    left_myo = subms[0].get_mesh()
    right_myo = subms[1].get_mesh()
    
    
    
#%% 
    # Cut organ into segments
    q = 'Do you want to use the centreline to aid cut of tissue into segments?'
    res = {0: 'No, I would like to define the cuts by hand', 1: 'yes, please!'}
    segm_using_cl = fcBasics.ask4input(q, res, bool)
    if segm_using_cl: 
        #Find centreline first
        dict_cl = fcMeshes.plot_organCLs(organ)
        q = 'Select the centreline you want to use to aid organ cut into segments:'
        select = fcBasics.ask4input(q, dict_cl, int)
        ch_cont_cl = dict_cl[select].split(' (')[1].split('-')
        ch = ch_cont_cl[0]
        cont = ch_cont_cl[1]
        cl = organ.obj_meshes[ch+'_'+cont].get_centreline()
        spheres_spl = fcMeshes.sphs_in_spline(kspl = cl, colour = True)
    
    segm_names = [item for item in organ.parent_project.mH_param2meas if 'segm1' in item]
    
    ext_ch, _ = organ.get_ext_int_chs()
    if (ext_ch.channel_no, 'tiss', 'segm1', 'volume') in segm_names:
        mesh_ext = organ.obj_meshes[ext_ch.channel_no+'_tiss']
    else: 
        ch = segm_names[0][0]; cont = segm_names[0][1]
        mesh_ext = organ.obj_meshes[ch+'_'+cont]
        
    happyWithCut = False
    happyWithDisc = False
    number_cuts_4segm = 2
    segm_name = organ.mH_settings['general_info']['segments']['name_segments']
    for n in range(number_cuts_4segm):
        print('Creating disc No.'+str(n)+' for cutting tissues into segments!')
        while not happyWithDisc: 
            if segm_using_cl:
                vp = vedo.Plotter(N=1, axes = 7)
                text = organ.user_organName+"\n\n >> Define the centreline point number to use to initialise \n  disc to divide heart into chambers \n  [NOTE: Spheres appear in centreline every 10 points, starting from \n  outflow (blue) to inflow (red) tract]"
                txt = vedo.Text2D(text, c="k")#, font= font)
                vp.show(mesh_ext.mesh, cl, spheres_spl, txt, at=0, azimuth = 0, interactive=True)
    
                q = 'Enter the centreline point number you want to use to initialise the disc to divide the heart into chambers:'
                num_pt = fcBasics.ask4input(q,{},int)
                # Use flat disc or centreline orientation at point to define disc?
                q2 = 'Select the object you want to use: '
                res = {0:'Use the centreline orientation at the selected point to define disc orientation', 1: 'Initialise the disc in a plane normal to the y-z plane?'}
                cl_or_flat = fcBasics.ask4input(q2, res, bool)
             
                if not cl_or_flat:
                    pl_normal, pl_centre = fcMeshes.get_plane_normal2pt(pt_num = num_pt, points = cl.points())
                else:
                    pl_centre = cl.points()[num_pt]
                    pl_normal = [1,0,0]
            else: 
                
                pl_centre = mesh_ext.mesh.center_of_mass()
                pl_normal = [0,1,0]
                
            radius = 60
            # Modify (rotate and move cylinder/disc)
            cyl_test, sph_test, rotX, rotY, rotZ = fcMeshes.modify_disc(filename = organ.user_organName,
                                                                txt = 'cut tissues into segments', 
                                                                mesh = mesh_ext.mesh,
                                                                option = [True,True,True,True,True,True],
                                                                def_pl = {'pl_normal': pl_normal, 'pl_centre': pl_centre},
                                                                radius = radius)
            
            # Get new normal of rotated disc
            pl_normal_corrected = fcMeshes.newNormal3DRot(normal = pl_normal, rotX = rotX, rotY = rotY, rotZ = rotZ)
            normal_unit = fcMeshes.unit_vector(pl_normal_corrected)*10
            # Get central point of newly defined disc
            pl_centre_new = sph_test.pos()
            
            # Newly defined centreline point
            cl_point = pl_centre_new# kspl_CL.points()[num_pt]
            sph_cut = vedo.Sphere(pos = pl_centre_new, r=4, c='gold').legend('sph_ChamberCut')
    
            # Build new disc to confirm
            cyl_final = vedo.Cylinder(pos = pl_centre_new, r = radius, height = 2*0.225, axis = normal_unit, c = 'purple', cap = True, res = 300)
            
            text = organ.user_organName+"\n\n >> Check the position and the radius of the disc to cut the heart into chambers.\n  Make sure it is cutting the heart through the AVC and hopefully not cutting any other chamber regions. \n >> Close the window when done"
            txt = vedo.Text2D(text, c='k')#, font=font)
            vp = vedo.Plotter(N=1, axes=4)
            vp.show(mesh_ext.mesh, cyl_final, cl, txt, at=0, viewup="y", azimuth=0, elevation=0, interactive=True)
            
            disc_radius = radius
            q_happy = 'Are you happy with the position of the disc [radius: '+str(disc_radius)+'um] to cut heart into chambers?'
            res_happy = {0: 'no, I would like to define a new position for the disc', 1: 'yes, but I would like to redefine the disc radius', 2: 'yes, I am happy with both, disc position and radius'}
            happy = fcBasics.ask4input(q_happy, res_happy, int)
            if happy == 1:
                happy_rad = False
                while not happy_rad:
                    disc_radius = fcBasics.ask4input('Input disc radius [um]: ',{}, float)
                    text = organ.user_organName+"\n\n >> New radius \n  Check the radius of the disc to cut the myocardial tissue into \n   chambers. Make sure it is cutting through the AVC and not catching any other chamber regions. \n >> Close the window when done"
                    cyl_final = vedo.Cylinder(pos = pl_centre_new, r = disc_radius, height = 2*0.225, axis = normal_unit, c = 'purple', cap = True, res = 300)
                    txt = vedo.Text2D(text, c="k"), #font= font)
                    vp = vedo.Plotter(N=1, axes = 10)
                    vp.show(mesh_ext.mesh.alpha(1), cl, cyl_final, sph_cut, txt, at = 0, interactive=True)
                    q_happy_rad = 'Is the selected radius ['+str(disc_radius)+'um] sufficient to cut heart into chambers?'
                    res_happy_rad = {0: 'no, I would like to change its value', 1: 'yes, it cuts the heart without disrupting too much the chambers!'}
                    happy_rad = fcBasics.ask4input(q_happy_rad, res_happy_rad, bool)
                happyWithDisc = True
            elif happy == 2:
                happyWithDisc = True
       
        #HEREE!!!
        # Save disc info
        cyl_final.legend('cyl2CutChambers_o')
        cyl_data = [r_circle_max, r_circle_min, normal_unit, pl_Ch_centre]
        dict_shapes = addShapes2Dict (shapes = [cyl_final], dict_shapes = dict_shapes, radius = [cyl_data], print_txt = False)

        # Create mask for created disc
        print('- Creating disc mask to cut chambers... (this takes about 2mins)')
        r_circle_max = dict_shapes['cyl2CutChambers_o']['radius_max']
        r_circle_min = dict_shapes['cyl2CutChambers_o']['radius_min']
        normal_unit = dict_shapes['cyl2CutChambers_o']['cyl_axis']
        cl_point = dict_shapes['cyl2CutChambers_o']['cyl_centre']
 
        # Create a disc with better resolution to transform into pixels to mask stack
        res_cyl = 2000
        num_rad = int(3*int(r_circle_max)) #int(((r_circle_max-r_circle_min)/0.225)+1)
        num_h = 9; h_min = 0.225/2; h_max = 0.225*2
        for j, rad in enumerate(np.linspace(r_circle_min/2, r_circle_max, num_rad)):
            for i,h in enumerate(np.linspace(h_min,h_max, num_h)):
                cyl = Cylinder(pos = cl_point,r = rad, height = h, axis = normal_unit, c = 'lime', cap = True, res = res_cyl)#.wireframe(True)
                if i == 0 and j == 0:
                    cyl_pts = cyl.points()
                else:
                    cyl_pts = np.concatenate((cyl_pts, cyl.points()))
 
        cyl.legend('cyl2CutChambers_final')
        cyl_data = [r_circle_max, r_circle_min/2, num_rad, h_max, h_min, num_h, normal_unit, cl_point, res_cyl]
        dict_shapes = addShapes2Dict (shapes = [cyl], dict_shapes = dict_shapes, radius = [cyl_data], print_txt = False)
 
        # Rotate the points that make up the HR disc, to convert them to a stack
        cyl_points_rot = np.zeros_like(cyl_pts)
        if 'CJ' not in filename:
            axis = [0,0,1]
        else:
            axis = [1,0,0]
 
        for i, pt in enumerate(cyl_pts):
            cyl_points_rot[i] = (np.dot(rotation_matrix(axis = axis, theta = np.radians(90)),pt))
 
        cyl_pix = np.transpose(np.asarray([cyl_points_rot[:,i]//resolution[i] for i in range(len(resolution))]))
        cyl_pix = cyl_pix.astype(int)
        cyl_pix = np.unique(cyl_pix, axis =0)
        # print(cyl_pix.shape)
 
        cyl_pix_out = cyl_pix.copy()
        index_out = []
        # Clean cyl_pix if out of stack shape
        for index, pt in enumerate(cyl_pix):
            # print(index, pt)
            if pt[0] > xdim-2 or pt[0] < 0:
                delete = True
            elif pt[1] > ydim-2 or pt[1] < 0:
                delete = True
            elif pt[2] > zdim+2-1 or pt[2] < 0:
                delete = True
            else:
                delete = False
 
            if delete:
                # print(pt)
                index_out.append(index)
 
        cyl_pix_out = np.delete(cyl_pix_out, index_out, axis = 0)
 
        # Create mask of ring
        s3_cyl = np.zeros((xdim, ydim, zdim+2))
        s3_cyl[cyl_pix_out[:,0],cyl_pix_out[:,1],cyl_pix_out[:,2]] = 1
        
        
        
    
    #%%
    ext_ch, _ = organ.get_ext_int_chs()
    mesh_ext = organ.obj_meshes[ext_ch.channel_no+'_tiss']
    fcMeshes.sphs_in_spline()
    
#%%
import vedo as vedo

mesh_ext = vedo.Mesh(vedo.dataurl + "bunny.obj").color("m")

pos = mesh_ext.center_of_mass()
color_o = [152, 251, 152, 255]
orient_cube = vedo.Cube(pos=pos, side=0.15, c=color_o[:-1])
orient_cube.linewidth(1).force_opaque()
orient_cube.pos(pos)
orient_cube_clear = orient_cube.clone().alpha(0.5)

planar_views = {
    "top": {"color": [255, 215, 0, 200]},
    "ventral": {"color": [0, 0, 205, 200]},
    "left": {"color": [255, 0, 0, 200]},
}


def select_cube_face(evt):
    orient_cube = evt.actor
    if not orient_cube:
        return
    pt = evt.picked3d
    idcell = orient_cube.closest_point(pt, return_cell_id=True)
    print("You clicked (idcell):", idcell)
    if set(orient_cube.cellcolors[idcell]) == set(color_o):
        orient_cube.cellcolors[idcell] = color_selected  # RGBA
        for cell_no in range(len(orient_cube.cells())):
            if cell_no != idcell and cell_no not in selected_faces:
                orient_cube.cellcolors[cell_no] = color_o  # RGBA

    planar_views[planar_view]["idcell"] = idcell
    cells = orient_cube.cells()[idcell]
    points = [orient_cube.points()[cell] for cell in cells]

    plane_fit = vedo.fit_plane(points, signed=True)
    planar_views[planar_view]["pl_normal"] = plane_fit.normal
    msg.text(
        "You selected face number: "
        + str(idcell)
        + " as "
        + planar_view.upper()
        + " face"
    )


def keypress(evt):
    if evt.keypress != "c":
        return
    selected_faces = []
    for planar_view in planar_views.keys():
        txt0.text(
            " - Reference cube and mesh to select "
            + planar_view.upper()
            + " planar view ..."
        )

        txt1.text(
            "Select (click) the cube face that represents the "
            + planar_view.upper()
            + " face and close the window when done.\nNote: The face that is last selected will be used for that planar face.",
        )
        plt.render()

        selected_faces.append(planar_views[planar_view]["idcell"])

msg = vedo.Text2D(pos="bottom-center", c="k", bg="white", alpha=0.8, s=0.7)
txt0 = vedo.Text2D(c="black", s=0.7)
txt1 = vedo.Text2D(c="black", s=0.7)

plt = vedo.Plotter(N=2, axes=1)
plt.add_callback("mouse click", select_cube_face)
plt.show(mesh_ext, orient_cube_clear, txt0, at=0)
plt.show(
    orient_cube,
    txt1,
    msg,
    at=1,
    azimuth=45,
    elevation=30,
    zoom=0.8,
)
plt.close


#%%
    #-------
    #Select direction of extended centreline
    #Create multiple cubes with different orientations based in the cust_angle? 
    # and with organ in centre? 
    # Ask the user to select the face that will be used to extend centreline?
    # Create a cube with orientation of heart using (tilted?)
    #https://github.com/marcomusy/vedo/blob/master/examples/basic/color_mesh_cells2.py
    from vedo import Mesh, Plotter, dataurl

    def func(evt):
        msh = evt.actor
        if not msh:
            return
        pt = evt.picked3d
        idcell = msh.closest_point(pt, return_cell_id=True)
        m.cellcolors[idcell] = [255,0,0,200] #RGBA 

    m = Mesh(dataurl + "panther.stl").c("blue7")
    m.force_opaque().linewidth(1)

    plt = Plotter()
    plt.add_callback("mouse click", func)
    plt.show(m, __doc__, axes=1).close()
    
    from vedo import Mesh, Plotter, dataurl, Cube, fit_plane

    def func(evt):
        msh = evt.actor
        if not msh:
            return
        pt = evt.picked3d
        idcell = msh.closest_point(pt, return_cell_id=True)
        print('idcell:', idcell)
        m.cellcolors[idcell] = [255,0,0,200] #RGBA 
        center = m.cell_centers()[idcell]
        cells = m.cells()[idcell]
        points = []
        for cell in cells: 
            point = m.points()[cell]
            points.append(point)
        print('m.cell_centers[idcell]',center)
        print('m.cell[idcell]',cells)
        print('m.points[cells]', points)
        
        plane = fit_plane(points, signed=True)
        print('normal:',plane.normal, 'center:',plane.center)
        
        

    # m = Mesh(dataurl + "panther.stl").c("blue7")
    m = Cube(pos=(0, 0, 0), side=1, c='g4', alpha=1)
    m.force_opaque().linewidth(1)

    plt = Plotter()
    plt.add_callback("mouse click", func)
    plt.show(m, __doc__, axes=1, interactive=True)
    
    

    #https://github.com/marcomusy/vedo/blob/master/examples/basic/mousehighlight.py
    #-------
    # return face direction ans use that as input in get_CLRibbon?



    # Select the centreline to use to divide organ into sections
    # nPoints = 300
    # organ_info = organ.mH_settings['general_info']
    # dict_cl = {}; obj = []; txt = []; n = 0
    # for item in organ.parent_project.mH_param2meas: 
    #     if 'centreline' in item: 
    #         n += 1
    #         ch = item[0]; cont = item[1]; segm = item[2]
    #         name = organ_info[ch]['user_chName']+'-'+cont+' ('+ch+'-'+cont+'-'+segm+')'
    #         dict_cl[n] = name
    #         mesh_o = organ.obj_meshes[ch+'_'+cont]
    #         cl_o = mesh_o.get_centreline(nPoints, 'indigo')
    #         obj.append((mesh_o.mesh, cl_o))
    #         if n-1==0:
    #             txt.append((n-1, organ.user_organName+'\n->'+name))
    #         else:  
    #             txt.append((n-1, '\n->'+name))
                
    # fcMeshes.plot_grid(obj=obj, txt=txt, axes=5)
    dict_cl = fcMeshes.plot_organCLs(organ)

    q ='Select the centreline  you would like to use to divide the organ tissues into sections'
    q_cl = fcBasics.ask4inputList(q, dict_cl, res_all=False)
    cl_sel = dict_cl[q_cl[0]].split(' (')[1]
    ch_sel = cl_sel.split('-')[0]
    cont_sel = cl_sel.split('-')[1]
    
    cl_mesh = organ.obj_meshes[ch_sel+'_'+cont_sel]
    nRes = 601
    plotshow=True
    cl_ribbon, kspl_ext = cl_mesh.get_clRibbon(nPoints,nRes, clRib_type='HDStack',plotshow=plotshow)
    
    fcMeshes.get_cube_clRibbon(organ, cl_mesh, cl_ribbon)
    
#%%
    """
    Created on Tue Mar 21 16:40:47 2023

    @author: bi1jsa
    """

    """Compute the (signed) distance of one mesh to another"""
    import vedo as vedo

    s1 = vedo.Sphere().pos(10,20,30)
    s2 = vedo.Cube(c='grey4').scale([2,1,1]).pos(14,20,30)

    def func(evt):
        if not evt.actor:
            return
        sil = evt.actor.silhouette().linewidth(6).c('red5')
        sil.name = "silu" # give it a name so we can remove the old one
        msg.text("You clicked: "+evt.actor.name)
        plt.remove('silu').add(sil)
        
    msg = vedo.Text2D("", pos="bottom-center", c='k', bg='r9', alpha=0.8)
        
    plt = vedo.Plotter(axes=1)
    plt.add_callback('mouse click', func)
    # plt.show(s1, s2, msg, __doc__, zoom=1.2)
    plt.show(mask_cube, mask_cubeB, msg, __doc__, zoom=1.2)
    plt.close()


#%%
"""Render meshes into inset windows
(which can be dragged)"""
from vedo import *

plt = Plotter(bg2='bisque', size=(1000,800), interactive=False)

e = Volume(dataurl+"embryo.tif").isosurface()
e.normalize().shift(-2,-1.5,-2).c("gold")

plt.show(e, __doc__, viewup='z')

# make clone copies of the embryo surface and cut them:
e1 = e.clone().cut_with_plane(normal=[0,1,0]).c("green4")
e2 = e.clone().cut_with_plane(normal=[1,0,0]).c("red5")

# add 2 draggable inset windows:
plt.add_inset(e1, pos=(0.9,0.8))
plt.add_inset(e2, pos=(0.9,0.5))

# customised axes can also be inserted:
ax = Axes(
    xrange=(0,1), yrange=(0,1), zrange=(0,1),
    xtitle='front', ytitle='left', ztitle='head',
    yzgrid=False, xtitle_size=0.15, ytitle_size=0.15, ztitle_size=0.15,
    xlabel_size=0, ylabel_size=0, zlabel_size=0, tip_size=0.05,
    axes_linewidth=2, xline_color='dr', yline_color='dg', zline_color='db',
    xtitle_offset=0.05, ytitle_offset=0.05, ztitle_offset=0.05,
)

ex = e.clone().scale(0.25).pos(0,0.1,0.1).alpha(0.1).lighting('off')
plt.add_inset(ax, ex, pos=(0.1,0.1), size=0.15, draggable=False)
plt.interactive().close()


#%%
import vedo as vedo

b = vedo.Mesh(vedo.dataurl+'bunny.obj').color('m')

b.name = 'Bunny'
# c = vedo.Mesh(vedo.dataurl+'bunny.obj').color('g').pos((0.1,0,0))
c = vedo.Cube(side=0.1).alpha(0.8).y(-0.02).lw(1)
c.name = 'Cube'

def func(evt):
    if not evt.actor:
        return
    sil = evt.actor.silhouette().linewidth(6).c('red5')
    sil.name = "silu" # give it a name so we can remove the old one
    msg.text("You clicked: "+evt.actor.name)
    plt.remove('silu').add(sil)
    
msg = vedo.Text2D("", pos="bottom-center", c='k', bg='r9', alpha=0.8)

plt = vedo.Plotter(axes=1, bg='black')
plt.add_callback('mouse click', func)
plt.show(b, c, msg, __doc__, zoom=1.2)
plt.close()

#%%
import vedo as vedo

mesh_ext = vedo.Mesh(vedo.dataurl+'bunny.obj').color('m')

pos = mesh_ext.center_of_mass()
color_o = [152,251,152,255]
orient_cube = vedo.Cube(pos=pos, side=0.15, c=color_o[:-1])
orient_cube.linewidth(1).force_opaque()
orient_cube.pos(pos)
orient_cube_clear = orient_cube.clone().alpha(0.5)

planar_views = {'top': {'color': [255, 215, 0, 200]},
                 'ventral': {'color': [0, 0, 205, 200]},
                 'left': {'color': [255, 0, 0, 200]}}

def select_cube_face(evt):
    orient_cube = evt.actor
    if not orient_cube:
        return
    pt = evt.picked3d
    idcell = orient_cube.closest_point(pt, return_cell_id=True)
    print('You clicked (idcell):', idcell)
    if set(orient_cube.cellcolors[idcell]) == set(color_o):
        orient_cube.cellcolors[idcell] = color_selected #RGBA 
        for cell_no in range(len(orient_cube.cells())):
            if cell_no != idcell and cell_no not in selected_faces: 
                orient_cube.cellcolors[cell_no] = color_o #RGBA 
                
    planar_views[planar_view]['idcell'] = idcell
    cells = orient_cube.cells()[idcell]
    points = [orient_cube.points()[cell] for cell in cells]
    
    plane_fit = vedo.fit_plane(points, signed=True)
    planar_views[planar_view]['pl_normal'] = plane_fit.normal
    msg.text('You selected face number: '+str(idcell)+' as '+planar_view.upper()+' face')
    
selected_faces = []
for planar_view in planar_views.keys(): 
    print('Selecting '+planar_view.upper()+'...')
    color_selected = planar_views[planar_view]['color']
    
    msg = vedo.Text2D("", pos="bottom-center", c='k', bg='white', alpha=0.8, s=0.7)
    txt0 = vedo.Text2D(' - Reference cube and mesh to select '+planar_view.upper()+' planar view ...', c='black', s=0.7)
    txt1 = vedo.Text2D('Select (click) the cube face that represents the '+planar_view.upper()+' face and close the window when done.\nNote: The face that is last selected will be used for that planar face.', c='black', s=0.7)
  
    plt = vedo.Plotter(N=2, axes=1)
    plt.add_callback("mouse click", select_cube_face)
    plt.show(mesh_ext, orient_cube_clear, txt0, at=0)
    plt.show(orient_cube, txt1, msg, at=1, azimuth=45, elevation=30, zoom=0.8, interactive=True)        
    
    selected_faces.append(planar_views[planar_view]['idcell'])
    
#%% To do: 
    #D update workflow when maesuring centrelines
    #D update workflow when measuring volumes
    #D revise segment creation in the workflow
    # see if there can be an easier way to create workflow dict
    # ask user if the project already exists if he/she wants to change some of the settings
    #D run it again to check if the changes from 'NotInitialised' to 'NI' works
    # create a kspline ribbon using the kspline
    #D add to the workflow - measurements if to divide meshes l/R with CL
    #D which name?
    #D which process would that be included in? - measure?
    # see whether to ask the user to select the cl to use to divide meshes L/R 
    # When creating the disk to cut meshes A/V how many discs to create and cut?
    # save the stacks for the disks?
    # save the stacks for the L/R
    # how to call l/r 
    #add to workflow and settings orientation, angle meas?, chamber dimensions
    
    
#%%
    # # Divide heart layers into chambers and save data
    # cyl_Chambers, num_pt, m_atr, m_vent, dict_shapes, dict_pts, s3_cyl = fcMeshes.getRing2CutChambers(filename = filename, 
    #                                                                               kspl_CL = kspl_CL[0], mesh2cut = m_myoc, 
    #                                                                               resolution = res, dir_stl = directories[2], 
    #                                                                               dir_txtNnpy = directories[1],
    #                                                                               dict_pts = dict_pts, 
    #                                                                               dict_shapes = dict_shapes)
    
#%%
from vedo import dataurl, Picture 
from vedo.applications import SplinePlotter  # ready to use class!

pic = Picture(dataurl + "images/embryo.jpg")

plt = SplinePlotter(pic)
plt.show(mode="image", zoom='tightest')
print("Npts =", len(plt.cpoints), "NSpline =", plt.line.npoints)

# %%
#%% pip freeze > requirements.txt