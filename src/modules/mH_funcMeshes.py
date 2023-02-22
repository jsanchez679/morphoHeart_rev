'''
morphoHeart_funcMeshes

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
import os
from datetime import datetime
from pathlib import Path, WindowsPath
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

path_fcMeshes = os.path.abspath(__file__)
path_mHImages = Path(path_fcMeshes).parent.parent.parent / 'images'


#%% Set default fonts and sizes for plots
txt_font = 'Dalim'
leg_font = 'LogoType' # 'Quikhand' 'LogoType'  'Dalim'
leg_width = 0.18
leg_height = 0.2
txt_size = 0.7
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
        elif isinstance(obj, WindowsPath):
            return str(obj)
        else:
            return super(NumpyArrayEncoder, self).default(obj)
        
#%% ##### - Other Imports - ##################################################
# from ...config import dict_gui
from .mH_funcBasics import ask4input, get_by_path, alert
# from .mH_classes import ImChannelNS#, Mesh_mH

alert_all = True
heart_default = False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default, 
            'colorMap': 'turbo'}
            
#%% - morphoHeart B functions
#%% func - clean_intCh
def clean_intCh(organ, plot=False):
    # Clean channels
    ch_ext, ch_int = organ.get_extIntChs()
    
    #Check workflow status
    workflow = organ.workflow
    process = ['ImProc', ch_int.channel_no,'E-CleanCh','Status']
    check_proc = get_by_path(workflow, process)
    if check_proc == 'DONE':
        q = 'You already cleaned the stacks of this channel ('+ ch_int.user_chName+') with the '+ch_ext.user_chName+'. Do you want to clean them again?'
        res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
        clean_ch = ask4input(q, res, bool)
    else: 
        q = 'Do you want to clean the '+ch_int.user_chName+' with the '+ch_ext.user_chName+'?'
        res = {0: 'no, thanks',1: 'yes, please!'}
        clean_ch = ask4input(q, res, bool)
        
    if clean_ch:
        ch_int_name = ch_int.channel_no
        obj1 = [(organ.obj_meshes[ch_int_name+'_int'].mesh.clone()), 
                (organ.obj_meshes[ch_int_name+'_ext'].mesh.clone()),
                (organ.obj_meshes[ch_int_name+'_tiss'].mesh.clone())]
        q = 'Select the mask you would like to use to clean the '+ch_int.user_chName+':'
        res = {0: 'Just the tissue layer of the '+ch_ext.user_chName,1: '(Recommended) The inverted internal segmentation of the '+ch_ext.user_chName+' (more profound cleaning).'}
        inverted = ask4input(q, res, bool)
        if not hasattr(ch_ext, 's3_ext'):
            s3_mask = ch_ext.load_chS3s(cont_types = ['ext'])
        if not hasattr(ch_int, 's3_ext'):
            ch_int.load_chS3s(cont_types = ['tiss','int','ext'])
        s3_mask = ch_ext.s3_ext
        ch_int.ch_clean(s3_mask=s3_mask, inverted=inverted, plot=plot, proceed=True)
       
        print('\n---RECREATING MESHES CHANNEL 2 WITH CLEANED ENDOCARDIUM---')
        meshes_out = ch_int.s32Meshes(cont_types=['int', 'ext', 'tiss'], new_set=True)
        
        # Plot cleaned ch2
        obj2 = []
        for mesh in meshes_out:
            obj2.append(mesh.mesh)
        
        txt = [(0, organ.user_organName + ' - Original'), (3,'Cleaned Meshes')]
        plot_grid(obj=obj1+obj2, txt=txt, axes=5)
  
    else: 
        meshes_out = []
        for mesh in organ.obj_meshes:
            if ch_int.channel_no in mesh:
                meshes_out.append(organ.obj_meshes[mesh])
    

#%% func - s32Meshes
def s32Meshes(organ, gui_keep_largest:dict, rotateZ_90=True):
    
    # Check workflow status
    workflow = organ.workflow
    meshes_out = []
    for ch in organ.obj_imChannels.keys(): 
        print('\n---CREATING MESHES ('+ch+')---')
        im_ch = organ.obj_imChannels[ch]
        process = ['MeshesProc','A-Create3DMesh', im_ch.channel_no]
        mesh_done = [get_by_path(workflow, process+[cont]+['Status']) for cont in ['tiss', 'int', 'ext']]
        if not all(flag == 'DONE' for flag in mesh_done):
            new_set = True
        else: 
            new_set = False
            
        meshes = im_ch.s32Meshes(cont_types=['int', 'ext', 'tiss'],
                                        keep_largest=gui_keep_largest[im_ch.channel_no],
                                        rotateZ_90 = True, new_set = new_set)
        meshes_out.append(meshes)
      
    txt = [(0, organ.user_organName)]
    obj = []
    for meshes in meshes_out:
        for mesh in meshes: 
            obj.append((mesh.mesh))
            
    plot_grid(obj=obj, txt=txt, axes=5)

#%% func - select_meshes2trim
def select_meshes2trim(organ):
    
    names_mesh_tiss = [name for name in organ.obj_meshes if 'tiss' in name and 'NS' not in name]
    obj = []
    # meshes = []
    for name in names_mesh_tiss: 
        obj.append(organ.obj_meshes[name].mesh)
        # meshes.append(organ.obj_meshes[name])
    obj_t = tuple(obj)
    obj.append(obj_t)
    
    # obj = [(msh1_tiss.mesh),(msh2_tiss.mesh),(msh1_tiss.mesh, msh2_tiss.mesh)]
    text = organ.user_organName+"\n\nTake a closer look at both meshes and decide from which layer to cut\n the inflow and outflow. \nClose the window when done"
    txt = [(0, text)]
    plot_grid(obj=obj, txt=txt, axes=5, lg_pos='bottom-right')
    
    # return meshes

#%% func - trim_top_bottom_S3s
def trim_top_bottom_S3s(organ, cuts):
    
    #Get meshes to cut
    meshes = []
    no_cut = []
    for ch in organ.obj_imChannels.keys():
            if cuts['top']['chs'][ch] or cuts['bottom']['chs'][ch]:
                meshes.append(organ.obj_meshes[ch+'_tiss'])
            else: 
                no_cut.append(ch)
    # print(meshes, no_cut)
    #Check workflow status
    workflow = organ.workflow
    check_proc = []
    mesh_names = []
    for mesh in meshes: 
        process = ['ImProc', mesh.channel_no,'E-TrimS3','Status']
        check_proc.append(get_by_path(workflow, process))
        mesh_names.append(mesh.channel_no)
    if all(flag == 'DONE' for flag in check_proc):
        q = 'You already trimmed the top/bottom of '+ str(mesh_names)+'. Do you want to cut them again?'
        res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
        proceed = ask4input(q, res, bool)
    else: 
        proceed = True
        
    if proceed: 
        filename = organ.user_organName
        # User user input to select which meshes need to be cut
        cuts_names = {'top': {'heart_def': 'outflow tract','other': 'top'},
                    'bottom': {'heart_def': 'inflow tract','other': 'bottom'}}
        cuts_out = {'top': {'chs': {}},
                    'bottom': {'chs': {}}}
        
        cut_top = []; cut_bott = []; cut_chs = {}
        for ch in organ.imChannels.keys():
            cuts_out['top']['chs'][ch] = cuts['top']['chs'][ch]
            cuts_out['bottom']['chs'][ch] = cuts['bottom']['chs'][ch] 
            cut_chs[ch] = []
            
        cuts_flat = flatdict.FlatDict(cuts)
        for key in cuts_flat.keys():
            if 'top' in key: 
                cut_top.append(cuts_flat[key])
            if 'bot' in key: 
                cut_bott.append(cuts_flat[key])
            for ch in organ.imChannels.keys(): 
                if ch in key:
                    if cuts_flat[key]:
                        cut_chs[ch].append(key.split(':')[0])
                                   
        print('cut_chs:', cut_chs)
        print('cut_top:', cut_top)
        print('cut_bott:', cut_bott)
                
        if dict_gui['heart_default']: 
            name_dict =  'heart_def'     
        else: 
            name_dict = 'other'
           
        #Define plane to cut bottom
        if any(cut_bott):
            #Define plane to cut bottom
            plane_bott, pl_dict_bott = getPlane(filename=filename, 
                                                txt = 'cut '+cuts_names['bottom'][name_dict],
                                                meshes = meshes)    
            cuts_out['bottom']['plane_info_mesh'] = pl_dict_bott
            # Reorient plane to images (s3)
            plane_bottIm, pl_dict_bottIm = rotatePlane2Images(pl_dict_bott['pl_centre'], 
                                                              pl_dict_bott['pl_normal'])
            cuts_out['bottom']['plane_info_image'] = pl_dict_bottIm
            
        #Define plane to cut top
        if any(cut_top):
            #Define plane to cut top
            plane_top, pl_dict_top = getPlane(filename=filename, 
                                              txt = 'cut '+cuts_names['top'][name_dict],
                                              meshes = meshes)
            cuts_out['top']['plane_info_mesh'] = pl_dict_top
            # Reorient plane to images (s3)
            plane_topIm, pl_dict_topIm = rotatePlane2Images(pl_dict_top['pl_centre'], 
                                                            pl_dict_top['pl_normal'])
            cuts_out['top']['plane_info_image'] = pl_dict_topIm
            
        # print('cuts_out:', cuts_out)
        # Get the channels from the meshes to cut
        ch_meshes = {}
        ch_planes = []
        for mesh in meshes:
            ch_meshes[mesh.imChannel.channel_no] = mesh.imChannel
            ch_planes.append(mesh.imChannel.channel_no)
        
        #Update mH_settings with channels to be cut
        update_im = {}; update_mesh = {}
        for ch_a in ch_planes: 
            update_im[ch_a] = {'cut_image': None}
            update_mesh[ch_a] = {'cut_mesh': None}
        proc_im = ['wf_info','ImProc','E-TrimS3','Planes']
        organ.update_settings(proc_im, update_im, 'mH')
        proc_meshes = ['wf_info','MeshesProc','B-TrimMesh','Planes']
        organ.update_settings(proc_meshes, update_mesh, 'mH')
        # print('ch_planes:', ch_planes)
        
        #update workflow for channels that were not cut
        for ch_c in no_cut:
            proc_c = ['ImProc',ch_c,'E-TrimS3']
            for cont in ['int','ext','tiss']:
                organ.update_workflow(proc_c+['Info',cont,'Status'],'DONE-NoCut')
            organ.update_workflow(proc_c+['Status'],'DONE-NoCut')
        organ.check_status(process='ImProc')
        
        #Cut channel s3s and recreate meshes
        meshes_out = []
        for ch_b in ch_meshes: 
            im_ch = ch_meshes[ch_b]
            # print('cut_chs[ch_b]:',cut_chs[ch_b])
            im_ch.trimS3(cuts=cut_chs[ch_b], cuts_out=cuts_out)
            print('\n---RECREATING MESHES AFTER TRIMMING ('+ch_b+')---')
            meshes = im_ch.createNewMeshes(cont_types=['int', 'ext', 'tiss'],
                                           process = 'AfterTrimming', new_set=True)
            meshes_out.append(meshes)
        organ.mH_settings['cut_ch'] = cut_chs
        
        obj = []
        for ch_d in meshes_out:
            for mesh in ch_d: 
                obj.append(mesh.mesh)
                
        txt = [(0, organ.user_organName  + ' - Meshes after trimming')]
        plot_grid(obj=obj, txt=txt, axes=5)


#%% func - extractNSCh
def extractNSCh(organ, plot):
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
        plot_grid(obj=obj, txt=txt, axes=5)
        
        txt = [(0, organ.user_organName  + ' - Final reconstructed meshes')]
        obj = [organ.obj_meshes[key].mesh for key in organ.obj_meshes.keys() if 'tiss' in key]
        obj.append(tuple(obj))
        # obj = [(msh1_tiss.mesh),(msh2_tiss.mesh),(mshNS_tiss.mesh),(msh1_tiss.mesh, msh2_tiss.mesh, mshNS_tiss.mesh)]
        plot_grid(obj=obj, txt=txt, axes=5)
    
    else: 
        print('>> No layer between segments is being created as it was not setup by user!')
        alert('error_beep')

    
#%% func - cutMeshes4CL
def cutMeshes4CL(organ, tol, plot=True, printshow=True):
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
            ch_ext, _ = organ.get_extIntChs()
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
                            plane, pl_dict = getPlane(filename=filename, 
                                                        txt = 'cut '+cuts_names[pl_cut][name_dict],
                                                        meshes = [sm_msh]) 
                        else:
                            print('-Planes have been initialised for ', pl_cut)
                            # Planes have been initialised
                            plane, pl_dict = getPlane(filename=filename, 
                                                        txt = 'cut '+cuts_names[pl_cut][name_dict],
                                                        meshes = [sm_msh], def_pl = planes_info[pl_cut]) 
                        
                        plane_cuts[pl_cut]['plane'] = plane
                        plane_cuts[pl_cut]['pl_dict'] = pl_dict
                        #Update mH_settings
                        proc_wf = ['wf_info','MeshesProc', 'C-Centreline', 'Planes', pl_cut]
                        organ.update_settings(process = proc_wf, update = pl_dict, mH='mH')
                
                    print('> Cutting mesh: ', mH_msh.legend, '-', pl_cut)
                    pts2cut, _ = getPointsAtPlane(points = sm_msh.points(), 
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
                        plot_grid(obj=obj, txt=txt, axes=5)
                    
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
                plot_grid(obj=obj, txt=txt, axes=5)
                
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

#%% func - extractCL
def extractCL(organ, voronoi=False):
    
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
                vmtktxt, dir_npcl = code4vmtkCL(organ, ch, cont, voronoi)
                
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

#%% func- code4vmtkCL
def code4vmtkCL(organ, ch, cont, voronoi=False):
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

#%% func - loadCLData
def loadCLData(organ, ch, cont):
    
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
    
#%% func - createCLs
def createCLs(organ, nPoints = 300):
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
            cl_data = loadCLData(organ, ch, cont)
            #Get cl points from vmtk
            pts_cl = np.asarray(cl_data['Points'])
            # Interpolate points of original centreline
            pts_int_o = getInterpolatedPts(points=pts_cl, nPoints = nPoints)
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
            pts_int_opt1 = getInterpolatedPts(points=pts_all_opt1, nPoints = nPoints)
            # Create kspline with points
            kspl_opt1 = vedo.KSpline(pts_int_opt1, res = nPoints)
            kspl_opt1.color(cl_colors['Op1']).legend('(Op1) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 1'] = {'kspl': kspl_opt1, 'sph_bot': sph_outf_o, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add_inf, 
                                      'description': 'Point in meshesCut4Cl'}

            # - Option 2 (add point of extended original centreline)
            num = -10
            pts_int_opt2, pt2add2, sph_m2 = extendCL(pts_int_o, pts_withOutf, num, nPoints, plane_info)
            kspl_opt2 = vedo.KSpline(pts_int_opt2, res = nPoints)
            kspl_opt2.color(cl_colors['Op2']).legend('(Op2) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 2'] = {'kspl': kspl_opt2, 'sph_bot': sph_m2, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add2, 
                                      'description': 'Unit vector extension (-1,'+str(num)+')'}
            
            # - Option 3 (add point of extended original centreline midline between chamber centre and in/outf tract)
            num = -25
            pts_int_opt3, pt2add3, sph_m3 = extendCL(pts_int_o, pts_withOutf, num, nPoints, plane_info)
            kspl_opt3 = vedo.KSpline(pts_int_opt3, res = nPoints)
            kspl_opt3.color(cl_colors['Op3']).legend('(Op3) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 3'] = {'kspl': kspl_opt3, 'sph_bot': sph_m3, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add3, 
                                      'description': 'Unit vector extension (-1,'+str(num)+')'}
            
            # - Option 4 (add point of extended original centreline midline between chamber centre and in/outf tract)
            num = -50
            pts_int_opt4, pt2add4, sph_m4 = extendCL(pts_int_o, pts_withOutf, num, nPoints, plane_info)
            kspl_opt4 = vedo.KSpline(pts_int_opt4, res = nPoints)
            kspl_opt4.color(cl_colors['Op4']).legend('(Op4) CL_'+ch+'_'+cont).lw(5)
            dict_clOpt['Option 4'] = {'kspl': kspl_opt4, 'sph_bot': sph_m4, 
                                      'sph_top': sph_inf_o, 'pt2add': pt2add4,
                                      'description': 'Unit vector extension (-1,'+str(num)+')'}
            
            # - Option 5 (add point of extended original centreline midline between chamber centre and in/outf tract)
            num = -60
            pts_int_opt5, pt2add5, sph_m5 = extendCL(pts_int_o, pts_withOutf, num, nPoints, plane_info)
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
            pts_int_opt6 = getInterpolatedPts(points=pts_all_opt6f, nPoints = nPoints)
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
            
            plot_grid(obj=obj, txt=txt, axes=5)
            
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
            plot_grid(obj=obj_final, txt=txt_final, axes=5)
            
            # Update organ workflow
            proc_wft = ['MeshesProc', 'C-Centreline', 'buildCL', ch, cont, 'Status']
            organ.update_workflow(process = proc_wft, update = 'DONE')
            
        # Update organ workflow
        organ.update_workflow(process = process, update = 'DONE')
        organ.update_workflow(process = ['MeshesProc','C-Centreline','Status'], update = 'DONE')
        organ.check_status(process='MeshesProc')
        organ.save_organ()     

#%% func - extendCL
def extendCL(pts_int_o, pts_withOutf, num, nPoints, plane_info):
    
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
    pts_int_opt = getInterpolatedPts(points=pts_all_opt, nPoints = nPoints)
    
    return pts_int_opt, pt2add, sph_m10

#%% func - extractBallooning
def extractBallooning(organ, color_map, plot=False):

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
            
            mesh_ball, distance, min_max = getDistance2(mesh_to=mesh2ball, 
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
                plot_grid(obj=obj, txt=txt, axes=5)
            
            proc_wft = ['MeshesProc','D-Ballooning',ch, cont, 'Status']
            organ.update_workflow(process = proc_wft, update = 'DONE')
            proc_done.append('DONE')
        
        if len(proc_done) == len(ball_names):
            organ.update_workflow(process = process, update = 'DONE')
    
    else:
        return None

#%% func - extractThickness
def extractThickness(organ, color_map, plot=False):
    
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
            res = getThickness(organ, n_type, thck_values[n_type], color_map, plot)
            if res: 
                organ.update_workflow(process = process, update = 'DONE')
            
    
#%% func - getThickness
def getThickness(organ, n_type, thck_dict, color_map, plot=False):
    
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
        
        mesh_thck, distance, min_max = getDistance2(mesh_to=mesh_to, mesh_from=mesh_from, 
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
            plot_grid(obj=obj, txt=txt, axes=5)
        
        proc_wft = ['MeshesProc', thck_dict['method'], ch, cont, 'Status']
        proc_done.append('DONE')

    if len(proc_done) == len(thck_names):
        organ.update_workflow(process = proc_wft, update = 'DONE')
        return True
    else: 
        return False

#%% func - getDistance2Mesh
def getDistance2(mesh_to, mesh_from, from_name, color_map='turbo'):
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

#%% func - sphs_in_spline
def sphs_in_spline(kspl, colour=False, color_map='turbo', every=10):
    """
    Function that creates a group of spheres through a spline given as input.
    """
    if colour:
        # scalars->colors
        vcols = [vedo.colorMap(v, color_map, 0, len(kspl.points())) for v in list(range(len(kspl.points())))]  
    
    if every > 1:
        spheres_spline = []
        for num, point in enumerate(kspl.points()):
            if num % every == 0 or num == kspl.npoints-1:
                if colour:
                    sphere_pt = vedo.Sphere(pos=point, r=2, c=vcols[num]).addScalarBar(title='Centreline\nPoint Number')
                else:
                    sphere_pt = vedo.Sphere(pos=point, r=2, c='coral')
                spheres_spline.append(sphere_pt)
    else:
        kspl_new = vedo.KSpline(kspl.points(), res = round(kspl.npoints/every))
        spheres_spline = vedo.Spheres(kspl_new.points(), c='coral', r=2)

    return spheres_spline

#%% func - 

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
        
    
#%% - Plotting functions
#%% func - plot_grid
def plot_grid(obj:list, txt=[], axes=1, zoom=2, lg_pos='top-left',sc_side=350):
    
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
            pos = (0.1,2) # correct 
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
            lbox.append(vedo.LegendBox(list(obj[num]), font=leg_font, width=leg_width))
        else: 
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
    
    plot_grid(obj=obj, txt=txt, axes=5)

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
        plot_grid(obj, txt, axes=5)
        
#%% - Plane handling functions 
#%% func - getPlane
def getPlane(filename, txt:str, meshes:list, def_pl = None, 
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
        
    while True:
        # Create plane
        if def_pl != None:
            plane, normal, rotX, rotY, rotZ = getPlanePos(filename, txt, meshes_mesh, option, def_pl)
        else:
            plane, normal, rotX, rotY, rotZ = getPlanePos(filename, txt, meshes_mesh, option)
            
        # Get new normal of rotated plane
        normal_corrected = newNormal3DRot(normal, rotX, rotY, rotZ)
        # Get central point of new plane and create sphere
        pl_centre = plane.pos()
        sph_centre = vedo.Sphere(pos=pl_centre,r=2,c='black')
        # Build new plane to confirm
        plane_new = vedo.Plane(pos=pl_centre,normal=normal_corrected).color('green').alpha(1).legend('New Plane')

        normal_txt = str([' {:.2f}'.format(i) for i in normal_corrected]).replace("'","")
        centre_txt = str([' {:.2f}'.format(i) for i in pl_centre]).replace("'","")
        text = filename+'\n\nUser defined plane to '+ txt +'.\nPlane normal: '+normal_txt+' - Plane centre: '+centre_txt+'.\nClose the window when done.'
        txt2D = vedo.Text2D(text, c=txt_color, font=txt_font)

        # meshes_mesh = [mesh.mesh for mesh in meshes]
        # meshes_all = [plane, plane_new, sph_centre] + meshes_mesh
        # lbox = vedo.LegendBox(meshes_all, font=leg_font, width=leg_width, height=leg_height)
        vp = vedo.Plotter(N=1, axes=4)
        vp.add_icon(logo, pos=(0.8,0.05), size=0.25)
        vp.show(meshes_mesh, plane, plane_new, sph_centre, txt2D, at=0, viewup='y', azimuth=0, elevation=0, interactive=True)
        
        q = 'Are you happy with the defined plane to '+txt+'?'
        res = {0 :'no, I would like to define a new plane.', 1 :'yes, continue!'}
        happy = ask4input(q, res, bool)
        if happy:
            pl_dict = {'pl_normal': normal_corrected,
                       'pl_centre': pl_centre}
            # print(pl_dict)
            break

    return plane_new, pl_dict

#%% func - getPlanePos
def getPlanePos (filename, txt, meshes, option, 
                     def_pl= {'pl_normal': (0,1,0), 'pl_centre': []}):
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
    txt = vedo.Text2D(text, c=txt_color, font=txt_font)
    vp.show(meshes, plane, lbox, txt, viewup='y', zoom=1, interactive=True)

    return plane, normal, rotX, rotY, rotZ

#%% - Mesh Operations
#%% func - getPointsAtPlane
def getPointsAtPlane (points, pl_normal, pl_centre, tol=2, addData = []):
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
#%% func - newNormal3DRot
def newNormal3DRot (normal, rotX, rotY, rotZ):
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

#%% func - rotatePlane2Images
def rotatePlane2Images (pl_centre_o, pl_normal_o, chNS = False):
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

#%% func - getInterpolatedPts
def getInterpolatedPts(points, nPoints):
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