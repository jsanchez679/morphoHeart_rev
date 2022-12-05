'''
morphoHeart_classDef

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
import os
from datetime import datetime
from pathlib import Path
import numpy as np
import vedo as vedo
from skimage import measure

# from tkinter import filedialog
# from pathlib import Path


#%% ##### - Other Imports - ##################################################

#%% ##### - Authorship - #####################################################
__author__     = 'Juliana Sanchez-Posada'
__license__    = 'MIT'
__maintainer__ = 'J. Sanchez-Posada'
__email__      = 'julianasanchezposada@gmail.com'
__website__    = 'https://github.com/jsanchez679/morphoHeart'


#%% ##### - Class definition - ###############################################

class Organ():
    'Organ Class'
    
    def __init__(self, user_name_in=str, stage=str, strain=str, genotype=str, dir_input=str, dir_out=str):
        
        now_str = datetime.now().strftime('%Y%m%d%H%M')
        self.mH_name = 'mH_'+now_str
        
        user_name = user_name_in.replace(' ', '_')
        self.user_name = user_name
        self.stage = stage
        self.strain = strain
        self.genotype = genotype
        self.dir_input = Path(dir_input)
        
        # set_dir_out()
        
        # def set_dir_out(self, dir_out):
        dir_parent_out = os.path.join(dir_out,'Results_'+self.user_name)
        if os.path.isdir(dir_parent_out) == False:
            os.mkdir(dir_parent_out)

        dirResults = ['dicts', 'stacks_npy', 'meshes', 'centreline', 'imgs_videos', 'csv_all']
        for num, direc in enumerate(dirResults):
            dir2create = os.path.join(dir_parent_out, direc)
            if os.path.isdir(dir2create) == False:
                os.mkdir(dir2create)

        self.dir_out = Path(dir_parent_out)
        self.dir_parent_out = 'Results_'+self.user_name
        

    #Get all the set mH variables in __init__
    def get_mH_name(self):
        return self.mH_name

    def get_user_name(self):
        return self.user_name

    def get_stage(self):
        return self.stage

    def get_strain(self):
        return self.strain

    def get_genotype(self):
        return self.genotype

    def get_dir_in(self):
        return self.dir_input

    def get_dir_out(self):
        return self.dir_out

    def set_meshes_dict(self, meshes_dict):
        self.meshes_dict = meshes_dict

    def get_meshes_dict(self):
        return self.meshes_dict
    
    
class Mesh_mH(Organ):
    'morphoHeart Mesh Class'
    
    def __init__(self, channel_no=int, mesh_name=str, mesh_type=str, npy_stack=np.ndarray, resolution=list, 
                 extractLargest=bool, rotateZ_90=bool):
        
        self.channel_no = channel_no # should this come from tissue or tissues from which it was created - maybe not int?
        self.mesh_name = mesh_name
        self.mesh_type = mesh_type
        
        #self.create_mesh(npy_stack, resolution, extractLargest, rotateZ_90)
        
    def get_channel_no(self):
        return self.channel_no
    
    def get_mesh_name(self):
        return self.mesh_name
    
    def change_mesh_name(self, new_mesh_name):
        self.mesh_name = new_mesh_name
    
    def get_mesh_type(self):
        return self.mesh_type
    
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
        
    def create_mesh(self, npy_stack=np.ndarray, resolution=list, extractLargest=bool, rotateZ_90=bool) -> 'Mesh_mH':
        
        # Extract vertices, faces, normals and values of each mesh
        verts, faces, _, _ = measure.marching_cubes_lewiner(npy_stack, spacing=resolution)
    
        # Create meshes
        mesh = vedo.Mesh([verts, faces])
        if extractLargest:
            mesh = mesh.extractLargestRegion()
        if rotateZ_90:
            mesh.rotateZ(-90)
        mesh.legend(self.mesh_name).wireframe()
        
        self.mesh = mesh
        #mesh = vedo.mesh.Mesh
        
    def get_mesh(self):
        try: 
            return self.mesh #confirmar con vedo
        except:
            return None
    
    def getCentreline(self): 
        pass
        
        
class ImTissue(Organ): #channel
    'morphoHeart Tissue Class'
    
    def __init__(self, channel_no=int, tissue_name=str, resolution=list, 
                 im_orientation=str, stack_npy_o=np.ndarray):
        
        self.channel_no = channel_no
        self.tissue_name = tissue_name
        self.resolution = resolution
        self.stack_npy_o = stack_npy_o
        self.im_orientation = im_orientation
        self.masked = False
        self.stack_shape = stack_npy_o.shape
    
    def get_channel_no(self):
        return self.channel_no
    
    def get_tissue_name(self):
        return self.tissue_name
    
    def change_tissue_name(self, tissue_name):
        self.tissue_name = tissue_name
        
    def mask_tissue(self, dir_mask=str):#maybe this should ask for 
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
    
    def s3_create (self, contours_type=str, heartLayer=dict):
        """
        contours_type : str, optional 
            String indicating the imFilledContours to use.
            The default is str.
        heartLayer : TYPE, optional
            DESCRIPTION. The default is dict.
        """
        x_dim = self.stack_shape[0]
        y_dim = self.stack_shape[1]
        z_dim = self.stack_shape[2]
        
        s3 = np.empty((x_dim,y_dim,z_dim+2))
    
        for pos, keySlc in enumerate(heartLayer.keys()):
            if keySlc[0:3] == "slc":
                slcNum = int(keySlc[3:6])
                im_FilledCont = heartLayer[keySlc][contours_type]
                s3[:,:,slcNum+1] = im_FilledCont
    
        s3 = s3.astype('uint8')
    
        return s3


    

## testing##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

user_name_in = 'Heart 01'
stage = '72-74hpf'
strain = 'myl7:lifeActGFP, fli1a:AcTag-RFP'
genotype = 'wt'
dir_input = os.path.normpath('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS09_F07_V/Im_LS09_F07_V_DS_1100/')
dir_out = os.path.normpath('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS09_F07_V/')

organ1 = Organ(user_name_in=user_name_in,
               stage=stage,
               strain=strain, 
               genotype=genotype,
               dir_input=dir_input,
               dir_out=dir_out)

channel_no = 1
mesh_name = 'myocardium'
mesh_type = 'tissue'
mesh_color = 'teal'
mesh_alpha = 0.1
contours_source = np.array(range(10))

extractLargest = False
res = [0.22832596445005054, 0.22832596445005054, 0.652961]
npy_stack = np.load(os.path.join(str(organ1.dir_out), 'stacks_npy','LS09_F07_V_DS_1100_s3_ch0_all.npy'))
rotateZ_90 = True

m_Myoc = Mesh_mH(channel_no=channel_no,
                 mesh_name=mesh_name,
                 mesh_type=mesh_type)

m_Myoc.create_mesh(npy_stack,res, extractLargest, rotateZ_90=rotateZ_90)

vp = vedo.Plotter(N=1, axes=1)
vp.show(m_Myoc.mesh, at=0, zoom=1.2, interactive=True)

# m_Myoc.set_mesh_alpha(0.1)
m_Myoc.set_mesh_color('Teal')
m_Myoc.set_mesh_alpha(0.1)
        
vp = vedo.Plotter(N=1, axes=1)
vp.show(m_Myoc.mesh, at=0, zoom=1.2, interactive=True)

myoc = m_Myoc.mesh
m_Myoc.mesh.volume()
m_Myoc.mesh.area()


tissue_name = 'myocardium'
resolution = res
im_orientation = 'ventral'
stack_npy_o = npy_stack

#t_Myoc = ImTissue(channel_no=channel_no, tissue_name=tissue_name, resolution=resolution,
            #      im_orientation=im_orientation, stack_npy_o=stack_npy_o)
