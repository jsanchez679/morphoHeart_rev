

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
def mask_channel(controller, ch_name): 
    # Workflow process
    workflow = controller.organ.workflow['morphoHeart']
    process = ['ImProc', ch_name, 'A-MaskChannel','Status']
    #Initial message
    controller.main_win.win_msg('Masking Channel '+str(ch_name[-1])+'!')
    #Get channel
    im_ch = controller.organ.obj_imChannels[ch_name]
    controller.main_win.win_msg('Masking Channel '+str(ch_name[-1]))
    #Mask channel
    im_ch.maskIm()
    #Update Status in GUI and in CH Progress 
    status_btn = getattr(controller.main_win, 'mask_'+ch_name+'_status')
    controller.main_win.update_status(workflow, process, status_btn)
    controller.main_win.update_ch_progress()
    #Toggle button
    getattr(controller.main_win, 'mask_'+ch_name+'_play').setChecked(True)
    #Win msg 
    controller.main_win.win_msg('Channel '+str(ch_name[-1])+' has been masked!')

def autom_close_contours(controller, ch_name): 

    # # Workflow process
    workflow = controller.organ.workflow['morphoHeart']
    process = ['ImProc', ch_name, 'B-CloseCont','Steps','A-Autom','Status']
    #Initial message    
    controller.main_win.win_msg('Automatic Closure of Contours has started for Channel '+str(ch_name[-1])+'!')
    #Get channel
    im_ch = controller.organ.obj_imChannels[ch_name]
    # Automatically Close Contours
    im_ch.closeContours_auto(gui_param = controller.main_win.gui_autom_close_contours[ch_name], 
                              gui_plot = controller.main_win.plot_contours_settings[ch_name], 
                              win = controller.main_win)
    #Toggle button
    getattr(controller.main_win, 'autom_close_'+ch_name+'_play').setChecked(True)
    #Win msg 
    controller.main_win.win_msg('Contours of Channel '+str(ch_name[-1])+' have been automatically closed!')
    alert('woohoo')

def manual_close_contours(controller, ch_name):

    # Workflow process
    workflow = controller.organ.workflow['morphoHeart']
    process = ['ImProc', ch_name, 'B-CloseCont','Steps','A-Manual','Status']
    #Initial message    
    controller.main_win.win_msg('Manually closing contours for Channel '+str(ch_name[-1])+'!')
    #Close contours manually
    controller.main_win.running_process = 'manual'
    #Open Section
    getattr(controller.main_win, 'close_contours_open').setChecked(False)
    controller.main_win.open_section(name = 'close_contours')

    #Get channel
    im_ch = controller.organ.obj_imChannels[ch_name]
    # Load image
    im_proc = im_ch.im_proc()
    im_proc = fcC.manual_close_contours(stack = im_proc, ch = ch_name,
                                        gui_param = controller.main_win.gui_manual_close_contours[ch_name], 
                                        gui_plot = controller.main_win.plot_contours_settings[ch_name], 
                                        win = controller.main_win)

    # #Setting up thread to run close contours
    # controller.main_win.setup_manual_close_thread(im_ch = im_ch, 
    #                                               gui_param = controller.main_win.gui_manual_close_contours[ch_name],
    #                                               gui_plot = controller.main_win.plot_contours_settings[ch_name],
    #                                               win = controller.main_win)

    # im_ch.closeContours_manual(gui_param = controller.main_win.gui_manual_close_contours[ch_name],
    #                            gui_plot = controller.main_win.plot_contours_settings[ch_name],
    #                            win = controller.main_win)
    # #Toggle button
    # getattr(controller.main_win, 'manual_close_'+ch_name+'_play').setChecked(True)
    # #Win msg 
    # controller.main_win.win_msg('Contours of Channel '+str(ch_name[-1])+' have been manually closed!')
    # alert('woohoo')
    # #Update running process
    # controller.main_win.running_process = None
    # controller.main_win.options = []

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

#ANALYSIS TAB
def run_keeplargest(controller):
    workflow = controller.organ.workflow
    #Check channels have already been created: 
    if len(controller.organ.obj_imChannels.keys()) == controller.organ.mH_settings['setup']['no_chs']:
        fcM.s32Meshes(organ = controller.organ, gui_keep_largest=controller.main_win.gui_keep_largest, 
                    win = controller.main_win, rotateZ_90=controller.organ.mH_settings['setup']['rotateZ_90'])

        #Update Status in GUI
        controller.main_win.update_status(None, 'DONE', controller.main_win.keeplargest_status, override = True)

        #Enable button for plot all
        getattr(controller.main_win, 'keeplargest_plot').setEnabled(True)

        #Toggle button
        getattr(controller.main_win, 'keeplargest_play').setChecked(True)

        #Update progress in main_win
        controller.main_win.update_workflow_progress()

        #Add meshes to plot_user
        controller.main_win.fill_comboBox_all_meshes()
        
    else: 
        title = 'Channels not closed / Contours not selected!'
        msg = 'You are not done closing/selecting the contours of the input channels! \nPlease go back to  -mH: Segment Channels-  Tab and continue processing the channels before running the processes in this tab'
        prompt = Prompt_ok_cancel(title, msg, parent=controller.welcome_win)
        prompt.exec()
        print('output:', prompt.output)
        return

    print('\nEND Keeplargest')
    print('organ.mH_settings:', controller.organ.mH_settings)
    print('organ.workflow:', workflow)

def run_cleanup(controller):
    if controller.main_win.keeplargest_play.isChecked(): 
        workflow = controller.organ.workflow
        if controller.main_win.gui_clean['plot2d']:
            plot_settings = (True, controller.main_win.gui_clean['n_slices'])
        else: 
            plot_settings = (False, None) 

        fcM.clean_ch(organ = controller.organ, 
                    gui_clean = controller.main_win.gui_clean, 
                    win=controller.main_win, plot_settings=plot_settings)

        #Enable button for plot all
        getattr(controller.main_win, 'clean_plot').setEnabled(True)

        #Toggle button
        getattr(controller.main_win, 'cleanup_play').setChecked(True)

        #Update progress in main_win
        controller.main_win.update_workflow_progress()

        #Add meshes to plot_user
        controller.main_win.fill_comboBox_all_meshes()

    else: 
        controller.main_win.win_msg('*To clean-up the tissues make sure you have at least run the  -Keep Largest-  section.')
            
def run_trimming(controller):
    if controller.main_win.keeplargest_play.isChecked(): 
        workflow = controller.organ.workflow
        meshes, no_cut, cuts_out = get_trimming_planes(organ = controller.organ,
                                                        gui_trim = controller.main_win.gui_trim,
                                                        win = controller.main_win)
        
        fcM.trim_top_bottom_S3s(organ = controller.organ, meshes = meshes, 
                                no_cut = no_cut, cuts_out = cuts_out,
                                win = controller.main_win)
        
        #Enable button for plot all
        getattr(controller.main_win, 'trimming_plot').setEnabled(True)

        #Toggle button
        getattr(controller.main_win, 'trimming_play').setChecked(True)

        #Update progress in main_win
        controller.main_win.update_workflow_progress()

        #Add meshes to plot_user
        controller.main_win.fill_comboBox_all_meshes()

    else: 
        controller.main_win.win_msg('*To trim the tissues make sure you have at least run the  -Keep Largest-  section.')

def get_trimming_planes(organ, gui_trim, win): 
    filename = organ.user_organName
    #Get meshes to cut
    meshes = []
    no_cut = []
    settings = {'color': {}, 'name':{}}
    aa = 0
    for ch in organ.obj_imChannels.keys():
        for cont in ['tiss', 'ext', 'int']:
            if gui_trim['top']['chs'][ch][cont] or gui_trim['bottom']['chs'][ch][cont]:
                meshes.append(organ.obj_meshes[ch+'_'+cont])
                settings['color'][aa] = organ.obj_meshes[ch+'_'+cont].color
                settings['name'][aa] = organ.obj_meshes[ch+'_'+cont].legend
                aa+=1
                break
            else: 
                no_cut.append(ch+'_'+cont)
    print('settings:', settings)

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
                                                meshes = meshes, settings=settings)#, win=win)  
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
                                                meshes = meshes, settings=settings)#, win=win)

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

def run_axis_orientation(controller, only_roi=False):
    if controller.main_win.keeplargest_play.isChecked(): 
        #CHECK HERE WHICH ONE HAS BEEN RUN AND IF STACK WAS RUN, 
        # PROGRAM SO THAT THE STACK DATA DOESN'T GET REMOVED 
        workflow = controller.organ.workflow['morphoHeart']
        if not only_roi: 
            fcM.get_stack_orientation(organ = controller.organ,  
                                    gui_orientation = controller.main_win.gui_orientation, 
                                    win = controller.main_win)
        
        try: 
            print('tryA')
            gui_orientation = controller.main_win.gui_orientation
        except: 
            print('exceptA')
            gui_orientation = controller.organ.mH_settings['wf_info']['orientation']

        on_hold = fcM.get_roi_orientation(organ = controller.organ,
                                            gui_orientation = gui_orientation,  
                                            win = controller.main_win)
        
        #Update Status in GUI
        process = ['MeshesProc', 'A-Set_Orientation', 'Status']
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

        #Update progress in main_win
        controller.main_win.update_workflow_progress()
    else: 
        controller.main_win.win_msg('*To set the stack and roi axes make sure you have at least run the  -Keep Largest-  section.')

def run_chNS(controller):
    if controller.main_win.keeplargest_play.isChecked(): 
        workflow = controller.organ.workflow['morphoHeart']

        if controller.main_win.gui_chNS['plot2d']:
            plot_settings = (True, controller.main_win.gui_chNS['n_slices'])
        else: 
            plot_settings = (False, None) 

        fcM.extract_chNS(organ = controller.organ, 
                        rotateZ_90 = controller.organ.mH_settings['setup']['rotateZ_90'],
                        win = controller.main_win, 
                        plot_settings = plot_settings)

        #Toggle button
        getattr(controller.main_win, 'chNS_play').setChecked(True)
        getattr(controller.main_win, 'summary_whole_plot_chNS').setEnabled(True)

        #Update progress in main_win
        controller.main_win.update_workflow_progress()

        #Add meshes to plot_user
        controller.main_win.fill_comboBox_all_meshes()

    else: 
        controller.main_win.win_msg('*To extract the channel from the negative space make sure you have at least run the  -Keep Largest-  section.')

def run_centreline_clean(controller):
    if controller.main_win.keeplargest_play.isChecked(): 
        workflow = controller.organ.workflow['morphoHeart']

        m4clf = fcM.proc_meshes4cl(controller.organ, 
                                    win=controller.main_win) 
                                                                    
        if not hasattr(controller.organ, 'obj_temp'):
            controller.organ.obj_temp = {}
        controller.organ.obj_temp['centreline'] = {'SimplifyMesh': m4clf}
        print('obj_temp: ', controller.organ.obj_temp)

        #Enable button for ML
        getattr(controller.main_win, 'centreline_ML_play').setEnabled(True)

        #Toggle button
        getattr(controller.main_win, 'centreline_clean_play').setChecked(True)

        #Update Status in GUI
        process = process =  ['MeshesProc','C-Centreline','Status']
        controller.main_win.update_status(workflow, process, controller.main_win.centreline_status)

        prompt_meshLab(controller)

        #Update progress in main_win
        controller.main_win.update_workflow_progress()

    else: 
        controller.main_win.win_msg('*To extract the centreline from tissues make sure you have at least run the  -Keep Largest-  section.')

def run_centreline_ML(controller): 
    workflow = controller.organ.workflow['morphoHeart']
    proc_simp = ['MeshesProc', 'C-Centreline', 'SimplifyMesh', 'Status']
    if get_by_path(workflow, proc_simp) == 'DONE':
        #Check all the MeshLab meshes have been created
        cl_names = list(controller.organ.mH_settings['measure']['CL'].keys())
        all_saved = []
        for nn, cl in enumerate(cl_names): 
            ch, cont, _ = cl.split('_')
            #Get name and path
            directory = controller.organ.dir_res(dir ='centreline')
            name_ML = controller.organ.mH_settings['wf_info']['centreline']['dirs'][ch][cont]['dir_meshLabMesh']
            mesh_dir = directory / name_ML
            if mesh_dir.is_file():
                controller.main_win.win_msg('MeshLab cut mesh ' +str(name_ML)+' was found!')
                all_saved.append(True)

                # Update organ workflow
                status_sq = getattr(controller.main_win, 'meshLab_status'+str(nn+1))
                controller.main_win.update_status(None, 'DONE', status_sq, override=True)

                #Enable button for vmtk
                getattr(controller.main_win, 'centreline_vmtk_play').setEnabled(True)

                #Toggle button
                getattr(controller.main_win, 'centreline_ML_play').setChecked(True)

                #Update progress in main_win
                controller.main_win.update_workflow_progress()

            else:
                error = '*'+str(name_ML)+' has not been created! Clean this mesh in MeshLab to proceed.'
                controller.main_win.win_msg(error)
                msg_add = [str(name_ML)+' was not found in the centreline folder. Make sure you have named your cleaned meshes correctly after running the processing in Meshlab.', 
                            'To clean up the meshes with MeshLab follow the next steps:']
                prompt_meshLab(controller, msg_add=msg_add)
                controller.main_win.centreline_ML_play.setChecked(False)
                return
            
            controller.main_win.win_msg('All MeshLab cut Meshes were successfully found!')

def run_centreline_vmtk(controller): 
    if controller.main_win.centreline_ML_play.isChecked(): 
        workflow = controller.organ.workflow['morphoHeart']
        try: 
            print('try')
            voronoi = controller.main_win.gui_centreline['vmtk_CL']['voronoi']
        except:
            print('except') 
            voronoi = controller.organ.mH_settings['wf_info']['centreline']['vmtk_CL']['voronoi']
        fcM.extract_cl(organ=controller.organ, 
                    win=controller.main_win, 
                    voronoi=voronoi)
        
        #Enable button for select
        getattr(controller.main_win, 'centreline_select').setEnabled(True)

        #Toggle button
        getattr(controller.main_win, 'centreline_vmtk_play').setChecked(True)

        #Update progress in main_win
        controller.main_win.update_workflow_progress()
    else: 
        controller.main_win.win_msg('*To extract the centrelines using VMTK make sure you have run the  -MeshLab-  cleanup first.')

def run_centreline_select(controller):
    if controller.main_win.centreline_vmtk_play.isChecked(): 

        nPoints = controller.main_win.gui_centreline['buildCL']['nPoints']
        same_plane = controller.main_win.gui_centreline['SimplifyMesh']['same_planes']

        workflow = controller.organ.workflow['morphoHeart']
        process = ['MeshesProc','C-Centreline','buildCL','Status']
        cl_names = list(controller.organ.mH_settings['measure']['CL'].keys())
        nn = 0
        for name in cl_names: 
            ch, cont, _ = name.split('_')
            print('name:', name)
            proc_wft = ['MeshesProc', 'C-Centreline', 'buildCL', ch, cont, 'Status']
            dict_clOpt = fcM.create_CLs(organ=controller.organ, 
                                        name=name,
                                        nPoints = nPoints, 
                                        same_plane = same_plane)
            
            title = 'Select best centreline for tissue-contour' 
            msg = 'Select the preferred centreline for processing this tissue-contour ('+ch+'-'+cont+')'
            items = {1: {'opt': 'Option 1'}, 2: {'opt': 'Option 2'}, 3: {'opt': 'Option 3'}, 
                        4: {'opt': 'Option 4'}, 5:{'opt': 'Option 5'}, 6:{'opt': 'Option 6'}}
            prompt = Prompt_ok_cancel_radio(title, msg, items, parent=controller.main_win)
            prompt.exec()
            print('output:', prompt.output, '\n')  
            opt_selected = prompt.output[0]
            cl_selected = items[opt_selected]['opt']
            proc_set = ['wf_info','centreline','buildCL','connect_cl',ch+'_'+cont]
            update = cl_selected +'-'+dict_clOpt[items[opt_selected]['opt']]['description']
            controller.organ.update_settings(process = proc_set, update = update, mH='mH')

            #Add text to Opt Centreline
            getattr(controller.main_win, 'opt_cl'+str(nn+1)).setText(prompt.output[1])
            
            #Add centreline to organ
            cl_final = dict_clOpt[cl_selected]['kspl']
            controller.organ.add_object(cl_final, proc='Centreline', class_name=ch+'_'+cont, name='KSpline')
            controller.organ.obj_meshes[ch+'_'+cont].set_centreline()
            
            # Update organ workflow
            controller.organ.update_mHworkflow(process = proc_wft, update = 'DONE')
            status_sq = getattr(controller.main_win, 'opt_cl_status'+str(nn+1))
            controller.main_win.update_status(workflow, proc_wft, status_sq)

            #Enable button for plot cl
            getattr(controller.main_win, 'cl_plot'+str(nn+1)).setEnabled(True)

            #Update progress in main_win
            controller.main_win.update_workflow_progress()
            nn+=1
        
        # Update organ workflow
        controller.organ.update_mHworkflow(process = process, update = 'DONE')
        controller.organ.update_mHworkflow(process = ['MeshesProc','C-Centreline','Status'], update = 'DONE')
        controller.organ.check_status(process='MeshesProc')

        #Update Status in GUI
        controller.main_win.update_status(workflow, ['MeshesProc','C-Centreline','Status'], 
                                        controller.main_win.centreline_status)

        #Toggle button
        getattr(controller.main_win, 'centreline_select').setChecked(True)

        #Check if user selected measuring centreline length
        cl_measurements = controller.organ.mH_settings['setup']['params']['2']['measure']
        cl_measure = [cl_measurements[key] for key in cl_measurements.keys()]
        if any(cl_measure): 
            fcM.measure_centreline(organ=controller.organ, nPoints=nPoints)
            controller.main_win.fill_results()

        #If orientation is on_hold
        if controller.organ.on_hold: 
            run_axis_orientation(controller=controller, only_roi=True)

    else: 
        controller.main_win.win_msg('*To select the centreline to use make sure you have created the centrelines using VMTK first.')
    
def prompt_meshLab(controller, msg_add=None):

    # Prompt with instructions
    title = 'Instructions for cleaning up meshes with MeshLab!'
    msg = []
    if msg_add != None: 
        msg = msg+msg_add
    else: 
        msg.append('You are done in morphoHeart for a little while. To get the centreline of each of the selected meshes follow the next steps:')
    msg.append("   > 1. Open the .stl file(s) in Meshlab")
    msg.append("   > 2. Run Filters > Remeshing, Simplification.. > Screened Poisson Surf Reco (check Pre-clean)")
    msg.append("   > 3. Cut inflow and outflow tract as close as the cuts from the original mesh you opened in Meshlab.") 
    msg.append("   > 4. Export the resulting surface adding 'ML' at the end of the filename (e.g _cut4clML.stl) in the same folder")
    msg.append("   > 5. Come back, press OK and continue processing!...")
    prompt = Prompt_ok_cancel_Big(title, msg, parent=controller.main_win)
    prompt.exec()
    print('output:',prompt.output, '\n')

def run_heatmaps3D(controller, btn):
    if controller.main_win.keeplargest_play.isChecked(): 
        workflow = controller.organ.workflow['morphoHeart']
        thck_values = {'i2e': {'short': 'th_i2e',
                                'method': 'D-Thickness_int>ext', 
                                'param': 'thickness int>ext', 
                                'n_type': 'int>ext'},
                    'e2i': {'short': 'th_e2i', 
                                'method': 'D-Thickness_ext>int', 
                                'param': 'thickness ext>int',
                                'n_type': 'ext>int'}}

        hm3d_list = list(controller.main_win.hm_btns.keys())
        if btn != None: 
            for key in hm3d_list: 
                num_key = controller.main_win.hm_btns[key]['num']
                if int(num_key) == int(btn): 
                    hm3get = key
                    break
            hm3d_set = [hm3get] #[segm_list[int(num)-1]]
        else: 
            hm3d_set = hm3d_list
        print('hm3d_set:',hm3d_set)

        for hmitem in hm3d_set:
            short, ch_info = hmitem.split('[') #short = th_i2e, th_e2i, ball
            ch_info = ch_info[:-1]
            if 'th' in short: 
                _, th_val = short.split('_')
                ch, cont = ch_info.split('-')
                method = thck_values[th_val]['method']
                mesh_tiss = controller.organ.obj_meshes[ch+'_tiss'].legend
                print('\n>> Extracting thickness information for '+mesh_tiss+'... \nNOTE: it takes about 5min to process each mesh... just be patient :) ')
                controller.main_win.win_msg('Extracting thickness information for '+mesh_tiss+'... NOTE: it takes about 5min to process each mesh... just be patient :)')
                setup = controller.main_win.gui_thickness_ballooning[hmitem]
                fcM.get_thickness(organ = controller.organ, name = (ch, cont), 
                                    thck_dict = thck_values[th_val], 
                                    setup = setup)

            else: # if 'ball' in short
                ch_cont, cl_info = ch_info.split('(')
                ch, cont = ch_cont.split('-')

                cl_info = cl_info[:-1].split('.')[1]
                cl_ch, cl_cont = cl_info.split('-')
                mesh2ball = controller.organ.obj_meshes[ch+'_'+cont].legend
                print('\n>> Extracting ballooning information for '+mesh2ball+'... \nNOTE: it takes about 10-15 to process each mesh... just be patient :) ')
                controller.main_win.win_msg('Extracting ballooning information for '+mesh2ball+'... NOTE: it takes about 10-15 to process each mesh... just be patient :)')
                setup = controller.main_win.gui_thickness_ballooning[hmitem]

                fcM.extract_ballooning(organ = controller.organ, name = (ch, cont),
                                    name_cl = (cl_ch, cl_cont), setup = setup)

            #Enable buttons to plot heatmaps
            controller.main_win.hm_btns[hmitem]['plot'].setEnabled(True)
            hm2d_btn = controller.main_win.hm_btns[hmitem]['play2d']
            num = controller.main_win.hm_btns[hmitem]['num']
            d3d2_btn = getattr(controller.main_win, 'd3d2_'+str(num))
            #Hereee!
            if d3d2_btn.isChecked() and controller.main_win.thickness2D_set.isChecked(): 
                hm2d_btn.setEnabled(True)

            # controller.main_win.prog_bar_update(nn)
            #Update progress in main_win
            controller.main_win.update_workflow_progress()

        # Update organ workflow
        all_all_done = []
        processes = ['D-Thickness_int>ext', 'D-Thickness_ext>int', 'D-Ballooning']
        for proc in processes:
            all_done = []
            if len(workflow['MeshesProc'][proc].keys())>0: 
                for ch in workflow['MeshesProc'][proc].keys():
                    if ch != 'Status':
                        for cont in workflow['MeshesProc'][proc][ch].keys():
                            print(proc, ch, cont, workflow['MeshesProc'][proc][ch][cont]['Status'])
                            all_done.append(workflow['MeshesProc'][proc][ch][cont]['Status'])

                if all(flag == 'DONE' for flag in all_done): 
                    proc_wft = ['MeshesProc', proc, 'Status']
                    controller.organ.update_mHworkflow(process = proc_wft, update = 'DONE')
                    all_all_done.append('DONE')
                elif any(flag == 'DONE' for flag in all_done):
                    proc_wft = ['MeshesProc', proc, 'Status']
                    controller.organ.update_mHworkflow(process = proc_wft, update = 'Initialised')
                    all_all_done.append('Initialised')
                else: 
                    pass
            else: 
                all_all_done.append(True)

        # Update mH_settings
        proc_set = ['wf_info']
        update = controller.main_win.gui_thickness_ballooning
        controller.organ.update_settings(proc_set, update, 'mH', add='heatmaps')

        #Update Status in GUI
        if all(flag == 'DONE' for flag in all_all_done): 
            process = ['MeshesProc', processes[0], 'Status']
            toggle = True
        elif any(flag == 'DONE' for flag in all_all_done):
            for proc in processes: 
                test_proc = ['MeshesProc', proc, 'Status']
                if get_by_path(workflow, test_proc) == 'Initialised' or get_by_path(workflow, test_proc) == 'NI': 
                    process = test_proc
                    break
            toggle = False
        else: 
            process = ['MeshesProc', processes[0], 'Status']
            toggle = False
        controller.main_win.update_status(workflow, process, controller.main_win.heatmaps_status)
                
        #Toggle button
        if toggle: 
            getattr(controller.main_win, 'heatmaps3D_play').setChecked(True)
        else: 
            getattr(controller.main_win, 'heatmaps3D_play').setChecked(False)

        print('\nEND Heatmaps')
        print('organ.mH_settings:', controller.organ.mH_settings)
        print('organ.workflow:', workflow)

        #Add meshes to plot_user
        controller.main_win.fill_comboBox_all_meshes()

    else: 
        controller.main_win.win_msg('*To extract the thickness meshes make sure you have at least run the  -Keep Largest-  section.')

def run_heatmaps2D(controller, btn):

    if controller.main_win.keeplargest_play.isChecked():
        if controller.main_win.thickness2D_set.isChecked():  
            workflow = controller.organ.workflow['morphoHeart']
            hm2d_list = list(controller.main_win.hm_btns.keys())
            if btn != None: 
                for key in hm2d_list: 
                    num_key = controller.main_win.hm_btns[key]['num']
                    if int(num_key) == int(btn): 
                        hm2get = key
                        break
                hm2d_set = [hm2get] #[segm_list[int(num)-1]]
            else: 
                hm2d_set = hm2d_list
            print('hm2d_set:',hm2d_set)

            gui_heatmaps2d = controller.main_win.gui_thickness_ballooning['heatmaps2D']

            for hmitem in hm2d_set: 
                short, ch_info = hmitem.split('[') #short = th_i2e, th_e2i, ball
                ch_info = ch_info[:-1]
                if 'th' in short: 
                    ch, contf = ch_info.split('-')
                    if 'i2e' in short: 
                        n_type = 'intTOext'
                        cont = 'ext'
                    else:# 'e2i' in short: 
                        n_type = 'extTOint'
                        cont = 'int'
                    array_name = 'thck('+n_type+')'
                else: 
                    # hm2d_set: ['ball[ch1-int(CL.ch1-int)]']
                    ch_cont, cl_info = ch_info.split('(CL.')
                    ch, contf = ch_cont.split('-')
                    from_cl, from_cl_type = cl_info.split('-')
                    array_name = 'ballCL('+from_cl+'_'+from_cl_type
                    cont = contf

                print('array_name:', array_name)
                #Get whole mesh and heatmap3d data
                whole_mesh = controller.organ.obj_meshes[ch+'_'+contf]
                array_mesh = controller.organ.obj_meshes[ch+'_'+cont]
                
                #Get data from heatmap 3D - LS52_F02_ch1_tiss_CMthck(intTOext)
                print(whole_mesh.dirs['arrays'])
                
                title = str(whole_mesh.dirs['arrays'][array_name])+'.npy'
                dir_npy = whole_mesh.parent_organ.dir_res(dir='csv_all') / title
                npy_array = np.load(dir_npy)
                print(short+'> whole_mesh: '+ch+'_'+contf+' -- array_mesh: '+ch+'_'+cont+' - loaded_npy:', dir_npy)

                #Get the extended and cut centrelines
                # Get the centreline ribbon
                cl_ribbon, kspl_ext = controller.main_win.plot_cl_ext1D(plotshow=False)

                # KSpline on surface
                ext_plane = controller.main_win.gui_thickness_ballooning['heatmaps2D']['direction']['plane_normal']
                kspl_vSurf = fcM.get_extCL_on_surf(mesh = array_mesh.mesh, kspl_ext = kspl_ext, direction = ext_plane)

                # Create new extended and cut kspline with higher resolution
                kspl_CLnew = fcM.get_extCL_highRes(organ = controller.organ, mesh = array_mesh.mesh, 
                                                    kspl_ext = kspl_ext) 
                
                #If the user wants to use the segments to aid heatmap unlooping....
                if gui_heatmaps2d['use_segms']: 
                    cut2use = gui_heatmaps2d['segms'].split(': ')[0]
                    segm_setup = controller.organ.mH_settings['setup']['segm'][cut2use]
                    segm_cuts_info = controller.organ.mH_settings['wf_info']['segments']['setup'][cut2use]['cut_info']
                    print('segm_setup:',segm_setup)

                    #See if the meshes have already been cut
                    obj_segm = {}
                    for n_segm in range(1,segm_setup['no_segments']+1,1):
                        segm_name = cut2use+'_'+ch+'_'+cont+'_segm'+str(n_segm)
                        if segm_name in controller.organ.submeshes.keys():
                            key = 'segm'+str(n_segm)+':'+segm_setup['name_segments']['segm'+str(n_segm)]
                            print('segm_name:', segm_name)
                            obj_segm[key] = controller.organ.obj_subm[segm_name]
                        else: 
                            controller.main_win.win_msg('*The segments for this tissue ('+ch+'_'+cont+") have not been obtained yet! Please create this tissue's segments to be able to run this process.") 
                            controller.main_win.hm_btns[hmitem]['play2d'].setChecked(False)
                            print('*The segments for this tissue have not been obtained yet! ('+controller.main_win.gui_thickness_ballooning['heatmaps2D']['segms']+')')
                            return
                        
                    print('len(obj_segm):', len(obj_segm), obj_segm)

                    data = {hmitem: npy_array}
                    #Use the whole tissue to create 2D heatmap
                    if len(obj_segm) != segm_setup['no_segments']: 
                        controller.main_win.win_msg('*The number of segments saved for this tissue ('+ch+'_'+cont+") is different than the number of segments expected. Please re-run segment creation for this tissue to be able to run this process.") 
                        print('*The number of segments saved for this tissue ('+ch+'_'+cont+") is different than the number of segments expected. Please re-run segment creation for this tissue to be able to run this process.")
                        return

                    else: 
                        # Classify points
                        print('Classify points into segments')
                        df_classPts, class_name = fcM.classify_heart_pts(array_mesh.mesh, obj_segm, data)

                        # Create kspline for each segment
                        print('controller.main_win.ordered_kspl:',controller.main_win.ordered_kspl)
                        ordered_kspl = copy.deepcopy(controller.organ.mH_settings['wf_info']['heatmaps']['heatmaps2D']['div'])
                        ordered_kspl = fcM.kspl_chamber_cut(organ = controller.organ, 
                                                            mesh = array_mesh.mesh, 
                                                            kspl_CLnew = kspl_CLnew, 
                                                            segm_cuts_info=segm_cuts_info, 
                                                            cut=cut2use, ordered_segm=ordered_kspl)
                        print('ordered_kspl (segm):',ordered_kspl)
                        order_segm_upside = list(ordered_kspl.keys())
                        order_segm_upside.reverse()
                
                #If the user wants to unloop the whole tissue without segments aid....
                else:
                    data = {hmitem: npy_array} 
                    #Use the whole tissue to create 2D heatmap
                    print('Use the whole tissue to create 2D heatmap')
                    df_classPts, class_name = fcM.classify_heart_pts(array_mesh.mesh, obj_segm=[], data=data)
                    # Create kspline for whole tissue
                    ordered_kspl = copy.deepcopy(controller.organ.mH_settings['wf_info']['heatmaps']['heatmaps2D']['div'])
                    print(ordered_kspl)
                    kspl_CLnewf = vedo.KSpline(kspl_CLnew.points()[::-1], res = 600).lw(5).color('deeppink').legend('HighResCL')
                    ordered_kspl['div1']['kspl'] = kspl_CLnewf
                    ordered_kspl['div1']['num_pts_range'] = (0, kspl_CLnewf.NPoints())
                    print('ordered_kspl (whole):',ordered_kspl)
                    order_segm_upside = ordered_kspl

                ##################################################################################################
                # Now Unloop the chambers (or not if whole) and get heatmap
                dirs = {}
                for div in order_segm_upside: 
                    print('\n\n- Unlooping the heart chambers for '+ordered_kspl[div]['name']+'...')
                    # print('div:', div, 'ordered_kspl[div]:', ordered_kspl[div])
                    # print(array_name, short, hmitem)
                    df_unloopedf, title_df = fcM.unloop_chamber(organ = controller.organ,
                                                                mesh = array_mesh.mesh, 
                                                                kspl_CLnew = kspl_CLnew,
                                                                kspl_vSurf = kspl_vSurf,
                                                                df_classPts = df_classPts,
                                                                labels = (hmitem, class_name),
                                                                gui_heatmaps2d = gui_heatmaps2d, 
                                                                kspl_data=ordered_kspl[div])
                    dirs[div] = Path(title_df)
                    fcM.heatmap_unlooped(organ = controller.organ, kspl_data = ordered_kspl[div], 
                                                df_unloopedf = df_unloopedf, hmitem= hmitem, ch = ch,
                                                gui_thball = controller.main_win.gui_thickness_ballooning)
                    
                    #Update dirs to check if things have been made
                    controller.main_win.gui_thickness_ballooning[hmitem]['hm2d_dirs'] = dirs
                                
                #Enable buttons to plot heatmaps
                plot_btn = controller.main_win.hm_btns[hmitem]['plot2d']
                plot_btn.setEnabled(True)

            print('\nEND Heatmaps')
            print('organ.mH_settings:', controller.organ.mH_settings)
            print('organ.workflow:', workflow)

        else: 
            controller.main_win.win_msg('*Set the 2D Heatmap settings first to be able to run this process')
    else: 
        controller.main_win.win_msg('*To extract the 2D Heatmaps make sure you have run the  -Keep Largest-  section, extracted the Centreline and created the 3D Heatmap.')

def run_segments(controller, btn): 

    workflow = controller.organ.workflow['morphoHeart']
    segm_list = list(controller.main_win.segm_btns.keys())
    if btn != None: 
        cut, num = btn.split('_')
        for key in segm_list: 
            cut_key = key.split(':')[0]
            num_key = controller.main_win.segm_btns[key]['num']
            if cut_key == cut and int(num_key) == int(num): 
                segm2cut = key
                break
        segm_set = [segm2cut] #[segm_list[int(num)-1]]
    else: 
        segm_set = segm_list
    print('segm_set:',segm_set)

    #Setup everything to cut
    if controller.main_win.gui_segm['use_centreline']: 
        cl_name = controller.main_win.gui_segm['centreline'].split('(')[1][:-1]
        cl_ch, cl_cont = cl_name.split('_')
        if workflow['MeshesProc']['C-Centreline']['buildCL'][cl_ch][cl_cont]['Status'] != 'DONE':
            controller.main_win.win_msg('*Finish obtaining the centreline ('+cl_name+') to continue running this section!')
            controller.main_win.segm_btns[segm_set[0]]['play'].setChecked(False)
            return 
        else: 
            #Get centreline
            nPoints = controller.organ.mH_settings['wf_info']['centreline']['buildCL']['nPoints']
            cl = controller.organ.obj_meshes[cl_name].get_centreline(nPoints = nPoints)
            spheres_spl = fcM.sphs_in_spline(kspl = cl, colour = True)
            cl_spheres = {'centreline': cl, 
                        'spheres': spheres_spl, 
                        'nPoints' : nPoints}
    else: 
        cl_spheres = None
    # print('cl_spheres: ', cl_spheres)
    print('organ.obj_temp:', controller.organ.obj_temp)

    #Loop through all the tissues that are going to be segmented
    for segm in segm_set: 
        print('Cutting segm:', segm)
        #Find cut
        cut, ch_cont = segm.split(':')
        ch, cont = ch_cont.split('_')
        #Extract info for cut
        colors_all = controller.organ.mH_settings['setup']['segm'][cut]['colors']
        palette = [colors_all[key] for key in colors_all.keys()]
        segm_names = controller.organ.mH_settings['setup']['segm'][cut]['name_segments']
        
        #Find method to cut
        method = controller.organ.mH_settings['wf_info']['segments']['setup'][cut]['ch_info'][ch][cont]
        mesh2cut = controller.organ.obj_meshes[ch+'_'+cont]
        print('Cutting into segments:', mesh2cut.name, '- method: ', method)

        #Get usernames string
        user_names = '('+', '.join([segm_names[val] for val in segm_names])+')'
        print('\n- Dividing '+mesh2cut.legend+' into segments '+user_names)
        controller.main_win.win_msg('Dividing '+mesh2cut.legend+' into segments '+user_names)

        if method == 'ext-ext': 
            # -> Get the discs that are going to be used to cut
            get_segm_discs(controller.organ, 
                            cut = cut, ch=ch, cont=cont, 
                            cl_spheres=cl_spheres, win=controller.main_win)
            # -> Create masks of discs
            fcM.create_disc_mask(controller.organ, cut = cut, h_min = 0.1125)
            ext_subsgm, meshes_segm = fcM.segm_ext_ext(controller.organ, mesh2cut, cut, 
                                                      segm_names, palette, win=controller.main_win)
            #Add submeshes of ext_ext as attribute to organ
            controller.organ.ext_subsgm = ext_subsgm

            #Enable Plot Buttons
            controller.main_win.segm_btns[segm]['plot'].setEnabled(True)
            print('wf:', controller.organ.workflow['morphoHeart']['MeshesProc'])

            #Enable play buttons of meshes with other methods
            for sgmt in segm_list:
                if sgmt != segm: 
                    play_btn = controller.main_win.segm_btns[sgmt]['play']
                    play_btn.setEnabled(True)
            
        elif method == 'cut_with_ext-ext' or method == 'cut_with_other_ext-ext':
            #Loading external subsegments 
            try: 
                ext_subsgm = controller.organ.ext_subsgm
                print('try ext_subsgm')
            except: 
                ext_subsgm = controller.organ.get_ext_subsgm(cut)
                print('except ext_subsgm')
            print('ext_subsgm: ',ext_subsgm)

            # -> Get segments using ext segments
            meshes_segm = fcM.get_segments(controller.organ, mesh2cut, cut, 
                                            segm_names, palette, ext_subsgm,  win=controller.main_win)
            
            #Enable Plot Buttons
            btn = controller.main_win.segm_btns[segm]['plot']
            btn.setEnabled(True)
            print('wf:', controller.organ.workflow['morphoHeart']['MeshesProc'])

        else: 
            print('No functions for this method:', method)
            alert('error_beep')
            meshes_segm = None

        #Save meshes temporarily within segment buttons
        controller.main_win.segm_btns[segm]['meshes'] = meshes_segm
        print(controller.main_win.segm_btns)
        print('meshes_segm: ',meshes_segm)
        print(controller.main_win.segm_btns[segm])

        #Update progress in main_win
        controller.main_win.update_workflow_progress()
        #Fill-up results table
        controller.main_win.fill_results()
        #Check button 
        controller.main_win.segm_btns[segm]['play'].setChecked(True)
        #Check segm-sections
        if hasattr(controller.main_win, 'segm_sect_btns'):
            btn_final = 'NA'
            for btn_ss in controller.main_win.segm_sect_btns:
                if 's'+cut.title() in btn_ss and ch_cont in btn_ss:
                    btn_final = btn_ss
                    break
            if btn_final != 'NA': 
                reg_cut = btn_final.split(':')[0].split('_o_')[1]
                reg_btn = reg_cut+':'+ch_cont
                if controller.main_win.sect_btns[reg_btn]['plot'].isEnabled(): 
                    controller.main_win.segm_sect_btns[btn_final]['play'].setEnabled(True)
        
    # Update organ workflow and GUI Status
    flat_semg_wf = flatdict.FlatDict(copy.deepcopy(workflow['MeshesProc']['E-Segments']))
    all_done = []
    for key in flat_semg_wf.keys(): 
        key_split = key.split(':')
        if len(key_split) > 1: 
            all_done.append(flat_semg_wf[key])

    proc_wft = ['MeshesProc', 'E-Segments', 'Status']
    if all(flag == 'DONE' for flag in all_done): 
        controller.organ.update_mHworkflow(process = proc_wft, update = 'DONE')
    elif any(flag == 'DONE' for flag in all_done): 
        controller.organ.update_mHworkflow(process = proc_wft, update = 'Initialised')
    else: 
        pass
    controller.main_win.update_status(workflow, proc_wft, controller.main_win.segments_status)

    #Add meshes to plot_user
    controller.main_win.fill_comboBox_all_meshes()

    print('organ.obj_temp:', controller.organ.obj_temp)

def get_segm_discs(organ, cut, ch, cont, cl_spheres, win): 

    if cl_spheres != None: 
        segm_using_cl = True
        cl = cl_spheres['centreline']
        spheres_spl = cl_spheres['spheres']
        nPoints = cl_spheres['nPoints']
    else:
        segm_using_cl = False

    # Get user segment names
    dict_names = organ.mH_settings['setup']['segm'][cut]['name_segments']
    user_names = '('+', '.join([dict_names[val] for val in dict_names])+')'

    # Number of discs expected to be created
    no_cuts_4segments = organ.mH_settings['setup']['segm'][cut]['no_cuts_4segments']
    #Get mesh
    mesh2cut = organ.obj_meshes[ch+'_'+cont]
    res = mesh2cut.resolution

    for n in range(no_cuts_4segments):
        happyWithDisc = False
        print('Creating Disc No.'+str(n)+' for cutting tissues into segments!')
        win.win_msg('Creating Disc No.'+str(n)+' for cutting tissues into segments!')
        while not happyWithDisc: 
            if segm_using_cl:
                msg = '\n> Define the centreline point number to use to initialise Disc No.'+str(n)+' to divide heart into segments '+user_names+' \n[NOTE: Spheres appear in centreline every 10 points, but you can select intermediate points, eg. 142].'
                txt = [(0, organ.user_organName + msg)]
                obj = [(mesh2cut.mesh.alpha(0.05), cl, spheres_spl)]
                plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))
                
                num_pt = None
                while num_pt == None: 
                    msg = 'Enter the centreline point number you want to use to initialise Disc No.'+str(n)+' to divide the tissue into segments '+user_names+':'
                    title = 'Centreline point number to initialise Disc'
                    prompt = Prompt_user_input(msg = msg, title = title, info = (0, nPoints), parent = win)
                    prompt.exec()
                    num_pt = prompt.output
                    print('prompt.output:', prompt.output)
                
                if prompt.output != None:
                    del prompt
                    cl_orient = None
                    while cl_orient == None: 
                        items = {0: {'opt': 'Use the centreline orientation at the selected point to define disc orientation', 'lineEdit': False, 'regEx': 'all'}, 
                                1: {'opt': 'Initialise the disc in the selected position but in plane normal to the y-z plane', 'lineEdit': False}}
                        title = 'Initilise disk orientation!'
                        msg = 'Select the orientation in which you would like to initialise the disc: '
                        prompt = Prompt_ok_cancel_radio(title, msg, items, parent = win)
                        prompt.exec()
                        cl_orient = prompt.output
                        print('output:', prompt.output, '\n')

                    if cl_orient[0] == 0: 
                        pl_normal, pl_centre = fcM.get_plane_normal2pt(pt_num = num_pt, points = cl.points())
                    else:# prompt.output[0] == 1: 
                        pl_centre = cl.points()[num_pt]
                        pl_normal = [1,0,0]
                    del prompt

            else: 
                pl_centre = mesh2cut.mesh.center_of_mass()
                pl_normal = [1,0,0]
            
            height = 2*0.225; disc_color = 'purple'; disc_res = 300
            # Modify (rotate and move cylinder/disc)
            radius = organ.mH_settings['wf_info']['segments']['radius'][cut]
            cyl_test, sph_test, rotX, rotY, rotZ = fcM.modify_disc(filename = organ.user_organName,
                                                                txt = 'cut tissues into segments '+user_names, 
                                                                mesh = mesh2cut.mesh,
                                                                option = [True,True,True,True,True,True],
                                                                def_pl = {'pl_normal': pl_normal, 'pl_centre': pl_centre},
                                                                radius = radius, height = height, 
                                                                color = disc_color, res = disc_res, 
                                                                zoom=0.8)

            # Get new normal of rotated disc
            pl_normal_corrected = fcM.new_normal_3DRot(normal = pl_normal, rotX = rotX, rotY = rotY, rotZ = rotZ)
            normal_unit = unit_vector(pl_normal_corrected)*10
            # Get central point of newly defined disc
            pl_centre_new = sph_test.pos()
            
            # Newly defined centreline point
            sph_cut = vedo.Sphere(pos = pl_centre_new, r=4, c='gold').legend('sph_ChamberCut')
    
            # Build new disc to confirm
            cyl_final = vedo.Cylinder(pos = pl_centre_new, r = radius, height = height, axis = normal_unit, c = disc_color, cap = True, res = disc_res)
            cyl_final.legend('Disc')

            msg = '\n> Check the position and the radius of Disc No.'+str(n)+' to cut the tissue into segments '+user_names+'.\nMake sure it is cutting the tissue effectively separating it into individual segments.\nClose the window when done.'
            txt = [(0, organ.user_organName + msg)]
            obj = [(mesh2cut.mesh, cyl_final, cl)]
            plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))

            happy = None
            while happy == None: 
                disc_radius = radius
                items = {0: {'opt': 'no, I would like to define a new position for the disc'}, 
                         1: {'opt': 'yes, but I would like to redefine the disc radius [um]', 'lineEdit': True, 'regEx': "int3d"}, 
                         2: {'opt': 'yes, I am happy with both, disc position and radius'}}
                title = 'Happy with the defined Disc No.'+str(n)+'?'
                msg = 'Are you happy with the position of the disc [radius: '+str(disc_radius)+'um] to cut tissue into segments  '+user_names+'?'
                prompt = Prompt_ok_cancel_radio(title, msg, items, parent = win)
                prompt.exec()
                happy = prompt.output
                del prompt
            if happy[0] == 1: 
                happy_rad = False
                disc_radius = int(happy[2])
                while not happy_rad: 
                    cyl_final = vedo.Cylinder(pos = pl_centre_new, r = disc_radius, height = height, axis = normal_unit, c = disc_color, cap = True, res = disc_res)
                    msg = '\n> New radius:'+str(disc_radius)+'um. \nCheck the radius of Disc No.'+str(n)+' to cut the tissue into segments '+user_names+'. \nMake sure it is cutting the tissue effectively separating it into individual segments.\nClose the window when done.'
                    txt = [(0, organ.user_organName + msg)]
                    obj = [(mesh2cut.mesh.alpha(1), cl, cyl_final, sph_cut)]
                    plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(organ.get_maj_bounds()))

                    items = {0: {'opt': 'no, I would like to change its value', 'lineEdit': True, 'regEx': "int3d"}, 
                             1: {'opt': 'yes, it cuts the tissue without disrupting too much the segments!'}}
                    title = 'Happy with the defined Disc No.'+str(n)+'?'
                    msg = 'Is the selected radius ['+str(disc_radius)+'um] for Disc No.'+str(n)+' sufficient to cut the tissue into segments '+user_names+'?'
                    prompt = Prompt_ok_cancel_radio(title, msg, items, parent = win)
                    prompt.exec()
                    output = prompt.output
                    print('output:', output)
                    del prompt
                    if output[0] == 0: 
                        disc_radius = int(output[2])
                    else: 
                        happy_rad = True
                happyWithDisc = True
            elif happy[0] == 2:
                happyWithDisc = True
                
        # Save disc info
        cyl_name = 'Disc No.'+str(n)

        cyl_final.legend(cyl_name)
        cyl_dict = {'radius': disc_radius,
                    'normal_unit': normal_unit,
                    'pl_centre': pl_centre_new,
                    'height': height, 
                    'color': disc_color, 
                    'res': res}
        
        # Create new key in mH_settings to save disc info
        proc = ['wf_info', 'segments','setup', cut, 'cut_info']
        if 'cut_info' not in organ.mH_settings['wf_info']['segments']['setup'][cut].keys():
            organ.update_settings(proc, update = {}, mH = 'mH')
        organ.update_settings(proc+[cyl_name], update = cyl_dict, mH = 'mH')
        print('wf_info:', organ.mH_settings['wf_info']['segments']['setup'])

def run_sections(controller, btn): 

    workflow = controller.organ.workflow['morphoHeart']
    sect_list = list(controller.main_win.sect_btns.keys())
    if btn != None: 
        cut, num = btn.split('_')
        for key in sect_list: 
            cut_key = key.split(':')[0]
            num_key = controller.main_win.sect_btns[key]['num']
            if cut_key == cut and int(num_key) == int(num): 
                sect2cut = key
                break
        sect_set = [sect2cut] 
    else: 
        sect_set = sect_list
    print('sect_set:',sect_set)

    #Setup everything to cut
    clRib_type = 'ext2sides'
    sect_settings = controller.organ.mH_settings['wf_info']['sections']

    #Loop through all the tissues that are going to be sectioned
    for sect in sect_set: 
        #Find cut
        cut, ch_cont = sect.split(':')
        ch, cont = ch_cont.split('_')
        #Extract info for cut
        colors_all = controller.organ.mH_settings['setup']['sect'][cut]['colors']
        palette = [colors_all[key] for key in colors_all.keys()]
        sect_names = controller.organ.mH_settings['setup']['sect'][cut]['name_sections']
        
        #Find mesh to cut
        mesh2cut = controller.organ.obj_meshes[ch+'_'+cont]

        #Check if the mask has already been saved
        if 'mask_name' in sect_settings[cut.title()].keys(): 
            #Add mask_name as attribute to organ in case it is not
            mask_name = sect_settings[cut.title()]['mask_name']
            if not hasattr(controller.organ, 'mask_sect_'+cut.lower()): 
                setattr(controller.organ, 'mask_sect_'+cut.lower(), mask_name)
        else: 
            #Find centreline and settings to cut
            cl_name = controller.main_win.gui_sect[cut]['centreline'].split('(')[1][:-1]
            nPoints = controller.main_win.gui_sect[cut]['nPoints']
            mesh_cl = controller.organ.obj_meshes[cl_name]
            nRes = controller.main_win.gui_sect[cut]['nRes']

            #Create mask_cube and save
            ext_plane = getattr(controller.main_win, 'extend_dir_'+cut.lower())['plane_normal']
            # -> Create ribbon
            cl_ribbon = mesh_cl.get_clRibbon(nPoints=nPoints, nRes=nRes, 
                                            pl_normal=ext_plane, 
                                            clRib_type=clRib_type)
            # obj = [(mesh2cut.mesh, cl_ribbon)]
            # txt = [(0, controller.organ.user_organName+'- Extended Centreline Ribbon to cut organ into sections')]
            # plot_grid(obj=obj, txt=txt, axes=8, sc_side=max(controller.organ.get_maj_bounds()))
            
            # -> Create high resolution ribbon
            print('Creating high resolution centreline ribbon for '+cut.title())
            controller.main_win.win_msg('Creating high resolution centreline ribbon for '+cut.title())
            s3_filledCube, test_rib = fcM.get_stack_clRibbon(organ = controller.organ, 
                                                            mesh_cl = mesh_cl, 
                                                            nPoints = nPoints, 
                                                            nRes = nRes, 
                                                            pl_normal = ext_plane, 
                                                            clRib_type=clRib_type)
            
            # obj = [(test_rib, mesh_cl.mesh)]
            # txt = [(0, controller.organ.user_organName)]
            # plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(controller.organ.get_maj_bounds()))

            # -> Create cube of ribbon and mask one side
            print('Creating cube sections for masking ('+cut.title()+')')
            controller.main_win.win_msg('Creating cube sections for masking ('+cut.title()+')')
            mask_cube_split, s3_filledCubes = fcM.get_cube_clRibbon(organ = controller.organ,
                                                                    cut = cut,  
                                                                    s3_filledCube = s3_filledCube,
                                                                    res = mesh_cl.resolution,  
                                                                    pl_normal = ext_plane)
            
            # obj = [(mask_cube_split[0], mask_cube_split[1], test_rib, mesh_cl.mesh)]
            # txt = [(0, controller.organ.user_organName)]
            # plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(controller.organ.get_maj_bounds()))
            
            #Select the side of the ribbon that corresponds to section 1
            selected_side = fcM.select_ribMask(controller.organ, cut, mask_cube_split, mesh_cl.mesh)
            
            if selected_side['name'] == 'NS': 
                name_sect1 = controller.organ.mH_settings['setup']['sect'][cut.title()]['name_sections']['sect1']
                title = name_sect1.title()+' section not selected!' 
                msg = 'Select the mesh that corresponds to Section No.1 ('+name_sect1.upper()+'):'
                items = {0: {'opt':'dark blue mesh (A)'}, 1: {'opt':'light blue mesh (B)'}}
                prompt = Prompt_ok_cancel_radio(title, msg, items, parent=controller.main_win)
                prompt.exec()
                print('output:', prompt.output, '\n')  
                if prompt.output[0] == 0: 
                    selected_side = {'name': 'Filled CLRibbon SideA'}
                else: #prompt.output[0] == 1: 
                    selected_side = {'name': 'Filled CLRibbon SideB'}

            else: 
                pass
            print('final selected_mesh:', selected_side)

            fcM.save_ribMask_side(organ = controller.organ, 
                                    cut = cut, 
                                    selected_side=selected_side, 
                                    s3_filledCubes = s3_filledCubes)
                
            #Enable plot button for centreline extension
            cl_ext_btn = getattr(controller.main_win, 'cl_ext_'+cut.lower()).setEnabled(True)
        
        #Cut input tissue into sections
        print(type(mesh2cut))
        meshes_sect = fcM.get_sections(controller.organ, mesh2cut, cut, 
                                        sect_names, palette, win=controller.main_win)
        
        #Save meshes temporarily within section buttons
        controller.main_win.sect_btns[sect]['meshes'] = meshes_sect
        print(controller.main_win.sect_btns)
        print('meshes_sect: ',meshes_sect)
        print(controller.main_win.sect_btns[sect])

        #Enable Plot Buttons
        btn = controller.main_win.sect_btns[sect]['plot']
        btn.setEnabled(True)
        print('wf:', controller.organ.workflow['morphoHeart']['MeshesProc'])

        #Update progress in main_win
        controller.main_win.update_workflow_progress()
        #Fill-up results table
        controller.main_win.fill_results()
        #Check button 
        controller.main_win.sect_btns[sect]['play'].setChecked(True)
        #Check segm-sections
        if hasattr(controller.main_win, 'segm_sect_btns'):
            btn_final = 'NA'
            for btn_ss in controller.main_win.segm_sect_btns:
                if '_o_'+cut.title() in btn_ss and ch_cont in btn_ss:
                    btn_final = btn_ss
                    break
            if btn_final != 'NA': 
                seg_cut = btn_final.split('_o_')[0][1:]
                seg_btn = seg_cut+':'+ch_cont
                if controller.main_win.segm_btns[seg_btn]['plot'].isEnabled(): 
                    controller.main_win.segm_sect_btns[btn_final]['play'].setEnabled(True)
    
    # Update organ workflow and GUI Status
    flat_sect_wf = flatdict.FlatDict(copy.deepcopy(workflow['MeshesProc']['E-Sections']))
    all_done = []
    for key in flat_sect_wf.keys(): 
        key_split = key.split(':')
        if len(key_split) > 1: 
            all_done.append(flat_sect_wf[key])

    proc_wft = ['MeshesProc', 'E-Sections', 'Status']
    if all(flag == 'DONE' for flag in all_done): 
        controller.organ.update_mHworkflow(process = proc_wft, update = 'DONE')
    elif any(flag == 'DONE' for flag in all_done): 
        controller.organ.update_mHworkflow(process = proc_wft, update = 'Initialised')
    else: 
        pass
    controller.main_win.update_status(workflow, proc_wft, controller.main_win.sections_status)

    #Add meshes to plot_user
    controller.main_win.fill_comboBox_all_meshes()

def run_segm_sect(controller, btn): 
    workflow = controller.organ.workflow['morphoHeart']
    segm_sect_list = list(controller.main_win.segm_sect_btns.keys())
    if btn != None: 
        scuto, rcut_num = btn.split('_o_')
        scut = scuto[1:]
        rcut, num = rcut_num.split('_')
        for key in segm_sect_list: 
            ch_cont = key.split(':')[1]
            seg_cut = key.split('_o_')[0][1:]
            reg_cut = key.split(':')[0].split('_o_')[1]
            num_key = controller.main_win.segm_sect_btns[key]['num']
            if seg_cut == scut and reg_cut == rcut and int(num_key) == int(num): 
                segmsect2cut = key
                break
        segm_sect_set = [segmsect2cut] 
    else: 
        segm_sect_set = segm_sect_list
    print('segm_sect_set:',segm_sect_set)

    #Loop through all the tissues that are going to be sectioned
    for segm_sect in segm_sect_set: 
        ch_cont = segm_sect.split(':')[1]
        ch, cont = ch_cont.split('_')
        seg_cut = segm_sect.split('_o_')[0][1:]
        reg_cut = segm_sect.split(':')[0].split('_o_')[1]
        print(ch, cont, seg_cut, reg_cut)

        #Extract info for cut
        colors_all = controller.organ.mH_settings['setup']['segm-sect']['s'+seg_cut][reg_cut]['colors']
        segm_names = controller.organ.mH_settings['setup']['segm'][seg_cut]['name_segments']
        sect_names = controller.organ.mH_settings['setup']['sect'][reg_cut]['name_sections']
        print(colors_all, '\n', segm_names, '\n', sect_names)

        #Get mask to use
        sect_settings = controller.organ.mH_settings['wf_info']['sections']
        if 'mask_name' in sect_settings[reg_cut.title()].keys(): 
            #Add mask_name as attribute to organ in case it is not
            mask_name = sect_settings[reg_cut.title()]['mask_name']
            if not hasattr(controller.organ, 'mask_sect_'+reg_cut.lower()): 
                setattr(controller.organ, 'mask_sect_'+reg_cut.lower(), mask_name)
        else: 
            print('error no mask? ')

        # Cut input tissue into sections
        meshes_segm_sect = fcM.get_segm_sects(controller.organ, 
                                                ch_cont = ch_cont, 
                                                cuts = (seg_cut, reg_cut), 
                                                names = (segm_names, sect_names), 
                                                palette=colors_all,
                                                win=controller.main_win)
        
        #Save meshes temporarily within section buttons
        controller.main_win.segm_sect_btns[segm_sect]['meshes'] = meshes_segm_sect
        print('meshes_segm_sect: ',meshes_segm_sect)
        print(controller.main_win.segm_sect_btns[segm_sect])

        #Enable Plot Buttons
        btn = controller.main_win.segm_sect_btns[segm_sect]['plot']
        btn.setEnabled(True)
        print('wf:', controller.organ.workflow['morphoHeart']['MeshesProc'])

    #Update progress in main_win
    controller.main_win.update_workflow_progress()

    #Fill-up results table
    controller.main_win.fill_results()

    # Update organ workflow and GUI Status
    flat_sect_wf = flatdict.FlatDict(copy.deepcopy(workflow['MeshesProc']['E-Segments_Sections']))
    all_done = []
    for key in flat_sect_wf.keys(): 
        key_split = key.split(':')
        if len(key_split) > 1: 
            all_done.append(flat_sect_wf[key])

    proc_wft = ['MeshesProc', 'E-Segments_Sections', 'Status']
    if all(flag == 'DONE' for flag in all_done): 
        controller.organ.update_mHworkflow(process = proc_wft, update = 'DONE')
    elif any(flag == 'DONE' for flag in all_done): 
        controller.organ.update_mHworkflow(process = proc_wft, update = 'Initialised')
    else: 
        pass
    controller.main_win.update_status(workflow, proc_wft, controller.main_win.segm_sect_status)
    
    #Add meshes to plot_user
    controller.main_win.fill_comboBox_all_meshes()

def run_measure(controller): 
    if controller.main_win.keeplargest_play.isChecked(): 
        organ = controller.organ
        measurements = organ.mH_settings['measure']
        all_done = []; whole_done = []; other_done = []
        df_res = fcB.df_reset_index(df=organ.mH_settings['df_res'], 
                                     mult_index= ['Parameter', 'Tissue-Contour'])
        print(controller.main_win.index_param)
        #{'Looping direction', 'Centreline: Linear Length', 'Ellipsoid: Depth', 
        # 'Ellipsoid: Length', 'Ellipsoid: Asphericity', 'Volume: Segm-Reg', 'Volume: Segment', 
        # 'Surface Area', 'Centreline: Looped Length', 'Embryo Notes', 'Aortic length', 
        # 'Ellipsoid: Width', 'Volume: Region', 'Volume', 'Angles: Segment'}

        for param in measurements.keys():
            for item in measurements[param]:
                if 'whole' in item: 
                    ch, cont, _ = item.split('_')
                    try: 
                        mesh2meas = organ.obj_meshes[ch+'_'+cont]
                        mesh = mesh2meas.mesh
                        if param == 'Vol': 
                            vol = mesh.volume()
                            df_res = fcB.df_add_value(df=df_res, index=('Volume', ch+'_'+cont+'_whole'), value=vol)
                            # organ.mH_settings['measure']['Vol'][mesh2meas.name+'_whole'] = vol
                        if param == 'SA': 
                            area = mesh.area()
                            df_res = fcB.df_add_value(df=df_res, index=('Surface Area', ch+'_'+cont+'_whole'), value=area)
                            # organ.mH_settings['measure']['SA'][mesh2meas.name+'_whole'] = area
                        all_done.append(True); whole_done.append(True)
                    except: 
                        print('Ch-Cont: '+ch+'_'+cont+' not found!')
                        all_done.append(False); whole_done.append(False)
                else: 
                    print('Variable to measure:', item, param)
                    all_done.append(False)
                    pass

        # Update organ workflow and GUI Status
        # Whole 
        if all(whole_done): 
            controller.main_win.update_status(None, 'DONE', controller.main_win.measure_whole_status, override=True)
        elif any(whole_done): 
            controller.main_win.update_status(None, 'Initialised', controller.main_win.measure_whole_status, override=True)
        else: 
            controller.main_win.update_status(None, 'NI', controller.main_win.measure_whole_status, override=True)

        # All 
        if all(all_done): 
            controller.main_win.update_status(None, 'DONE', controller.main_win.measure_status, override=True)
        elif any(all_done): 
            controller.main_win.update_status(None, 'Initialised', controller.main_win.measure_status, override=True)
        else: 
            controller.main_win.update_status(None, 'NI', controller.main_win.measure_status, override=True)
        
        #Fill-up results table
        df_res = fcB.df_reset_index(df=df_res, mult_index= ['Parameter', 'Tissue-Contour', 'User (Tissue-Contour)'])
        organ.mH_settings['df_res'] = df_res
        controller.main_win.fill_results()
    
    else: 
        controller.main_win.win_msg('*To measure whole tissue make sure you have at least run the  -Keep Largest-  section.')
