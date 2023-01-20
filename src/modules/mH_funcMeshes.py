'''
morphoHeart_funcBasics

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
import os
from pathlib import Path
import vedo as vedo

path_fcMeshes = os.path.abspath(__file__)
path_mHImages = Path(path_fcMeshes).parent.parent.parent / 'images'

#%% ##### - morphoHeart Imports - ##################################################
# from .mH_funcBasics import *
# from .mH_classes import *


#%%
def plot_grid(obj:list, txt =[], axes=1, font='LogoType', width=0.25):
    
    # Load logo
    path_logo = path_mHImages / 'logo-07.jpg'
    logo = vedo.Picture(str(path_logo))
    
    # Set logo position
    if len(obj)>3:
        pos = (0.1,2)
    else:
        pos = (0.1,1)
    
    # Create tuples for text
    post = [tup[0] for tup in txt]; txt_out = []; n = 0
    for num in range(len(obj)):
        if num in post:
            txt_out.append(vedo.Text2D(txt[n][1], c='#696969', font='Dalim', s=0.8))
            n += 1
        else: 
            txt_out.append(vedo.Text2D('', c='#696969', font='Dalim', s=0.8))
    
    # Now plot
    lbox = []
    vp = vedo.Plotter(N=len(obj), axes=axes)
    vp.add_icon(logo, pos=pos, size=0.25)
    for num in range(len(obj)):
        lbox.append(vedo.LegendBox([obj[num]], font=font, width=width))
        if num != len(obj)-1:
            vp.show(obj[num], lbox[num], txt_out[num], at=num)
        else: 
            vp.show(obj[num], lbox[num], txt_out[num], at=num, interactive=True)
            
#%% Module loaded
print('morphoHeart! - Loaded funcMeshes')