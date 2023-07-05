

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
    #Check channels have already been created: 

    if len(controller.organ.obj_imChannels.keys()) == controller.organ.mH_settings['setup']['no_chs']:
        fcM.s32Meshes(organ = controller.organ, gui_keep_largest=controller.main_win.gui_keep_largest, 
                    win = controller.main_win, rotateZ_90=controller.organ.mH_settings['setup']['rotateZ_90'])

        #Update Status in GUI
        controller.main_win.update_status(None, 'DONE', controller.main_win.keeplargest_status, override = True)

        #Enable button for plot all
        plot_all = getattr(controller.main_win, 'keeplargest_plot')
        plot_all.setEnabled(True)

        #Toggle button
        select_btn = getattr(controller.main_win, 'keeplargest_play')
        select_btn.setChecked(True)
        toggled(select_btn)
    
    else: 
        title = 'Channels not closed / Contours not selected!'
        msg = 'You are not done closing/selecting the contours of the input channels! \nPlease go back to  -mH: Segment Channels-  Tab and continue processing the channels before turning into this tab'
        prompt = Prompt_ok_cancel(title, msg, parent=controller.welcome_win)
        prompt.exec()
        print('output:', prompt.output)

    print('\nEND Keeplargest')
    print('organ.mH_settings:', controller.organ.mH_settings)
    print('organ.workflow:', workflow)

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
    if controller.main_win.gui_clean['plot2d']:
        plot_settings = (True, controller.main_win.gui_clean['n_slices'])
    else: 
        plot_settings = (False, None) 

    fcM.clean_ch(organ = controller.organ, 
                 gui_clean = controller.main_win.gui_clean, 
                 win=controller.main_win, plot_settings=plot_settings)

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
                                                meshes = meshes)#, win=win)  
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
                                                meshes = meshes)#, win=win)

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
    if controller.main_win.gui_chNS['plot2d']:
        plot_settings = (True, controller.main_win.gui_chNS['n_slices'])
    else: 
        plot_settings = (False, None) 

    fcM.extract_chNS(organ = controller.organ, 
                     rotateZ_90 = controller.organ.mH_settings['setup']['rotateZ_90'],
                     win = controller.main_win, 
                     plot_settings = plot_settings)

    #Toggle button
    select_btn = getattr(controller.main_win, 'chNS_play')
    select_btn.setChecked(True)
    toggled(select_btn)

def run_centreline_clean(controller):

#   #Check first if extracting centrelines is a process involved in this organ/project
#     if organ.check_method(method = 'C-Centreline'): 
#     # if 'C-Centreline' in organ.parent_project.mH_methods: 
#         #Check workflow status
#         workflow = organ.workflow
#         process = ['MeshesProc','C-Centreline','SimplifyMesh','Status']
#         check_proc = get_by_path(workflow, process)
        
#         #Check meshes to process in MeshLab have been saved
#         path2files = organ.mH_settings['wf_info']['MeshesProc']['C-Centreline']
#         files_exist = []
#         for ch_s in path2files.keys():
#             if 'ch' in ch_s:
#                 for cont_s in path2files[ch_s].keys():
#                     dir2check = path2files[ch_s][cont_s]['dir_meshLabMesh']
#                     if dir2check != None: 
#                         files_exist.append(dir2check.is_file())
#                     else: 
#                         files_exist.append(dir2check)
#                     print (ch_s, cont_s)
        
#         if check_proc == 'DONE' and all(flag for flag in files_exist):
#             q = 'You already cleaned and cut the meshes to extract the centreline. Do you want to clean and cut them again?'
#             res = {0: 'no, continue with next step', 1: 'yes, re-run these two processes!'}
#             cut_meshes4cl = ask4input(q, res, bool)
#         else: 
#             cut_meshes4cl = True
            
    workflow = controller.organ.workflow['morphoHeart']

    m4clf = fcM.proc_meshes4cl(controller.organ, 
                                win=controller.main_win) 
                                                    
    if not hasattr(controller.organ, 'obj_temp'):
        controller.organ.obj_temp = {}
    controller.organ.obj_temp['centreline'] = {'SimplifyMesh': m4clf}
    print('obj_temp: ', controller.organ.obj_temp)

    #Enable button for ML
    plot_btn = getattr(controller.main_win, 'centreline_ML_play')
    plot_btn.setEnabled(True)

    #Toggle button
    select_btn = getattr(controller.main_win, 'centreline_clean_play')
    select_btn.setChecked(True)
    toggled(select_btn)

    #Update Status in GUI
    process = process =  ['MeshesProc','C-Centreline','Status']
    controller.main_win.update_status(workflow, process, controller.main_win.centreline_status)

    prompt_meshLab(controller)

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
                all_saved.append(True)

                # Update organ workflow
                status_sq = getattr(controller.main_win, 'meshLab_status'+str(nn+1))
                controller.main_win.update_status(None, 'DONE', status_sq, override=True)

                #Enable button for vmtk
                plot_btn = getattr(controller.main_win, 'centreline_vmtk_play')
                plot_btn.setEnabled(True)

                #Toggle button
                select_btn = getattr(controller.main_win, 'centreline_ML_play')
                select_btn.setChecked(True)
                toggled(select_btn)

            else:
                error = '*'+str(name_ML)+' has not been created! Clean this mesh in MeshLab to proceed.'
                controller.main_win.win_msg(error)
                msg_add = [str(name_ML)+' was not found in the centreline folder. Make sure you have named your cleaned meshes correctly after running the processing in Meshlab and press  -Enter-  when ready.', 
                            'To clean up the meshes with MeshLab follow the next steps:']
                prompt_meshLab(controller, msg_add=msg_add)
                return

def run_centreline_vmtk(controller): 
    workflow = controller.organ.workflow['morphoHeart']
    # Please input list of inlet profile ids: Please input list of outlet profile ids (leave empty for all available profiles):
    # #Check first if extracting centrelines is a process involved in this organ/project
    # if organ.check_method(method = 'C-Centreline'): 
    # # if 'C-Centreline' in organ.parent_project.mH_methods: 
    #     #Check workflow status
    #     workflow = organ.workflow
    #     process = ['MeshesProc','C-Centreline','vmtk_CL','Status']
    #     check_proc = get_by_path(workflow, process)
    #     if check_proc == 'DONE': 
    #         q = 'You already extracted the centreline of the selected meshes. Do you want to extract the centreline again?'
    #         res = {0: 'no, continue with next step', 1: 'yes, re-run this process!'}
    #         extractCL = ask4input(q, res, bool)
    #     else: 
    #         extractCL = True
            
    #     if extractCL: 

    #   while not dir_meshML.is_file():
    #     q = 'No meshes are recognised in the path: \n'+ str(dir_meshML) +'.\nMake sure you have named your cleaned meshes correctly after running the processing in Meshlab and press -Enter- when ready.'
    #     res = {0:'Please remind me what I need to do', 1:'I have done it now, please continue'}
    #     print_ins = ask4input(q, res, int)
    #     if print_ins == 0:
    #         print("\nTo get the centreline of each of the selected meshes follow the next steps:")
    #         print("> 1. Open the stl file(s) in Meshlab")
    #         print("> 2. Run Filters > Remeshing, Simplification.. > Screened Poisson Surf Reco (check Pre-clean)")
    #         print("> 3. Cut inflow and outflow tract as close as the cuts from the original mesh you opened in \n\t Meshlab and export the resulting surface adding 'ML' at the end of the filename\n\t (e.g _cut4clML.stl) in the same folder")
    #         print("> 4. Come back and continue processing!...")
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
    plot_btn = getattr(controller.main_win, 'centreline_select')
    plot_btn.setEnabled(True)

    #Toggle button
    select_btn = getattr(controller.main_win, 'centreline_vmtk_play')
    select_btn.setChecked(True)
    toggled(select_btn)

def run_centreline_select(controller):
    
    # #Check first if extracting centrelines is a process involved in this organ/project
    # if organ.check_method(method = 'C-Centreline'): 
    # # if 'C-Centreline' in organ.parent_project.mH_methods: 
    #     #Check workflow status
    #     workflow = organ.workflow
    #     process = ['MeshesProc','C-Centreline','buildCL','Status']
    #     check_proc = get_by_path(workflow, process)
    #     if check_proc == 'DONE': 
    #         q = 'You already extracted the centreline of the selected meshes. Do you want to extract the centreline again?'
    #         res = {0: 'no, continue with next step', 1: 'yes, re-run this process!'}
    #         buildCL = ask4input(q, res, bool)
    #     else: 
    #         buildCL = True
    
    # if buildCL: 
    try: 
        print('try')
        nPoints = controller.main_win.gui_centreline['buildCL']['nPoints']
    except: 
        print('except')
        nPoints = controller.organ.mH_settings['wf_info']['centreline']['buildCL']['nPoints']

    workflow = controller.organ.workflow['morphoHeart']
    process = ['MeshesProc','C-Centreline','buildCL','Status']
    cl_names = list(controller.organ.mH_settings['measure']['CL'].keys())
    nn = 0
    for name in cl_names: 
        ch, cont, _ = name.split('_')
        proc_wft = ['MeshesProc', 'C-Centreline', 'buildCL', ch, cont, 'Status']
        dict_clOpt = fcM.create_CLs(organ=controller.organ, 
                                    name=name,
                                    nPoints = nPoints)
        
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
        opt_txt = getattr(controller.main_win, 'opt_cl'+str(nn+1))
        opt_txt.setText(prompt.output[1])
        
        #Add centreline to organ
        cl_final = dict_clOpt[cl_selected]['kspl']
        controller.organ.add_object(cl_final, proc='Centreline', class_name=ch+'_'+cont, name='KSpline')
        controller.organ.obj_meshes[ch+'_'+cont].set_centreline()
        
        # Update organ workflow
        controller.organ.update_mHworkflow(process = proc_wft, update = 'DONE')
        status_sq = getattr(controller.main_win, 'opt_cl_status'+str(nn+1))
        controller.main_win.update_status(workflow, proc_wft, status_sq)

        #Enable button for plot cl
        plot_btn = getattr(controller.main_win, 'cl_plot'+str(nn+1))
        plot_btn.setEnabled(True)
        nn+=1
    
    # Update organ workflow
    controller.organ.update_mHworkflow(process = process, update = 'DONE')
    controller.organ.update_mHworkflow(process = ['MeshesProc','C-Centreline','Status'], update = 'DONE')
    controller.organ.check_status(process='MeshesProc')

    #Update Status in GUI
    controller.main_win.update_status(workflow, ['MeshesProc','C-Centreline','Status'], 
                                      controller.main_win.centreline_status)

    #Toggle button
    select_btn = getattr(controller.main_win, 'centreline_select')
    select_btn.setChecked(True)
    toggled(select_btn)

    #Check if user selected measuring centreline length
    cl_measurements = controller.organ.mH_settings['setup']['params']['2']['measure']
    cl_measure = [cl_measurements[key] for key in cl_measurements.keys()]
    if any(cl_measure): 
        fcM.measure_centreline(organ=controller.organ, nPoints=nPoints)

    #If orientation is on_hold
    if controller.organ.on_hold: 
        run_axis_orientation(controller=controller, only_roi=True)
    
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

    workflow = controller.organ.workflow['morphoHeart']
    thck_values = {'i2e': {'short': 'th_i2e',
                            'method': 'D-Thickness_int>ext', 
                            'param': 'thickness int>ext', 
                            'n_type': 'int>ext'},
                   'e2i': {'short': 'th_e2i', 
                            'method': 'D-Thickness_ext>int', 
                            'param': 'thickness ext>int',
                            'n_type': 'ext>int'}}
    
    if btn != None: 
        items = [list(controller.main_win.heatmap_dict.keys())[btn-1]]
        controller.main_win.prog_bar_range(0,1)
    else: 
        controller.main_win.prog_bar_range(0,len(controller.main_win.heatmap_dict))
        items = controller.main_win.heatmap_dict
    nn = 0
    for item in items:
        short, ch_info = item.split('[') #short = th_i2e, th_e2i, ball
        ch_info = ch_info[:-1]
        if 'th' in short: 
            _, th_val = short.split('_')
            ch, cont = ch_info.split('-')
            method = thck_values[th_val]['method']
            mesh_tiss = controller.organ.obj_meshes[ch+'_tiss'].legend
            print('\n>> Extracting thickness information for '+mesh_tiss+'... \nNOTE: it takes about 5min to process each mesh... just be patient :) ')
            controller.main_win.win_msg('Extracting thickness information for '+mesh_tiss+'... NOTE: it takes about 5min to process each mesh... just be patient :)')
            setup = controller.main_win.gui_thickness_ballooning[item]
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
            setup = controller.main_win.gui_thickness_ballooning[item]

            fcM.extract_ballooning(organ = controller.organ, name = (ch, cont),
                                name_cl = (cl_ch, cl_cont), setup = setup)

        #Enable buttons to plot heatmaps
        if btn != None:
            plot_btn = getattr(controller.main_win, 'hm_plot'+str(btn))
            hm2d_btn = getattr(controller.main_win, 'hm2d_play'+str(btn))
            d3d2_btn = getattr(controller.main_win, 'd3d2_'+str(btn))
        else: 
            plot_btn = getattr(controller.main_win, 'hm_plot'+str(nn+1))
            hm2d_btn = getattr(controller.main_win, 'hm2d_play'+str(nn+1))
            d3d2_btn = getattr(controller.main_win, 'd3d2_'+str(nn+1))

        plot_btn.setEnabled(True)
        if d3d2_btn.isChecked(): 
            hm2d_btn.setEnabled(True)
        nn+=1
        controller.main_win.prog_bar_update(nn)

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
        select_btn = getattr(controller.main_win, 'heatmaps3D_play')
        select_btn.setChecked(True)
        toggled(select_btn)

    print('\nEND Heatmaps')
    print('organ.mH_settings:', controller.organ.mH_settings)
    print('organ.workflow:', workflow)
    
        # controller.organ.update_workflow(process = process, update = 'DONE')

    #Check first if extracting centrelines is a process involved in this organ/project
    # if organ.check_method(method = 'D-Ballooning'): 
    # # if 'D-Ballooning' in organ.parent_project.mH_methods: 
    #     #Check workflow status
    #     workflow = organ.workflow
    #     process = ['MeshesProc','D-Ballooning','Status']
    #     check_proc = get_by_path(workflow, process)
    #     if check_proc == 'DONE': 
    #         q = 'You already extracted the ballooning parameters of the selected meshes. Do you want to extract them again?'
    #         res = {0: 'no, continue with next step', 1: 'yes, re-run this process!'}
    #         balloon = ask4input(q, res, bool)
    #     else: 
    #         balloon = True
    # else:
    #     balloon = False
    #     return None
    
    # if balloon: 
    

    # print(thck_names)
    
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
        #Get centreline
        nPoints = controller.organ.mH_settings['wf_info']['centreline']['buildCL']['nPoints']
        cl = controller.organ.obj_meshes[cl_name].get_centreline(nPoints = nPoints)
        spheres_spl = fcM.sphs_in_spline(kspl = cl, colour = True)
        cl_spheres = {'centreline': cl, 
                      'spheres': spheres_spl, 
                      'nPoints' : nPoints}
    else: 
        cl_spheres = None

    print('organ.obj_temp:', controller.organ.obj_temp)
    #Loop through all the tissues that are going to be segmented
    for segm in segm_set: 
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
        print('Cutting into segments:', mesh2cut.name, '- method: ', method, )

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
            btn = controller.main_win.segm_btns[segm]['plot']
            btn.setEnabled(True)
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
            except: 
                ext_subsgm = controller.organ.get_ext_subsgm(cut)
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
        print('meshes_segm: ',meshes_segm)
        print(controller.main_win.segm_btns[segm])

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

    print('organ.obj_temp:', controller.organ.obj_temp)
        
            # #Check if there ir already a created mask
            # mask_file_bool = []
            # for ii in range(no_cuts):
            #     name2save = organ.user_organName + '_mask_DiscNo'+str(ii)+'.npy'
            #     mask_file = organ.dir_res(dir ='s3_numpy') / name2save
            #     mask_file_bool.append(mask_file.is_file())
            
            # if all(mask_file_bool): 
            #     q = 'You already created the disc mask(s) to cut tissues into segments '+user_names+'. Do you want to re-run this process?'
            #     res = {0: 'no, continue with next step', 1: 'yes, re-run it!'}
            #     proceed = ask4input(q, res, bool)
        
            # else: 
            #     proceed = True
        
    # if proceed: 
              # #Check first if segments is a method involved in this organ
    # if organ.check_method(method = 'E-Segments'): 
    #     meshes_segm=[]; final_subsgm=[]
    #     name_segments = organ.mH_settings['general_info']['segments']['name_segments']
    #     user_names = '('+', '.join([name_segments[val] for val in name_segments])+')'
        
    #     #See if all sections have been stored in organ.submeshes
    #     segm_names = [item for item in organ.parent_project.mH_param2meas if 'segm1' in item and 'volume' in item]
    #     org_subm = [key for key in organ.submeshes if 'segm' in key]
        
    #     #Check workflow status
    #     workflow = organ.workflow
    #     process = ['MeshesProc','E-Segments','Status']
    #     check_proc = get_by_path(workflow, process)
    #     if check_proc == 'DONE' and len(org_subm)==len(name_segments)*len(segm_names): 
    #         q = 'You already divided the tissues into segments '+user_names+'. Do you want to repeat this process?'
    #         res = {0: 'no, continue with next step', 1: 'yes, I want to repeat it!'}
    #         proceed = ask4input(q, res, bool)
    #     else: 
    #         proceed = True
    # else:
    #     proceed = False
    #     return None

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
                         1: {'opt': 'yes, but I would like to redefine the disc radius', 'lineEdit': True, 'regEx': "int3d"}, 
                         2: {'opt': 'yes, I am happy with both, disc position and radius'}}
                title = 'Happy with the defined Disc No.'+str(n)+'?'
                msg = 'Are you happy with the position of the disc [radius: '+str(disc_radius)+'um] to cut tissue into segments  '+user_names+'?'
                prompt = Prompt_ok_cancel_radio(title, msg, items, parent = win)
                prompt.exec()
                happy = prompt.output
                del prompt
            if happy[0] == 1: 
                happy_rad = False
                while not happy_rad: 
                    disc_radius = int(happy[2])
                    cyl_final = vedo.Cylinder(pos = pl_centre_new, r = disc_radius, height = height, axis = normal_unit, c = disc_color, cap = True, res = disc_res)

                    msg = '\n> New radius: Check the radius of Disc No.'+str(n)+' to cut the tissue into segments '+user_names+'. \nMake sure it is cutting the tissue effectively separating it into individual segments.\nClose the window when done.'
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
                    del prompt

                    if output[0] == 0: 
                        disc_radius = output[2]
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
            obj = [(mesh2cut.mesh, cl_ribbon)]
            txt = [(0, controller.organ.user_organName+'- Extended Centreline Ribbon to cut organ into sections')]
            plot_grid(obj=obj, txt=txt, axes=8, sc_side=max(controller.organ.get_maj_bounds()))
            
            # -> Create high resolution ribbon
            print('Creating high resolution centreline ribbon for '+cut.title())
            controller.main_win.win_msg('Creating high resolution centreline ribbon for '+cut.title())
            s3_filledCube, test_rib = fcM.get_stack_clRibbon(organ = controller.organ, 
                                                            mesh_cl = mesh_cl, 
                                                            nPoints = nPoints, 
                                                            nRes = nRes, 
                                                            pl_normal = ext_plane, 
                                                            clRib_type=clRib_type)
            
            obj = [(test_rib, mesh_cl.mesh)]
            txt = [(0, controller.organ.user_organName)]
            plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(controller.organ.get_maj_bounds()))

            # -> Create cube of ribbon and mask one side
            mask_cube_split, s3_filledCubes = fcM.get_cube_clRibbon(organ = controller.organ,
                                                            cut = cut,  
                                                                s3_filledCube = s3_filledCube,
                                                                res = mesh_cl.resolution,  
                                                                pl_normal = ext_plane)
            
            obj = [(mask_cube_split[0], mask_cube_split[1], test_rib, mesh_cl.mesh)]
            txt = [(0, controller.organ.user_organName)]
            plot_grid(obj=obj, txt=txt, axes=5, sc_side=max(controller.organ.get_maj_bounds()))

            #Select the side of the ribbon that corresponds to section 1
            selected_side = fcM.select_ribMask(controller.organ, cut, mask_cube_split, mesh_cl.mesh)
            fcM.save_ribMask_side(organ = controller.organ, 
                                cut = cut, 
                                selected_side=selected_side, 
                                s3_filledCubes = s3_filledCubes)
            
            #Enable plot button for centreline extension
            cl_ext_btn = getattr(controller.main_win, 'cl_ext_'+cut.lower()).setEnabled(True)
        
        #Cut input tissue into sections
        meshes_sect = fcM.get_sections(controller.organ, mesh2cut, cut, 
                                        sect_names, palette, win=controller.main_win)
        
        #Save meshes temporarily within section buttons
        controller.main_win.sect_btns[sect]['meshes'] = meshes_sect
        print('meshes_sect: ',meshes_sect)
        print(controller.main_win.sect_btns[sect])

        #Enable Plot Buttons
        btn = controller.main_win.sect_btns[sect]['plot']
        btn.setEnabled(True)
        print('wf:', controller.organ.workflow['morphoHeart']['MeshesProc'])
    
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


 # if organ.check_method(method = 'E-Sections'): 
    #     name_sections = organ.mH_settings['general_info']['sections']['name_sections']
    #     user_names = '('+', '.join([name_sections[val] for val in name_sections])+')'
      
    #     #Check if there ir already a created mask
    #     name2save = organ.user_organName + '_mask_sect.npy'
    #     mask_file = organ.dir_res(dir ='s3_numpy') / name2save
    #     # organ.info['dirs']['s3_numpy'] / name2save
        
    #     if mask_file.is_file(): 
    #         q = 'You already created the mask to cut tissues into sections '+user_names+'. Do you want to create it again?'
    #         res = {0: 'no, continue with next step', 1: 'yes, re-create it!'}
    #         proceed = ask4input(q, res, bool)
    
    #     else: 
    #         proceed = True
        
       
        
        # # organ.info['shape_s3'] = organ.imChannels['ch1']['shape']
        # fcM.get_sect_mask(controller.organ, plotshow=True)

        # # Cut organ into sections
        # subms = fcM.get_sections(controller.organ, plotshow=True)

    # #Check if the orientation has alredy been stablished
    # if 'orientation' in organ.mH_settings.keys(): 
    #     if 'cl_ribbon' in organ.mH_settings['orientation'].keys():
    #         q = 'You already created the centreline ribbon to cut tissues into sections. Do you want to create it again?'
    #         res = {0: 'no, continue with next step', 1: 'yes, re-create it!'}
    #         proceed = ask4input(q, res, bool)
    #     else: 
    #         proceed = True
    # else: 
    #     proceed = True
            
    # if proceed: 
    #     q = 'Select the coordinate-axes you would like to use to define the plane in which the centreline will be extended to cut organ into sections:'
    #     res = {0: 'Stack Coordinate Axes', 
    #            1: 'ROI (Organ) Specific Coordinate Axes', 
    #            2: 'Other'}
    #     opt = ask4input(q, res, int)
        
    #     if opt in [0,1]: 
    #         if opt == 0:
    #             axes = res[opt].split(' ')[0].lower(); print(axes)
    #         else: 
    #             axes = res[opt].split(' ')[0].upper(); print(axes)
    #         coord_ax = organ.mH_settings['orientation'][axes]
    #         views = {}
    #         for n, view in enumerate(list(coord_ax['planar_views'].keys())):
    #             views[n] = view
    #         q2 = 'From the -'+res[opt]+'- select the plane you want to use to extend the centreline: '
    #         opt2 = ask4input(q2, views, int)