

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

        #Enable button for plot cl
        if btn != None:
            plot_btn = getattr(controller.main_win, 'hm_plot'+str(btn))
        else: 
            plot_btn = getattr(controller.main_win, 'hm_plot'+str(nn+1))
        plot_btn.setEnabled(True)
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

    # if organ.check_method(method = 'E-Segments'): 
    #     name_segments = organ.mH_settings['general_info']['segments']['name_segments']
    #     user_names = '('+', '.join([name_segments[val] for val in name_segments])+')'
      
    #     if 'segm_cuts' in organ.mH_settings.keys():
    #         if 'Disc No.0' in organ.mH_settings['segm_cuts']: 
    #             q = 'You already created the disc(s) to cut tissues into segments '+user_names+'. Do you want to repeat this process?'
    #             res = {0: 'no, continue with next step', 1: 'yes, I want to repeat it!'}
    #             proceed = ask4input(q, res, bool)
    #         else: 
    #             proceed = True
    #     else: 
    #         proceed = True
            
    #     if proceed: 
    segm_list = list(controller.main_win.segm_btns.keys())
    if btn != None: 
        segm_set = [segm_list[btn]]
    else: 
        segm_set = segm_list

    #Setup everything to cut
    if controller.main_win.gui_segm['use_centreline']: 
        cl_name = controller.main_win.gui_segm['centreline'].split('(')[1][:-1]
        #Get centreline
        cl = controller.organ.obj_meshes[cl_name].get_centreline()
        spheres_spl = fcM.sphs_in_spline(kspl = cl, colour = True)
    
    if controller.organ.mH_settings['setup']['all_contained'] or controller.organ.mH_settings['setup']['one_contained']:
        ext_ch, _ = controller.organ.get_ext_int_chs()
        if (ext_ch.channel_no, 'tiss', 'segm1', 'volume') in segm_names:
            mesh_ext = organ.obj_meshes[ext_ch.channel_no+'_tiss']

    for item in segm_set: 
        

        



    fcM.get_segm_discs(organ = controller.organ, )
    fcM.create_disc_mask(controller.organ, h_min = 0.1125)
    m_subg, segms = fcM.get_segments(controller.organ)