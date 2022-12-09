'''
morphoHeart_api_B

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
import pathlib
from pathlib import Path
import numpy as np
import os

#%% ##### - morphoHeart Imports - ##################################################
from morphoHeart_rev.src.mH_module_B.py import *

###



.morphoHeart_funcBasics import alert, ask4input, loadNPY, saveDF, loadDF, getInputNumbers, new_dir #, saveDict
from .morphoHeart_funcContours import save_s3, loadStacks, drawLine #, plt_s3, save_s3s

#%%

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

print(organ1.__dict__)
channel_no = 1
mesh_name = 'myocardium'
mesh_type = 'tissue'
mesh_color = 'teal'
mesh_alpha = 0.1
contours_source = np.array(range(10))

extractLargest = False
resolution = [0.22832596445005054, 0.22832596445005054, 0.652961]
npy_stack = np.load(os.path.join(str(organ1.dir_out), 'stacks_npy','LS09_F07_V_DS_1100_s3_ch0_all.npy'))
rotateZ_90 = True

m_Myoc = Mesh_mH(channel_no=channel_no,
                 mesh_name=mesh_name,
                 mesh_type=mesh_type, 
                 npy_stack=npy_stack,
                 resolution=resolution, 
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

tissue_name = 'myocardium'
im_orientation = 'ventral'
stack_npy_o = npy_stack

t_Myoc = ImTissue(channel_no=channel_no, tissue_name=tissue_name, resolution=resolution,
                  im_orientation=im_orientation, stack_npy_o=stack_npy_o)
print(t_Myoc.__dict__)