'''
morphoHeart_api_B

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
# import pathlib
from pathlib import Path
import numpy as np
import os
import vedo as vedo

#%% ##### - morphoHeart Imports - ##################################################
from modules import mH_classes as mCl
from modules import mH_funcBasics as fcBasics
from modules import mH_funcMeshes as fcMeshes

#%% Info coming from the gui (user's selection)
alert_all=True

user_name_in = 'Heart 01'
stage = '72-74hpf'
strain = 'myl7:lifeActGFP, fli1a:AcTag-RFP'
genotype = 'wt'
no_chs = 2
dir_channels = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS09_F07_V/Im_LS09_F07_V_DS_1100/')
dir_res = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS09_F07_V/')

# connection = 24
fcBasics.alert('woohoo', alert_all)

#%% API 

organ1 = mCl.Organ(user_name_in=user_name_in,
                   dir_channels=dir_channels,
                   dir_res=dir_res, 
                   no_chs = no_chs,
                   stage=stage,
                   strain=strain, 
                   genotype=genotype)

print(organ1.__dict__)

channel_no = 1
user_chName = 'myocardium'
im_orientation = 'ventral'
dir_cho = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS09_F07_V/Im_LS09_F07_V_DS_1100/LS09_F07_V_DS_1100_ch0_EDC.tif')
resolution = [0.22832596445005054, 0.22832596445005054, 0.652961]


chMyoc = mCl.ImChannel(channel_no=channel_no, 
                      organ=organ1,
                      user_chName=user_chName, 
                      resolution= resolution,
                      im_orientation=im_orientation, 
                      to_mask=False, 
                      dir_cho=dir_cho)
print(chMyoc.__dict__)

chMyoc.get_images_o()

user_meshName = 'myocardium'
mesh_type = 'tissue'
mesh_color = 'teal'
mesh_alpha = 0.1
contours_source = np.array(range(10))

extractLargest = False
npy_mesh = np.load(os.path.join(str(organ1.dir_res), 'stacks_npy','LS09_F07_V_DS_1100_s3_ch0_all.npy'))
rotateZ_90 = True

m_Myoc = mCl.Mesh_mH(organ=organ1, 
                     imChannel=chMyoc,
                     user_meshName = user_meshName,
                     mesh_type=mesh_type, 
                     npy_mesh=npy_mesh,
                     extractLargest=extractLargest, 
                     rotateZ_90=rotateZ_90)

print(m_Myoc.__dict__)

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

