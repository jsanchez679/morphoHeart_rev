"""
morphoHeart_funcContours

Version: Feb 13, 2023
@author: Juliana Sanchez-Posada

"""
#%% ##### - Imports - ########################################################


#%% ##### - Other Imports - ##################################################
from .mH_funcBasics import ask4input, ask4inputList, get_by_path, alert
from .mH_classes import ImChannel

#%% - morphoHeart A functions
#%% func - closeContours()
def closeContours(organ, ch_name:str):
    
    workflow = organ.workflow
    process = ['ImProc',ch_name,'Status']
    check_proc = get_by_path(workflow, process)
    close_done = checkWfCloseCont(workflow, ch_name)
    if all(flag == 'DONE' for flag in close_done):
        ch_userName = organ.imChannels[ch_name]['user_chName']
        q = 'You already finished processing the contours of this channel ('+ch_userName+'). Do you want to re-run any of the processes?'
        res = {0: 'no, continue with next step', 1: 'yes, I would like to re-run some process(es)!'}
        proceed_q = ask4input(q, res, bool)
        
        if proceed_q:
            # Here ask for processes that the user might want to re-run
            q = 'Select the process(es) you want to run:'
            res = {0: 'Mask Stack', 1: 'Close contours Automatically', 2: 'Close contours manually', 3: 'Close Inflow/Outflow'}
            num_proc = ask4inputList(q, res)
            for num in num_proc:
                close_done[num] = 'Re-run'
            proceed = True
            print(close_done)
        else: 
            proceed = False
            
    elif check_proc == 'Initialised': 
        proceed = True
        print('Processing had been initialised!')
    else: 
        close_done = ['NI']*4
        print('\tchannel:',ch_name, '-CloseCont:', close_done)
        proceed = True
        
    if proceed: 
        if close_done[0] != 'DONE':
            im_ch = organ.load_TIFF(ch_name=ch_name)
            im_ch.maskIm()
        else: 
            im_ch = ImChannel(organ=organ, ch_name=ch_name, new=False)            
            
        # if close_done[1] != 'DONE':
        #     im_ch.closeContours_auto()
            
        # if close_done[2] != 'DONE':
        #     im_ch.closeContours_manual()
            
        # if close_done[3] != 'DONE':
        #     im_ch.closeInfOutf()
    
    else: 
        im_ch = ImChannel(organ=organ, ch_name=ch_name, new=False)
    
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