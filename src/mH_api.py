

'''
morphoHeart_API

Version: Jun 02, 2023
@author: Juliana Sanchez-Posada

'''
#%% Imports - ########################################################


#%% morphoHeart Imports - ##################################################
from .modules import mH_funcBasics as fcB
from .modules import mH_funcContours as fcC
from .modules import mH_funcMeshes as fcM
from .modules.mH_classes_new import *
from .gui.config import mH_config
from .gui.gui_classes import *


def close_cont(controller, ch_name):
    #Check workflow status
    workflow = controller.organ.workflow['morphoHeart']
    process = ['ImProc',ch_name,'Status']
    check_proc = get_by_path(workflow, process)
    close_done = fcC.checkWfCloseCont(workflow, ch_name)
    proceed = False
    dict_names = {'A-MaskChannel': 'Mask Stack', 'A-Autom': 'Close Contours Automatically', 
                    'B-Manual': 'Close Contours Manually', 'C-CloseInOut': 'Close Inflow/Outflow Tract(s)'}

    if all(close_done[flag] == 'DONE' for flag in close_done):
        #Ask if the user wants to re-run any of the processes
        ch_userName = controller.organ.imChannels[ch_name]['user_chName']
        title = 'Processes already performed in '+ch_userName
        msg = 'You already finished processing the contours of this channel ('+ch_userName+'). Do you want to re-run any of the processes?'
        items = {0: {'opt':'no, continue with next step'}, 1: {'opt':'yes, I would like to re-run a(some) process(es)!'}}
        controller.prompt = Prompt_ok_cancel_radio(title, msg, items, parent=controller.main_win)
        controller.prompt.exec()
        print('output:',controller.prompt.output, '\n')

        if controller.prompt.output[0] == 1:
            print('close_done (original):',close_done)
            controller.prompt = None
            # Here ask for processes that the user might want to re-run
            title = 'Select process(ess) to re-run'
            msg = 'Select the process(es) you want to run:'
            #- Get the items 
            items = {}
            for nn, key in enumerate(list(close_done.keys())): 
                items[key] = {'opt': dict_names[key]}
            # Prompt
            controller.prompt = Prompt_ok_cancel_checkbox(title, msg, items, parent=controller.welcome_win)
            controller.prompt.exec()
            for key in close_done.keys():
                if controller.prompt.output[key]: 
                    close_done[key] = 'NI'
            controller.prompt = None
            proceed = True
        else: 
            proceed = False
    elif check_proc == 'Initialised': 
        proceed = True
        print('Processing had been initialised!')
    else: 
        print('All new')
        print('\tChannel:',ch_name, '-CloseCont:', close_done)
        proceed = True
        
    if proceed: 
        fcC.closeContours(organ=controller.organ, ch_name=ch_name, close_done=close_done, win=controller.main_win)
        controller.main_win.win_msg('Contours of channel '+str(ch_name[-1])+ ' were successfully closed and saved!')
    else: 
        fcC.ImChannel(organ=controller.organ, ch_name=ch_name)
        controller.main_win.win_msg('Channel '+str(ch_name[-1])+ ' was loaded successfully!')

    close_cont_btn = getattr(controller.main_win, ch_name+'_closecont')
    close_cont_btn.setChecked(True)
    toggled(close_cont_btn)

def select_cont(controller, ch_name):
    #Check workflow status
    workflow = controller.organ.workflow['morphoHeart']
    process = ['ImProc', ch_name,'C-SelectCont','Status']
    check_proc = get_by_path(workflow, process)
    proceed = False
    if check_proc == 'DONE':
        #Ask if the user wants to re-run selecting contours
        ch_userName = controller.organ.imChannels[ch_name]['user_chName']
        title = 'Processes already performed in '+ch_userName
        msg = 'You already finished selecting the contours of this channel ('+ch_userName+'). Do you want to re-select them?'
        items = {0: {'opt':'no, continue with next step'}, 1: {'opt': 'yes, I would like to re-select them!'}}
        controller.prompt = Prompt_ok_cancel_radio(title, msg, items, parent=controller.main_win)
        controller.prompt.exec()
        if controller.prompt.output[0] == 1: 
            proceed = True
        else: 
            proceed = False
        controller.prompt = None
    else: 
        proceed = True
            
    if proceed: 
        im_o = controller.organ.obj_imChannels[ch_name]
        fcC.selectContours(organ=controller.organ, im_ch = im_o, win=controller.main_win)
    else: 
        layerDict = {}
        return layerDict
    
    select_btn = getattr(controller.main_win, ch_name+'_selectcont')
    select_btn.setChecked(True)
    toggled(select_btn)

def run_keeplargest(controller):
    fcM.s32Meshes(organ = controller.organ, gui_keep_largest=controller.main_win.gui_keep_largest, 
                  win = controller.main_win, rotateZ_90=controller.main_win.rotateZ_90)
    select_btn = getattr(controller.main_win, 'keeplargest_play')
    select_btn.setChecked(True)
    toggled(select_btn)