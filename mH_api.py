
'''
morphoHeart_api

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% Imports - ########################################################
# import pathlib
import sys
from pathlib import Path

print('package:', __package__)
print('name:', __name__)

alert_all=True
heart_default=False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}

#%% morphoHeart Imports - ##################################################
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
        #Initial set-up
        no_chs = 2
        layer_btw_chs = True
        cutLayersIn2Segments = True
        no_segments = 2
        no_cuts_4segments = 2
        cutLayersIn2Sections = True
        no_sections = 2

        #Setup 
        name_chs = {'ch1': 'myocardium', 'ch2': 'endocardium'}
        chs_relation =  {'ch1': 'external', 'ch2': 'internal'}
        color_chs = {'ch1':{'tiss':'lightseagreen','int':'gold','ext':'crimson'}, 
                     'ch2':{'tiss':'darkmagenta','int':'deepskyblue','ext':'deeppink'}}
        ch_ext = ('ch1', 'int')
        ch_int = ('ch2', 'ext')
        user_nsChName = 'cardiac jelly'
        color_chNS = {'tiss':'darkorange','ext':'powderblue', 'int':'greenyellow'}
        # By default the volume and surface area of the segments per tissue selected will be measured

        name_segments = {'segm1': 'atrium', 'segm2': 'ventricle'}
        # channels/meshes that will be divided into segments 
        ch_segments = {'ch1':['tiss', 'ext'],'ch2':['tiss', 'int'],'chNS':['tiss']}
        
        name_sections = {'sect1': 'left', 'sect2': 'right'}
        ch_sections = {'ch1':['tiss'],'ch2':['tiss'],'chNS':['tiss']}
        rotateZ_90 = True
        
        mH_settings = {'no_chs': no_chs,
                        'name_chs': name_chs,
                        'chs_relation': chs_relation,
                        'color_chs': color_chs,
                        'ns': #chNS
                            {'layer_btw_chs': layer_btw_chs,
                            'ch_ext': ch_ext,
                            'ch_int': ch_int,
                            'user_nsChName': user_nsChName,
                            'color_chns': color_chNS},
                        'segments': #segm 
                            {'cutLayersIn2Segments': cutLayersIn2Segments,
                            'no_segments': no_segments,
                            'no_cuts_4segments': no_cuts_4segments,
                            'name_segments': name_segments,
                            'ch_segments': ch_segments},
                        'sections': #sect
                            {'cutLayersIn2Sections': cutLayersIn2Sections,
                            'no_sections': no_sections,
                            'name_sections': name_sections,
                            'ch_sections': ch_sections},
                        'rotateZ_90': rotateZ_90}
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
    
    # Using one of the just created meshes, ask the user to select the stack 
    # planar views 
    colors = [[255,215,0,200],[0,0,205,200],[255,0,0,200]]
    views = ['top', 'ventral', 'left']
    organ.get_stack_orientation(views, colors)
    
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
    fcMeshes.extract_chNS(organ, plot)
        
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
    fcMeshes.proc_meshes4cl(organ, tol=tol, plot=plot)
    fcMeshes.extract_cl(organ)
    nPoints = 300
    fcMeshes.create_CLs(organ, nPoints = nPoints)
    
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
    fcMeshes.extract_thickness(organ, color_map='turbo', plot=plot)
    fcMeshes.extract_ballooning(organ, color_map='turbo', plot=plot)
    
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
    
#%% Part C-sect/segm
if partC: 
    if not partA and not partB and not partB_vmtk and not partC_thk: 
        # proj_name = proj_name
        folder_name = 'R_'+proj_name
        dir_proj = dir_proj_res / folder_name
        proj = mHC.Project(name = proj_name, dir_proj = dir_proj)
        # organName2Load = 'LS52_F02_V_SR_1029'
        organ = proj.load_organ(user_organName = organName2Load)
        fcMeshes.plot_all_organ(organ)
    
    # Get roi (organ) orientation
    colors = [[255,215,0,200],[0,0,205,200],[255,0,0,200]]
    views = ['top', 'ventral', 'left']
    organ.get_stack_orientation(views, colors)
    
    # Get organ orientation
    plane = 'YZ'
    ref_vect = 'Y+'
    colors = [[255,215,0,200],[0,0,205,200],[255,0,0,200]]
    views = ['top', 'ventral', 'left']
    organ.get_ROI_orientation(views, colors, plane='YZ',ref_vect=ref_vect)
    
    #--- CUT SECTIONS
    # Get organ centreline ribbon 
    nRes = 601; nPoints = 300; clRib_type = 'ext2sides'
    fcMeshes.get_organ_ribbon(organ, nRes, nPoints, clRib_type)
    # organ.info['shape_s3'] = organ.imChannels['ch1']['shape']
    fcMeshes.get_sect_mask(organ, plotshow=True)

    # Cut organ into sections
    subms = fcMeshes.get_sections(organ, plotshow=True)
    # myoc_tiss_left = subms[0].get_sect_mesh()
    # obj = [myoc_tiss_left]; txt = [(0,'test')]
    # fcMeshes.plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
    
    #--- CUT SEGMENTS
    fcMeshes.get_segm_discs(organ)
    # organ.mH_settings['general_info']['rotateZ_90'] = True
    fcMeshes.create_disc_mask(organ, h_min = 0.1125)
    # Cut organ into segments
    m_subg, segms = fcMeshes.get_segments(organ, plotshow=True)
    cj_tiss_vent = segms[-1].get_segm_mesh()
    obj = [cj_tiss_vent]; txt = [(0,'test')]
    fcMeshes.plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
    
    # Save organ
    organ.save_organ()
    # Load project, organ
    fcBasics.check_gral_loading(proj, proj_name, dir_proj, organ, organName2Load)
    
    #%%
    # Get volume measurements
    fcMeshes.measure_volume(organ)
    fcMeshes.measure_area(organ)


#%% Vedo examples
    #%%
    from vedo import *

    mesh = Mesh(dataurl + "bunny.obj")
    
    nv = mesh.ncells
    scals = range(nv)
    lut = build_lut([(nv / 2, "green5"), (nv, "red5"),], vmin=0, vmax=nv,)
    mesh.cmap(lut, scals, on="cells")
    mesh.legend("Bunny mesh")
    
    mk1 = Marker("*").c("green5").legend("cool faces")
    mk2 = Marker("*").c("red5").legend("ugly faces")
    lb = LegendBox(
        [mesh, mk1, mk2],
        markers=["s", "o", "0"],
        font="Cartoons123",
        width=0.4,
        height=0.2,
    )
    
    plt = Plotter()
    plt.show(mesh, lb, axes=1)

    
    
#%%
import vedo as vedo
b = vedo.Mesh(vedo.dataurl+'bunny.obj').color('dimgray').legend('No.1')
c = vedo.Mesh(vedo.dataurl+'bunny.obj').color('darkgray').pos((0.15,0,0)).legend('No.2')
d = vedo.Mesh(vedo.dataurl+'bunny.obj').color('lightgray').pos((-0.15,0,0)).legend('No.3')

mesh_classif = testing_callbacks([b,c,d])

e = vedo.Mesh(vedo.dataurl+'bunny.obj').color('grey')
#%%
### This class is a simplified version of the above, shown here as an example: #######
import vedo

class FreeHandCutPlotter(vedo.Plotter):
    def __init__(self, mesh):
        vedo.Plotter.__init__(self)
        self.mesh = mesh
        self.drawmode = False
        self.cpoints = []
        self.points = None
        self.spline = None
        self.msg  = "Right-click and move to draw line\n"
        self.msg += "Second right-click to stop drawing\n"
        self.msg += "Press z to cut mesh"
        self.txt2d = vedo.Text2D(self.msg, pos='top-left', font="Bongas")
        self.txt2d.c("white").background("green4", alpha=1)
        self.add_callback('KeyPress', self.onKeyPress)
        self.add_callback('RightButton', self.onRightClick)
        self.add_callback('MouseMove', self.onMouseMove)

    def onRightClick(self, evt):
        self.drawmode = not self.drawmode  # toggle mode

    def onMouseMove(self, evt):
        if self.drawmode:
            self.remove([self.points, self.spline])
            cpt = self.computeWorldPosition(evt.picked2d) # make this 2d-screen point 3d
            self.cpoints.append(cpt)
            self.points = vedo.Points(self.cpoints, r=8).c('black')
            if len(self.cpoints) > 2:
                self.spline = vedo.Line(self.cpoints, closed=True).lw(5).c('red5')
                self.add([self.points, self.spline]).render()

    def onKeyPress(self, evt):
        if evt.keypress == 'z' and self.spline:       # cut mesh with a ribbon-like surface
            vedo.printc("Cutting the mesh please wait..", invert=True)
            tol = self.mesh.diagonal_size()/2            # size of ribbon
            pts = self.spline.points()
            n = vedo.fitPlane(pts, signed=True).normal  # compute normal vector to points
            rib = vedo.Ribbon(pts - tol*n, pts + tol*n, closed=True)
            self.mesh.cutWithMesh(rib)
            self.remove([self.spline, self.points]).render()
            self.cpoints, self.points, self.spline = [], None, None

    def start(self, **kwargs):
        return self.show(self.txt2d, self.mesh, **kwargs)

#####################################################################################
vedo.settings.use_parallel_projection = True  # to avoid perspective artifacts

msh = vedo.Volume(vedo.dataurl+'embryo.tif').isosurface().color('gold', 0.25) # Mesh

plt = FreeHandCutPlotter(msh).add_hover_legend()
#plt.init(some_list_of_initial_pts) #optional!
plt.start(axes=1, bg2='lightblue').close()

#%%
from vedo import dataurl, Picture 
from vedo.applications import SplinePlotter  # ready to use class!

pic = Picture(dataurl + "images/embryo.jpg")

plt = SplinePlotter(pic)
plt.show(mode="image", zoom='tightest')
print("Npts =", len(plt.cpoints), "NSpline =", plt.line.npoints)

#####################################################################
# This is a simplified version of vedo.applications.SplinePlotter 
#####################################################################
from vedo import printc, precision, Plotter, Spline, Points, Text2D

class MySplinePlotter(Plotter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cpoints = []
        self.points = None
        self.spline = None

    def on_left_click(self, evt):
        if not evt.actor:
            return
        print('ev:', evt.picked3d)
        p = evt.picked3d + [0, 0, 1]
        self.cpoints.append(p)
        self.update()
        printc("Added point:", precision(p[:2], 4), c="g")

    def on_right_click(self, evt):
        if evt.actor and len(self.cpoints) > 0:
            self.cpoints.pop()  # pop removes the last point
            self.update()
            printc("Deleted last point", c="r")

    def on_key_press(self, evt):
        if evt.keypress == "c":
            self.cpoints = []
            self.remove(self.spline, self.points).render()
            printc("==== Cleared all points ====", c="r", invert=True)

    def update(self):
        self.remove([self.spline, self.points])  # remove old points and spline
        self.points = Points(self.cpoints).ps(10).c("purple5")
        self.points.pickable(False)  # avoid picking the same point
        if len(self.cpoints) > 2:
            self.spline = Spline(self.cpoints, closed=False).c("yellow5").lw(3)
            self.add(self.points, self.spline)
        else:
            self.add(self.points)

plt = MySplinePlotter(axes=True, bg="blackboard")
plt.add_callback("key press", plt.on_key_press)
plt.add_callback("left mouse click", plt.on_left_click)
plt.add_callback("right mouse click", plt.on_right_click)
plt.show(pic, mode="image", zoom=1.2)
plt.close()

#%%
from vedo import settings, Plotter, ParametricShape, VedoLogo, Text2D

settings.renderer_frame_width = 1

##############################################################################
def on_left_click(evt):
    if not evt.actor: return
    shapename.text(f'This is called: {evt.actor.name}, on renderer nr.{evt.at}')
    plt.at(1).remove(actsonshow).add(evt.actor).reset_camera()
    actsonshow.clear()
    actsonshow.append(evt.actor)

##############################################################################
sy, sx, dx = 0.12, 0.12, 0.01
# Define the renderers rectangle areas
# to help finding bottomleft&topright corners check out utils.grid_corners()
shape = [
    dict(bottomleft=(0,0), topright=(1,1), bg='k7'), # the full empty window
    dict(bottomleft=(dx*2+sx,0.01), topright=(1-dx,1-dx), bg='w'), # the display window
    dict(bottomleft=(dx,sy*1), topright=(dx+sx,sy*2), bg='k8', bg2='lb'), # CrossCap
    dict(bottomleft=(dx,sy*2), topright=(dx+sx,sy*3), bg='k8', bg2='lb'),
    dict(bottomleft=(dx,sy*3), topright=(dx+sx,sy*4), bg='k8', bg2='lb'),
    dict(bottomleft=(dx,sy*4), topright=(dx+sx,sy*5), bg='k8', bg2='lb'),
    dict(bottomleft=(dx,sy*5), topright=(dx+sx,sy*6), bg='k8', bg2='lb'),
    dict(bottomleft=(dx,sy*6), topright=(dx+sx,sy*7), bg='k8', bg2='lb'),
    dict(bottomleft=(dx,sy*7), topright=(dx+sx,sy*8), bg='k8', bg2='lb'), # RandomHills
]

plt = Plotter(shape=shape, sharecam=False, size=(1050, 980))
plt.add_callback("when i click my mouse button please call", on_left_click)

for i in range(2,9):
    ps = ParametricShape(i).color(i)
    pname = Text2D(ps.name, c='k', bg='blue', s=0.7, font='Calco')
    plt.at(i).show(ps, pname)

shapename = Text2D(pos='top-center', c='r', bg='y', font='Calco') # empty text

vlogo = VedoLogo(distance=5)
actsonshow = [vlogo]

title = "My Multi Viewer 1.0"
instr = "Click on the left panel to select a shape\n"
instr+= "Press h to print the full list of options"

plt.at(1).show(
    vlogo, shapename,
    Text2D(title, pos=(0.5,0.85), s=2.5, c='dg', font='Kanopus', justify='center'),
    Text2D(instr, bg='g', pos=(0.5,0.05), s=1.2, font='Quikhand', justify='center'),
)
plt.interactive().close()

#%%
# Create a class which wraps the vedo.Plotter class and adds a timer callback
# Credits: Nicolas Antille, https://github.com/nantille
# Check out the simpler example: timer_callback1.py
import vedo


class Viewer:

    def __init__(self, *args, **kwargs):
        self.dt = kwargs.pop("dt", 100) # update every dt milliseconds
        self.timer_id = None
        self.isplaying = False
        self.counter = 0 # frame counter
        self.button = None

        self.plotter = vedo.Plotter(*args, **kwargs) # setup the Plotter object
        self.timerevt = self.plotter.add_callback('timer', self.handle_timer)

    def initialize(self):
        # initialize here extra elements like buttons etc..
        self.button = self.plotter.add_button(
            self._buttonfunc,
            states=["\u23F5 Play  ","\u23F8 Pause"],
            font="Kanopus",
            size=32,
        )
        return self

    def show(self, *args, **kwargs):
        plt = self.plotter.show(*args, **kwargs)
        return plt

    def _buttonfunc(self):
        if self.timer_id is not None:
            self.plotter.timer_callback("destroy", self.timer_id)
        if not self.isplaying:
            self.timer_id = self.plotter.timer_callback("create", dt=100)
        self.button.switch()
        self.isplaying = not self.isplaying

    def handle_timer(self, event):
        #####################################################################
        ### Animate your stuff here                                       ###
        #####################################################################
        #print(event)               # info about what was clicked and more
        moon.color(self.counter)    # change color to the Moon
        earth.rotate_z(2)           # rotate the Earth
        moon.rotate_z(1)
        txt2d.text("Moon color is:").color(self.counter).background(self.counter,0.1)
        txt2d.text(vedo.get_color_name(self.counter), "top-center")
        txt2d.text("..press q to quit", "bottom-right")
        self.plotter.render()
        self.counter += 1


viewer = Viewer(axes=1, dt=150).initialize()

earth  = vedo.Earth()
moon   = vedo.Sphere(r=0.1).x(1.5).color('k7')
txt2d  = vedo.CornerAnnotation().font("Kanopus")

viewer.show(earth, moon, txt2d, viewup='z').close()

#%%
"""Create a scatter plot to overlay
three different distributions"""
from vedo import *
from numpy.random import randn

### first cloud in blue, place it at z=0:
x = randn(2000) * 3
y = randn(2000) * 2
pts1 = Points([x,y], c="blue", alpha=0.5).z(0.0)
bra1 = Brace([-7,-8], [7,-8],
             comment='whole population', s=0.4, c='b')

### second cloud in red
x = randn(1200) + 4
y = randn(1200) + 2
pts2 = Points([x,y], c="red", alpha=0.5).z(0.1)
bra2 = Brace([8,2,0.3], [6,5,0.3], comment='red zone',
             angle=180, justify='bottom-center', c='r')

### third cloud with a black marker
x = randn(20) + 4
y = randn(20) - 4
mark = Marker('*', s=0.25)
pts3 = Glyph([x,y], mark, c='k').z(0.2)
bra3 = Brace([8,-6], [8,-2], comment='my stars').z(0.3)

# some text message
msg = Text3D("preliminary\nresults!", font='Quikhand', s=1.5)
msg.c('black').rotate_z(20).pos(-10,3,.2)

show(pts1, pts2, pts3, msg, bra1, bra2, bra3, __doc__,
     axes=1, zoom=1.2, viewup="2d",
).close()

#%%
"""Hover mouse onto an object
to pop a flag-style label"""
from vedo import *

b = Mesh(dataurl+'bunny.obj').color('m')
c = Cube(side=0.1).compute_normals().alpha(0.8).y(-0.02).lighting("off").lw(1)

fp = b.flagpole('A flag pole descriptor\nfor a rabbit', font='Quikhand')
fp.scale(0.5).color('v').use_bounds() # tell camera to take fp bounds into account

c.caption('2d caption for a cube\nwith face indices', point=[0.044, 0.03, -0.04],
          size=(0.3,0.06), font="VictorMono", alpha=1)

# create a new object made of polygonal text labels to indicate the cell numbers
flabs = c.labels('id', on="cells", font='Theemim', scale=0.02, c='k')
vlabs = c.clone().clean().labels2d(font='ComicMono', scale=3, bc='orange7')

# create a custom entry to the legend
b.legend('Bugs the bunny')
c.legend('The Cube box')
lbox = LegendBox([b,c], font="Bongas", width=0.25)

show(b, c, fp, flabs, vlabs, lbox, __doc__, axes=11, bg2='linen').close()

#%%
"""Modify a spline interactively.
- Drag points with mouse
- Add points by clicking on the line
- Remove them by selecting&pressing DEL
--- PRESS q TO PROCEED ---"""
from vedo import Circle, show

# Create a set of points in space
pts = Circle(res=8).extrude(zshift=0.5).ps(4)

# Visualize the points
plt = show(pts, __doc__, interactive=False, axes=1)

# Add the spline tool using the same points and interact with it
sptool = plt.add_spline_tool(pts, closed=True)
plt.interactive()

# Switch off the tool
sptool.off()

# Extract and visualize the resulting spline
sp = sptool.spline().lw(4)
show(sp, "My spline is ready!", interactive=True, resetcam=False).close()

#%%
"""Drag the sphere to cut the mesh interactively
Use mouse buttons to zoom and pan"""
from vedo import *

# s = Mesh(dataurl+'cow.vtk')

plt = show(s, __doc__, bg='black', bg2='white', interactive=False)
plt.add_cutter_tool(s, mode='sphere') #modes= sphere, plane, box
plt.close()

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
    # sil.name = "silu" # give it a name so we can remove the old one
    # msg.text("You clicked: "+evt.actor.name)
    plt.remove('silu').add(sil)
    
# msg = vedo.Text2D("", pos="bottom-center", c='k', bg='r9', alpha=0.8)

plt = vedo.Plotter(axes=1, bg='black')
plt.add_callback('mouse click', func)
plt.show(b, __doc__, zoom=1.2)
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