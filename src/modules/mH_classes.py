'''
morphoHeart_classes

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
import os
from datetime import datetime
import pathlib
from pathlib import Path
import numpy as np
import vedo as vedo
from skimage import measure, io

#%% ##### - Other Imports - ##################################################

#%% ##### - Authorship - #####################################################
__author__     = 'Juliana Sanchez-Posada'
__license__    = 'MIT'
__maintainer__ = 'J. Sanchez-Posada'
__email__      = 'julianasanchezposada@gmail.com'
__website__    = 'https://github.com/jsanchez679/morphoHeart'


#%% ##### - Class definition - ###############################################
class Project(): 
    '''
    Project class: 
    A new project would include a group or groups of Organs
    that are part of the same experiment and will then be averaged and/or
    compared. From this a project can contain just one organ or 
    multiple organs with different genotypes and stages. The settings to
    process all the organs contained in a project are set up when starting a 
    new project and can be amended if needed as the organs are processed.
    '''
    def __init__(self):
        
        self.create_mHName()
        self.dict_projInfo = {'proj_info': 
                                    {'mH_projName': self.mH_projName}}
        self.create_projWF()
        self.crete_projDir()

    def create_gralprojWF(self, user_proj_settings:dict):
        '''Create general project workflow'''

        self.user_projName = user_proj_settings['user_projName'].replace(' ', '_')
        self.user_projNotes = user_proj_settings['user_projNotes']
        self.results_dir = user_proj_settings['project_dir']

        gral_wf = {}
        gral_struct = []
        channels = []
        for ch_num in range(0, user_proj_settings['no_chs']):
            ch_str = 'ch'+str(ch_num+1)
            dict_info_ch = {'mH_chName':None,
                            'user_chName':user_proj_settings['name_chs'][ch_num].replace(' ', '_'),
                            'dir_cho': None, 
                            'colorCh_tiss': user_proj_settings['color_chs'][ch_num][0],
                            'colorCh_ext': user_proj_settings['color_chs'][ch_num][1],
                            'colorCh_int': user_proj_settings['color_chs'][ch_num][2],
                            'mask_ch': None,
                            'dir_mk': None}
            gral_wf[ch_str] = {}
            gral_wf[ch_str]['general_info'] = dict_info_ch
            gral_wf[ch_str]['measure'] = {}
            for cont in ['tissue', 'int', 'ext']:
                gral_wf[ch_str]['measure'][cont] = {}
                gral_wf[ch_str]['measure'][cont]['whole'] ={} #{'volume': True, 
                                                            # 'surf_area': True}
                gral_struct.append((ch_str,cont,'whole'))
            channels.append(ch_str)

        if user_proj_settings['ns']['layer_btw_chs']:
            ch_str = 'chNS'
            gral_wf['chNS']={}
            gral_wf['chNS']['general_info']={'mH_chName':None,
                                            'user_chName':user_proj_settings['ns']['user_nsChName'].replace(' ', '_'),
                                            'ch_ext': user_proj_settings['ns']['ch_ext'],
                                            'ch_int': user_proj_settings['ns']['ch_int'],
                                            'colorCh_tiss': user_proj_settings['ns']['color_chns'][0],
                                            'colorCh_ext': user_proj_settings['ns']['color_chns'][1],
                                            'colorCh_int': user_proj_settings['ns']['color_chns'][2]}
            gral_wf[ch_str]['measure'] = {}
            for cont in ['tissue', 'int', 'ext']:
                gral_wf[ch_str]['measure'][cont] = {}
                gral_wf[ch_str]['measure'][cont]['whole'] = {} #{'volume': True, 
                                                            # 'surf_area': True}
                gral_struct.append((ch_str,cont,'whole'))
            channels.append(ch_str)

        segments = []
        if user_proj_settings['segments']['cutLayersIn2Segments']:
            for ch_str in channels:
                print(ch_str)
                ch_segments = list(user_proj_settings['segments']['ch_segments'].keys())
                print(ch_segments)
                if ch_str in ch_segments:
                    print('in')
                    for s_num in range(0, user_proj_settings['segments']['no_segments']):
                        segm_str = 'segm'+str(s_num+1)
                        print(segm_str)
                        segments.append(segm_str)
                        for cont in user_proj_settings['segments']['ch_segments'][ch_str]:
                            gral_wf[ch_str]['measure'][cont][segm_str] = {} #{'volume': True, 
                                                                         #'surf_area': True}
                            gral_struct.append((ch_str,cont,segm_str))

        self.dict_gral_wf = gral_wf
        self.gral_struct = gral_struct
        self.channels = channels
        segments_new = list(set(segments))
        self.segments = segments_new #possible unsorted

    def create_table2select_meas_param(self):
        '''
        This function will create a dictionary with all the possible measurement parameters 
        a user can get based on the settings given when setting the initial project 
        (no_ch, no_segments and the corresponding channels from which the segments will be obtained, etc)
        The output of this function will help to set up the GUI table for the user to 
        modify the default selected parameters.
        '''
        channels = self.channels
        conts = ['tissue', 'int', 'ext']
        gral_struct_blank = []
        dict_params_blank = {}
        for ch_b in channels: 
            dict_params_blank[ch_b] = {}
            for cont_b in conts: 
                dict_params_blank[ch_b][cont_b] = {}

        for tup in self.gral_struct:
            ch, cont, segm = tup
            print(ch, cont, segm)
            dict_params_blank[ch][cont][segm] = {'volume': True, 
                                                    'surf_area': False}

            gral_struct_blank.append((ch,cont,segm,'volume'))
            gral_struct_blank.append((ch,cont,segm,'surf_area'))

            if cont in ['int', 'ext']:
                dict_params_blank[ch][cont][segm]['surf_area'] = True 
            if cont == 'tissue':
                if segm == 'whole': 
                    dict_params_blank[ch][cont][segm]['thickness int>ext'] = True
                    dict_params_blank[ch][cont][segm]['thickness ext>int'] = False

                    gral_struct_blank.append((ch,cont,segm,'thickness int>ext'))
                    gral_struct_blank.append((ch,cont,segm,'thickness ext>int'))
                else: 
                    dict_params_blank[ch][cont][segm]['thickness int>ext'] = False
                    dict_params_blank[ch][cont][segm]['thickness ext>int'] = False

                    gral_struct_blank.append((ch,cont,segm,'thickness int>ext'))
                    gral_struct_blank.append((ch,cont,segm,'thickness ext>int'))
            if segm == 'whole':
                dict_params_blank[ch][cont][segm]['centreline'] = True
                dict_params_blank[ch][cont][segm]['centreline_linlength'] = True
                dict_params_blank[ch][cont][segm]['centreline_looplength'] = True

                gral_struct_blank.append((ch,cont,segm,'centreline'))
                gral_struct_blank.append((ch,cont,segm,'centreline_linlength'))
                gral_struct_blank.append((ch,cont,segm,'centreline_looplength'))

        self.gral_struct_blank = gral_struct_blank
        return dict_params_blank

    def set_measure_param(self, user_params2meas:dict):
        '''
        This function will get the input of the updated selected parameters from the GUI and 
        will include those measurements in the dictionary of the project. This dictionary will then 
        be used as a workflow templete for all the Organs created within the project. 
        '''
        gral_wf_updated = self.dict_gral_wf
        gral_struct = self.gral_struct
        gral_struct_blank = self.gral_struct_blank

        for tup in gral_struct: #self.gral_struct:
            ch, cont, segm = tup
            print(ch, cont, segm)
            gral_wf_updated[ch]['measure'][cont][segm] = user_params2meas[ch][cont][segm]


    def set_project_status(self):
        '''
        This function will initialise the dictionary that will contain the workflow of the
        project. 
        '''
        # Project status
        self.dict_Workflow = {'ImProc': {},
                              'MeshesProc': {}}

    



    def addOrgan2Proj(self):



        # User selected analysis parameters 
        self.dict_UserPipeline = {'ns': 
                                    {'layer_btw_chs': False,
                                    'ch_ext': None,
                                    'ch_int': None,
                                    'mH_nsChName': None,
                                    'user_nsChName': None},
                                'segments': 
                                    {'cutLayersIn2Segments':False,
                                    'segments_no': None, 
                                    'user_segName1': None, 
                                    'mH_segName1': None,
                                    'user_segName2': None,
                                    'mH_segName2': None,},
                                'params2measure': None,
                                }

        self.organ = Organ(self)

    def create_mHName(self):
        now_str = datetime.now().strftime('%Y%m%d%H%M')
        self.mH_projName = 'mH_Proj-'+now_str
    
    def create_folders(self, dir_res:pathlib.WindowsPath):
        # set_dir_res()
        folder_name = 'R_'+self.user_projName
        self.dir_out = Path(os.path.join(dir_res,folder_name))
        self.dir_out.mkdir(parents=True, exist_ok=True)

class Organ():
    'Organ Class'
    
    def __init__(self, project:Project):
        self.mH_organName = self.create_mHName()
        self.parent_project = project
                 
    def updateOrgan(self, no_chs:int, stage='', strain='', genotype=''):
    
        self.no_chs = no_chs
        # Optional
        self.stage = stage
        self.strain = strain
        self.genotype = genotype

        self.create_folders()

    def create_folders(self):
        dirResults = ['dicts', 'stacks_npy', 'meshes', 'centreline', 'imgs_videos', 'csv_all']
        for num, direc in enumerate(dirResults):
            dir2create = self.parent_project.dir_out / direc
            dir2create.mkdir(parents=True, exist_ok=True)
        self.dir_res = self.parent_project.dir_out

    def create_mHName(self):
        now_str = datetime.now().strftime('%Y%m%d%H%M')
        self.mH_organName = 'mH_Organ-'+now_str

    #Get all the set mH variables in __init__
    def get_mH_organName(self):
        return self.mH_organName

    def get_user_organName(self):
        return self.user_organName

    def get_stage(self):
        return self.stage

    def get_strain(self):
        return self.strain

    def get_genotype(self):
        return self.genotype

    def get_dir_channels(self):
        return self.dir_channels

    def get_dir_res(self):
        return self.dir_res

    def set_meshes_dict(self, meshes_dict):
        self.meshes_dict = meshes_dict

    def get_meshes_dict(self):
        return self.meshes_dict
        
class ImChannel(): #channel
    'morphoHeart Image Channel Class'
    
    def __init__(self, channel_no:int, organ:Organ, user_chName:str, 
                 resolution:list, im_orientation:str, to_mask:bool,
                 dir_cho:pathlib.WindowsPath):
        
        self.channel_no = channel_no
        self.mH_chName = organ.mH_organName+'_ch0'+str(self.channel_no)
        self.user_chName = user_chName
        
        self.resolution = resolution
        self.im_orientation = im_orientation
        
        self.dir_cho = dir_cho
        self.to_mask = to_mask
        self.masked = False

        self.get_images_o()
        
    def get_channel_no(self):
        return self.channel_no
    
    def get_mH_chName(self):
        return self.mH_chName
    
    def get_user_chName(self):
        return self.user_chName
    
    def change_user_chName(self, new_user_chName):
        self.user_chName = new_user_chName
    
    def get_images_o(self) -> 'np.ndarray':
        images_o = io.imread(str(self.dir_cho))
        self.images_o = images_o
        self.images_pr = images_o
        self.stack_shape = images_o.shape
    
    def get_images_pr(self):
        return self.images_pr
    
    def get_resolution(self):
        return self.resolution
    
    def get_im_orientation(self):
        return self.im_orientation
        
    def get_stack_shape(self):
        return self.stack_shape
    
    def get_dir_cho(self):
        return self.dir_cho
        
    def mask_tissue(self, dir_mask:str):
        #Check better this function
        self.maskIm_dir = Path(dir_mask)
        maskSt = np.load(Path(self.maskIm_dir))
        if self.stack_shape == maskSt.shape:
            #Check the dimensions of the mask with those of the image
            stack_masked = np.copy(self.stack_npy_o)
            stack_masked[maskSt == False] = 0
            self.masked = True
        else: 
            print('self.stack_shape != maskSt.shape')
        return stack_masked

    def create_chS3s (self, organ:Organ, layerDict:dict):
        s3_int = ContStack(organ, self, cont_type='int')
        print(s3_int.__dict__)
        s3_int.s3_create(layerDict, self.cont_type)
        self.s3_int = s3_int

        s3_ext = ContStack(organ, self, cont_type='ext')
        print(s3_ext.__dict__)
        s3_ext.s3_create(layerDict, self.cont_type)
        self.s3_ext = s3_ext

        s3_tiss = ContStack(organ, self, cont_type='all')
        print(s3_tiss.__dict__)
        s3_tiss.s3_create(layerDict, self.cont_type)
        self.s3_tiss = s3_tiss

    def load_chS3s (self, organ:Organ):
        s3_int = ContStack(organ, self.channel_no, cont_type='int')
        print(s3_int.__dict__)
        s3_int.loadContStack(organ, self.channel_no, s3_int.cont_type)
        self.s3_int = s3_int

        s3_ext = ContStack(organ, self.channel_no, cont_type='ext')
        print(s3_ext.__dict__)
        s3_ext.loadContStack(organ, self.channel_no, s3_ext.cont_type)
        self.s3_ext = s3_ext

        s3_tiss = ContStack(organ, self.channel_no, cont_type='all')
        print(s3_tiss.__dict__)
        s3_tiss.loadContStack(organ, self.channel_no, s3_tiss.cont_type)
        self.s3_tiss = s3_tiss

class ContStack(): 
    'morphoHeart Contour Stack Class'
    def __init__(self, organ:Organ, channel_no:int, 
                 cont_type:str):

        self.cont_type = cont_type
        self.cont_name = str(channel_no)+'_'+self.cont_type
        print(self.cont_name)
        
    def s3_create(self, layerDict:dict, cont_type:str):
        x_dim = self.stack_shape[0]
        y_dim = self.stack_shape[1]
        z_dim = self.stack_shape[2]
        
        s3 = np.empty((x_dim,y_dim,z_dim+2))
        for pos, keySlc in enumerate(layerDict.keys()):
            if keySlc[0:3] == "slc":
                slcNum = int(keySlc[3:6])
                im_FilledCont = layerDict[keySlc][cont_type]
                s3[:,:,slcNum+1] = im_FilledCont
    
        s3 = s3.astype('uint8')
        if cont_type == 'int':
            self.s3 = s3
        elif cont_type == 'ext':
            self.s3 = s3
        elif cont_type == 'all' or cont_type == 'tiss':
            self.s3 = s3

    def loadContStack(self, organ:Organ, channel_no:int, cont_type:str):
        filename = organ.user_organName + '_s3_' + str(channel_no) + '_' + cont_type + '.npy'
        s3_dir = organ.dir_res / 'stacks_npy' / filename
        s3 = np.load(s3_dir)
        if cont_type == 'int':
            self.s3 = s3
        elif cont_type == 'ext':
            self.s3 = s3
        elif cont_type == 'all' or cont_type == 'tiss':
            self.s3 = s3

class Mesh_mH():
    'morphoHeart Mesh Class'
    
    def __init__(self, organ:Organ,imChannel:ImChannel, 
                 user_meshName:str, mesh_type:str, 
                 npy_mesh:np.ndarray, 
                 extractLargest:bool, rotateZ_90:bool):
        
        self.channel_no = imChannel.channel_no 
        self.user_meshName = user_meshName
        self.mesh_type = mesh_type
        self.mH_meshName = organ.mH_organName+'_ch0'+str(self.channel_no)+'_'+mesh_type
        
        # Attributes from ImChannel
        self.imchannel = imChannel #(resolution, mH_chName, user_chName)
        self.organ = Organ #(get_mH_organName, user_organName))
        
        self.create_mesh(npy_mesh, self.imchannel.resolution, extractLargest, rotateZ_90)
        
    def get_channel_no(self):
        return self.channel_no
    
    def get_user_meshName(self):
        return self.user_meshName
    
    def change_user_meshName(self, new_user_meshName):
        self.user_meshName = new_user_meshName
    
    def get_mesh_type(self):
        return self.mesh_type
    
    def get_mH_meshName(self):
        return self.mH_meshName
    
    def get_imchannel(self):
        return self.imchannel
    
    def get_organ(self):
        return self.organ
    
    def set_contours_source(self, contours_source):
        self.contours_source = contours_source
    
    def set_mesh_alpha(self, mesh_alpha):
        self.mesh_alpha = mesh_alpha
        self.mesh.alpha(self.mesh_alpha)
    
    def get_mesh_alpha(self):
        return self.mesh_alpha
        
    def set_mesh_color(self, mesh_color):
        self.mesh_color = mesh_color
        self.mesh.color(self.mesh_color)
        
    def get_mesh_color(self):
        return self.mesh_color
        
    def create_mesh(self, npy_mesh:np.ndarray, resolution:list, extractLargest:bool, rotateZ_90:bool) -> 'Mesh_mH':

        # Extract vertices, faces, normals and values of each mesh
        verts, faces, _, _ = measure.marching_cubes_lewiner(npy_mesh, spacing=resolution)
    
        # Create meshes
        mesh = vedo.Mesh([verts, faces])
        if extractLargest:
            mesh = mesh.extractLargestRegion()
        if rotateZ_90:
            mesh.rotateZ(-90)
        mesh.legend(self.user_meshName).wireframe()
        
        self.mesh = mesh
        #mesh = vedo.mesh.Mesh
        
    def get_mesh(self):
        try: 
            return self.mesh #confirmar con vedo
        except:
            return None
    
    def getCentreline(self): 
        pass

print('morphoHeart! - Loaded Module Classes')
