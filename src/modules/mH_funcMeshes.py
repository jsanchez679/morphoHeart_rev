'''
morphoHeart_funcMeshes

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
import os
from datetime import datetime
from pathlib import Path, WindowsPath, PurePath
import vedo as vedo
import numpy as np
import math
# from textwrap import wrap
import flatdict
from itertools import count
import json
import vmtk
from vmtk import pypes, vmtkscripts
from scipy.interpolate import splprep, splev, interpn
from time import perf_counter
import copy
from typing import Union
from skimage import measure
import seaborn as sns
import random

path_fcMeshes = os.path.abspath(__file__)
path_mHImages = Path(path_fcMeshes).parent.parent.parent / 'images'


#%% Set default fonts and sizes for plots
txt_font = 'Dalim'
leg_font = 'LogoType' # 'Quikhand' 'LogoType'  'Dalim'
leg_width = 0.18
leg_height = 0.2
txt_size = 0.8
txt_color = '#696969'
txt_slider_size = 0.8

#%%
# Definition of class to save dictionary
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, Union(WindowsPath, PurePath)):
            return str(obj)
        else:
            return super(NumpyArrayEncoder, self).default(obj)
        
#%% ##### - Other Imports - ##################################################
from ..gui.config import mH_config
from .mH_funcBasics import ask4input, get_by_path, alert
from ..gui.gui_classes import Prompt_ok_cancel_radio

# from .mH_classes_new import ImChannelNS#, Mesh_mH

# alert_all = True
# heart_default = False
# dict_gui = {'alert_all': alert_all,
#             'heart_default': heart_default, 
#             'colorMap': 'turbo'}
            
#%% - morphoHeart B functions
#%% func - s32Meshes
def s32Meshes(organ, gui_keep_largest:dict, win, rotateZ_90=True):

    workflow = organ.workflow['morphoHeart']
    for ch in organ.obj_imChannels.keys(): 
        win.win_msg('Creating Channel '+ch[-1]+' meshes!')
        #Check if all the meshes for each channel ha
        im_ch = organ.obj_imChannels[ch]
        process = ['MeshesProc','A-Create3DMesh', im_ch.channel_no]
        mesh_done = [get_by_path(workflow, process+[cont]+['Status']) for cont in ['tiss', 'int', 'ext']]
        if not all(flag == 'DONE' for flag in mesh_done):
            new_set = True
        else: 
            new_set = False
            
        meshes = im_ch.s32Meshes(cont_types=['int', 'ext', 'tiss'],
                                    keep_largest=gui_keep_largest[im_ch.channel_no],
                                    win=win,
                                    rotateZ_90 = rotateZ_90, new_set = new_set)
        
        #Message User
        win.win_msg(' Channel '+ch[-1]+' meshes were successfully created!')

        #Enable button for plot
        plot_btn = getattr(win, 'keeplargest_plot_'+ch)
        plot_btn.setEnabled(True)
    
    #Enable button for plot all
    plot_all = getattr(win, 'keeplargest_plot')
    plot_all.setEnabled(True)

#%% func - clean_intCh
def clean_ch(organ, gui_clean, win, plot=False):

    workflow = organ.workflow['morphoHeart']
    for ch in gui_clean.keys():
        win.win_msg('Cleaning Channel '+ch[-1]+' meshes!')
        #Get channel and contours to clean
        ch_to_clean = organ.obj_imChannels[ch]
        ch_to_clean.load_chS3s(cont_types = gui_clean[ch]['cont'])

        #Get channel to use as mask for cleaning
        with_ch = gui_clean[ch]['with_ch']
        ch_with = organ.obj_imChannels[with_ch]
        with_cont = gui_clean[ch]['with_cont']
        ch_with.load_chS3s(cont_types = [with_cont])
        s3_mask = getattr(ch_with, 's3_'+with_cont)
        inverted = gui_clean[ch]['inverted']
        process = ['ImProc', ch, 'E-CleanCh', 'Status']
        
        for cont in gui_clean[ch]['cont']:
            print('Cleaning '+ch+'-'+cont+' with '+with_ch+'-'+with_cont+' (inverted: '+str(inverted)+').')
            win.win_msg('Cleaning '+ch+'-'+cont+' with '+with_ch+'-'+with_cont+' (inverted: '+str(inverted)+').')
            #Get the contour to clean
            s3 = getattr(ch_to_clean, 's3_'+cont)
            ch_to_clean.ch_clean(s3_mask=s3_mask, s3=s3, inverted=inverted, plot=plot)
    
            #Update workflow 
            proc_up = ['ImProc',ch,'E-CleanCh','Info',s3.cont_type, 'Status']
            organ.update_mHworkflow(proc_up, 'DONE')
            print('> Update:', proc_up, get_by_path(workflow, proc_up))
                
        # Update organ workflow
        organ.update_mHworkflow(process, 'DONE')
        print('> Update:', process, get_by_path(workflow, process))

        #Message User
        win.win_msg('Contours of channel '+ch[-1]+' were successfully cleaned!')

        #Enable button for plot
        plot_btn = getattr(win, 'cleanup_plot_'+ch)
        plot_btn.setEnabled(True)

    #Enable button for plot all
    plot_all = getattr(win, 'clean_plot')
    plot_all.setEnabled(True)

#%% func - select_meshes2trim
def select_meshes2trim(organ): # to delete
    pass 
    # names_mesh_tiss = [name for name in organ.obj_meshes if 'tiss' in name and 'NS' not in name]
    # obj = []
    # # meshes = []
    # for name in names_mesh_tiss: 
    #     obj.append(organ.obj_meshes[name].mesh)
    #     # meshes.append(organ.obj_meshes[name])
    # obj_t = tuple(obj)
    # obj.append(obj_t)
    
    # # obj = [(msh1_tiss.mesh),(msh2_tiss.mesh),(msh1_tiss.mesh, msh2_tiss.mesh)]
    # text = organ.user_organName+"\n\nTake a closer look at both meshes and decide from which layer to cut\n the inflow and outflow. \nClose the window when done"
    # txt = [(0, text)]
    # plot_grid(obj=obj, txt=txt, axes=5, lg_pos='bottom-right', sc_side=max(organ.get_maj_bounds()))
    
    # # return meshes

#%% func - trim_top_bottom_S3s
def trim_top_bottom_S3s(organ, meshes, no_cut, cuts_out, win):

    # filename = organ.user_organName
    # #Get meshes to cut
    # meshes = []
    # no_cut = []
    # for ch in organ.obj_imChannels.keys():
    #     for cont in ['tiss', 'ext', 'int']:
    #         if gui_trim['top']['chs'][ch][cont] or gui_trim['bottom']['chs'][ch][cont]:
    #             meshes.append(organ.obj_meshes[ch+'_'+cont])
    #             break
    #         else: 
    #             no_cut.append(ch+'_'+cont)
    
    # # User user input to select which meshes need to be cut
    # cuts_names = {'top': {'heart_def': 'outflow tract','other': 'top'},
    #             'bottom': {'heart_def': 'inflow tract','other': 'bottom'}}
    # cuts_out = copy.deepcopy(gui_trim)
    
    # # cuts_out = {'top': {'chs': {}},
    # #             'bottom': {'chs': {}}
    # # cut_top = []; cut_bott = []; cut_chs = {}
    # # for ch in organ.imChannels.keys():
    # #     cuts_out['top']['chs'][ch] = gui_trim['top']['chs'][ch]
    # #     cuts_out['bottom']['chs'][ch] = gui_trim['bottom']['chs'][ch] 
    # #     cut_chs[ch] = []
        
    # cut_top = []; cut_bott = []; cut_chs = {}
    # cuts_flat = flatdict.FlatDict(gui_trim)
    # print('A:',cuts_flat)
    # for key in cuts_flat.keys():
    #     if 'top' in key and 'object' not in key: 
    #         cut_top.append(cuts_flat[key])
    #     if 'bot' in key and 'object' not in key: 
    #         cut_bott.append(cuts_flat[key])
    #     for ch in organ.imChannels.keys(): 
    #         if ch in key:
    #             if ch not in cut_chs.keys(): 
    #                 cut_chs[ch] = []
    #             else: 
    #                 pass
    #             if cuts_flat[key]:
    #                 cut_chs[ch].append(key.split(':')[0])
                                
    # print('cut_chs:', cut_chs)
    # print('cut_top:', cut_top)
    # print('cut_bott:', cut_bott)
            
    # if mH_config.heart_default:
    #     name_dict =  'heart_def'     
    # else: 
    #     name_dict = 'other'
        
    # #Define plane to cut bottom
    # if any(cut_bott):
    #     #Define plane to cut bottom
    #     plane_bott, pl_dict_bott = get_plane(filename=filename, 
    #                                         txt = 'cut '+cuts_names['bottom'][name_dict],
    #                                         meshes = meshes, win=win)    
    #     cuts_out['bottom']['plane_info_mesh'] = pl_dict_bott
    #     # Reorient plane to images (s3)
    #     plane_bottIm, pl_dict_bottIm = rotate_plane2im(pl_dict_bott['pl_centre'], 
    #                                                         pl_dict_bott['pl_normal'])
    #     cuts_out['bottom']['plane_info_image'] = pl_dict_bottIm
        
    # #Define plane to cut top
    # if any(cut_top):
    #     #Define plane to cut top
    #     plane_top, pl_dict_top = get_plane(filename=filename, 
    #                                         txt = 'cut '+cuts_names['top'][name_dict],
    #                                         meshes = meshes, win=win)
    #     cuts_out['top']['plane_info_mesh'] = pl_dict_top
    #     # Reorient plane to images (s3)
    #     plane_topIm, pl_dict_topIm = rotate_plane2im(pl_dict_top['pl_centre'], 
    #                                                     pl_dict_top['pl_normal'])
    #     cuts_out['top']['plane_info_image'] = pl_dict_topIm
        
    # print('cuts_out:', cuts_out)

    # #Update mH_settings with channels to be cut
    # update_im = {}; update_mesh = {}
    # for ch_a in ch_planes: 
    #     update_im[ch_a] = {'cut_image': None}
    #     update_mesh[ch_a] = {'cut_mesh': None}
    # proc_im = ['wf_info','ImProc','E-TrimS3','Planes']
    # organ.update_settings(proc_im, update_im, 'mH')
    # proc_meshes = ['wf_info','MeshesProc','B-TrimMesh','Planes']
    # organ.update_settings(proc_meshes, update_mesh, 'mH')
    # # print('ch_planes:', ch_planes)
    
    #Update workflow for channels that won't be cut
    for ch_c in no_cut:
        proc_c = ['ImProc', ch_c, 'E-TrimS3']
        for cont in ['int','ext','tiss']:
            organ.update_mHworkflow(proc_c+['Info',cont,'Status'],'DONE-NoCut')
        organ.update_mHworkflow(proc_c+['Status'],'DONE-NoCut')
    
    #Cut channel s3s and recreate meshes
    for mesh in meshes:
        ch_name = mesh.imChannel.channel_no
        im_ch = mesh.imChannel
        cont_to_cut = []
        for cont in ['int', 'tiss', 'ext']: 
            cuts = []
            for side in ['top', 'bottom']: 
                if cuts_out[side]['chs'][ch_name][cont]:
                    cuts.append(side)
            if len(cuts) > 0: 
                print('Cutting '+ch_name.title()+' (contour: '+cont+')...')
                win.msg_win('Cutting '+ch_name.title()+' (contour: '+cont+')...')
                im_ch.trimS3(cuts=cuts, cont=cont, cuts_out=cuts_out)
                cont_to_cut.append(cont)
        if len(cont_to_cut) > 0:
            im_ch.createNewMeshes(cont_types=cont_to_cut,
                                    process = 'AfterTrimming', new_set=True)
    
    # return cuts_out

    # for ch_b in ch_meshes: 
    #     print('ch_b:', ch_b)
    #     im_ch = ch_meshes[ch_b]
    #     print('cut_chs[ch_b]:',cut_chs[ch_b], '--',cuts_out)
    #     # im_ch.trimS3(cuts=cut_chs[ch_b], cuts_out=cuts_out)
    #     print('\n---RECREATING MESHES AFTER TRIMMING ('+ch_b+')---')
    #     meshes = im_ch.createNewMeshes(cont_types=['int', 'ext', 'tiss'],
    #                                     process = 'AfterTrimming', new_set=True)
    #     meshes_out.append(meshes)
    # organ.mH_settings['cut_ch'] = cut_chs
    
    # obj = []
    # for ch_d in meshes_out:
    #     for mesh in ch_d: 
    #         obj.append(mesh.mesh)
            
    # txt = [(0, organ.user_organName  + ' - Meshes after trimming')]
    # plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))


#%% func - extract_chNS
def extract_chNS(organ, plot):
    from .mH_classes import ImChannelNS
    if 'chNS' in organ.mH_settings['general_info'].keys():
        im_ns = ImChannelNS(organ=organ, ch_name='chNS')
        im_ns.create_chNSS3s(plot=plot)
        
        gui_keep_largest = {'int': True, 'ext': True, 'tiss': False}
        [mshNS_int, mshNS_ext, mshNS_tiss] = im_ns.s32Meshes(cont_types=['int', 'ext', 'tiss'],
                                                             keep_largest=gui_keep_largest,
                                                             rotateZ_90 = True, new_set = True)
       
        txt = [(0, organ.user_organName  + ' - Extracted ' + im_ns.user_chName)]
        obj = [(mshNS_ext.mesh),(mshNS_int.mesh),(mshNS_tiss.mesh)]
        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
        
        txt = [(0, organ.user_organName  + ' - Final reconstructed meshes')]
        obj = [organ.obj_meshes[key].mesh for key in organ.obj_meshes.keys() if 'tiss' in key]
        obj.append(tuple(obj))
        # obj = [(msh1_tiss.mesh),(msh2_tiss.mesh),(mshNS_tiss.mesh),(msh1_tiss.mesh, msh2_tiss.mesh, mshNS_tiss.mesh)]
        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
    
    else: 
        print('>> No layer between segments is being created as it was not setup by user!')
        alert('error_beep')

    
#%% func - proc_meshes4cl
def proc_meshes4cl(organ, tol, plot=True, printshow=True):
    """
    Funtion that cuts the inflow and outflow tract of meshes from which 
    the centreline will be obtained.

    """
    #Check first if extracting centrelines is a process involved in this organ/project
    if organ.check_method(method = 'C-Centreline'): 
    # if 'C-Centreline' in organ.parent_project.mH_methods: 
        #Check workflow status
        workflow = organ.workflow
        process = ['MeshesProc','C-Centreline','SimplifyMesh','Status']
        check_proc = get_by_path(workflow, process)
        
        #Check meshes to process in MeshLab have been saved
        path2files = organ.mH_settings['wf_info']['MeshesProc']['C-Centreline']
        files_exist = []
        for ch_s in path2files.keys():
            if 'ch' in ch_s:
                for cont_s in path2files[ch_s].keys():
                    dir2check = path2files[ch_s][cont_s]['dir_meshLabMesh']
                    if dir2check != None: 
                        files_exist.append(dir2check.is_file())
                    else: 
                        files_exist.append(dir2check)
                    print (ch_s, cont_s)
        
        if check_proc == 'DONE' and all(flag for flag in files_exist):
            q = 'You already cleaned and cut the meshes to extract the centreline. Do you want to clean and cut them again?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run these two processes!'}
            cut_meshes4cl = ask4input(q, res, bool)
        else: 
            cut_meshes4cl = True
            
        if cut_meshes4cl: 
            # Set cut names 
            cuts_names = {'top': {'heart_def': 'outflow tract','other': 'top'},
                        'bottom': {'heart_def': 'inflow tract','other': 'bottom'}}
            
            if dict_gui['heart_default']: 
                name_dict =  'heart_def'     
            else: 
                name_dict = 'other'
                
            # Assign colors to top and bottom splines and spheres
            color_cuts = {'bottom': 'salmon','top':'mediumseagreen' }
            
            # Get organ settings
            filename = organ.user_organName
            ch_ext, _ = organ.get_ext_int_chs()
            ext = 'stl'; directory = organ.info['dirs']['centreline']
            
            # Get the meshes from which the centreline needs to be extracted
            cl_names = [item for item in organ.parent_project.mH_param2meas if 'centreline' in item]
            cl_names = sorted(cl_names, key=lambda x: (x[0], x[1]))
            # Create lists with mesh_mH, channel number and mesh names
            mH_mesh4cl = []; chs4cl = []
            for n, name in enumerate(cl_names): 
                mH_mesh = organ.obj_meshes[name[0]+'_'+name[1]]
                mH_mesh4cl.append(mH_mesh)
                chs4cl.append(organ.obj_meshes[name[0]+'_'+name[1]].channel_no)
            
            # Get dictionary with initialised planes to cut top/bottom
            top_done = False; bot_done = False
            planes_info = {'top':None, 'bottom':None}
            for ch in organ.mH_settings['wf_info']['MeshesProc']['B-TrimMesh']['Planes'].keys():
                # print(ch)
                dict2check = organ.mH_settings['wf_info']['MeshesProc']['B-TrimMesh']['Planes'][ch]['cut_mesh']
                if 'top' in dict2check and not top_done:
                    print('in top:', ch)
                    planes_info['top'] = dict2check['top']
                    top_done = True
                if 'bottom' in dict2check and not bot_done:
                    print('in bot:', ch)
                    planes_info['bottom'] = dict2check['bottom']
                    bot_done = True
            print('planes_info:', planes_info)
            
            # cuts = ['bottom', 'top']; cut_direction = [True, False]
            ksplines = []; spheres = []; m4clf=[]
            plane_cuts = {'bottom': {'dir': True, 'plane': None, 'pl_dict': None}, 
                          'top': {'dir': False,'plane': None, 'pl_dict': None}}
            
            for n, mH_msh in enumerate(mH_mesh4cl):
                for nn, pl_cut in zip(count(), plane_cuts.keys()):
                    print('n:', n, 'nn:', nn, 'pl_cut:', pl_cut)
                    if nn == 0:
                        print('>> Smoothing mesh')
                        sm_msh = mH_msh.mesh4CL()
                    # Get planes for first mesh
                    if n == 0: 
                        if planes_info[pl_cut] == None:
                            #Planes have not been initialised
                            print('-Planes have not been initialised for ', pl_cut)
                            plane, pl_dict = get_plane(filename=filename, 
                                                        txt = 'cut '+cuts_names[pl_cut][name_dict],
                                                        meshes = [sm_msh]) 
                        else:
                            print('-Planes have been initialised for ', pl_cut)
                            # Planes have been initialised
                            plane, pl_dict = get_plane(filename=filename, 
                                                        txt = 'cut '+cuts_names[pl_cut][name_dict],
                                                        meshes = [sm_msh], def_pl = planes_info[pl_cut]) 
                        
                        plane_cuts[pl_cut]['plane'] = plane
                        plane_cuts[pl_cut]['pl_dict'] = pl_dict
                        #Update mH_settings
                        proc_wf = ['wf_info','MeshesProc', 'C-Centreline', 'Planes', pl_cut]
                        organ.update_settings(process = proc_wf, update = pl_dict, mH='mH')
                
                    print('> Cutting mesh: ', mH_msh.legend, '-', pl_cut)
                    pts2cut, _ = get_pts_at_plane(points = sm_msh.points(), 
                                                    pl_normal = plane_cuts[pl_cut]['pl_dict']['pl_normal'],
                                                    pl_centre = plane_cuts[pl_cut]['pl_dict']['pl_centre'], tol=tol)
                    ordpts, angle = order_pts(points = pts2cut)
                    # Create spline around cut
                    kspl = vedo.KSpline(ordpts, continuity=0, tension=0, bias=0, closed=True)
                    kspl.color(color_cuts[pl_cut]).legend('cut4CL_'+pl_cut).lw(2)
                    organ.add_object(kspl, proc='cut4cl', class_name=[pl_cut,mH_msh.name], name='KSpline')
                    ksplines.append(kspl)
                    
                    # Get centroid of kspline to add to the centreline
                    kspl_bounds = kspl.bounds()
                    pt_centroid = np.mean(np.asarray(kspl_bounds).reshape((3, 2)),axis=1)
                    sph_centroid = vedo.Sphere(pos=pt_centroid, r=2).legend('cut4CL_'+pl_cut).color(color_cuts[pl_cut])
                    organ.add_object(sph_centroid, proc='cut4cl', class_name=[pl_cut,mH_msh.name], name='Sphere')
                    spheres.append(sph_centroid)
                    
                    # Cutmesh using created plane
                    msh_new = sm_msh.clone().cut_with_mesh(plane_cuts[pl_cut]['plane'], invert=plane_cuts[pl_cut]['dir'])
                    msh_new = msh_new.extract_largest_region()
                    msh_new.alpha(0.05).wireframe(True).legend(mH_msh.legend)
                    
                    if plot: 
                        txt = [(0, organ.user_organName  + ' - Resulting mesh after cutting')]
                        obj = [(msh_new, kspl, sph_centroid)]
                        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
                    
                    sm_msh = msh_new.clone()
                    
                m4clf.append(sm_msh)
                
                print('> Saving cut meshes')
                mesh_title = filename+"_"+mH_msh.name+"_cut4cl."+ext
                mesh_titleML = filename+"_"+mH_msh.name+"_cut4clML."+ext
                mesh_dir = directory / mesh_title
                mesh_dirML = directory / mesh_titleML
                msh_new.write(str(mesh_dir))
                
                # Update mH_settings
                ch_cont = mH_msh.name
                ch = ch_cont.split('_')[0]
                cont = ch_cont.split('_')[1]
                
                proc_set = ['wf_info', 'MeshesProc', 'C-Centreline', ch, cont]
                organ.update_settings(process = proc_set+['dir_cleanMesh'], update = mesh_dir, mH='mH')
                organ.update_settings(process = proc_set+['dir_meshLabMesh'], update = mesh_dirML, mH='mH')
                
                # Update organ workflow
                proc_wft = ['MeshesProc', 'C-Centreline', 'SimplifyMesh', ch, cont, 'Status']
                organ.update_workflow(process = proc_wft, update = 'DONE')
                                   
            if plot: 
                txt = [(0, organ.user_organName  + ' - Resulting meshes after cutting')]
                obj = [(mesh) for mesh in m4clf]
                plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
                
            organ.update_workflow(process = process, update = 'DONE')
            organ.update_workflow(process =  ['MeshesProc','C-Centreline','Status'], update = 'Initialised')
            organ.save_organ()
        
        if printshow:
            print("\nYou are done in morphoHeart for a little while... \nTo get the centreline of each of the selected meshes follow the next steps:")
            print("> 1. Open the stl file(s) in Meshlab")
            print("> 2. Run Filters > Remeshing, Simplification.. > Screened Poisson Surf Reco (check Pre-clean)")
            print("> 3. Cut inflow and outflow tract as close as the cuts from the original mesh you opened in \n\t Meshlab and export the resulting surface adding 'ML' at the end of the filename\n\t (e.g _cut4clML.stl) in the same folder")
            print("> 4. Come back and continue processing!...")
            
        alert('countdown')

#%% func - extract_cl
def extract_cl(organ, voronoi=False):
    
    #Check first if extracting centrelines is a process involved in this organ/project
    if organ.check_method(method = 'C-Centreline'): 
    # if 'C-Centreline' in organ.parent_project.mH_methods: 
        #Check workflow status
        workflow = organ.workflow
        process = ['MeshesProc','C-Centreline','vmtk_CL','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE': 
            q = 'You already extracted the centreline of the selected meshes. Do you want to extract the centreline again?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run this process!'}
            extractCL = ask4input(q, res, bool)
        else: 
            extractCL = True
            
        if extractCL: 
            cl_names = [item for item in organ.parent_project.mH_param2meas if 'centreline' in item]
            
            for name in cl_names: 
                ch = name[0]; cont = name[1]
                #Get the vmtk txt
                vmtktxt, dir_npcl = code_vmtk(organ, ch, cont, voronoi)
                
                myArguments = vmtktxt
                myPype = pypes.PypeRun(myArguments)
                
                for m in range(len(myPype.ScriptObjectList)):
                    if isinstance(myPype.ScriptObjectList[m], vmtk.vmtkcenterlines.vmtkCenterlines):
                        centerlineReader = myPype.ScriptObjectList[m]
                clNumpyAdaptor = vmtkscripts.vmtkCenterlinesToNumpy()
                clNumpyAdaptor.Centerlines = centerlineReader.Centerlines # Surface # cl
                clNumpyAdaptor.Execute()
                numpyCenterlines = clNumpyAdaptor.ArrayDict
        
                # Copy dictionary into new dictionary to save
                centrelines_dict = dict()
                centrelines_dict['Points'] =  numpyCenterlines['Points']
        
                cellData = centrelines_dict['CellData'] = dict()
                cellData['CellPointIds'] = numpyCenterlines['CellData']['CellPointIds']
                pointData = centrelines_dict['PointData'] = dict()
                pointData['EdgeArray'] = numpyCenterlines['PointData']['EdgeArray']
                pointData['EdgePCoordArray'] = numpyCenterlines['PointData']['EdgePCoordArray']
                pointData['MaximumInscribedSphereRadius'] = numpyCenterlines['PointData']['MaximumInscribedSphereRadius']
        
                with open(dir_npcl, "w") as write_file:
                    json.dump(centrelines_dict, write_file, cls=NumpyArrayEncoder)
                    print('>> Dictionary saved correctly!\n> File: '+ dir_npcl.name);
                    alert('countdown')
                    
                proc_set = ['wf_info', 'MeshesProc', 'C-Centreline', ch, cont]
                organ.update_settings(process = proc_set+['vmtktxt'], update = vmtktxt, mH='mH')
            
                # Update organ workflow
                proc_wft = ['MeshesProc', 'C-Centreline', 'vmtk_CL', ch, cont, 'Status']
                organ.update_workflow(process = proc_wft, update = 'DONE')
                
            # Update organ workflow
            organ.update_workflow(process = process, update = 'DONE')
            organ.check_status(process='MeshesProc')
            organ.save_organ()
                 
        # --------
        # ArrayDict
        #     ['Points']                   <-- required, is Nx3 array of N vertexes and x, y, z locations
        #     ['PointData']                <-- required, even if subarrays are empty
        #         ['PointDataArray1']      <-- optional, (ex. MaximumInscribedSphereRadius)
        #         ['PointDataArray2']      <-- optional
        #         ...
        #     ['CellData']                 <-- required
        #         ['CellPointIds']         <-- required, list of Mx1 arrays defining cell connectivity to ['Points']
        #         ['CellDataArray1']       <-- optional, (ex: CenterlineTractId)
        #         ['CellDataArray2']       <-- optional
        #            ...

#%% func- code_vmtk
def code_vmtk(organ, ch, cont, voronoi=False):
    """
    Function that gets directories information and prints a series of instructions to process the meshes to obtain centreline and
    run the vmtk code.

    """

    dir_cl = organ.info['dirs']['centreline']
    dir_meshML = organ.mH_settings['wf_info']['MeshesProc']['C-Centreline'][ch][cont]['dir_meshLabMesh']
    dir_npcl = dir_meshML.name.replace('_cut4clML.stl', '_npcl.json')
    dir_npcl = dir_cl / dir_npcl
    
    while not dir_meshML.is_file():
        q = 'No meshes are recognised in the path: \n'+ str(dir_meshML) +'.\nMake sure you have named your cleaned meshes correctly after running the processing in Meshlab and press -Enter- when ready.'
        res = {0:'Please remind me what I need to do', 1:'I have done it now, please continue'}
        print_ins = ask4input(q, res, int)
        if print_ins == 0:
            print("\nTo get the centreline of each of the selected meshes follow the next steps:")
            print("> 1. Open the stl file(s) in Meshlab")
            print("> 2. Run Filters > Remeshing, Simplification.. > Screened Poisson Surf Reco (check Pre-clean)")
            print("> 3. Cut inflow and outflow tract as close as the cuts from the original mesh you opened in \n\t Meshlab and export the resulting surface adding 'ML' at the end of the filename\n\t (e.g _cut4clML.stl) in the same folder")
            print("> 4. Come back and continue processing!...")
    
    dir_meshML_str = str(dir_meshML).replace('\\','/')
    dir_meshML_strF = '"'+dir_meshML_str+'"'
    
    vtp_name = dir_meshML.name.replace('_cut4clML.stl', '_cl.vtp')
    dir_vtp = dir_cl / vtp_name
    dir_vtp_str = str(dir_vtp).replace('\\','/')
    dir_vtp_strF = '"'+dir_vtp_str+'"'
    
    # General code
    # vmtktxt = "vmtksurfacereader -ifile "+ dir_meshML_strF +" --pipe vmtksurfacesmoothing -passband 0.1 -iterations 30 --pipe vmtkcenterlines -seedselector openprofiles -ofile " + dir_vtp_strF + " --pipe vmtkrenderer --pipe vmtksurfaceviewer -opacity 0.25 --pipe vmtksurfaceviewer -i @vmtkcenterlines.o -array MaximumInscribedSphereRadius"
    # code for voronoi diagrams
    # vmtktxt = "vmtksurfacereader -ifile "+ dir_meshML_strF +" --pipe vmtksurfacesmoothing -passband 0.1 -iterations 30 --pipe vmtkcenterlines -seedselector openprofiles -ofile " + dir_vtp_strF + " --pipe vmtkrenderer --pipe vmtksurfaceviewer -opacity 0.25 --pipe vmtksurfaceviewer -i @vmtkcenterlines.voronoidiagram -array MaximumInscribedSphereRadius -i @vmtkcenterlines.o -array MaximumInscribedSphereRadius"

    vmtk_txt1_reader = "vmtksurfacereader -ifile "+ dir_meshML_strF+" "
    vmtk_txt2_smooth = "--pipe vmtksurfacesmoothing -passband 0.1 -iterations 30 "
    vmtk_txt3_cl = "--pipe vmtkcenterlines -seedselector openprofiles -ofile "+ dir_vtp_strF + " "
    if voronoi: 
        vmtk_txt4_viewer = "--pipe vmtkrenderer --pipe vmtksurfaceviewer -opacity 0.25 --pipe vmtksurfaceviewer -i @vmtkcenterlines.voronoidiagram -array MaximumInscribedSphereRadius -i @vmtkcenterlines.o -array MaximumInscribedSphereRadius"
    else: 
        vmtk_txt4_viewer = "--pipe vmtkrenderer --pipe vmtksurfaceviewer -opacity 0.25 --pipe vmtksurfaceviewer -i @vmtkcenterlines.o -array MaximumInscribedSphereRadius"
    vmtk_txtF = vmtk_txt1_reader + vmtk_txt2_smooth + vmtk_txt3_cl + vmtk_txt4_viewer

    return vmtk_txtF, dir_npcl

#%% func - load_vmtkCL
def load_vmtkCL(organ, ch, cont):
    
    dir_cl = organ.info['dirs']['centreline']
    dir_meshML = organ.mH_settings['wf_info']['MeshesProc']['C-Centreline'][ch][cont]['dir_meshLabMesh']
    dir_npclo = dir_meshML.name.replace('_cut4clML.stl', '_npcl.json')
    dir_npcl = dir_cl / dir_npclo
    
    json2open_dir = dir_npcl
    #print("Started Reading JSON file")
    with open(json2open_dir, "r") as read_file:
        print("\t>> "+dir_npclo+": Converting JSON encoded data into Numpy Array")
        decodedArray = json.load(read_file)

    return decodedArray
    
#%% func - create_CLs
def create_CLs(organ, nPoints = 300):
    """
    Function that creates the centrelines using the points given as input in the dict_cl

    """
    #Check first if extracting centrelines is a process involved in this organ/project
    if organ.check_method(method = 'C-Centreline'): 
    # if 'C-Centreline' in organ.parent_project.mH_methods: 
        #Check workflow status
        workflow = organ.workflow
        process = ['MeshesProc','C-Centreline','buildCL','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE': 
            q = 'You already extracted the centreline of the selected meshes. Do you want to extract the centreline again?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run this process!'}
            buildCL = ask4input(q, res, bool)
        else: 
            buildCL = True
    
    if buildCL: 
        cl_colors = {'Op1':'navy','Op2':'blueviolet','Op3':'deeppink',
                     'Op4': 'orangered','Op5':'slategray', 'Op6':'maroon'}
        cl_names = [item for item in organ.parent_project.mH_param2meas if 'centreline' in item]
        for name in cl_names: 
            ch = name[0]; cont = name[1]
            cl_data = load_vmtkCL(organ, ch, cont)
            #Get cl points from vmtk
            pts_cl = np.asarray(cl_data['Points'])
            # Interpolate points of original centreline
            pts_int_o = get_interpolated_pts(points=pts_cl, nPoints = nPoints)
            # Last CL point
            pt_m1 = pts_int_o[-1]
            sph_m1 = vedo.Sphere(pos = pt_m1, r=4, c='black')
            # Create kspline with original points
            kspl_o = vedo.KSpline(pts_int_o, res = nPoints).color('gold').legend('CLo_'+ch+'_'+cont).lw(5)
            # Create IFT and OFT spheres to show original points position
            sph_inf_o = vedo.Sphere(pts_int_o[-1], r = 3, c='tomato')
            sph_outf_o = vedo.Sphere(pts_int_o[0], r = 3, c='navy')
            
            # Get outflow point for that layer
            pt2add_outf = organ.objects['Spheres']['cut4cl']['top'][ch+'_'+cont]['center']
            pts_withOutf = np.insert(pts_cl, 0, np.transpose(pt2add_outf), axis=0)
            
            #Dictionary with kspl options
            dict_clOpt = {}
            #Get planes that cut meshes4cl
            plane_info = organ.mH_settings['wf_info']['MeshesProc']['C-Centreline']['Planes']['bottom']
            
            # Get inflow point for that layer (four options)
            # - Option 1, use centroids of kspline cuts
            pt2add_inf = organ.objects['Spheres']['cut4cl']['bottom'][ch+'_'+cont]['center']
            pts_all_opt1 = np.insert(pts_withOutf, len(pts_withOutf), np.transpose(pt2add_inf), axis=0)

            # Interpolate points
            pts_int_opt1 = get_interpolated_pts(points=pts_all_opt1, nPoints = nPoints)
            # Create kspline with points
            kspl_opt1 = vedo.KSpline(pts_int_opt1, res = nPoints)
            kspl_opt1.color(cl_colors['Op1']).legend('(Op1) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 1'] = {'kspl': kspl_opt1, 'sph_bot': sph_outf_o, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add_inf, 
                                      'description': 'Point in meshesCut4Cl'}

            # - Option 2 (add point of extended original centreline)
            num = -10
            pts_int_opt2, pt2add2, sph_m2 = extend_CL(pts_int_o, pts_withOutf, num, nPoints, plane_info)
            kspl_opt2 = vedo.KSpline(pts_int_opt2, res = nPoints)
            kspl_opt2.color(cl_colors['Op2']).legend('(Op2) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 2'] = {'kspl': kspl_opt2, 'sph_bot': sph_m2, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add2, 
                                      'description': 'Unit vector extension (-1,'+str(num)+')'}
            
            # - Option 3 (add point of extended original centreline midline between chamber centre and in/outf tract)
            num = -25
            pts_int_opt3, pt2add3, sph_m3 = extend_CL(pts_int_o, pts_withOutf, num, nPoints, plane_info)
            kspl_opt3 = vedo.KSpline(pts_int_opt3, res = nPoints)
            kspl_opt3.color(cl_colors['Op3']).legend('(Op3) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 3'] = {'kspl': kspl_opt3, 'sph_bot': sph_m3, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add3, 
                                      'description': 'Unit vector extension (-1,'+str(num)+')'}
            
            # - Option 4 (add point of extended original centreline midline between chamber centre and in/outf tract)
            num = -50
            pts_int_opt4, pt2add4, sph_m4 = extend_CL(pts_int_o, pts_withOutf, num, nPoints, plane_info)
            kspl_opt4 = vedo.KSpline(pts_int_opt4, res = nPoints)
            kspl_opt4.color(cl_colors['Op4']).legend('(Op4) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 4'] = {'kspl': kspl_opt4, 'sph_bot': sph_m4, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add4,
                                      'description': 'Unit vector extension (-1,'+str(num)+')'}
            
            # - Option 5 (add point of extended original centreline midline between chamber centre and in/outf tract)
            num = -60
            pts_int_opt5, pt2add5, sph_m5 = extend_CL(pts_int_o, pts_withOutf, num, nPoints, plane_info)
            kspl_opt5 = vedo.KSpline(pts_int_opt5, res = nPoints)
            kspl_opt5.color(cl_colors['Op5']).legend('(Op5) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 5'] = {'kspl': kspl_opt5, 'sph_bot': sph_m5, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add5,
                                      'description': 'Unit vector extension (-1,'+str(num)+')'}
            
            # - Option 6 (add mid point between final point of original centreline and inf tract)
            pt_m6 = pt_m1+(pt2add_inf-pt_m1)/2
            sph_m6 = vedo.Sphere(pos = pt_m6, r=4, c='gold')

            pts_all_opt6 = np.insert(pts_withOutf, len(pts_withOutf), np.transpose(pt_m6), axis=0)
            pts_all_opt6f = np.insert(pts_all_opt6, len(pts_all_opt6), np.transpose(pt2add_inf), axis=0)

            # Interpolate points
            pts_int_opt6 = get_interpolated_pts(points=pts_all_opt6f, nPoints = nPoints)
            # Create kspline with points
            kspl_opt6 = vedo.KSpline(pts_int_opt6, res = nPoints)
            kspl_opt6.color(cl_colors['Op6']).legend('(Op6) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 6'] = {'kspl': kspl_opt6, 'sph_bot': sph_m6, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add_inf,
                                      'description': 'Center point between last and meshesCut4Cl'}
            
            obj = []; txt = []
            mesh = organ.obj_meshes[ch+'_'+cont].mesh.clone()
            for num, opt in enumerate(dict_clOpt.keys()):
                obj2add = (mesh.alpha(0.01), sph_m1, kspl_o, dict_clOpt[opt]['kspl'], dict_clOpt[opt]['sph_bot'], dict_clOpt[opt]['sph_top'])
                obj.append(obj2add)
                if num == 0: 
                    txt.append((num, organ.user_organName +' - '+opt))
                else: 
                    txt.append((num, opt))
            
            plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
            
            q_select = 'Select the preferred centreline for processing this heart'
            res_select = {1: 'Option 1', 2: 'Option 2', 3: 'Option 3', 4: 'Option 4', 5:'Option 5', 6:'Option 6'}
            opt_selected = ask4input(q_select, res_select, int)
            cl_selected = res_select[opt_selected]
            proc_set = ['wf_info','MeshesProc','C-Centreline',ch,cont,'connect_cl']
            update = cl_selected +'-'+dict_clOpt[res_select[opt_selected]]['description']
            organ.update_settings(process = proc_set, update = update, mH='mH')
            
            #Add centreline to organ
            cl_final = dict_clOpt[cl_selected]['kspl']
            organ.add_object(cl_final, proc='Centreline', class_name=ch+'_'+cont, name='KSpline')
            organ.obj_meshes[ch+'_'+cont].set_centreline()
            
            # Plot final centreline
            cl_final = organ.obj_meshes[ch+'_'+cont].get_centreline(nPoints=nPoints)
            obj_final = [(mesh.alpha(0.01), cl_final)]
            txt_final = [(0, organ.user_organName +' - Final Centreline')]
            plot_grid(obj=obj_final, txt=txt_final, axes=5, sc_side=max(organ.get_maj_bounds()))
            
            # Update organ workflow
            proc_wft = ['MeshesProc', 'C-Centreline', 'buildCL', ch, cont, 'Status']
            organ.update_workflow(process = proc_wft, update = 'DONE')
            
        # Update organ workflow
        organ.update_workflow(process = process, update = 'DONE')
        organ.update_workflow(process = ['MeshesProc','C-Centreline','Status'], update = 'DONE')
        organ.check_status(process='MeshesProc')
        organ.save_organ()     

#%% func - extend_CL
def extend_CL(pts_int_o, pts_withOutf, num, nPoints, plane_info):
    
    pt_m10 = pts_int_o[-num]
    sph_m10 = vedo.Sphere(pos = pt_m10, r=4, c='lime')
    pt_m1 = pts_int_o[-1]
    # sph_m1 = vedo.Sphere(pos = pt_m1, r=4, c='tomato')
    dir_v = unit_vector(pt_m1-pt_m10)*3
    pts_ext = np.array([pt_m10, pt_m1, pt_m1+dir_v*2,pt_m1+dir_v*4,pt_m1+dir_v*6,pt_m1+dir_v*8,pt_m1+dir_v*10])
    xd = np.diff(pts_ext[:,0])
    yd = np.diff(pts_ext[:,1])
    zd = np.diff(pts_ext[:,2])
    dist = np.sqrt(xd**2+yd**2+zd**2)
    u = np.cumsum(dist)
    u = np.hstack([[0],u])
    t = np.linspace(0, u[-1],nPoints)
    resamp_pts = interpn((u,), pts_ext, t)
    kspl_resamp = vedo.KSpline(resamp_pts, res = nPoints).lw(5)
    
    #Get plane
    pl_centre_bot = plane_info['pl_centre']
    pl_normal_bot = plane_info['pl_normal']
    pl_IFT = vedo.Plane(pos = pl_centre_bot, normal = pl_normal_bot)
    
    #Cut KSpline
    kspl_test = kspl_resamp.clone().cutWithMesh(pl_IFT, invert = True)
    pt2add = kspl_test.points()[-1]
    
    #Insert last point into the original CL
    pts_all_opt = np.insert(pts_withOutf, len(pts_withOutf), np.transpose(pt2add), axis=0)

    # Interpolate points
    pts_int_opt = get_interpolated_pts(points=pts_all_opt, nPoints = nPoints)
    
    return pts_int_opt, pt2add, sph_m10

#%% func - extract_ballooning
def extract_ballooning(organ, color_map, plot=False):

    #Check first if extracting centrelines is a process involved in this organ/project
    if organ.check_method(method = 'D-Ballooning'): 
    # if 'D-Ballooning' in organ.parent_project.mH_methods: 
        #Check workflow status
        workflow = organ.workflow
        process = ['MeshesProc','D-Ballooning','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE': 
            q = 'You already extracted the ballooning parameters of the selected meshes. Do you want to extract them again?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run this process!'}
            balloon = ask4input(q, res, bool)
        else: 
            balloon = True
    else:
        balloon = False
        return None
    
    if balloon: 
        proc_done = []
        ball_names = [item for item in organ.parent_project.mH_param2meas if 'ballooning' in item]
        for name in ball_names: 
            ch = name[0]; cont = name[1]
            mesh2ball = organ.obj_meshes[ch+'_'+cont]
            print('\n>> Extracting ballooning information for '+mesh2ball.legend+'... \nNOTE: it takes about 10-15 to process each mesh... just be patient :) ')
            from_cl = organ.mH_settings['wf_info']['MeshesProc']['D-Ballooning'][ch][cont]['from_cl']
            from_cl_type = organ.mH_settings['wf_info']['MeshesProc']['D-Ballooning'][ch][cont]['from_cl_type']
            cl4ball = organ.obj_meshes[from_cl+'_'+from_cl_type].get_centreline()
            sph4ball = sphs_in_spline(kspl=cl4ball,every=0.6)
            sph4ball.legend('sphs_ball').alpha(0.1)
            
            mesh_ball, distance, min_max = get_distance_to(mesh_to=mesh2ball, 
                                                        mesh_from = sph4ball, 
                                                        from_name='CL('+from_cl+'_'+from_cl_type+')', 
                                                        color_map=color_map)
            mesh_ball.alpha(1)
            #Add min-max values to mH_settings
            proc_range = ['measure', ch, cont,'whole','ballooning', 'range']
            upd_range = {'min_val': min_max[0], 'max_val': min_max[1]}
            organ.update_settings(proc_range, update = upd_range, mH = 'mH')
            
            #Add mesh_ball to the mesh_meas attribute
            m_type = 'ballCL('+from_cl+'_'+from_cl_type+')'
            
            mesh2ball.mesh_meas[m_type] = mesh_ball
            mesh2ball.save_mesh(m_type=m_type)
            mesh2ball.save_array(array=distance, m_type=m_type)
            
            if plot: 
                obj = [(mesh2ball.mesh, cl4ball, sph4ball), (mesh_ball, cl4ball, sph4ball)]
                txt = [(0, organ.user_organName +' - Ballooning Setup')]
                plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
            
            proc_wft = ['MeshesProc','D-Ballooning',ch, cont, 'Status']
            organ.update_workflow(process = proc_wft, update = 'DONE')
            proc_done.append('DONE')
        
        if len(proc_done) == len(ball_names):
            organ.update_workflow(process = process, update = 'DONE')
    
    else:
        return None

#%% func - extract_thickness
def extract_thickness(organ, color_map, plot=False):
    
    thck_values = {'int>ext': {'method': 'D-Thickness_int>ext', 
                                    'param': 'thickness int>ext'},
                   'ext>int': {'method': 'D-Thickness_ext>int', 
                                  'param': 'thickness ext>int'}}
                        
    for n_type in thck_values.keys(): 
        # print(thck_values[n_type])
        method = thck_values[n_type]['method']
        if organ.check_method(method = method): 
            #Check workflow status
            workflow = organ.workflow
            process = ['MeshesProc', method,'Status']
            check_proc = get_by_path(workflow, process)
            if check_proc == 'DONE': 
                q = 'You already extracted the thickness ('+n_type+') parameters of the selected meshes. Do you want to extract them again?'
                res = {0: 'no, continue with next step', 1: 'yes, re-run this process!'}
                thickness = ask4input(q, res, bool)
            else: 
                thickness = True
        else:
            thickness = False
            return None
        
        if thickness: 
            print('>> Extracting thickness for:', method)
            # print(n_type, thck_values[n_type])
            res = get_thickness(organ, n_type, thck_values[n_type], color_map, plot)
            if res: 
                organ.update_workflow(process = process, update = 'DONE')
            
    
#%% func - get_thickness
def get_thickness(organ, n_type, thck_dict, color_map, plot=False):
    
    thck_names = [item for item in organ.parent_project.mH_param2meas if thck_dict['param'] in item]
    # print(thck_names)
    proc_done = []
    for name in thck_names: 
        ch = name[0]; cont = name[1]
        mesh_tiss = organ.obj_meshes[ch+'_tiss']
        if n_type == 'int>ext': 
            mesh_to = organ.obj_meshes[ch+'_ext']
            mesh_from = organ.obj_meshes[ch+'_int'].mesh
        elif n_type == 'ext>int': 
            mesh_to = organ.obj_meshes[ch+'_int']
            mesh_from = organ.obj_meshes[ch+'_ext'].mesh
        # mesh_to = 
        print('\n>> Extracting thickness information for '+mesh_tiss.legend+'... \nNOTE: it takes about 5min to process each mesh... just be patient :) ')
        
        mesh_thck, distance, min_max = get_distance_to(mesh_to=mesh_to, mesh_from=mesh_from, 
                                                    from_name=n_type, color_map=color_map)
        mesh_thck.alpha(1)
        # Add mesh_ball to the mesh_meas attribute
        n_type_new = n_type.replace('>','TO')
        m_type = 'thck('+n_type_new+')'
        proc_range = ['measure', ch, 'tiss','whole', thck_dict['param']]
        upd_range = {'range':{'min_val': min_max[0], 'max_val': min_max[1]}}
        organ.update_settings(proc_range, update = upd_range, mH = 'mH')
        
        if not hasattr(mesh_from, 'mesh_meas'):
            mesh_tiss.mesh_meas = {}
        mesh_tiss.mesh_meas[m_type] = mesh_thck
        mesh_tiss.save_mesh(m_type=m_type)
        mesh_tiss.save_array(array=distance, m_type=m_type)
        
        if plot: 
            obj = [(mesh_from, mesh_to.mesh), (mesh_tiss.mesh), (mesh_thck)]
            txt = [(0, organ.user_organName +' - Thickness Setup')]
            plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
        
        proc_wft = ['MeshesProc', thck_dict['method'], ch, cont, 'Status']
        organ.update_workflow(process = proc_wft, update = 'DONE')
        proc_done.append('DONE')

    if len(proc_done) == len(thck_names):
        return True
    else: 
        return False

#%% func - get_distance_to
def get_distance_to(mesh_to, mesh_from, from_name, color_map='turbo'):
    """
    Function that gets the distance between m_ext and m_int and color codes m_ext accordingly
    mesh_from = cl/int
    mesh_to = ext - the one that has the colors
    """
    if isinstance(mesh_from,vedo.shapes.Spheres): 
        name = 'Ballooning'
        multip = 1
        mesh_name = mesh_to.legend
        suffix = '_Ballooning'
        title = mesh_name+'\n'+name+' [um]\n'+from_name
    else: 
        name = 'Thickness'
        if from_name == 'int>ext':
            multip = -1
        else: 
            multip = 1
        mesh_name = mesh_to.legend.split('_')
        if len(mesh_name)>2:
            mesh_name = mesh_to.legend.replace('_'+mesh_name[-1],'')
        else: 
            mesh_name = mesh_name[0]
        suffix = '_Thickness'
        title = mesh_name+'\n'+name+' [um]\n('+from_name+')'
    
    tic = perf_counter()
    print('> Start time: \t', str(datetime.now())[11:-7])
    mesh_toB = mesh_to.mesh.clone()
    # print(type(mesh_toB))

    mesh_toB.distance_to(mesh_from, signed=True)
    toc = perf_counter()
    time = toc-tic
    print('> End time: \t', str(datetime.now())[11:-7])
    print("\t>> Total time taken to get "+name+" = ", format(time/60,'.2f'), "min")
    distance = multip*mesh_toB.pointdata['Distance']
    mesh_toB.pointdata['Distance'] = distance
    vmin, vmax = np.min(distance),np.max(distance)
    min_max = (vmin, vmax)
    print('> vmax:', format(vmax,'.2f'), 'vmin:', format(vmin,'.2f'))
    alert('jump')
    
    mesh_toB.cmap(color_map)
    mesh_toB.add_scalarbar(title=title, pos=(0.8, 0.05))
    mesh_toB.mapper().SetScalarRange(vmin,vmax)
    mesh_toB.legend(mesh_name+suffix)
    
    return mesh_toB, distance, min_max
    
#%% func - get_organ_ribbon
def get_organ_ribbon(organ, nRes, nPoints, clRib_type): 
    
    #Check if the orientation has alredy been stablished
    if 'orientation' in organ.mH_settings.keys(): 
        if 'cl_ribbon' in organ.mH_settings['orientation'].keys():
            q = 'You already created the centreline ribbon to cut tissues into sections. Do you want to create it again?'
            res = {0: 'no, continue with next step', 1: 'yes, re-create it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
    else: 
        proceed = True
            
    if proceed: 
        q = 'Select the coordinate-axes you would like to use to define the plane in which the centreline will be extended to cut organ into sections:'
        res = {0: 'Stack Coordinate Axes', 
               1: 'ROI (Organ) Specific Coordinate Axes', 
               2: 'Other'}
        opt = ask4input(q, res, int)
        
        if opt in [0,1]: 
            if opt == 0:
                axes = res[opt].split(' ')[0].lower(); print(axes)
            else: 
                axes = res[opt].split(' ')[0].upper(); print(axes)
            coord_ax = organ.mH_settings['orientation'][axes]
            views = {}
            for n, view in enumerate(list(coord_ax['planar_views'].keys())):
                views[n] = view
            q2 = 'From the -'+res[opt]+'- select the plane you want to use to extend the centreline: '
            opt2 = ask4input(q2, views, int)
            
            plane_normal = coord_ax['planar_views'][views[opt2]]['pl_normal']
            
            #% Mesh centreline
            # Select the centreline you want to use to cut organ into sides
            dict_cl = plot_organCLs(organ)
            q = 'Select the centreline you want to use to cut organ into sections:'
            select = ask4input(q, dict_cl, int)
            
            ch_cont_cl = dict_cl[select].split(' (')[1].split('-')
            ch = ch_cont_cl[0]
            cont = ch_cont_cl[1]
            mesh_cl = organ.obj_meshes[ch+'_'+cont]
            
            cl_ribb_dict = {'coord_ax': res[opt].split(' ')[0],
                            'planar_view': views[opt2],
                            'mesh_cl': ch+'_'+cont,
                            'pl_normal': plane_normal,
                            'nRes': nRes,
                            'nPoints': nPoints, 
                            'cl_type': clRib_type}
            
            proc = ['orientation', 'cl_ribbon']
            organ.update_settings(proc, update = cl_ribb_dict, mH = 'mH')
            
            cl_ribbon = mesh_cl.get_clRibbon(nPoints=nPoints, nRes=nRes, 
                                  pl_normal=plane_normal, 
                                  clRib_type=clRib_type)
            
            obj = [(mesh_cl.mesh, cl_ribbon)]
            txt = [(0, organ.user_organName+'- Extended Centreline Ribbon to cut organ into sections')]
            plot_grid(obj=obj, txt=txt, axes=8, sc_side=max(organ.get_maj_bounds()))
            
        else: 
            print('Opt2: Code under development!')
            
            # sect_names = [item for item in organ.parent_project.mH_param2meas if 'sect1' in item]
            # ext_ch, _ = organ.get_ext_int_chs()
            # if any(ext_ch.channel_no in flag for (flag,_,_,_) in sect_names):
            #     mesh_ext = organ.obj_meshes[ext_ch.channel_no+'tiss']
            # else: 
            #     mesh_ext = organ.obj_meshes[sect_names[0][0]+'_'+sect_names[0][1]]
           
            # pos = mesh_ext.mesh.center_of_mass()
            # sph = vedo.Sphere(pos=pos,r=2,c='black')
            # side = max(organ.get_maj_bounds())
            
            # color_o = [90,156,254,255]
            # orient_cube = vedo.Cube(pos=pos, side=side, c=color_o[:-1])
            # orient_cube.linewidth(1).force_opaque()
            
            # plane = organ.mH_settings['organ_orientation']['organ_specific']['plane']
            # if rotate: 
            #     pos_rot = new_normal_3DRot(pos, [angle], [0], [0])
            #     sph_rot = vedo.Sphere(pos=pos_rot,r=2,c='tomato')
            #     if plane=='XY':
            #         orient_cube.rotate_z(angle, rad=False)
            #         sph.rotate_z(angle, rad=False)
            #     elif plane=='YZ':
            #         orient_cube.rotate_x(angle, rad=False)
            #         sph.rotate_x(angle, rad=False)
            #     elif plane=='XZ':
            #         orient_cube.rotate_y(angle, rad=False)
            #         sph.rotate_y(angle, rad=False)
            
            # if rotateY: 
            #     orient_cube.rotate_y(cust_angle, rad=False)
            #     sph.rotate_z(cust_angle, rad=False)
            
            # pos = mesh_ext.mesh.center_of_mass()
            # orient_cube.pos(pos)
            # sph_COM = vedo.Sphere(pos=pos,r=5,c='gold')
            
            # #% Mesh centreline
            # # Select the centreline you want to use to cut organ into sides
            # dict_cl = plot_organCLs(organ)
            # q = 'Select the centreline you want to use to cut organ into sections:'
            # select = ask4input(q, dict_cl, int)
            
            # ch_cont_cl = dict_cl[select].split(' (')[1].split('-')
            # ch = ch_cont_cl[0]
            # cont = ch_cont_cl[1]
            # mesh_cl = organ.obj_meshes[ch+'_'+cont]
        
            # orient_cube_clear = orient_cube.clone().alpha(0.5)
            
            # def select_cube_face(evt):
            #     color_selected = [255,0,0,200]
                
            #     orient_cube = evt.actor
            #     if not orient_cube:
            #         return
            #     pt = evt.picked3d
            #     idcell = orient_cube.closest_point(pt, return_cell_id=True)
            #     print('You clicked (idcell):', idcell)
            #     if set(orient_cube.cellcolors[idcell]) == set(color_o):
            #         orient_cube.cellcolors[idcell] = color_selected #RGBA 
            #         for cell_no in range(len(orient_cube.cells())):
            #             # print(cell_no)
            #             if cell_no != idcell: 
            #                 orient_cube.cellcolors[cell_no] = color_o #RGBA 
                            
            #     elif set(orient_cube.cellcolors[idcell]) == set(color_selected):
            #         orient_cube.cellcolors[idcell] = color_o #RGBA 
            #         for cell_no in range(len(orient_cube.cells())):
            #             # print(cell_no)
            #             if cell_no != idcell: 
            #                 orient_cube.cellcolors[cell_no] = color_selected #RGBA 
                            
            #     cells = orient_cube.cells()[idcell]
            #     points = [orient_cube.points()[cell] for cell in cells]
                
            #     plane_fit = vedo.fit_plane(points, signed=True)
            #     # print('normal:',plane_fit.normal, 'center:',plane_fit.center)
            #     organ.mH_settings['orientation']['cl_ribbon'] = {'mesh_cl': ch+'_'+cont,
            #                                                         'pl_normal': plane_fit.normal,
            #                                                         'nRes': nRes,
            #                                                         'nPoints': nPoints, 
            #                                                         'cl_type': clRib_type}
         
            # txt0 = vedo.Text2D(organ.user_organName+' - Reference cube and mesh.', c=txt_color, font=txt_font, s=txt_size)
            # txt1 = vedo.Text2D('Select (click) cube face you want to use to extended centreline.\nNote: The face that is last selected will be used', c=txt_color, font=txt_font, s=txt_size)
            # vpt = vedo.Plotter(N=2, axes=1)
            # vpt.add_callback("mouse click", select_cube_face)
            # vpt.show(mesh_ext.mesh, orient_cube_clear, txt0, at=0)
            # vpt.show(orient_cube, txt1, at=1, azimuth=45, interactive=True)
            
            # pl_normal = organ.mH_settings['organ_orientation']['organ_specific']['cl_ribbon']['pl_normal']
            # cl_ribbon = mesh_cl.get_clRibbon(nPoints=nPoints, nRes=nRes, 
            #                       pl_normal=pl_normal, 
            #                       clRib_type=clRib_type)
            
            # txt0 = vedo.Text2D('Final selected face', c=txt_color, font=txt_font, s=txt_size)
            # txt1 = vedo.Text2D('Extended Centreline Ribbon to cut organ into sides', c=txt_color, font=txt_font, s=txt_size)
            # vp = vedo.Plotter(N=2,axes=8)
            # vp.show(mesh_ext.mesh, orient_cube_clear, sph, sph_rot, sph_COM, txt0, at=0)
            # vp.show(mesh_cl.mesh, cl_ribbon, txt1, at=1, interactive=True)
    
#%% func - get_sect_mask
def get_sect_mask(organ, plotshow=True):
    
    if organ.check_method(method = 'E-Sections'): 
        name_sections = organ.mH_settings['general_info']['sections']['name_sections']
        user_names = '('+', '.join([name_sections[val] for val in name_sections])+')'
      
        #Check if there ir already a created mask
        name2save = organ.user_organName + '_mask_sect.npy'
        mask_file = organ.info['dirs']['s3_numpy'] / name2save
        
        if mask_file.is_file(): 
            q = 'You already created the mask to cut tissues into sections '+user_names+'. Do you want to create it again?'
            res = {0: 'no, continue with next step', 1: 'yes, re-create it!'}
            proceed = ask4input(q, res, bool)
    
        else: 
            proceed = True
                
        if proceed: 
            cl_settings =  organ.mH_settings['orientation']['cl_ribbon']
            mesh_cl = organ.obj_meshes[cl_settings['mesh_cl']]
            
            s3_filledCube, test_rib = get_stack_clRibbon(organ, mesh_cl, plotshow)
            get_cube_clRibbon(organ, mesh_cl, s3_filledCube, test_rib, plotshow)
    
#%% func - get_stack_clRibbon
def get_stack_clRibbon(organ, mesh_cl, plotshow=True):
    
    cl_settings =  organ.mH_settings['orientation']['cl_ribbon']
    cl_ribbon =  mesh_cl.get_clRibbon(nPoints=cl_settings['nPoints'], 
                                      nRes=cl_settings['nRes'], 
                                      pl_normal=cl_settings['pl_normal'], 
                                      clRib_type=cl_settings['cl_type'])
    
    res = mesh_cl.resolution
    cl_ribbonR = cl_ribbon.clone().x(res[0])
    cl_ribbonF = cl_ribbon.clone().y(res[1])
    cl_ribbonT = cl_ribbon.clone().z(res[1])
    cl_ribbonS = [cl_ribbon, cl_ribbonR, cl_ribbonF, cl_ribbonT]

    #Load stack shape
    shape_s3 = organ.info['shape_s3']
    zdim, xdim, ydim = shape_s3
    # print('shape_s3:',shape_s3, '- xdim:', xdim, '- ydim:',ydim, '- zdim:', zdim)

    # Rotate the points that make up the cl_ribbon, to convert them to a stack
    cust_angle = organ.info['custom_angle']
    
    if organ.mH_settings['general_info']['rotateZ_90']: #'CJ' not in filename: 
        axis = [0,0,1]
        theta = np.radians(90)
    else: 
        axis = [0,0,0]
        theta = np.radians(0)
    
    print('axis:',axis, '- theta:',theta)
    if cust_angle != 0: 
        print('cust_angle != 0, develop this!')

    s3_rib = np.zeros((xdim, ydim, zdim+2))
    s3_filledCube = np.zeros((xdim, ydim, zdim+2))
    s3_filledCube[1:xdim-1,1:ydim-1,1:zdim+1] = 1

    # Rotate the points in all ribbons and fit into stack size 
    for cl_rib in cl_ribbonS:
        rib_pts = cl_rib.points()
        rib_points_rot = np.zeros_like(rib_pts)
        for i, pt in enumerate(rib_pts):
            rib_points_rot[i] = (np.dot(rotation_matrix(axis = axis, theta = theta),pt))
        rib_pix = np.transpose(np.asarray([rib_points_rot[:,i]//res[i] for i in range(len(res))]))
        rib_pix = rib_pix.astype(int)
        rib_pix = np.unique(rib_pix, axis=0)

        rib_pix_out = rib_pix.copy()
        index_out = []
        # Clean rib_pix if out of stack shape
        for index, pt in enumerate(rib_pix):
            if pt[0] > xdim-2 or pt[0] < 0:
                delete = True
            elif pt[1] > ydim-2 or pt[1] < 0:
                delete = True
            elif pt[2] > zdim+2-1 or pt[2] < 0:
                delete = True
            else: 
                delete = False
            
            if delete:
                index_out.append(index)

        rib_pix_out = np.delete(rib_pix_out, index_out, axis = 0)
        # Create mask of cl_ribbon
        s3_rib[rib_pix_out[:,0],rib_pix_out[:,1],rib_pix_out[:,2]] = 1
        # Create filled cube just to one side of cl
        s3_filledCube[rib_pix_out[:,0],rib_pix_out[:,1],rib_pix_out[:,2]] = 0
        alert('clown')
        
    # Create volume of extended centreline mask
    test_rib = s3_to_mesh(s3_rib, res=res, name='Extended CL', color='darkmagenta')
    
    if plotshow: 
        obj = [(test_rib, mesh_cl.mesh)]
        txt = [(0, organ.user_organName)]
        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
        
    return s3_filledCube, test_rib

#%% func - get_cube_clRibbon
def get_cube_clRibbon(organ, mesh_cl, s3_filledCube, test_rib, plotshow=True):
    
    cl_settings =  organ.mH_settings['orientation']['cl_ribbon']
    res = mesh_cl.resolution

    # #Load stack shape
    shape_s3 = organ.info['shape_s3']
    zdim, xdim, ydim = shape_s3
      
    #Identify the direction in which the cubes need to be built
    pl_normal = cl_settings['pl_normal']
    ref_vect = organ.mH_settings['orientation']['ROI']['ref_vectF'][0]
    ext_dir = list(np.cross(ref_vect, pl_normal))
    max_ext_dir = max(ext_dir)
    coord_dir = ext_dir.index(max_ext_dir)
    print('pl_normal:', pl_normal, '\nref_vect:', ref_vect, '\next_dir:', ext_dir, '\ncoord_dir:', coord_dir)
    
    if coord_dir == 0: 
        print('Extending cube in the x? direction')
        for xpos in range(0,xdim):
            for zpos in range(0,zdim+2): 
                yline = s3_filledCube[xpos,0:ydim,zpos]
                index_y = np.where(yline == 0)[0]
                index_y = list(index_y)
                index_y.pop(0);index_y.pop(-1)
                if len(index_y) > 0:
                    # if not repeat: 
                    s3_filledCube[xpos,index_y[0]:ydim,zpos] = 0
                    # else: # repeat: 
                    #     s3_filledCube[xpos,0:index_y[0],zpos] = 0
        
    elif coord_dir == 1:
        print('Extending cube in the y direction - check!!!')
        for ypos in range(0,ydim):
            for zpos in range(0,zdim+2): 
                xline = s3_filledCube[0:xdim,ypos,zpos]
                index_x = np.where(xline == 0)[0]
                index_x = list(index_x)
                index_x.pop(0);index_x.pop(-1)
                if len(index_x) > 0:
                    # if not repeat:
                    s3_filledCube[index_x[-1]:xdim,ypos,zpos] = 0#[1]
                    # else:
                    #     s3_filledCube[0:index_x[1],ypos,zpos] = 0#[0]

    elif coord_dir == 2: 
        print('Extending cube in the z direction')
        for xpos in range(0,xdim):
            for ypos in range(0,ydim): 
                zline = s3_filledCube[xpos,ypos,0:zdim+2]
                index_z = np.where(zline == 0)[0]
                index_z = list(index_z)
                index_z.pop(0);index_z.pop(-1)
                if len(index_z) > 0:
                    # if not repeat: 
                    s3_filledCube[xpos,ypos,index_z[0]:zdim+2] = 0
                    # else: 
                    #     s3_filledCube[xpos,ypos,0:index_z[0]] = 0
        
    alert('woohoo')
    
    #Create volume of filled side of extended centreline mask
    mask_cube = s3_to_mesh(s3_filledCube, res=res, name='Filled CLRibbon SideA', color='darkblue')
    mask_cube.alpha(0.05)
    
    if plotshow: 
        obj = [(mask_cube, test_rib, mesh_cl.mesh)]
        txt = [(0, organ.user_organName)]
        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
   
    s3_filledCube = s3_filledCube.astype('uint8')

    #Create the inverse section and make the user select the section that corresponds to section 1
    s3_filledCubeBoolA =  copy.deepcopy(s3_filledCube).astype(bool)
    s3_filledCubeBoolB = np.full_like(s3_filledCubeBoolA, False)
    s3_filledCubeBoolB[1:-1,1:-1,1:-1] = True
    s3_filledCubeBoolB[s3_filledCubeBoolA] = False

    mask_cubeB = s3_to_mesh(s3_filledCubeBoolB, res=res, name='Filled CLRibbon SideB', color='skyblue')
    mask_cubeB.alpha(0.05).linewidth(1)
    mask_cube.linewidth(1)
    
    mask_cube.color('darkblue'); mask_cubeB.color('skyblue')
    mask_cube_split = [mask_cube, mask_cubeB]
    
    sel_side = select_ribMask(organ, mask_cube_split, mesh_cl.mesh)
    
    if 'SideA' in sel_side['name']:
        mask_selected = s3_filledCube.astype('uint8')
    else: #'SideB' in sel_side['name']:
        mask_selected = s3_filledCubeBoolB.astype('uint8')

    name2save = organ.user_organName + '_mask_sect.npy'
    dir2save = organ.info['dirs']['s3_numpy'] / name2save
    np.save(dir2save, mask_selected)
    if not dir2save.is_file():
        print('>> Error: s3 mask of sections was not saved correctly!\n>> File: mask_sect.npy')
        alert('error_beep')
    else: 
        print('>> s3 mask of sections saved correctly!')
        alert('countdown')
    
#%% func - select_ribMask
def select_ribMask(organ, mask_cube_split, mesh_cl): 
    
    dict_sides = {}
    for mesh in mask_cube_split:
        dict_sides[mesh.info['legend']] = {'color': mesh.color()*255}

    # dict_sides = copy.deepcopy(dict_sides)
    flat_segm = flatdict.FlatDict(dict_sides)
    colors = [flat_segm[key] for key in flat_segm if 'color' in key]
    color_sel = [210,105,30] # yellow [255,215,0] # chocolate (210,105,30)
    
    def func(evt):
        if not evt.actor:
            return
        mesh_no = evt.actor.info['legend']
        if 'Ribbon' in mesh_no: 
            mesh_color = evt.actor.color()*255
            msg.text(mesh_no +' has been selected as '+name_sect1.upper())
            is_in_list = np.any(np.all(mesh_color == colors, axis=1))
            if is_in_list: 
                new_color = color_sel
                evt.actor.color(new_color)
                selected_mesh['name'] = mesh_no
                for mesh in mask_cube_split:
                    if mesh.info['legend'] != mesh_no:
                        # print('running for mesh: ', mesh.info['legend'])
                        mesh.color(dict_sides[mesh.info['legend']]['color'])
            else: 
                new_color = color_sel
                evt.actor.color(new_color)
                selected_mesh['name'] = mesh_no
                for mesh in mask_cube_split:
                    if mesh.info['legend'] != mesh_no:
                        mesh.color(dict_sides[mesh.info['legend']]['color'])
        else: 
            print('Other mesh was selected')
    
    name_sect1 = organ.mH_settings['general_info']['sections']['name_sections']['sect1']
    mks = [vedo.Marker('*').c(color_sel).legend('Section No.1 ('+name_sect1+')')]
    sym = ['o']
    lb = vedo.LegendBox(mks, markers=sym, font=txt_font, 
                        width=leg_width, height=leg_height/3)
    path_logo = path_mHImages / 'logo-07.jpg'
    logo = vedo.Picture(str(path_logo))
    msg = vedo.Text2D("", pos="bottom-center", c=txt_color, s=txt_size, bg='red', alpha=0.2)
    selected_mesh = {'name': 'NS'}
    
    txA = 'Instructions: Select the mesh that corresponds to Section No.1 ('+name_sect1+'). Close the window when you are done.'
    txt0 = vedo.Text2D(txA, c=txt_color, font=txt_font, s=txt_size)
    
    vpt = vedo.Plotter(axes=1)
    vpt.add_icon(logo, pos=(0.1,1), size=0.25)
    vpt.add_callback('mouse click', func)
    vpt.show(mask_cube_split, mesh_cl, txt0, lb, msg, azimuth=45, elevation=20, zoom=0.8, interactive=True)
    
    return selected_mesh
    
#%% func - get_sections
def get_sections(organ, plotshow):
    
    #Check first if sections is a method involved in this organ
    if organ.check_method(method = 'E-Sections'): 
        subms = []
        name_sections = organ.mH_settings['general_info']['sections']['name_sections']
        user_names = '('+', '.join([name_sections[val] for val in name_sections])+')'
        
        #See if all sections have been stored in organ.submeshes
        sect_names = [item for item in organ.parent_project.mH_param2meas if 'sect1' in item and 'volume' in item]
        org_subm = [key for key in organ.submeshes if 'sect' in key]
        
        #Check workflow status
        workflow = organ.workflow
        process = ['MeshesProc','E-Sections','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE' and len(org_subm)==len(name_sections)*len(sect_names): 
            q = 'You already divided the tissues into sections '+user_names+'. Do you want to repeat this process?'
            res = {0: 'no, continue with next step', 1: 'yes, I want to repeat it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
            
    else: 
        proceed = False
        return None
        
    if proceed: 
        # Get user section names
        sect_names = [item for item in organ.parent_project.mH_param2meas if 'sect1' in item and 'volume' in item]
        palette =  sns.color_palette("husl", len(sect_names)*2)
        aa = 0
        
        for name in sect_names: 
            ch = name[0]; cont = name[1]
            mesh = organ.obj_meshes[ch+'_'+cont]
            print('\n- Dividing '+mesh.legend+' into sections '+user_names)
            submeshes = [(mesh.mesh)]; 
            for n, sect, color in zip(count(), name_sections, palette[aa:aa+len(name_sections)]):
                # print(n, sect, color)
                subm = mesh.create_section(name = sect, color = color)
                sub_mesh = subm.get_sect_mesh()
                submeshes.append((sub_mesh))
                subms.append(subm)
                
                # Update organ workflow
                proc_wft = ['MeshesProc', 'E-Sections', ch, cont, sect, 'Status']
                organ.update_workflow(process = proc_wft, update = 'DONE')
                
            if plotshow: 
                obj = submeshes
                txt = [(0, organ.user_organName +' - '+mesh.legend)]
                plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
            
            # Update organ workflow
            proc_wft_up = ['MeshesProc', 'E-Sections', ch, cont, 'Status']
            organ.update_workflow(process = proc_wft_up, update = 'DONE')
            aa+=2
            
        # Update organ workflow
        organ.update_workflow(process = process, update = 'DONE')
        organ.check_status(process='MeshesProc')
        organ.save_organ()  
           
    return subms

#%% func - s3_to_mesh
def s3_to_mesh(s3, res, name:str, color='cyan', rotateZ_90=True):

    verts, faces, _, _ = measure.marching_cubes(s3, spacing=res, method='lewiner')
    alert('frog')
    mesh = vedo.Mesh([verts, faces])
    if rotateZ_90: 
        mesh.rotateZ(-90).wireframe(True)
    mesh = mesh.extract_largest_region()
    alert('clown')
    mesh.color(color).alpha(1).wireframe().legend(name)

    return mesh

#%% func - sphs_in_spline
def sphs_in_spline(kspl, colour=False, color_map='turbo', every=10):
    """
    Function that creates a group of spheres through a spline given as input.
    """
    if colour:
        # scalars->colors
        vcols = [vedo.color_map(v, color_map, 0, len(kspl.points())) for v in list(range(len(kspl.points())))]  
    
    if every > 1:
        spheres_spline = []
        for num, point in enumerate(kspl.points()):
            if num % every == 0 or num == kspl.npoints-1:
                if num < 100:
                    size = (0.02,0.02)
                else: 
                    size = (0.03,0.02)
                if colour:
                    sphere_pt = vedo.Sphere(pos=point, r=2, c=vcols[num]).addScalarBar(title='Centreline\nPoint Number')
                    sphere_pt.legend('sph.'+str(num))
                    sphere_pt.caption(str(num), point=point,
                              size=size, padding = 3, justify='center', font=txt_font, alpha=0.8)
                else:
                    sphere_pt = vedo.Sphere(pos=point, r=2, c='coral')
                spheres_spline.append(sphere_pt)
    else:
        kspl_new = vedo.KSpline(kspl.points(), res = round(kspl.npoints/every))
        spheres_spline = vedo.Spheres(kspl_new.points(), c='coral', r=2)

    return spheres_spline

#%% func - get_segm_discs
def get_segm_discs(organ): 
    
    if organ.check_method(method = 'E-Segments'): 
        name_segments = organ.mH_settings['general_info']['segments']['name_segments']
        user_names = '('+', '.join([name_segments[val] for val in name_segments])+')'
      
        if 'segm_cuts' in organ.mH_settings.keys():
            if 'Disc No.0' in organ.mH_settings['segm_cuts']: 
                q = 'You already created the disc(s) to cut tissues into segments '+user_names+'. Do you want to repeat this process?'
                res = {0: 'no, continue with next step', 1: 'yes, I want to repeat it!'}
                proceed = ask4input(q, res, bool)
            else: 
                proceed = True
        else: 
            proceed = True
            
        if proceed: 
            segm_names = [item for item in organ.parent_project.mH_param2meas if 'segm1' in item]
            
            if len(segm_names)>0:
                # Get user segment names
                dict_names = organ.mH_settings['general_info']['segments']['name_segments']
                user_names = '('+', '.join([dict_names[val] for val in dict_names])+')'
                # Cut organ into segments
                q = 'Do you want to use the centreline to aid cut of tissue into segments '+user_names+'?'
                res = {0: 'No, I would like to define the cuts by hand', 1: 'yes, please!'}
                segm_using_cl = ask4input(q, res, bool)
                if segm_using_cl: 
                    #Find centreline first
                    dict_cl = plot_organCLs(organ, plotshow=False)
                    q = 'Select the centreline you want to use to aid organ cut into segments '+user_names+':'
                    select = ask4input(q, dict_cl, int)
                    ch_cont_cl = dict_cl[select].split(' (')[1].split('-')
                    ch = ch_cont_cl[0]
                    cont = ch_cont_cl[1]
                    cl = organ.obj_meshes[ch+'_'+cont].get_centreline()
                    spheres_spl = sphs_in_spline(kspl = cl, colour = True)
                
                ext_ch, _ = organ.get_ext_int_chs()
                if (ext_ch.channel_no, 'tiss', 'segm1', 'volume') in segm_names:
                    mesh_ext = organ.obj_meshes[ext_ch.channel_no+'_tiss']
                else: 
                    ch = segm_names[0][0]; cont = segm_names[0][1]
                    mesh_ext = organ.obj_meshes[ch+'_'+cont]
                    
                # Number of discs expected to be created
                no_cuts_4segments = organ.mH_settings['general_info']['segments']['no_cuts_4segments']
                
                # Create new key in mH_settings to save disc info
                proc = ['segm_cuts']
                organ.update_settings(proc, update = {}, mH = 'mH')
                    
                for n in range(no_cuts_4segments):
                    happyWithDisc = False
                    print('Creating disc No.'+str(n)+' for cutting tissues into segments!')
                    while not happyWithDisc: 
                        if segm_using_cl:
                            msg = '\n> Define the centreline point number to use to initialise disc to divide heart into segments '+user_names+' \n[NOTE: Spheres appear in centreline every 10 points, but you can select intermediate points, eg. 142].'
                            txt = [(0, organ.user_organName + msg)]
                            obj = [(mesh_ext.mesh.alpha(0.05), cl, spheres_spl)]
                            plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
                            
                            q = 'Enter the centreline point number you want to use to initialise the disc to divide the tissue into segments '+user_names+':'
                            num_pt = ask4input(q,{},int)
                            # Use flat disc or centreline orientation at point to define disc?
                            q2 = 'What would you like to use to initialise disc: '
                            res = {0:'Use the centreline orientation at the selected point to define disc orientation', 1: 'Initialise the disc in the selected position but in plane normal to the y-z plane?'}
                            cl_or_flat = ask4input(q2, res, bool)
                         
                            if not cl_or_flat:
                                pl_normal, pl_centre = get_plane_normal2pt(pt_num = num_pt, points = cl.points())
                            else:
                                pl_centre = cl.points()[num_pt]
                                pl_normal = [1,0,0]
                        else: 
                            pl_centre = mesh_ext.mesh.center_of_mass()
                            pl_normal = [1,0,0]
                            
                        radius = 60
                        height = 2*0.225
                        disc_color = 'purple'
                        disc_res = 300
                        # Modify (rotate and move cylinder/disc)
                        cyl_test, sph_test, rotX, rotY, rotZ = modify_disc(filename = organ.user_organName,
                                                                            txt = 'cut tissues into segments '+user_names, 
                                                                            mesh = mesh_ext.mesh,
                                                                            option = [True,True,True,True,True,True],
                                                                            def_pl = {'pl_normal': pl_normal, 'pl_centre': pl_centre},
                                                                            radius = radius, height = height, 
                                                                            color = disc_color, res = disc_res, 
                                                                            zoom=0.8)
                        
                        # Get new normal of rotated disc
                        pl_normal_corrected = new_normal_3DRot(normal = pl_normal, rotX = rotX, rotY = rotY, rotZ = rotZ)
                        normal_unit = unit_vector(pl_normal_corrected)*10
                        # Get central point of newly defined disc
                        pl_centre_new = sph_test.pos()
                        
                        # Newly defined centreline point
                        sph_cut = vedo.Sphere(pos = pl_centre_new, r=4, c='gold').legend('sph_ChamberCut')
                
                        # Build new disc to confirm
                        cyl_final = vedo.Cylinder(pos = pl_centre_new, r = radius, height = height, axis = normal_unit, c = disc_color, cap = True, res = disc_res)
                        cyl_final.legend('Disc')
                        
                        msg = '\n> Check the position and the radius of the disc to cut the tissue into segments '+user_names+'.\nMake sure it is cutting the tissue effectively separating it into individual segments.\nClose the window when done.'
                        txt = [(0, organ.user_organName + msg)]
                        obj = [(mesh_ext.mesh, cyl_final, cl)]
                        plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
            
                        disc_radius = radius
                        q_happy = 'Are you happy with the position of the disc [radius: '+str(disc_radius)+'um] to cut tissue into segments  '+user_names+'?'
                        res_happy = {0: 'no, I would like to define a new position for the disc', 1: 'yes, but I would like to redefine the disc radius', 2: 'yes, I am happy with both, disc position and radius'}
                        happy = ask4input(q_happy, res_happy, int)
                        if happy == 1:
                            happy_rad = False
                            while not happy_rad:
                                disc_radius = ask4input('Input disc radius [um]: ',{}, float)
                                cyl_final = vedo.Cylinder(pos = pl_centre_new, r = disc_radius, height = height, axis = normal_unit, c = disc_color, cap = True, res = disc_res)
                            
                                msg = '\n> New radius: Check the radius of the disc to cut the tissue into segments '+user_names+'. \nMake sure it is cutting the tissue effectively separating it into individual segments.\nClose the window when done.'
                                txt = [(0, organ.user_organName + msg)]
                                obj = [(mesh_ext.mesh.alpha(1), cl, cyl_final, sph_cut)]
                                plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
                                
                                q_happy_rad = 'Is the selected radius ['+str(disc_radius)+'um] sufficient to cut the tissue into segments '+user_names+'?'
                                res_happy_rad = {0: 'no, I would like to change its value', 1: 'yes, it cuts the tissue without disrupting too much the segments!'}
                                happy_rad = ask4input(q_happy_rad, res_happy_rad, bool)
                            happyWithDisc = True
                        elif happy == 2:
                            happyWithDisc = True
                    
                    # Save disc info
                    cyl_name = 'Disc No.'+str(n)
                    cyl_final.legend(cyl_name)
                    cyl_dict = {'radius': disc_radius,
                                'normal_unit': normal_unit,
                                'pl_centre': pl_centre_new,
                                'height': height, 
                                'color': disc_color}
             
                    proc_disc = ['segm_cuts', cyl_name]
                    organ.update_settings(proc_disc, update = cyl_dict, mH = 'mH')
    else: 
        print('None')
        
#%% func - create_disc_mask
def create_disc_mask(organ, h_min = 0.1125): 
    
    if organ.check_method(method = 'E-Segments'): 
        name_segments = organ.mH_settings['general_info']['segments']['name_segments']
        user_names = '('+', '.join([name_segments[val] for val in name_segments])+')'
        no_cuts = organ.mH_settings['general_info']['segments']['no_cuts_4segments']
      
        #Check if there ir already a created mask
        mask_file_bool = []
        for ii in range(no_cuts):
            name2save = organ.user_organName + '_mask_DiscNo'+str(ii)+'.npy'
            mask_file = organ.info['dirs']['s3_numpy'] / name2save
            mask_file_bool.append(mask_file.is_file())
        
        if all(mask_file_bool): 
            q = 'You already created the disc mask(s) to cut tissues into segments '+user_names+'. Do you want to re-run this process?'
            res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
            proceed = ask4input(q, res, bool)
    
        else: 
            proceed = True
        
    if proceed: 
        segm_names = [item for item in organ.parent_project.mH_param2meas if 'segm1' in item]
        
        ext_ch, _ = organ.get_ext_int_chs()
        if (ext_ch.channel_no, 'tiss', 'segm1', 'volume') in segm_names:
            mesh_ext = organ.obj_meshes[ext_ch.channel_no+'_tiss']
        else: 
            ch = segm_names[0][0]; cont = segm_names[0][1]
            mesh_ext = organ.obj_meshes[ch+'_'+cont]
            
        res = mesh_ext.resolution
        
        #Load stack shape
        shape_s3 = organ.info['shape_s3']
        zdim, xdim, ydim = shape_s3
        print('shape_s3:',shape_s3, '- xdim:', xdim, '- ydim:',ydim, '- zdim:', zdim)
            
        disc_info = organ.mH_settings['segm_cuts']
        for disc in disc_info:
            print('Creating mask for '+ disc)
            disc_name = disc.replace(' ', '').replace('.','')
            
            disc_radius = disc_info[disc]['radius']
            normal_unit = disc_info[disc]['normal_unit']
            pl_centre = disc_info[disc]['pl_centre']
            height = disc_info[disc]['height']
            
            # Create a disc with better resolution to transform into pixels to mask stack
            res_cyl = 2000
            num_rad = int(3*int(disc_radius)) #int(((r_circle_max-r_circle_min)/0.225)+1)
            num_h = 9
            for j, rad in enumerate(np.linspace((disc_radius*0.2)/2, disc_radius, num_rad)):
                for i, h in enumerate(np.linspace(h_min,height, num_h)):
                    cyl = vedo.Cylinder(pos = pl_centre, r = rad, height = h, axis = normal_unit, c = 'lime', cap = True, res = res_cyl)#.wireframe(True)
                    if i == 0 and j == 0:
                        cyl_pts = cyl.points()
                    else:
                        cyl_pts = np.concatenate((cyl_pts, cyl.points()))
    
            # Rotate the points that make up the HR disc, to convert them to a stack
            cyl_points_rot = np.zeros_like(cyl_pts)
            if organ.mH_settings['general_info']['rotateZ_90']: #'CJ' not in filename: 
                axis = [0,0,1]
            else: 
                axis = [0,0,0]
     
            for i, pt in enumerate(cyl_pts):
                cyl_points_rot[i] = (np.dot(rotation_matrix(axis = axis, theta = np.radians(90)),pt))
     
            cyl_pix = np.transpose(np.asarray([cyl_points_rot[:,i]//res[i] for i in range(len(res))]))
            cyl_pix = cyl_pix.astype(int)
            cyl_pix = np.unique(cyl_pix, axis=0)
            
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
            s3_cyl = s3_cyl.astype('uint8')
            
            name2save = organ.user_organName + '_mask_'+disc_name+'.npy'
            dir2save = organ.info['dirs']['s3_numpy'] / name2save
            np.save(dir2save, s3_cyl)
            
            if not dir2save.is_file():
                print('>> Error: s3 mask of '+disc+' was not saved correctly!\n>> File: mask_'+disc_name+'.npy')
                alert('error_beep')
            else: 
                print('>> s3 mask of '+disc+' saved correctly!')
                alert('countdown')

#%% func - get_segments
def get_segments(organ, plotshow): 

    #Check first if segments is a method involved in this organ
    if organ.check_method(method = 'E-Segments'): 
        meshes_segm=[]; final_subsgm=[]
        name_segments = organ.mH_settings['general_info']['segments']['name_segments']
        user_names = '('+', '.join([name_segments[val] for val in name_segments])+')'
        
        #See if all sections have been stored in organ.submeshes
        segm_names = [item for item in organ.parent_project.mH_param2meas if 'segm1' in item and 'volume' in item]
        org_subm = [key for key in organ.submeshes if 'segm' in key]
        
        #Check workflow status
        workflow = organ.workflow
        process = ['MeshesProc','E-Segments','Status']
        check_proc = get_by_path(workflow, process)
        if check_proc == 'DONE' and len(org_subm)==len(name_segments)*len(segm_names): 
            q = 'You already divided the tissues into segments '+user_names+'. Do you want to repeat this process?'
            res = {0: 'no, continue with next step', 1: 'yes, I want to repeat it!'}
            proceed = ask4input(q, res, bool)
        else: 
            proceed = True
    else:
        proceed = False
        return None
    
    proceed = True
    if proceed: 
        segm_names = [item for item in organ.parent_project.mH_param2meas if 'segm1' in item and 'volume' in item]
        sorted_segm = sorted(segm_names, key=lambda x: (x[0], x[1]))
        # Get external channel 
        ext_ch, _ = organ.get_ext_int_chs()
        ext_ch_no = ext_ch.channel_no
        
        #Get palette to color all segments distinctively
        palette =  sns.color_palette("husl", len(segm_names)*2)
        #First divide external-external channel into segments
        ch = ext_ch_no; cont = 'ext'#name[1]
        ext_subsgm, ext_meshes = segm_ext_ext(organ, ch, cont, user_names, palette[0:len(name_segments)])
        
        meshes_segm = [tuple(ext_meshes)]
        final_subsgm = [ext_subsgm[key] for key in ext_subsgm.keys()]
        
        if ch+'_'+cont+'_'+'segm1' in organ.submeshes.keys():
            sorted_segm.remove((ch, cont, 'segm1', 'volume'))
            aa = len(name_segments)
            
        for name in sorted_segm: 
            ch = name[0]; cont = name[1]
            mesh = organ.obj_meshes[ch+'_'+cont]
            print('\n- Dividing '+mesh.legend+' into segments '+user_names)
            cut_masked = mesh.mask_segments()
            dict_segm = dict_segments(organ, other=False)

            m_subs = []; f_subs = []
            for n, segm, color in zip(count(), name_segments, palette[aa:aa+len(name_segments)]):
                sp_dict_segm = {}
                sp_dict_segm = classify_segments_from_ext(meshes = cut_masked, 
                                                            dict_segm = dict_segm[segm],
                                                            ext_sub = ext_subsgm[segm])
                # print(sp_dict_segm)
                subsgm, final_segm_mesh = create_asign_subsg(organ, mesh, cut_masked, 
                                                                      segm, sp_dict_segm, color)
                m_subs.append(final_segm_mesh)
                f_subs.append(subsgm)
                
            obj = [(mesh.mesh),tuple(m_subs)]
            txt = [(0, organ.user_organName +' - '+mesh.legend)]
            plot_grid(obj=obj, txt=txt, axes=1, sc_side=max(organ.get_maj_bounds()))
            
            meshes_segm.append(tuple(m_subs))
            final_subsgm = final_subsgm + f_subs
            aa +=2
        
        if plotshow: 
            obj = meshes_segm
            txt = [(0, organ.user_organName)]
            plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
    
    return meshes_segm, final_subsgm

#%% func - segm_ext_ext
def segm_ext_ext(organ, ch, cont, user_names, colors):
    
    name_segments = organ.mH_settings['general_info']['segments']['name_segments']
    mesh = organ.obj_meshes[ch+'_'+cont]

    print('\n- Dividing '+mesh.legend+' into segments '+user_names)
    
    cut_masked = mesh.mask_segments()
    
    #Test if this info already exists?
    dict_segm = dict_segments(organ)
    dict_segm = classify_segments(meshes=cut_masked, dict_segm=dict_segm)

    meshes_segm = []; final_subsgm = {}
    organ.update_settings(['general_info','segments','ext_ext'], mesh.name, 'mH')
    proc = ['general_info','segments','ext_segm']
    organ.update_settings(proc, {}, 'mH')
    
    for n, segm, color in zip(count(), name_segments, colors):
        print('\t- Cutting segment No.',n)#,segm, color)
        sp_dict_segm = dict_segm[segm]
        # print('sp_dict_segm', sp_dict_segm)
        subsgm, final_segm_mesh = create_asign_subsg(organ, mesh, cut_masked, segm, sp_dict_segm, color)
        organ.update_settings(proc+[segm], {}, 'mH')
        organ.update_settings(proc+[segm,'name'], subsgm.sub_name_all, 'mH')
        save_submesh(organ, subsgm, final_segm_mesh)
        meshes_segm.append(final_segm_mesh)
        final_subsgm[segm]=subsgm
    
    return final_subsgm, tuple(meshes_segm)

#%% func - save_submesh
def save_submesh(organ, submesh, mesh, ext='.vtk'):
    
    mesh_name = organ.user_organName+'_'+submesh.sub_name_all+ext
    mesh_dir = organ.info['dirs']['meshes'] / mesh_name
    mesh.write(str(mesh_dir))
    
    organ.mH_settings['general_info']['segments']['ext_segm'][submesh.sub_name]['mesh_dir'] = mesh_dir
    print('>> Mesh '+mesh_name+' has been saved!')
    alert('countdown')        
    
#%% func - create_assign_subsg
def create_asign_subsg(organ, mesh, cut_masked, segm, sp_dict_segm, color):
    
    subsgm = mesh.create_segment(name = segm, color = color)
    final_segm_mesh, subsgm = assign_meshes2segm(organ, mesh, cut_masked, 
                                                 subsgm, sp_dict_segm, color)
    
    return subsgm, final_segm_mesh
    
#%% func - assign_meshes2segm
def assign_meshes2segm(organ, mesh, cut_masked, subsgm, sp_dict_segm, color): 
    
    print('\t- Assigning meshes into segments for '+mesh.legend+' ('+subsgm.sub_legend+')')
    # print(subsgm.sub_name, subsgm.sub_legend)
    list_meshes = sp_dict_segm['meshes_number']
    
    sp_dict_segm['meshes_info'] = {}
    
    #Find meshes and add them to the mesh
    mesh_segm = []; 
    for cut_mesh in cut_masked:
        if cut_mesh.info['legend'] in list_meshes: 
            # print(cut_mesh.info)
            mesh_segm.append(cut_mesh)
            # com = cut_mesh.center_of_mass()
            # vol = cut_mesh.volume()
            # area = cut_mesh.area()
            # sp_dict_segm['meshes_info'][cut_mesh.info['legend']] = {'COM': com,
            #                                                            'volume': vol, 
            #                                                            'area': area}
    final_segm_mesh = vedo.merge(mesh_segm)
    final_segm_mesh.color(color).alpha(0.1).legend(subsgm.sub_legend)
    subsgm.dict_segm = sp_dict_segm
    subsgm.color = color
    organ.add_submesh(subsgm)

    return final_segm_mesh, subsgm
    
#%% func - dict_segments
def dict_segments(organ, other=True):
    
    segments_info = organ.mH_settings['general_info']['segments']
    no_segm = segments_info['no_segments']
    #https://seaborn.pydata.org/tutorial/color_palettes.html
    palette_all = sns.color_palette("cool_r", no_segm*4)
    palette = random.sample(palette_all, no_segm)
    
    if other: 
        dict_segm = {'other': {'user_name': 'other',
                               'color': np.array([128,128,128]),
                               'meshes_number': []}}
    else:
        dict_segm = {}
    
    for n, segm in enumerate(segments_info['name_segments']): 
        dict_segm[segm] = {}
        dict_segm[segm]['user_name'] = segments_info['name_segments'][segm]
        dict_segm[segm]['color'] = [val*255 for val in palette[n]]
        dict_segm[segm]['meshes_number'] = []
    
    return dict_segm
    
#%% func - classify_segments
#Working clicking 
def classify_segments(meshes, dict_segm):
    
    flat_segm = flatdict.FlatDict(dict_segm)
    colors = [flat_segm[key] for key in flat_segm if 'color' in key]
    mesh_classif = [flat_segm[key] for key in flat_segm if 'meshes_number' in key]
    names = [flat_segm[key] for key in flat_segm if 'user_name' in key]
    # print(mesh_classif)
    
    #https://seaborn.pydata.org/tutorial/color_palettes.html
    palette = sns.color_palette("Set2", len(meshes))
    # palette = [np.random.choice(range(255),size=3) for num in range(len(meshes))]
    for n, mesh in enumerate(meshes):
        mesh.color(palette[n])
    
    def func(evt):
        if not evt.actor:
            return
        mesh_no = evt.actor.info['legend']
        mesh_color = evt.actor.color()*255
        # vedo.printc("You clicked: "+mesh_no)
        # print(mesh_classif)
        is_in_list = np.any(np.all(mesh_color == colors, axis=1))
        if is_in_list:
            bool_list = np.all(mesh_color == colors, axis=1)
            ind = np.where(bool_list == True)[0][0]
            ind_plus1 = ind+1
            new_ind = (ind_plus1)%len(colors)
            # print('ind:',ind, '-new_ind:', new_ind)
            new_color = colors[new_ind]
            evt.actor.color(new_color)
            mesh_classif[ind].remove(mesh_no)
            mesh_classif[new_ind].append(mesh_no)
            msg.text("You clicked Mesh "+mesh_no+' to classify it as '+names[new_ind])
        else: 
            evt.actor.color(colors[1])
            mesh_classif[1].append(mesh_no)
            msg.text("You clicked Mesh "+mesh_no+' to classify it as '+names[1])
        
    mks = []; sym = ['o']*len(dict_segm)
    for segm in dict_segm:
        mks.append(vedo.Marker('*').c(dict_segm[segm]['color']).legend(dict_segm[segm]['user_name']))
        
    # Load logo
    path_logo = path_mHImages / 'logo-07.jpg'
    logo = vedo.Picture(str(path_logo))
    
    txA = 'Instructions: Click each segment mesh until it is coloured according to the segment it belongs to.'
    txB = '\n[Note: Colours will rotate between segments]'
    txt0 = vedo.Text2D(txA+txB, c=txt_color, font=txt_font, s=txt_size)
    lb = vedo.LegendBox(mks, markers=sym, font=txt_font, 
                        width=leg_width/1.5, height=leg_height/1.5)
    
    msg = vedo.Text2D("", pos="bottom-center", c=txt_color, font=txt_font, bg='red', alpha=0.2)
    vpt = vedo.Plotter(axes=5, bg='white')
    vpt.add_icon(logo, pos=(0.1,1), size=0.25)
    vpt.add_callback('mouse click', func)
    vpt.show(meshes, lb, msg, txt0, zoom=1.2)
    
    return dict_segm
    
#%% func - classify_segments_from_ext
def classify_segments_from_ext(meshes, dict_segm, ext_sub):
    
    ext_sub_mesh = ext_sub.get_segm_mesh()
    
    # name = ext_sub.parent_mesh.parent_organ.user_organName
    # obj = [ext_sub_mesh]
    # txt = [(0, name +' - '+ext_sub.sub_legend)]
    # plot_grid(obj=obj, txt=txt, axes=1, sc_side=max(ext_sub.parent_mesh.parent_organ.get_maj_bounds()))
    
    list_meshes = []
    for mesh in meshes: 
        com = mesh.center_of_mass()
        if ext_sub_mesh.is_inside(com):
            # print('-'+mesh.info['legend']+' is inside '+ext_sub.sub_name_all)
            list_meshes.append(mesh.info['legend'])
    dict_segm['meshes_number'] = list_meshes
            
    return dict_segm
    
#%% - Measuring function
#%% func - measure_centreline
def measure_centreline(organ, nPoints):
    
    cl_names = [item for item in organ.parent_project.mH_param2meas if 'centreline' in item]
    for name in cl_names: 
        ch = name[0]; cont = name[1]; segm= name[2]
        cl_final = organ.obj_meshes[ch+'_'+cont].get_centreline(nPoints=nPoints)
        cl_length = cl_final.length()
    
        #Create linear line
        linLine = organ.obj_meshes[ch+'_'+cont].get_linLine(nPoints=nPoints)
        lin_length = linLine.length()
        process = ['measure', ch, cont, segm]
        organ.update_settings(process = process+['centreline_looplength'], 
                              update = cl_length, mH='mH')
        organ.update_settings(process = process+['centreline_linlength'], 
                              update = lin_length, mH='mH')
        organ.update_settings(process = process+['centreline'], 
                              update = 'DONE', mH='mH')
        
        processes = [['MeshesProc', 'F-Measure',ch, cont, segm, 'centreline'],
                   ['MeshesProc', 'F-Measure',ch, cont, segm, 'centreline_linlength'],
                   ['MeshesProc', 'F-Measure',ch, cont, segm, 'centreline_looplength']]
        
        for process in processes: 
            organ.update_workflow(process=process,update='DONE')

#%% func - measure_volume  
def measure_volume(organ):
    vol_names = [item for item in organ.parent_project.mH_param2meas if 'volume' in item]
    for name in vol_names: 
        # print(name)
        ch = name[0]; cont = name[1]; segm = name[2]
        # print(ch, cont, segm)
        mesh_mH = organ.obj_meshes[ch+'_'+cont]
        if segm == 'whole': 
            volume = mesh_mH.get_volume()
            
        elif 'sect' in segm: 
            print(segm)
            if ch+'_'+cont+'_'+segm in organ.submeshes.keys():
                sub_sect = organ.submeshes[ch+'_'+cont+'_'+segm]
                subm = mesh_mH.create_section(name = segm, color = sub_sect['color'])
                volume = subm.get_sect_mesh().volume()
        else: 
            print(segm)
            if ch+'_'+cont+'_'+segm in organ.submeshes.keys():
                sub_sect = organ.submeshes[ch+'_'+cont+'_'+segm]
                subm = mesh_mH.create_segment(name = segm, color = sub_sect['color'])
                volume = subm.get_segm_mesh().volume()
            
        process = ['measure', ch, cont, segm, 'volume']
        organ.update_settings(process = process, 
                              update = volume, mH='mH')
        wf_proc = ['MeshesProc', 'F-Measure',ch, cont, segm, 'volume']
        organ.update_workflow(process=wf_proc, update='DONE')
            
#%% func - measure_area 
def measure_area(organ):
    area_names = [item for item in organ.parent_project.mH_param2meas if 'surf_area' in item]
    for name in area_names: 
        # print(name)
        ch = name[0]; cont = name[1]; segm = name[2]
        mesh_mH = organ.obj_meshes[ch+'_'+cont]
        if segm == 'whole': 
            area = mesh_mH.get_area()
            
        elif 'sect' in segm: 
            print(segm)
            if ch+'_'+cont+'_'+segm in organ.submeshes.keys():
                sub_sect = organ.submeshes[ch+'_'+cont+'_'+segm]
                subm = mesh_mH.create_section(name = segm, color = sub_sect['color'])
                area = subm.get_mesh().area()
        else: 
            print(segm)
            if ch+'_'+cont+'_'+segm in organ.submeshes.keys():
                sub_sect = organ.submeshes[ch+'_'+cont+'_'+segm]
                subm = mesh_mH.create_segment(name = segm, color = sub_sect['color'])
                area = subm.get_segm_mesh().area()
                
        process = ['measure', ch, cont, segm, 'surf_area']
        organ.update_settings(process = process, 
                              update = area, mH='mH')
        wf_proc = ['MeshesProc', 'F-Measure',ch, cont, segm, 'surf_area']
        organ.update_workflow(process=wf_proc, update='DONE')
            
#%% func - find_angle_btw_pts
def find_angle_btw_pts(pts1, pts2):
    """
    Function that returns the angle between two vectors on the input-plane
    """
        
    mag_v1 = findDist(pts1[0],pts1[1])
    mag_v2 = findDist(pts2[0],pts2[1])

    vect1 = pts1[1]-pts1[0]
    vect2 = pts2[1]-pts2[0]

    dotProd = np.dot(vect1,vect2)

    angle = math.degrees(math.acos(dotProd/(mag_v1*mag_v2)))

    return angle

#%% func - findDist
def findDist(pt1, pt2):
    """
    Function that returns the distance between two points given as input
    """
    squared_dist = np.sum((pt1-pt2)**2, axis=0)
    dist = np.sqrt(squared_dist)

    return dist

#%% func - get_plane_normal2pt
def get_plane_normal2pt (pt_num, points):
    """
    Funtion that gets a plane normal to a point in a spline

    """

    pt_centre = points[pt_num]
    normal = points[pt_num-1]-points[pt_num+1]

    return normal, pt_centre

#%% - Plotting functions
#%% func - plot_grid
def plot_grid(obj:list, txt=[], axes=1, zoom=1, lg_pos='top-left',sc_side=350):
    
    # Load logo
    path_logo = path_mHImages / 'logo-07.jpg'
    logo = vedo.Picture(str(path_logo))
    
    # Create ScaleCube
    if isinstance(obj[0], tuple):
        scale_cube = vedo.Cube(pos=obj[0][0].center_of_mass(), side=sc_side, c='white', alpha=0.01).legend('ScaleCube')
    else: 
        scale_cube = vedo.Cube(pos=obj[0].center_of_mass(), side=sc_side, c='white', alpha=0.01).legend('ScaleCube')
    
    # Set logo position
    if lg_pos =='top-left':
        if len(obj)>5:
            pos = (0.1,3)
        elif len(obj)>3:
            pos = (0.1,2)
        else:
            pos = (0.1,1)
    else: 
        if len(obj)>3:
            pos = (0.1,2) # to correct 
        else:
            pos = (0.8,0.05)
    
    n_obj = len(obj)
    # Create tuples for text
    post = [tup[0] for tup in txt]; txt_out = []; n = 0
    for num in range(n_obj):
        if num in post:
            txt_out.append(vedo.Text2D(txt[n][1], c=txt_color, font=txt_font, s=txt_size))
            n += 1
        else: 
            txt_out.append(vedo.Text2D('', c=txt_color, font=txt_font, s=txt_size))
    
    # Add scale_cube to last plot
    if isinstance(obj[n_obj-1], tuple):
        obj_list = list(obj[n_obj-1])
        obj_list.append(scale_cube)
        obj_f = tuple(obj_list)
    else: #vedo.mesh.Mesh
        obj_f = (obj[n_obj-1], scale_cube)
    obj[n_obj-1] = obj_f
    
    # Now plot
    lbox = []
    vp = vedo.Plotter(N=len(obj), axes=axes)
    vp.add_icon(logo, pos=pos, size=0.25)
    for num in range(len(obj)):
        if isinstance(obj[num], tuple):
            # print('A')
            try: 
                lbox.append(vedo.LegendBox(list(obj[num]), font=leg_font, width=leg_width))
            except: 
                lbox.append('')
                # print('Legend box error:', type(obj[num]))
        else:
            # print('B')
            lbox.append(vedo.LegendBox([obj[num]], font=leg_font, width=leg_width))
        if num != len(obj)-1:
            vp.show(obj[num], lbox[num], txt_out[num], at=num)
        else: # num == len(obj)-1
            vp.show(obj[num], lbox[num], txt_out[num], at=num, zoom=zoom, interactive=True)

#%% func - plot_all_organ
def plot_all_organ(organ):
    
    obj = []
    txt = [(0, organ.user_organName  + ' - All organ meshes')]
    for mesh in organ.meshes.keys():
        # print(organ.obj_meshes[mesh].mesh)
        obj.append((organ.obj_meshes[mesh].mesh))
    
    plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))

#%% func - plot_meas_meshes
def plot_meas_meshes(organ, meas:list, color_map = 'turbo', alpha=1):
    obj = []
    for param in meas: 
        names = [item for item in organ.parent_project.mH_param2meas if param in item]
        for name in names: 
            ch = name[0]; cont = name[1]
            mesh_mHA = organ.obj_meshes[ch+'_'+cont]
            if 'ball' in param:
                from_cl = organ.mH_settings['wf_info']['MeshesProc']['D-Ballooning'][ch][cont]['from_cl']
                from_cl_type = organ.mH_settings['wf_info']['MeshesProc']['D-Ballooning'][ch][cont]['from_cl_type']
                mesh_out = mesh_mHA.balloon_mesh(n_type=from_cl+'_'+from_cl_type, color_map=color_map, alpha=alpha)
            elif 'thickness' in param:
                n_type = name[3][-7:].replace('>','TO')
                mesh_out = mesh_mHA.thickness_mesh(n_type=n_type, color_map=color_map, alpha=alpha)
            obj.append((mesh_out))
    
    if len(obj) == 0:
        print('>> No meshes were recognised for param', meas)
        alert('error_beep')
    else: 
        txt = [(0, organ.user_organName)]
        plot_grid(obj, txt, axes=5, sc_side=max(organ.get_maj_bounds()))
        
#%% ƒunc - plot_organCLs
def plot_organCLs(organ, axes=5, plotshow=True):
    organ_info = organ.mH_settings['general_info']
    dict_cl = {}; obj = []; txt = []; n = 0
    for item in organ.parent_project.mH_param2meas: 
        if 'centreline' in item: 
            n += 1
            ch = item[0]; cont = item[1]; segm = item[2]
            name = organ_info[ch]['user_chName']+'-'+cont+' ('+ch+'-'+cont+'-'+segm+')'
            dict_cl[n] = name
            mesh_o = organ.obj_meshes[ch+'_'+cont]
            cl_o = mesh_o.get_centreline(color = 'indigo')
            obj.append((mesh_o.mesh, cl_o))
            if n-1==0:
                txt.append((n-1, organ.user_organName+'\n-> '+name))
            else:  
                txt.append((n-1, '\n-> '+name))
    if plotshow: 
        plot_grid(obj=obj, txt=txt, axes=axes, sc_side=max(organ.get_maj_bounds()))

    return dict_cl

#%% - Plane handling functions 
#%% func - get_plane
def get_plane(filename, txt:str, meshes:list, win, def_pl = None, 
                             option = [True,True,True,True,True,True]):
    '''
    Function that creates a plane defined by the user

    '''
    
    # Load logo
    path_logo = path_mHImages / 'logo-07.jpg'
    logo = vedo.Picture(str(path_logo))
    
    if all([isinstance(mesh, vedo.Mesh) for mesh in meshes]):
        meshes_mesh = meshes
    else: 
        meshes_mesh = [mesh.mesh for mesh in meshes]
        
    # Create plane
    if def_pl != None:
        plane, normal, rotX, rotY, rotZ = get_plane_pos(filename, txt, meshes_mesh, option, def_pl)
    else:
        plane, normal, rotX, rotY, rotZ = get_plane_pos(filename, txt, meshes_mesh, option)
        
    # Get new normal of rotated plane
    normal_corrected = new_normal_3DRot(normal, rotX, rotY, rotZ)
    # Get central point of new plane and create sphere
    pl_centre = plane.pos()
    sph_centre = vedo.Sphere(pos=pl_centre,r=2,c='black')
    # Build new plane to confirm
    plane_new = vedo.Plane(pos=pl_centre,normal=normal_corrected).color('green').alpha(1).legend('New Plane')

    normal_txt = str([' {:.2f}'.format(i) for i in normal_corrected]).replace("'","")
    centre_txt = str([' {:.2f}'.format(i) for i in pl_centre]).replace("'","")
    text = filename+'\n\nUser defined plane to '+ txt +'.\nPlane normal: '+normal_txt+' - Plane centre: '+centre_txt+'.\nClose the window when done.'
    txt2D = vedo.Text2D(text, c=txt_color, font=txt_font, s=txt_size)

    vp = vedo.Plotter(N=1, axes=4)
    vp.add_icon(logo, pos=(0.8,0.05), size=0.25)
    vp.show(meshes_mesh, plane, plane_new, sph_centre, txt2D, at=0, viewup='y', azimuth=0, elevation=0, interactive=True)

    return plane_new, pl_dict

#%% func - get_plane_pos
def get_plane_pos(filename, txt, meshes, option, 
                     def_pl= {'pl_normal': (0,1,0), 'pl_centre': []}, zoom = 0.5):
    '''
    Function that shows a plot so that the user can define a plane (mesh opacity can be changed)
    meshes: list (outer mesh in position 0, inner mesh in position 1 or 2)

    '''
    
    # Load logo
    path_logo = path_mHImages / 'logo-07.jpg'
    logo = vedo.Picture(str(path_logo))
    
    xmin, xmax, ymin, ymax, zmin, zmax = meshes[0].bounds()
    x_size = xmax - xmin; y_size = ymax - ymin; z_size = zmax - zmin

    xval = sorted([xmin-0.3*x_size,xmax+0.3*x_size])
    yval = sorted([ymin-0.3*y_size,ymax+0.3*y_size])
    zval = sorted([zmin-0.3*z_size,zmax+0.3*z_size])

    box_size = max(x_size, y_size, z_size)

    if def_pl['pl_centre'] == []:
        centre = (x_size/2+xmin, ymin, z_size/2+zmin)
    else: 
        centre = def_pl['pl_centre']
    normal = def_pl['pl_normal']

    rotX = [0]; rotY = [0]; rotZ = [0]

    # Functions to move and rotate plane
    def sliderX(widget, event):
        valueX = widget.GetRepresentation().GetValue()
        plane.x(valueX)

    def sliderY(widget, event):
        valueY = widget.GetRepresentation().GetValue()
        plane.y(valueY)

    def sliderZ(widget, event):
        valueZ = widget.GetRepresentation().GetValue()
        plane.z(valueZ)

    def sliderRotX(widget, event):
        valueRX = widget.GetRepresentation().GetValue()
        rotX.append(valueRX)
        plane.rotateX(valueRX, rad=False)

    def sliderRotY(widget, event):
        valueRY = widget.GetRepresentation().GetValue()
        rotY.append(valueRY)
        plane.rotateY(valueRY, rad=False)

    def sliderRotZ(widget, event):
        valueRZ = widget.GetRepresentation().GetValue()
        rotZ.append(valueRZ)
        plane.rotateZ(valueRZ, rad=False)

    def sliderAlphaMeshOut(widget, event):
        valueAlpha = widget.GetRepresentation().GetValue()
        meshes[0].alpha(valueAlpha)

    lbox = vedo.LegendBox(meshes, font=leg_font, width=leg_width, padding=1)
    #vedo.settings.legendSize = .2
    vp = vedo.Plotter(N=1, axes=8)
    vp.add_icon(logo, pos=(0.85,0.75), size=0.10)
    plane = vedo.Plane(pos=centre, normal=normal, 
                       s=(box_size*1.5, box_size*1.5)).color('gainsboro').alpha(1)
    if option[0]: #sliderX
        vp.addSlider2D(sliderX, xval[0], xval[1], value=centre[0],
                    pos=[(0.1,0.15), (0.3,0.15)], title='- > x position > +', 
                    c='crimson', title_size=txt_slider_size)
    if option[1]: #sliderY
        vp.addSlider2D(sliderY, yval[0], yval[1], value=centre[1],
                    pos=[(0.4,0.15), (0.6,0.15)], title='- > y position > +', 
                    c='dodgerblue', title_size=txt_slider_size)
    if option[2]: #sliderZ
        vp.addSlider2D(sliderZ, zval[0], zval[1], value=centre[2],
                    pos=[(0.7,0.15), (0.9,0.15)], title='- > z position > +', 
                    c='limegreen', title_size=txt_slider_size)
    if option[3]: #sliderRotX
        vp.addSlider2D(sliderRotX, -1, +1, value=0,
                    pos=[(0.1,0.05), (0.3,0.05)], title='- > x rotation > +', 
                    c='deeppink', title_size=txt_slider_size)
    if option[4]: #sliderRotY
        vp.addSlider2D(sliderRotY, -1, +1, value=0,
                    pos=[(0.4,0.05), (0.6,0.05)], title='- > y rotation > +', 
                    c='gold', title_size=txt_slider_size)
    if option[5]: #sliderRotZ
        vp.addSlider2D(sliderRotZ, -1, +1, value=0,
                    pos=[(0.7,0.05), (0.9,0.05)], title='- > z rotation > +', 
                    c='teal', title_size=txt_slider_size)
        
    if len(meshes)>1: 
        titleOp = 'Outer mesh opacity'
    else: 
        titleOp = 'Mesh opacity'
        
    vp.addSlider2D(sliderAlphaMeshOut, xmin=0.01, xmax=0.99, value=0.01,
               pos=[(0.95,0.25), (0.95,0.45)], c='blue', 
               title=titleOp, title_size=txt_slider_size)

    text = filename+'\n\nDefine plane position to '+txt+'. \nClose the window when done'
    txt = vedo.Text2D(text, c=txt_color, font=txt_font, s=txt_size)
    vp.show(meshes, plane, lbox, txt, viewup='y', zoom=zoom, interactive=True)

    return plane, normal, rotX, rotY, rotZ

#%% func - modify_disc
def modify_disc(filename, txt, mesh, option,  
                    def_pl= {'pl_normal': (0,1,0), 'pl_centre': []}, 
                    radius=60, height = 0.45, 
                    color = 'purple', res = 300, zoom = 0.5):
    """
    Function that shows a plot so that the user can define a cylinder (disc)

    """

    # Load logo
    path_logo = path_mHImages / 'logo-07.jpg'
    logo = vedo.Picture(str(path_logo))
    
    xmin, xmax, ymin, ymax, zmin, zmax = mesh.bounds()
    x_size = xmax - xmin; y_size = ymax - ymin; z_size = zmax - zmin
    
    xval = sorted([xmin-0.3*x_size,xmax+0.3*x_size])
    yval = sorted([ymin-0.3*y_size,ymax+0.3*y_size])
    zval = sorted([zmin-0.3*z_size,zmax+0.3*z_size])
    
    if def_pl['pl_centre'] == []:
        centre = (x_size/2+xmin, ymin, z_size/2+zmin)
    else: 
        centre = def_pl['pl_centre']
    normal = def_pl['pl_normal']

    rotX = [0];    rotY = [0];    rotZ = [0]

    # Functions to move and rotate cyl_test
    def sliderX(widget, event):
        valueX = widget.GetRepresentation().GetValue()
        cyl_test.x(valueX)
        sph_cyl.x(valueX)

    def sliderY(widget, event):
        valueY = widget.GetRepresentation().GetValue()
        cyl_test.y(valueY)
        sph_cyl.y(valueY)

    def sliderZ(widget, event):
        valueZ = widget.GetRepresentation().GetValue()
        cyl_test.z(valueZ)
        sph_cyl.z(valueZ)

    def sliderRotX(widget, event):
        valueRX = widget.GetRepresentation().GetValue()
        rotX.append(valueRX)
        cyl_test.rotateX(valueRX, rad=False)
        sph_cyl.rotateX(valueRX, rad=False)

    def sliderRotY(widget, event):
        valueRY = widget.GetRepresentation().GetValue()
        rotY.append(valueRY)
        cyl_test.rotateY(valueRY, rad=False)
        sph_cyl.rotateY(valueRY, rad=False)

    def sliderRotZ(widget, event):
        valueRZ = widget.GetRepresentation().GetValue()
        rotZ.append(valueRZ)
        cyl_test.rotateZ(valueRZ, rad=False)
        sph_cyl.rotateZ(valueRZ, rad=False)

    def sliderAlphaMeshOut(widget, event):
        valueAlpha = widget.GetRepresentation().GetValue()
        mesh.alpha(valueAlpha)

    lbox = vedo.LegendBox([mesh], font=leg_font, width=leg_width, padding=1)
    vp = vedo.Plotter(N=1, axes=8)
    vp.add_icon(logo, pos=(0.85,0.75), size=0.10)
    
    cyl_test = vedo.Cylinder(pos = centre, r = radius, height = height, 
                             axis = normal, c = color, cap = True, res = res)
    sph_cyl = vedo.Sphere(pos = centre, r=4, c='gold')

    if option[0]: #sliderX
        vp.addSlider2D(sliderX, xval[0], xval[1], value=centre[0],
                    pos=[(0.1,0.15), (0.3,0.15)], title='- > x position > +', 
                    c='crimson', title_size=txt_slider_size)
    if option[1]: #sliderY
        vp.addSlider2D(sliderY, yval[0], yval[1], value=centre[1],
                    pos=[(0.4,0.15), (0.6,0.15)], title='- > y position > +', 
                    c='dodgerblue', title_size=txt_slider_size)
    if option[2]: #sliderZ
        vp.addSlider2D(sliderZ, zval[0], zval[1], value=centre[2],
                    pos=[(0.7,0.15), (0.9,0.15)], title='- > z position > +', 
                    c='limegreen', title_size=txt_slider_size)
    if option[3]: #sliderRotX
        vp.addSlider2D(sliderRotX, -1, +1, value=0,
                    pos=[(0.1,0.05), (0.3,0.05)], title='- > x rotation > +', 
                    c='deeppink', title_size=txt_slider_size)
    if option[4]: #sliderRotY
        vp.addSlider2D(sliderRotY, -1, +1, value=0,
                    pos=[(0.4,0.05), (0.6,0.05)], title='- > y rotation > +', 
                    c='gold', title_size=txt_slider_size)
    if option[5]: #sliderRotZ
        vp.addSlider2D(sliderRotZ, -1, +1, value=0,
                    pos=[(0.7,0.05), (0.9,0.05)], title='- > z rotation > +', 
                    c='teal', title_size=txt_slider_size)

    vp.addSlider2D(sliderAlphaMeshOut, xmin=0.01, xmax=0.99, value=0.01,
               pos=[(0.95,0.25), (0.95,0.45)], c="blue", title="Mesh Opacity")

    text = filename+'\nDefine disc position to '+txt+'.\nMake sure it cuts all the tissue effectively separating it into individual segments.\nClose the window when done.\n[Note: The initially defined disc radius is '+str(radius)+'um.\nIf you are not happy with the disc radius, you will be able to modify it just before proceeding with the cut].'
    txt = vedo.Text2D(text, c=txt_color, font=txt_font, s=txt_size)
    vp.show(mesh, cyl_test, sph_cyl, lbox, txt, azimuth=45, elevation=45, zoom=zoom, interactive=True)

    return cyl_test, sph_cyl, rotX, rotY, rotZ

#%% - Mesh Operations
#%% func - get_pts_at_plane
def get_pts_at_plane (points, pl_normal, pl_centre, tol=2, addData = []):
    """
    Function to get points within mesh at certain heights (y positions) to create kspline

    """
    pts_cut = []
    data_cut = []

    d = pl_normal.dot(pl_centre)
    #print('d for tol:', d)
    d_range = [d-tol, d+tol]
    #print('d range:', d_range)
    d_range.sort()

    for i, pt in enumerate(points):
        d_pt = pl_normal.dot(pt)
        if d_pt>d_range[0] and d_pt<d_range[1]:
            pts_cut.append(pt)
            if addData != []:
                data_cut.append(addData[i])

    pts_cut = np.asarray(pts_cut)
    data_cut = np.asarray(data_cut)

    return pts_cut, data_cut

#%% - Math operations 
#%% func - new_normal_3DRot
def new_normal_3DRot (normal, rotX, rotY, rotZ):
    '''
    Function that returns a vector rotated around X, Y and Z axis

    Parameters
    ----------
    normal : numpy array
        np array with the x,y,z coordinates of the original's plane axis
    rotX : list of floats
        List of angles (deg) of the resulting rotation around the x-axis.
    rotY : list of floats
        List of angles (deg) of the resulting rotation around the Y-axis.
    rotZ : list of floats
        List of angles (deg) of the resulting rotation around the Z-axis.

    Returns
    -------
    normal_rotZ : numpy array
        np array with the x,y,z coordinates of the rotated axis

    '''

    ang_X = np.radians(sum(rotX))
    ang_Y = np.radians(sum(rotY))
    ang_Z = np.radians(sum(rotZ))
    # print(sum(rotX), sum(rotY), sum(rotZ))

    normal_rotX = (np.dot(rotation_matrix(axis = [1,0,0], theta = ang_X), normal))
    normal_rotY = (np.dot(rotation_matrix(axis = [0,1,0], theta = ang_Y), normal_rotX))
    normal_rotZ = (np.dot(rotation_matrix(axis = [0,0,1], theta = ang_Z), normal_rotY))

    return normal_rotZ

#%% func - rotation_matrix
def rotation_matrix(axis, theta):
    """
    Returns the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    https://stackoverflow.com/questions/6802577/rotation-of-3d-vector

    Parameters
    ----------
    axis : numpy array
        np array with the x,y,z coordinates of the original's plane axis
    theta : float
        Angle of rotation around the axis.

    Returns
    -------
    numpy array
        Rotation matrix.

    """

    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d

    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

#%% func - rotate_plane2im
def rotate_plane2im (pl_centre_o, pl_normal_o, chNS = False):
    """
    Function that rotates the planes defined in the surface reconstructions to the images mask

    """
    pl_centre = copy.deepcopy(pl_centre_o)
    pl_normal = copy.deepcopy(pl_normal_o)
    if not chNS:
        pl_im_centre = (np.dot(rotation_matrix(axis = [0,0,1], theta = np.radians(90)), pl_centre))
        pl_im_normal = (np.dot(rotation_matrix(axis = [0,0,1], theta = np.radians(90)), pl_normal))
    else:
        pl_im_centre = (np.dot(rotation_matrix(axis = [1,0,0], theta = np.radians(90)), pl_centre))
        pl_im_normal = (np.dot(rotation_matrix(axis = [1,0,0], theta = np.radians(90)), pl_normal))

    plane_im = vedo.Plane(pos=pl_im_centre,normal=pl_im_normal, s=(500,500)).color("blue").alpha(0.5).legend('Rotated plane to images')
    
    pl_dict = {'pl_normal': pl_im_normal,
               'pl_centre': pl_im_centre}
    
    return plane_im, pl_dict

#%% func - unit_vector
def unit_vector(v):
    """
    Function that returns the unit vector of the vector given as input

    Parameters
    ----------
    v : numpy array
        np array with the x,y,z coordinates of a plane axis

    Returns
    -------
    numpy array
        np array with the x,y,z coordinates of a unitary plane axis

    """

    #mag = math.sqrt(sum(i**2 for i in x))
    sqrs = [i**2 for i in v]
    mag = math.sqrt(sum(sqrs))
    v_unit = [j/mag for j in v]

    return np.asarray(v_unit)

#%% func - order_pts
def order_pts (points):
    """
    Function that returns an ordered array of points
    """

    center_pt = np.mean(points, axis=0)
    cent_pts = np.zeros_like(points)
    for num in range(len(points)):
        cent_pts[num][0]=points[num][0]-center_pt[0]
        cent_pts[num][2]=points[num][2]-center_pt[2]

    angle_deg = np.zeros((len(points),1))
    for num, pt in enumerate(cent_pts):
        angle_deg[num] = np.arctan2(pt[2],pt[0])*(180/np.pi)

    index_sort = np.argsort(angle_deg, axis=0)
    ordered_pts = np.zeros_like(points)
    for i, pos in enumerate(index_sort):
        ordered_pts[i]=points[pos]

    return ordered_pts, angle_deg

#%% func - get_interpolated_pts
def get_interpolated_pts(points, nPoints):
    """
    Function that interpolates input points

    """

    minx, miny, minz = np.min(points, axis=0)
    maxx, maxy, maxz = np.max(points, axis=0)
    maxb = max(maxx - minx, maxy - miny, maxz - minz)
    smooth = 0.5*maxb/2  # must be in absolute units

    x = points[:,0]
    y = points[:,1]
    z = points[:,2]

    #https://stackoverflow.com/questions/47948453/scipy-interpolate-splprep-error-invalid-inputs
    okay = np.where(np.abs(np.diff(x)) + np.abs(np.diff(y)) + np.abs(np.diff(z)) > 0)
    xp = np.r_[x[okay], x[-1]]
    yp = np.r_[y[okay], y[-1]]
    zp = np.r_[z[okay], z[-1]]

    tck, u = splprep([xp, yp, zp], s=smooth)
    new_array = np.linspace(0, 1, nPoints)
    xnew, ynew, znew = splev(new_array, tck)

    pts_interp = np.c_[xnew, ynew, znew]

    return pts_interp
#%% 


#%% Module loaded
print('morphoHeart! - Loaded funcMeshes')