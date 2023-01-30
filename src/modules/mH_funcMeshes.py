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
from .mH_funcBasics import ask4input # , alert
# from .mH_classes import ImChannel, Mesh_mH

alert_all=True
heart_default=False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}

#%% - General - Create Meshes after different processes
# #%% func - s32Meshes
# def s32Meshes(imChannel, keep_largest, rotateZ_90, new):
    
#     meshes_out = []
#     for mesh_type in ['int', 'ext', 'tiss']:
#         mesh = Mesh_mH(imChannel, mesh_type, keep_largest[mesh_type], rotateZ_90, new)
#         meshes_out.append(mesh)
        
#     return meshes_out

# #%% func - createNewMeshes
# def createNewMeshes(imChannel, keep_largest:bool, process:str, info, rotateZ_90:bool, new:bool):
    
#     workflow = imChannel.parent_organ.workflow
#     ch_no = imChannel.channel_no
#     meshes_out = s32Meshes(imChannel, keep_largest, rotateZ_90, new)
#     if process == 'AfterTrimming':
#         for mesh_type in ['int', 'ext', 'tiss']:
#             workflow['MeshesProc']['B-TrimMesh'][ch_no][mesh_type]['Status'] = 'DONE'
#             workflow['MeshesProc']['B-TrimMesh'][ch_no][mesh_type]['stack_dir'] = imChannel.contStack[mesh_type]['s3_dir']
#             workflow['MeshesProc']['B-TrimMesh'][ch_no][mesh_type]['keep_largest'] = keep_largest[mesh_type]
#             workflow['MeshesProc']['B-TrimMesh'][ch_no][mesh_type]['trim_settings'] = info[ch_no]
            
#     # Save organ
#     imChannel.parent_organ.save_organ()   
    
#     return meshes_out
            
#%% - morphoHeart B functions
#%% func - trim_top_bottom_S3s
def trim_top_bottom_S3s(organ, cuts, meshes):
    
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
    for mesh in meshes:
        ch_meshes[mesh.imChannel.channel_no] = mesh.imChannel
        
    #Cut ch1 s3s
    for ch in organ.imChannels.keys(): 
        im_ch = ch_meshes[ch]
        im_ch.trimS3(cuts=cut_chs[ch], cuts_out=cuts_out)
        
    return cut_chs
    
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
    
    while True:
        # Create plane
        if def_pl != None:
            plane, normal, rotX, rotY, rotZ = getPlanePos(filename, txt, meshes, option, def_pl)
        else:
            plane, normal, rotX, rotY, rotZ = getPlanePos(filename, txt, meshes, option)
            
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

        meshes_mesh = [mesh.mesh for mesh in meshes]
        # meshes_all = [plane, plane_new, sph_centre] + meshes_mesh
        # lbox = vedo.LegendBox(meshes_all, font=leg_font, width=leg_width, height=leg_height)
        vp = vedo.Plotter(N=1, axes=4)
        vp.add_icon(logo, pos=(0.8,0.05), size=0.25)
        vp.show(meshes_mesh, plane, plane_new, sph_centre, txt2D, at=0, viewup='y', azimuth=0, elevation=0, interactive=True)

        happy = ask4input('Are you happy with the defined plane to '+txt+'? \n\t [0]:no, I would like to define a new plane. \n\t [1]:yes, continue! >>>:', bool)
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
    
    meshes_mesh = [mesh.mesh for mesh in meshes]
    xmin, xmax, ymin, ymax, zmin, zmax = meshes_mesh[0].bounds()
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
        meshes_mesh[0].alpha(valueAlpha)

    lbox = vedo.LegendBox(meshes_mesh, font=leg_font, width=leg_width, padding=1)
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

    vp.addSlider2D(sliderAlphaMeshOut, xmin=0.01, xmax=0.99, value=0.01,
               pos=[(0.95,0.25), (0.95,0.45)], c='blue', 
               title=meshes[0].user_meshName+' Opacity', title_size=txt_slider_size)

    text = filename+'\n\nDefine plane position to '+txt+'. \nClose the window when done'
    txt = vedo.Text2D(text, c=txt_color, font=txt_font)
    vp.show(meshes_mesh, plane, lbox, txt, viewup='y', zoom=1, interactive=True)

    return plane, normal, rotX, rotY, rotZ

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

#%% func - selectCutS3sOptMxLoad
# def selectCutS3sOptMxLoad(filename, m_endo, m_myoc, dict_planes, resolution, dir_txtNnpy, save):
#     '''
#     Function used to cut inflow and/or outflow tract of the s3 masks (s3s2cut) given as input

#     Parameters
#     ----------
#     filename : str
#         Reference name given to the images of the embryo being processed (LSXX_FXX_X_XX_XXXX).
#     m_endo : mesh
#         Endocardial mesh. (vedo Mesh)
#     m_myoc : mesh
#         Myocardial mesh. (vedo Mesh)
#     dict_planes : dictionary
#         Initialised dictionary with planes information
#     resolution : list of floats
#         List with the x,y, z scaling values of the images taken. This information is taken from the metadata of the original file.
#     dir_txtNnpy : path
#         Path to the folder where the np arrays are saved.
#     save : boolean
#         True if you want to save the final masks, else False.

#     Returns
#     -------
#     meshes_cut : list of meshes (vedo Meshes)
#         List of all the surface reconstructions created with the cut masks
#     dict_planes :  dictionary
#         Resulting dictionary with planes information updated

#     '''

#     if 'CJ' in filename:
#         azimuth = -90
#         cj = True
#     else:
#         azimuth = 0
#         cj = False

#     s3_myoc_names_in = ['ch0_all','ch0_int', 'ch0_ext']
#     s3_myoc_names_out = ['ch0_cut', 'ch0_cut_int', 'ch0_cut_ext']
#     myoc_names = ['Myoc', 'Int.Myoc', 'Ext.Myoc']
#     s3_endo_names_in = ['ch1_cut', 'ch1_int', 'ch1_cut_ext']
#     s3_endo_names_out = ['ch1_cut', 'ch1_cut_int', 'ch1_cut_ext']
#     endo_names = ['Endo', 'Int.Endo', 'Ext.Endo']

#     cut_type = ['inflow', 'outflow']
#     cuts = []
#     pls_normal = []
#     pls_centre = []
#     cuts_selected = []

#     # Define what to cut from each layer
#     myoc_cuts = []; endo_cuts = []
#     # Define lists to save final meshes
#     meshes_myoc = []; meshes_endo = []

#     for cut in cut_type:
#         text = filename+'\n\n >> Take a closer look at the -' +cut + '- of both meshes \n\tto decide which layer to cut\n >> [0]:myoc/[1]:endo/[2]:both/[3]:none\n >> Close the window when done'
#         txt = Text2D(text, c='k', font= font)
#         settings.legendSize = .15
#         vp = Plotter(N=3, axes=4)
#         vp.show(m_myoc, txt, at=0, zoom=1)
#         vp.show(m_endo, at=1, zoom=1)
#         vp.show(m_myoc, m_endo, at=2, zoom=1, azimuth = azimuth, interactive=True)

#         q_cuts = ask4input('Select the layer from which you want to cut the -'+ cut + '- tract \n  [0]:myoc/[1]:endo/[2]:both/[3]:none?: ',int)
#         cuts.append(q_cuts)

#         if q_cuts == 0 or q_cuts == 1 or q_cuts == 2:
#             cuts_selected.append(cut)
#             # Get plane to cut
#             plane_cut, pl_cut_centre, pl_cut_normal = getPlane(filename = filename, type_cut = cut, info = '', mesh_in = m_endo,
#                                                                         mesh_out = m_myoc)
#             # Reorient plane to images (s3)
#             plane_im, pl_im_centre, pl_im_normal = rotatePlane2Images(pl_cut_centre, pl_cut_normal, type_cut = cut, cj = cj)
#             pls_normal.append(pl_im_normal); pls_centre.append(pl_im_centre)
#             #Save planes to dict
#             dict_planes = addPlanes2Dict(planes = [plane_cut, plane_im], pls_centre = [pl_cut_centre ,pl_im_centre],
#                                                     pls_normal = [pl_cut_normal, pl_im_normal], info = ['',''], dict_planes = dict_planes, print_txt = False)
#             if q_cuts == 0 or q_cuts == 2:
#                 myoc_cuts.append(cut)
#             if q_cuts == 1 or q_cuts == 2:
#                 endo_cuts.append(cut)

#     # Cut Myocardial layers
#     if len(myoc_cuts) == 2:
#         # Cut myocardial s3_all, s3_int, s3_ext
#         bar = Bar('- Cutting s3 - inf&outf (Myoc)', max = 3, suffix = suffix, check_tty=False, hide_cursor=False)
#         for n, s3_name, myoc_name, s3_name_out in zip(count(), s3_myoc_names_in, myoc_names, s3_myoc_names_out):
#             [s3], _ = loadStacks(filename = filename, dir_txtNnpy = dir_txtNnpy, end_name = [s3_name], print_txt = False)
#             s3 = cutInfAndOutfOptMx(s3, pls_normal, pls_centre, resolution, '(Myoc)')
#             mesh_out = getCutMesh(filename = filename, s3_cut = s3, resolution = resolution,
#                                         mesh_original = m_myoc, layer = myoc_name, plotshow = False)
#             meshes_myoc.append(mesh_out)
#             save_s3(filename = filename, s3 = s3, dir_txtNnpy = dir_txtNnpy, layer = s3_name_out)
#             bar.next()
#         bar.finish()

#     elif len(myoc_cuts) == 1:
#         index_myoc = cuts_selected.index(myoc_cuts[0])
#         # Cut myocardial s3_all, s3_int, s3_ext
#         bar = Bar('- Cutting s3 - ' + myoc_cuts[0]+' (Myoc)', max = 3, suffix = suffix, check_tty=False, hide_cursor=False)
#         for n, s3_name, myoc_name, s3_name_out in zip(count(), s3_myoc_names_in, myoc_names, s3_myoc_names_out):
#             [s3], _ = loadStacks(filename = filename, dir_txtNnpy = dir_txtNnpy, end_name = [s3_name], print_txt = False)
#             s3 = cutInfOrOutfOptMx(s3, pls_normal[index_myoc], pls_centre[index_myoc], resolution = resolution,
#                                                                       option = myoc_cuts[0], mesh_name = '(Myoc)')
#             mesh_out = getCutMesh(filename = filename, s3_cut = s3, resolution = resolution,
#                                         mesh_original = m_myoc, layer = myoc_name, plotshow = False)
#             meshes_myoc.append(mesh_out)
#             save_s3(filename = filename, s3 = s3, dir_txtNnpy = dir_txtNnpy, layer = s3_name_out)
#             bar.next()
#         bar.finish()
#     else:
#         print('- No cuts made to Myocardium!')
#         for n, s3_name, myoc_name in zip(count(), s3_myoc_names_in, myoc_names):
#             [s3], _ = loadStacks(filename = filename, dir_txtNnpy = dir_txtNnpy, end_name = [s3_name], print_txt = False)
#             mesh_out = getCutMesh(filename = filename, s3_cut = s3, resolution = resolution,
#                                         mesh_original = m_myoc, layer = myoc_name, plotshow = False)
#             meshes_myoc.append(mesh_out)

#     alert('whistle', 1)

#     # Cut Endocardial layers
#     if len(endo_cuts) == 2:
#         # Cut endocardial s3_all, s3_int, s3_ext
#         bar = Bar('- Cutting s3 - inf&outf (Endo)', max = 3, suffix = suffix, check_tty=False, hide_cursor=False)
#         for n, s3_name, endo_name, s3_name_out in zip(count(), s3_endo_names_in, endo_names, s3_endo_names_out):
#             [s3], _ = loadStacks(filename = filename, dir_txtNnpy = dir_txtNnpy, end_name = [s3_name], print_txt = False)
#             s3 = cutInfAndOutfOptMx(s3, pls_normal, pls_centre, resolution, '(Endo)')
#             mesh_out = getCutMesh(filename = filename, s3_cut = s3, resolution = resolution,
#                                         mesh_original = m_endo, layer = endo_name, plotshow = False)
#             meshes_endo.append(mesh_out)
#             save_s3(filename = filename, s3 = s3, dir_txtNnpy = dir_txtNnpy, layer = s3_name_out)
#             bar.next()
#         bar.finish()

#     elif len(endo_cuts) == 1:
#         index_endo = cuts_selected.index(endo_cuts[0])
#         # Cut myocardial s3_all, s3_int, s3_ext
#         bar = Bar('- Cutting s3 - ' + endo_cuts[0]+' (Endo)', max = 3, suffix = suffix, check_tty=False, hide_cursor=False)
#         for n, s3_name, endo_name, s3_name_out in zip(count(), s3_endo_names_in, endo_names, s3_endo_names_out):
#             [s3], _ = loadStacks(filename = filename, dir_txtNnpy = dir_txtNnpy, end_name = [s3_name], print_txt = False)
#             s3 = cutInfOrOutfOptMx(s3, pls_normal[index_endo], pls_centre[index_endo], resolution = resolution,
#                                                                       option = endo_cuts[0], mesh_name = '(Endo)')
#             mesh_out = getCutMesh(filename = filename, s3_cut = s3, resolution = resolution,
#                                         mesh_original = m_endo, layer = endo_name, plotshow = False)
#             meshes_endo.append(mesh_out)
#             save_s3(filename = filename, s3 = s3, dir_txtNnpy = dir_txtNnpy, layer = s3_name_out)
#             bar.next()
#         bar.finish()
#     else:
#         print('- No cuts made to Endocardium!')
#         for n, s3_name, endo_name in zip(count(), s3_endo_names_in, endo_names):
#             [s3], _ = loadStacks(filename = filename, dir_txtNnpy = dir_txtNnpy, end_name = [s3_name], print_txt = False)
#             mesh_out = getCutMesh(filename = filename, s3_cut = s3, resolution = resolution,
#                                         mesh_original = m_endo, layer = endo_name, plotshow = False)
#             meshes_endo.append(mesh_out)
#     alert('jump', 1)

#     meshes_cut = meshes_myoc+meshes_endo
#     text= filename+'\n\n >> Resulting meshes'
#     txt = Text2D(text, c='k', font= font)
#     settings.legendSize = .3
#     vp = Plotter(N=6, axes=10)
#     for i, mesh in enumerate(meshes_cut):
#         if i == 0:
#             vp.show(mesh, txt, at = i, zoom = 1.2)
#         elif i > 0 and i < 5:
#             vp.show(mesh, at = i, zoom = 1.2)
#         else:
#             vp.show(mesh, at = i, zoom = 1.2, interactive = True)

#     return meshes_cut, dict_planes


#%% 


#%% Module loaded
print('morphoHeart! - Loaded funcMeshes')