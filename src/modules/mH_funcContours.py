"""
morphoHeart_funcContours

Version: Feb 13, 2023
@author: Juliana Sanchez-Posada

"""
#%% ##### - Imports - ########################################################


#%% ##### - Other Imports - ##################################################
from .mH_funcBasics import ask4input, ask4inputList, get_by_path, alert
from .mH_classes import ImChannel
from ..gui.config import mH_config

#%% - morphoHeart A functions
#%% func - closeContours()
def closeContours(organ, ch_name:str, close_done:list):
    
    if close_done[0] != 'DONE':
        im_ch = organ.load_TIFF(ch_name=ch_name)
        im_ch.maskIm()
    else: 
        im_ch = ImChannel(organ=organ, ch_name=ch_name)#, new=False)            
            
    # if close_done[1] != 'DONE':
    #     im_ch.closeContours_auto()
        
    # if close_done[2] != 'DONE':
    #     im_ch.closeContours_manual()
        
    # if close_done[3] != 'DONE':
    #     im_ch.closeInfOutf()
    
    return im_ch

#%% func - checkWfCloseCont
def checkWfCloseCont(workflow, ch_name):
    close_done = [get_by_path(workflow, ['ImProc',ch_name, 'A-MaskChannel','Status'])]
    for key_a in ['A-Autom', 'B-Manual', 'C-CloseInOut']:
        val = get_by_path(workflow, ['ImProc',ch_name,'B-CloseCont','Steps',key_a,'Status'])
        close_done.append(val)
    print('\tChannel:',ch_name, '-CloseCont:', close_done)
    
    return close_done

#%% func - selectContours
def selectContours(organ, im_ch):
        
    layerDict = im_ch.selectContours()
    im_ch.create_chS3s(layerDict=layerDict)
    
    return im_ch

#%% Module loaded
print('morphoHeart! - Loaded funcContours')