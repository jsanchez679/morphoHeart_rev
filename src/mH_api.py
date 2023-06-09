

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

#Here, check if process was already run,  
# update settings (wf_info) and create prompts and toggle buttons

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

    #Toggle Button
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
    
    #Toggle Button
    select_btn = getattr(controller.main_win, ch_name+'_selectcont')
    select_btn.setChecked(True)
    toggled(select_btn)

def run_keeplargest(controller):
    workflow = controller.organ.workflow
    fcM.s32Meshes(organ = controller.organ, gui_keep_largest=controller.main_win.gui_keep_largest, 
                  win = controller.main_win, rotateZ_90=controller.organ.mH_settings['setup']['rotateZ_90'])
    
    #Enable button for plot all
    plot_all = getattr(controller.main_win, 'keeplargest_plot')
    plot_all.setEnabled(True)

    #Toggle button
    select_btn = getattr(controller.main_win, 'keeplargest_play')
    select_btn.setChecked(True)
    toggled(select_btn)

def run_cleanup(controller):
    workflow = controller.organ.workflow
    # if proceed: #== None: 
    #     workflow = self.parent_organ.workflow['morphoHeart']
    #     s3s = [self.s3_int, self.s3_ext, self.s3_tiss]
    #     process = ['ImProc',self.channel_no,'E-CleanCh', 'Status']
    #     check_proc = get_by_path(workflow, process)
    #     if check_proc == 'DONE':
    #         q = 'You already cleanes the '+ self.user_chName+' with the '+s3_mask.im_channel.user_chName+'. Do you want to re-run this process?'
    #         res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
    #         proceed2 = ask4input(q, res, bool)
    #     else: 
    #         proceed2 = True
        
    # if proceed2: 

    fcM.clean_ch(organ = controller.organ, 
                 gui_clean = controller.main_win.gui_clean, 
                 win=controller.main_win, plot=False)

    #Enable button for plot all
    plot_all = getattr(controller.main_win, 'clean_plot')
    plot_all.setEnabled(True)

    #Toggle button
    select_btn = getattr(controller.main_win, 'cleanup_play')
    select_btn.setChecked(True)
    toggled(select_btn)
            
def run_trimming(controller):
    workflow = controller.organ.workflow

    # #Check workflow status
    # workflow = organ.workflow
    # check_proc = []
    # mesh_names = []
    # for mesh in meshes: 
    #     process = ['ImProc', mesh.channel_no,'E-TrimS3','Status']
    #     check_proc.append(get_by_path(workflow, process))
    #     mesh_names.append(mesh.channel_no)
    # if all(flag == 'DONE' for flag in check_proc):
    #     q = 'You already trimmed the top/bottom of '+ str(mesh_names)+'. Do you want to cut them again?'
    #     res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
    #     proceed = ask4input(q, res, bool)
    # else: 
    #     proceed = True
        
    # if proceed: 

    #  #Check workflow status
    #     workflow = self.parent_organ.workflow['morphoHeart']
    #     process = ['ImProc', self.channel_no, 'E-TrimS3','Status']
    #     check_proc = get_by_path(workflow, process)
    #     if check_proc == 'DONE':
    #         q = 'You already trimmed this channel ('+ self.user_chName+'). Do you want to re-run it?'
    #         res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
    #         proceed = ask4input(q, res, bool)
    #     else: 
    #         proceed = True
                
    #     if proceed: 
    meshes, no_cut, cuts_out = get_trimming_planes(organ = controller.organ,
                                                    gui_trim = controller.main_win.gui_trim,
                                                    win = controller.main_win)
    
    fcM.trim_top_bottom_S3s(organ = controller.organ, meshes = meshes, 
                            no_cut = no_cut, cuts_out = cuts_out,
                            win = controller.main_win)
    
    #Enable button for plot all
    plot_all = getattr(controller.main_win, 'trimming_plot')
    plot_all.setEnabled(True)

    #Toggle button
    select_btn = getattr(controller.main_win, 'trimming_play')
    select_btn.setChecked(True)
    toggled(select_btn)

def get_trimming_planes(organ, gui_trim, win): 
    filename = organ.user_organName
    #Get meshes to cut
    meshes = []
    no_cut = []
    for ch in organ.obj_imChannels.keys():
        for cont in ['tiss', 'ext', 'int']:
            if gui_trim['top']['chs'][ch][cont] or gui_trim['bottom']['chs'][ch][cont]:
                meshes.append(organ.obj_meshes[ch+'_'+cont])
                break
            else: 
                no_cut.append(ch+'_'+cont)
    # User user input to select which meshes need to be cut
    cuts_names = {'top': {'heart_def': 'outflow tract','other': 'top'},
                'bottom': {'heart_def': 'inflow tract','other': 'bottom'}}
    cuts_out = copy.deepcopy(gui_trim)

    cut_top = []; cut_bott = []; #cut_chs = {}
    cuts_flat = flatdict.FlatDict(gui_trim)
    print('A:',cuts_flat)
    for key in cuts_flat.keys():
        if 'top' in key and 'object' not in key: 
            cut_top.append(cuts_flat[key])
        if 'bot' in key and 'object' not in key: 
            cut_bott.append(cuts_flat[key])
        # for ch in organ.imChannels.keys(): 
        #     if ch in key:
        #         if ch not in cut_chs.keys(): 
        #             cut_chs[ch] = []
        #         else: 
        #             pass
        #         if cuts_flat[key]:
        #             cut_chs[ch].append(key.split(':')[0])
                                
    # print('cut_chs:', cut_chs)
    print('cut_top:', cut_top)
    print('cut_bott:', cut_bott)
            
    if mH_config.heart_default:
        name_dict =  'heart_def'     
    else: 
        name_dict = 'other'

    #Define plane to cut bottom
    if any(cut_bott):
        happy = False
        #Define plane to cut bottom
        while not happy: 
            plane_bott, pl_dict_bott = fcM.get_plane(filename=filename, 
                                                txt = 'cut '+cuts_names['bottom'][name_dict],
                                                meshes = meshes, win=win)  
            title = 'Happy with the defined plane?' 
            msg = 'Are you happy with the defined plane to cut '+cuts_names['bottom'][name_dict]+'?'
            items = {0: {'opt':'no, I would like to define a new plane.'}, 1: {'opt':'yes, continue!'}}
            prompt = Prompt_ok_cancel_radio(title, msg, items, parent=win)
            prompt.exec()
            print('output:', prompt.output, '\n')  
            if prompt.output[0] == 1: 
                happy = True

        cuts_out['bottom']['plane_info_mesh'] = pl_dict_bott
        # Reorient plane to images (s3)
        plane_bottIm, pl_dict_bottIm = fcM.rotate_plane2im(pl_dict_bott['pl_centre'], 
                                                            pl_dict_bott['pl_normal'])
        cuts_out['bottom']['plane_info_image'] = pl_dict_bottIm
        
    #Define plane to cut top
    if any(cut_top):
        happy = False
        #Define plane to cut top
        while not happy: 
            plane_top, pl_dict_top = fcM.get_plane(filename=filename, 
                                                txt = 'cut '+cuts_names['top'][name_dict],
                                                meshes = meshes, win=win)

            title = 'Happy with the defined plane?' 
            msg = 'Are you happy with the defined plane to cut '+cuts_names['top'][name_dict]+'?'
            items = {0: {'opt':'no, I would like to define a new plane.'}, 1: {'opt':'yes, continue!'}}
            prompt = Prompt_ok_cancel_radio(title, msg, items, parent=win)
            prompt.exec()
            print('output:', prompt.output, '\n')  
            if prompt.output[0] == 1: 
                happy = True
        
        cuts_out['top']['plane_info_mesh'] = pl_dict_top
        # Reorient plane to images (s3)
        plane_topIm, pl_dict_topIm = fcM.rotate_plane2im(pl_dict_top['pl_centre'], 
                                                        pl_dict_top['pl_normal'])
        cuts_out['top']['plane_info_image'] = pl_dict_topIm
        
    print('cuts_out:', cuts_out)
    return meshes, no_cut, cuts_out

def run_axis_orientation(controller):
    # #Check if the orientation has alredy been stablished
    #     if 'orientation' in self.mH_settings.keys(): 
    #         if 'ROI' in self.mH_settings['orientation'].keys():
    #             q = 'You already selected the ROI (organ) orientation for this organ. Do you want to re-assign it?'
    #             res = {0: 'no, continue with next step', 1: 'yes, re-assign it!'}
    #             proceed = ask4input(q, res, bool)
    #         else: 
    #             proceed = True
    #     else: 
    #         proceed = True
    #CHECK HERE WHICH ONE HAS BEEN RUN AND IF STACK WAS RUN, 
    # PROGRAM SO THAT THE STACK DATA DOESN'T GET REMOVED 
                
    workflow = controller.organ.workflow['morphoHeart']

    fcM.get_stack_orientation(organ = controller.organ,  
                              gui_orientation = controller.main_win.gui_orientation, 
                              win = controller.main_win)
    
    on_hold = fcM.get_roi_orientation(organ = controller.organ,
                                        gui_orientation = controller.main_win.gui_orientation,  
                                        win = controller.main_win)

    #Update Status in GUI
    process = ['MeshesProc', 'A-Create3DMesh', 'Set_Orientation', 'Status']
    controller.main_win.update_status(workflow, process, controller.main_win.orient_status)

    #Toggle button
    print('organ.on_hold:', on_hold)
    select_btn = getattr(controller.main_win, 'orientation_play')
    if not on_hold:
        controller.organ.on_hold = on_hold
        select_btn.setChecked(True)
    else: 
        controller.organ.on_hold = on_hold
        select_btn.setChecked(False)
    toggled(select_btn)

def run_chNS(controller):
    workflow = controller.organ.workflow['morphoHeart']
      # #Check workflow status
        # workflow = self.parent_organ.workflow
        # process = ['ImProc', self.channel_no,'D-S3Create','Status']
        # check_proc = get_by_path(workflow, process)
        # if check_proc == 'DONE':
        #     q = 'You already extracted the '+ self.user_chName+' from the negative space. Do you want to re-run this process?'
        #     res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
        #     proceed = ask4input(q, res, bool)
        # else: 
        #     proceed = True
            
        # if proceed: 

    fcM.extract_chNS(organ = controller.organ, 
                     rotateZ_90 = controller.organ.mH_settings['setup']['rotateZ_90'],
                     win = controller.main_win, 
                     plot = False)

    #Toggle button
    select_btn = getattr(controller.main_win, 'chNS_play')
    select_btn.setChecked(True)
    toggled(select_btn)

def run_centreline_clean(controller):

    workflow = controller.organ.workflow['morphoHeart']
    tol = controller.main_win.tolerance
    fcM.proc_meshes4cl(controller.organ, tol=tol, plot=plot)
    pass
