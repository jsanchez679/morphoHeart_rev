"""
morphoHeart_funcContours

Version: Feb 13, 2023
@author: Juliana Sanchez-Posada

"""
#%% ##### - Imports - ########################################################


#%% ##### - Other Imports - ##################################################
from .mH_funcBasics import ask4input, ask4inputList, get_by_path, alert
from .mH_classes_new import ImChannel
from ..gui.config import mH_config

#%% - morphoHeart A functions
#%% func - closeContours()
def closeContours(organ, ch_name:str, close_done:dict, win):

    if close_done['A-MaskChannel'] != 'DONE':
        im_ch = organ.create_ch(ch_name=ch_name)
        im_ch.maskIm()
        win.win_msg('Channel '+str(ch_name[-1])+ ' was successfully masked!')
    else: 
        im_ch = ImChannel(organ=organ, ch_name=ch_name)#, new=False)      
        win.win_msg('Channel '+str(ch_name[-1])+ ' was successfully loaded!') 
    print(ch_name,':', im_ch.__dict__)
    win.update_ch_progress()     
            
    # if close_done['A-Autom'] != 'DONE':
    #     im_ch.closeContours_auto()
    #     win.win_msg('Contours of channel '+str(ch_name[-1])+ 'have been automatically closed!')
    # win.update_ch_progress() 
        
    # if close_done['B-Manual'] != 'DONE':
    #     im_ch.closeContours_manual()
    #     win.win_msg('Contours of channel '+str(ch_name[-1])+ 'have been manually closed!')
    # win.update_ch_progress() 
        
    # if close_done['C-CloseInOut'] != 'DONE':
    #     im_ch.closeInfOutf()
    #     win.win_msg('The top and bottom contours of channel '+str(ch_name[-1])+ 'have been succesfully closed!')
    # win.update_ch_progress() 

#%% func - checkWfCloseCont
def checkWfCloseCont(workflow, ch_name):
    #Check if masking is part of the workflow
    if get_by_path(workflow, ['ImProc', ch_name, 'A-MaskChannel','Status']) != 'N/A': 
        close_done = {'A-MaskChannel': get_by_path(workflow, ['ImProc', ch_name, 'A-MaskChannel','Status'])}
    else: 
        close_done = {}

    for key_a in ['A-Autom', 'B-Manual', 'C-CloseInOut']:
        val = get_by_path(workflow, ['ImProc', ch_name, 'B-CloseCont','Steps', key_a, 'Status'])
        close_done[key_a] = val
    
    return close_done

#%% func - selectContours
def selectContours(organ, im_ch, win):
    
    layerDict = im_ch.selectContours()
    im_ch.create_chS3s(layerDict=layerDict, win=win)
    win.win_msg('Contour masks for channel '+str(im_ch.channel_no[-1])+ ' have been successfully created!')
    win.update_ch_progress() 


#%% Module loaded
print('morphoHeart! - Loaded funcContours')