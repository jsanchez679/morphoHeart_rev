'''
morphoHeart_funcBasics

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
import os
from pathlib import Path
import vedo as vedo
import numpy as np
import math
# from textwrap import wrap
import flatdict
from itertools import count

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

#%% ##### - Other Imports - ##################################################
# from ...config import dict_gui
from .mH_funcBasics import ask4input, get_by_path, alert
# from .mH_classes import ImChannel, Mesh_mH

alert_all=True
heart_default=False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}
            
#%% - morphoHeart B functions
#%% func - clean_intCh
def clean_intCh(organ):
    # Clean channels
    chs = list(organ.imChannels.keys())
    if len(chs)>1 and len(chs)<3:
        for ch in chs:
            if organ.mH_settings['general_info'][ch]['ch_relation'] == 'external':
                ch_ext = organ.obj_imChannels[ch]
            if organ.mH_settings['general_info'][ch]['ch_relation'] == 'internal':
                ch_int = organ.obj_imChannels[ch]
                
    #check the process has not been donde even before asking if you want to clean the channel
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
        q = 'Select the mask you would like to use to clean the '+ch_int.user_chName+':'
        res = {0: 'Just the tissue layer of the '+ch_ext.user_chName,1: '(Recommended) The inverted internal segmentation of the '+ch_ext.user_chName+' (more profound cleaning).'}
        inverted = ask4input(q, res, bool)
        plot = False
        ch_int.ch_clean(s3_mask=ch_ext.s3_ext, inverted=inverted, plot=plot, proceed=True)
        # print('>> Check Ch2 vs ChInt: \n',compare_nested_dicts(im_ch2.__dict__,ch_int.__dict__,'ch2','int'))
        
        print('\n---RECREATING MESHES CHANNEL 2 WITH CLEANED ENDOCARDIUM---')
        meshes_out = ch_int.s32Meshes(cont_types=['int', 'ext', 'tiss'])
        # msh2_int2, msh2_ext2, msh2_tiss2 = meshes_out
        
        # Plot cleaned ch2
        obj1 = []
        obj2 = []
        for mesh in meshes_out:
            obj2.append(organ.obj_meshes[mesh.name].mesh)
            obj1.append(mesh.mesh)
        
        txt = [(0, organ.user_organName + ' - Original'), (3,'Cleaned Meshes')]
        plot_grid(obj=obj2+obj1, txt=txt, axes=5)
  
    else: 
        meshes_out = []
        for mesh in organ.obj_meshes:
            if ch_int.channel_no in mesh:
                meshes_out.append(organ.obj_meshes[mesh])
    
    return meshes_out

#%% func - trim_top_bottom_S3s
def trim_top_bottom_S3s(organ, cuts, meshes):
    
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
            
        # Get the channels from the meshes to cut
        ch_meshes = {}
        ch_planes = []
        for mesh in meshes:
            ch_meshes[mesh.imChannel.channel_no] = mesh.imChannel
            ch_planes.append(mesh.imChannel.channel_no)
        
        #Update mH_settings with channels to be cut
        update = {}
        for ch in ch_planes: 
            update[ch] = None
        proc = ['wf_info','ImProc','E-TrimS3','Planes']
        organ.update_settings(proc, update, 'mH')
        # print('ch_planes:', ch_planes)
            
        #Cut channel s3s
        for ch in ch_meshes: 
            im_ch = ch_meshes[ch]
            im_ch.trimS3(cuts=cut_chs[ch], cuts_out=cuts_out)
            
        organ.mH_settings['cut_ch'] = cut_chs

#%% func - cutMeshes4CL
def cutMeshes4CL(organ, plot=True):
    """
    Funtion that cuts the inflow and outflow tract of meshes from which 
    the centreline will be obtained.

    """
    
    filename = organ.user_organName
    # Get the meshes from which the centreline needs to be extracted
    cl_names = [item for item in organ.parent_project.mH_param2meas if 'centreline' in item]
    # Create lists with the smoothed mesh and another with tuples composed of 
    # the corresponding channel number and Mesh_mH
    msh4cl = []; chs4cl = []; names4cl = []
    for name in cl_names: 
        mesh = organ.obj_meshes[name[0]+'_'+name[1]]
        names4cl.append({'legend': mesh.legend, 'name': mesh.name})
        chs4cl.append(organ.obj_meshes[name[0]+'_'+name[1]].channel_no)
        mesh_out = mesh.mesh4CL()
        msh4cl.append(mesh_out)
        
    if plot: 
        txt = [(0, organ.user_organName  + ' - Smoothed meshes')]
        obj = [(mesh) for mesh in msh4cl]
        plot_grid(obj=obj, txt=txt, axes=5)
    
    # Get dictionary with initialised planes to cut top/bottom
    top_done = False; bot_done = False
    planes_info = {'top':None, 'bottom':None}
    for ch in set(chs4cl):
        dict2check = organ.mH_settings['wf_info']['ImProc']['E-TrimS3']['Planes'][ch]
        if 'top' in dict2check and not top_done:
            print('in top:', ch)
            planes_info['top'] = dict2check['top']['cut_mesh']
            top_done = True
        if 'bottom' in dict2check and not bot_done:
            print('in bot:', ch)
            planes_info['bottom'] = dict2check['bottom']['cut_mesh']
            bot_done = True
    
    # Set cut names 
    cuts_names = {'top': {'heart_def': 'outflow tract','other': 'top'},
                'bottom': {'heart_def': 'inflow tract','other': 'bottom'}}
    
    if dict_gui['heart_default']: 
        name_dict =  'heart_def'     
    else: 
        name_dict = 'other'

    # Assign colors to top and bottom splines and spheres
    color_cuts = {'bottom': 'salmon','top':'mediumseagreen' }
    # Number of meshes that need to be returned
    num_meshes_out = len(msh4cl)
    
    ksplines = []; spheres = []
    cuts = ['bottom', 'top']; cut_direction = [True, False]
    for n, cut, cut_dir in zip(count(),cuts, cut_direction):
        print(n, cut, cut_dir)
        if planes_info[cut] == None:
            #Planes have not been initialised
            print('-Planes have not been initialised for ', cut)
            plane, pl_dict = getPlane(filename=filename, 
                                        txt = 'cut '+cuts_names[cut][name_dict],
                                        meshes = [msh4cl[0]]) 
        else:
            print('-Planes have been initialised for ', cut)
            # Planes have been initialised
            plane, pl_dict = getPlane(filename=filename, 
                                        txt = 'cut '+cuts_names[cut][name_dict],
                                        meshes = [msh4cl[0]], def_pl = planes_info[cut]) 
        
        #Update mH_settings
        proc_wf = ['wf_info','MeshesProc', 'C-Centreline', 'Planes', cut]
        organ.update_settings(process = proc_wf, update = pl_dict, mH='mH')
        
        for n, msh, name in zip(count(), msh4cl[-num_meshes_out:], names4cl[-num_meshes_out:]):
            print('> Cutting mesh: ', name['legend'])
            pts2cut, _ = getPointsAtPlane(points = msh.points(), 
                                                   pl_normal = pl_dict['pl_normal'],
                                                   pl_centre = pl_dict['pl_centre'])
            ordpts, angle = order_pts(points = pts2cut)
            # Create spline around cut
            kspl = vedo.KSpline(ordpts, continuity=0, tension=0, bias=0, closed=True)
            kspl.color(color_cuts[cut]).legend('cut4CL_'+cut).lw(2)
            organ.add_object(kspl, proc='cut4cl', classif=cut, mesh_name= name['legend'])
            ksplines.append(kspl)
            
            # Get centroid of kspline to add to the centreline
            kspl_bounds = kspl.bounds()
            pt_centroid = np.mean(np.asarray(kspl_bounds).reshape((3, 2)),axis=1)
            sph_centroid = vedo.Sphere(pos=pt_centroid, r=2).legend('cut4CL_'+cut).color(color_cuts[cut])
            organ.add_object(sph_centroid, proc='cut4cl', classif=cut, mesh_name= name['legend'])
            spheres.append(sph_centroid)
            
            # Cutmesh using created plane
            msh_new = msh.clone().cut_with_mesh(plane, invert=cut_dir)
            msh_new = msh_new.extract_largest_region()
            msh_new.alpha(0.05).wireframe(True).legend(name['legend'])
            
            txt = [(0, organ.user_organName  + ' - Resulting mesh after cutting')]
            obj = [(msh_new, kspl, sph_centroid)]
            plot_grid(obj=obj, txt=txt, axes=5)
            
            msh4cl.append(msh_new)
            names4cl.append(name)
          
    msh4cl_final = msh4cl[-num_meshes_out:]
    names4cl_final = [name['legend']+'_cut4cl' for name in names4cl[-num_meshes_out:]]
    ch4cl_final = [name['name'] for name in names4cl[-num_meshes_out:]]
    
    if plot: 
        txt = [(0, organ.user_organName  + ' - Resulting meshes after cutting')]
        obj = [(mesh) for mesh in msh4cl_final]
        plot_grid(obj=obj, txt=txt, axes=5)
        
        
    ext = 'stl'; directory = organ.info['dirs']['centreline']
    for n, m4cl, name, ch_cont in zip(count(), msh4cl_final, names4cl_final, ch4cl_final):
        ch = ch_cont.split('_')[0]
        cont = ch_cont.split('_')[1]
        
        # Save mesh
        mesh_title = filename+"_"+name+"."+ext
        mesh_dir = directory / mesh_title
        mesh.write(str(mesh_dir))
        
        # Update mH_settings
        proc_set = ['wf_info', 'MeshesProc', 'C-Centreline',ch,cont]
        organ.update_settings(process = proc_set+['dir_cleanMesh'], update = mesh_dir, mH='mH')
        
        # Update organ workflow
        proc_wft = ['MeshesProc', 'C-Centreline', ch, cont, 'Status']
        organ.update_workflow(process = proc_wft, update = 'DONE')
        
    organ.check_status(process='MeshesProc')

    print('- All meshes have been saved!')
    alert('countdown')


    # return meshes[-num_meshes_out:]

#%% - Plotting functions
#%% func - plot_grid
def plot_grid(obj:list, txt =[], axes=1, lg_pos='top-left'):
    
    # Load logo
    path_logo = path_mHImages / 'logo-07.jpg'
    logo = vedo.Picture(str(path_logo))
    
    # Set logo position
    if lg_pos =='top-left':
        if len(obj)>3:
            pos = (0.1,2)
        else:
            pos = (0.1,1)
    else: 
        if len(obj)>3:
            pos = (0.1,2) # correct 
        else:
            pos = (0.8,0.05)
    
    # Create tuples for text
    post = [tup[0] for tup in txt]; txt_out = []; n = 0
    for num in range(len(obj)):
        if num in post:
            # txt_wrap = wrap(txt[n][1])
            # print(txt_wrap)
            txt_out.append(vedo.Text2D(txt[n][1], c=txt_color, font=txt_font, s=txt_size))
            n += 1
        else: 
            txt_out.append(vedo.Text2D('', c=txt_color, font=txt_font, s=txt_size))
    
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
        else: 
            vp.show(obj[num], lbox[num], txt_out[num], at=num, interactive=True)
            
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
def rotatePlane2Images (pl_centre, pl_normal, chNS = False):
    """
    Function that rotates the planes defined in the surface reconstructions to the images mask

    """
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

#%% 


#%% Module loaded
print('morphoHeart! - Loaded funcMeshes')