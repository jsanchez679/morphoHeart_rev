from pathlib import Path
proj = {'mH_projName': 'mH_Proj-202305071332', 'user_projName': 'Testing_morphoHeart', 'info': {'mH_projName': 'mH_Proj-202305071332', 'user_projName': 'Testing_morphoHeart', 'user_projNotes': 'Description of this project', 'date_created': '2023-05-07', 'dirs': [], 'dir_proj': Path('C:/Users/pallo/Dropbox/Pallollo y Juli/R_Testing morphoHeart')}, 'analysis': {'morphoHeart': True, 'morphoCell': False, 'morphoPlot': False}, 'dir_proj': Path('C:/Users/pallo/Dropbox/Pallollo y Juli/R_Testing morphoHeart'), 'organs': {}, 'cellGroups': {}, 'mH_settings': {'setup': {'no_chs': 2, 'name_chs': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'chs_relation': {'ch1': 'external', 'ch2': 'internal'}, 'color_chs': {'ch1': {'int': 'gold', 'tiss': 'lightseagreen', 'ext': 'crimson'}, 'ch2': {'int': 'deepskyblue', 'tiss': 'darkmagenta', 'ext': 'deeppink'}}, 'orientation': {'stack': 'anterior, ventral, left', 'roi': 'anterior, ventral, left'}, 'rotateZ_90': True, 'mask_ch': {'ch1': False, 'ch2': False}, 'chNS': {'layer_btw_chs': True, 'ch_ext': ('ch1', 'int'), 'ch_int': ('ch2', 'ext'), 'user_nsChName': 'cardiac jelly', 'color_chns': {'int': 'greenyellow', 'tiss': 'darkorange', 'ext': 'powderblue'}}, 'segm': {'cutLayersIn2Segments': True, 'Cut1': {'no_segments': 2, 'obj_segm': 'Disc', 'no_cuts_4segments': 1, 'name_segments': {'segm1': 'atrium', 'segm2': 'ventricle'}, 'ch_segments': {'chNS': ['tiss'], 'ch1': ['tiss', 'ext'], 'ch2': ['int', 'tiss']}}, 'measure': {'Vol': True, 'SA': False, 'Ellip': True}}, 'sect': {'cutLayersIn2Sections': True, 'Cut1': {'no_sections': 2, 'obj_sect': 'Centreline', 'name_sections': {'sect1': 'left', 'sect2': 'right'}, 'ch_sections': {'chNS': ['tiss'], 'ch1': ['tiss'], 'ch2': ['tiss']}}, 'measure': {'Vol': True, 'SA': False}}, 'chs_all': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 
'cardiac jelly'}, 'params': {0: {'s': 'SA', 'l': 'surface area'}, 1: {'s': 'Vol', 'l': 'volume'}, 2: {'s': 'CL', 'l': 'centreline', 'measure': {'looped_length': True, 'linear_length': True}}, 3: {'s': 'th_i2e', 'l': 'thickness (int>ext)'}, 4: {'s': 'th_e2i', 'l': 'thickness (ext>int)'}, 5: {'s': 'ball', 'l': 'centreline>tissue (ballooning)', 'measure': {1: {'to_mesh': 'ch1', 'to_mesh_type': 'ext', 'from_cl': 'ch2', 'from_cl_type': 'ext'}, 2: {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch1', 'from_cl_type': 'int'}, 3: {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch1', 'from_cl_type': 'ext'}}}, 6: {'s': 'LoopDir', 'l': 'looping direction', 'description': "Heart's looping direction", 'classes': ['dv', 'sin', 'dex']}}}, 'wf_info': {}, 'measure': {'SA': {}, 'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True, 'ch2:int:whole': True, 'ch2:tiss:whole': True, 'ch2:ext:whole': True, 'chNS:int:whole': True, 'chNS:tiss:whole': True, 'chNS:ext:whole': True}, 'CL': {'ch1:int:whole': True, 'ch1:ext:whole': True, 'ch2:ext:whole': True}, 'th_i2e': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'th_e2i': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'ball': {'ch1:int:whole': True, 'ch1:ext:whole': True}, 'LoopDir': {'ch1:ext:whole': True}, 'Vol(segm)': {'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True, 'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True}, 'Ellip(segm)': {'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True, 'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True}, 'Vol(sect)': {'Cut1:chNS:tiss:sect1': True, 'Cut1:chNS:tiss:sect2': True, 'Cut1:ch1:tiss:sect1': True, 'Cut1:ch1:tiss:sect2': True, 'Cut1:ch2:tiss:sect1': True, 'Cut1:ch2:tiss:sect2': True}}}, 'mH_channels': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'mH_segments': {'Cut1': {'segm1': 'atrium', 'segm2': 'ventricle'}}, 'mH_sections': {'Cut1': {'sect1': 'left', 'sect2': 'right'}}, 'mH_param2meas': {'SA': {}, 'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True, 'ch2:int:whole': True, 'ch2:tiss:whole': True, 'ch2:ext:whole': True, 'chNS:int:whole': True, 'chNS:tiss:whole': True, 'chNS:ext:whole': True}, 'CL': {'ch1:int:whole': True, 'ch1:ext:whole': True, 'ch2:ext:whole': True}, 'th_i2e': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'th_e2i': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'ball': {'ch1:int:whole': True, 'ch1:ext:whole': True}, 'LoopDir': {'ch1:ext:whole': True}, 'Vol(segm)': {'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True, 'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True}, 'Ellip(segm)': {'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True, 'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True}, 'Vol(sect)': {'Cut1:chNS:tiss:sect1': True, 'Cut1:chNS:tiss:sect2': True, 'Cut1:ch1:tiss:sect1': True, 'Cut1:ch1:tiss:sect2': True, 'Cut1:ch2:tiss:sect1': True, 'Cut1:ch2:tiss:sect2': True}}, 'mH_methods': ['A-Create3DMesh', 'B-TrimMesh', 'C-Centreline', 'D-Ballooning', 'D-Thickness_int>ext', 'D-Thickness_ext>int', 'E-Segments', 'E-Sections'], 'mC_settings': {}, 'workflow': {'ImProc': {'Status': 'NI', 'ch1': {'Status': 'NI', 'A-MaskChannel': {'Status': 'NI'}, 'B-CloseCont': {'Status': 'NI', 'Steps': {'A-Autom': {'Status': 'NI'}, 'B-Manual': {'Status': 'NI'}, 'C-CloseInOut': {'Status': 'NI'}}}, 'C-SelectCont': {'Status': 'NI'}, 'D-S3Create': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-TrimS3': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}}, 'ch2': {'Status': 'NI', 'A-MaskChannel': {'Status': 'NI'}, 'B-CloseCont': {'Status': 'NI', 'Steps': {'A-Autom': {'Status': 'NI'}, 'B-Manual': {'Status': 'NI'}, 'C-CloseInOut': {'Status': 'NI'}}}, 'C-SelectCont': {'Status': 'NI'}, 'D-S3Create': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-CleanCh': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-TrimS3': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}}, 'chNS': {'Status': 'NI', 'D-S3Create': {'Status': 'NI'}}}, 'MeshesProc': {'Status': 'NI', 'A-Create3DMesh': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'chNS': {'Status': 'NI'}}, 'B-TrimMesh': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'C-Centreline': {'Status': 'NI', 
'SimplifyMesh': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}, 'vmtk_CL': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}, 'buildCL': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}}, 'D-Ballooning': {'Status': 'NI', 'ch1': {'ext': {'Status': 'NI'}}}, 'D-Thickness_int>ext': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}, 'D-Thickness_ext>int': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}, 'E-Segments': {'Status': 'NI', 'Cut1': {'ch1': {'tiss': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}}, 'E-Sections': {'Status': 'NI', 'Cut1': {'ch1': {'tiss': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}}, 'F-Measure': {'SA':{}, 'Vol': {'ch1': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}, 'ch2': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}, 'chNS': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}}, 'CL': {'ch1': {'int': {'whole': True}, 'ext': {'whole': True}}, 'ch2': {'ext': {'whole': True}}}, 'th_i2e': {'ch1': {'tiss': {'whole': True}}, 'ch2': {'tiss': {'whole': True}}, 'chNS': {'tiss': {'whole': True}}}, 'th_e2i': {'ch1': {'tiss': {'whole': True}}, 'ch2': {'tiss': {'whole': True}}, 'chNS': {'tiss': {'whole': True}}}, 'ball': {'ch1': {'int': {'whole': True}, 'ext': {'whole': True}}}, 'LoopDir': {'ch1': {'ext': {'whole': True}}}, 'Vol(segm)': {'Cut1': {'chNS': {'tiss': {'segm1': True, 'segm2': True}}, 'ch1': {'tiss': {'segm1': True, 'segm2': True}, 'ext': {'segm1': True, 'segm2': True}}, 'ch2': {'int': {'segm1': True, 'segm2': True}, 'tiss': {'segm1': True, 'segm2': True}}}}, 'Ellip(segm)': {'Cut1': {'chNS': {'tiss': {'segm1': True, 'segm2': True}}, 'ch1': {'tiss': {'segm1': True, 'segm2': True}, 'ext': {'segm1': True, 'segm2': True}}, 'ch2': {'int': {'segm1': True, 'segm2': True}, 'tiss': {'segm1': True, 'segm2': True}}}}, 'Vol(sect)': {'Cut1': {'chNS': {'tiss': {'sect1': True, 'sect2': True}}, 'ch1': {'tiss': {'sect1': True, 'sect2': True}}, 'ch2': {'tiss': {'sect1': True, 'sect2': True}}}}}}}}


mH_channels = sorted(proj['mH_channels'])
# mH_segments = proj['mH_segments']
# mH_sections = proj['mH_sections']
mH_param2meas = proj['mH_param2meas']

dict_ImProc = dict()
dict_ImProc['Status'] = 'NI'
dict_MeshesProc = dict()

# Find the meas_param that include the extraction of a centreline
item_centreline = [tuple(item.split(':')) for item in mH_param2meas['CL'].keys()]
# Find the meas_param that include the extraction of mH_segments
segm_vol = [item for item in mH_param2meas['Vol(segm)'].keys()]
if 'SA(segm)' in mH_param2meas:
    segm_sa = [item for item in mH_param2meas['SA(segm)'].keys()]
else: 
    segm_sa = []
segm_ellip = [item for item in mH_param2meas['Ellip(segm)'].keys()]
segm_list = list(set(segm_vol) | set(segm_sa) | set(segm_ellip))
segm_list = [tuple(tup.split(':')) for tup in segm_list]
cut_segm = sorted(list(set([tup for (tup,_,_,_) in segm_list])))
ch_segm = sorted(list(set([tup for (_,tup,_,_) in segm_list])))

# Find the meas_param that include the extraction of mH_sections
try: 
    sect_vol = [item for item in mH_param2meas['Vol(sect)'].keys()]
except:
    sect_vol = []
try: 
    sect_sa = [item for item in mH_param2meas['SA(sect)'].keys()]
except: 
    sect_sa = []
sect_list = list(set(sect_vol) | set(sect_sa))
sect_list = [tuple(item.split(':')) for item in sect_list]
cut_sect = sorted(list(set([tup for (tup,_,_,_) in sect_list])))
ch_sect=  sorted(list(set([tup for (_,tup,_,_) in sect_list])))

# Find the meas_param that include the extraction of ballooning
item_ballooning = [tuple(item.split(':')) for item in mH_param2meas['ball'].keys()]
# Find the meas_param that include the extraction of thickness
item_thickness_intext = [tuple(item.split(':')) for item in mH_param2meas['th_i2e'].keys()]
item_thickness_extint = [tuple(item.split(':')) for item in mH_param2meas['th_e2i'].keys()]
mH_methods = proj['mH_methods']
mH_settings = proj['mH_settings']
dict_MeshesProc = {'Status' : 'NI'}
for met in mH_methods:
    dict_MeshesProc[met] =  {'Status': 'NI'}
                    
# Project status
for ch in mH_channels:
    if 'A-Create3DMesh' in dict_MeshesProc.keys():
        if 'NS' not in ch:
            dict_ImProc[ch] = {'Status': 'NI',
                                'A-MaskChannel': {'Status': 'NI'},
                                'B-CloseCont':{'Status': 'NI',
                                                'Steps':{'A-Autom': {'Status': 'NI'},
                                                        'B-Manual': {'Status': 'NI'},
                                                        'C-CloseInOut':{'Status': 'NI'},}},
                                'C-SelectCont':{'Status': 'NI'},
                                'D-S3Create':{'Status': 'NI',
                                            'Info': {'tiss':{'Status': 'NI'}, 
                                                    'int':{'Status': 'NI'}, 
                                                    'ext':{'Status': 'NI'}}}}
            #Check the external channel
            if mH_settings['setup']['chs_relation'][ch] == 'external':
                dict_ImProc[ch]['E-TrimS3'] = {'Status': 'NI',
                                                    'Info':{'tiss':{'Status': 'NI'}, 
                                                            'int':{'Status': 'NI'},
                                                            'ext':{'Status': 'NI'}}}
            else: 
                dict_ImProc[ch]['E-CleanCh'] = {'Status': 'NI',
                                                    'Info': {'tiss':{'Status': 'NI'}, 
                                                            'int':{'Status': 'NI'}, 
                                                            'ext':{'Status': 'NI'}}}
                dict_ImProc[ch]['E-TrimS3'] = {'Status': 'NI',
                                                    'Info':{'tiss':{'Status': 'NI'}, 
                                                            'int':{'Status': 'NI'},
                                                            'ext':{'Status': 'NI'}}}
        else: 
            dict_ImProc[ch] = {'Status': 'NI',
                                'D-S3Create':{'Status': 'NI'}} 
        
for nn, ch in enumerate(mH_channels):
    for process in ['A-Create3DMesh','B-TrimMesh','C-Centreline']:
        if 'NS' not in ch:
            if process != 'C-Centreline':
                dict_MeshesProc[process][ch] = {}
            for nnn, cont in enumerate(['tiss', 'int', 'ext']):
                if process == 'A-Create3DMesh' or process == 'B-TrimMesh':
                    dict_MeshesProc[process][ch][cont] = {'Status': 'NI'}
                
                if process == 'C-Centreline' and 'C-Centreline' in dict_MeshesProc.keys():
                    # print('nn:', nn, 'nnn:', nnn)
                    if nn == 0 and nnn == 0: 
                        dict_MeshesProc[process]['Status'] = 'NI'
                        dict_MeshesProc[process]['SimplifyMesh'] = {'Status':'NI'}
                        dict_MeshesProc[process]['vmtk_CL'] = {'Status':'NI'}
                        dict_MeshesProc[process]['buildCL'] = {'Status':'NI'}
                        
                    if (ch, cont, 'whole') in item_centreline:
                        # print(ch,cont)
                        if ch not in dict_MeshesProc[process]['SimplifyMesh'].keys(): 
                            dict_MeshesProc[process]['SimplifyMesh'][ch] = {}
                            dict_MeshesProc[process]['vmtk_CL'][ch] = {}
                            dict_MeshesProc[process]['buildCL'][ch] = {}
                        dict_MeshesProc[process]['SimplifyMesh'][ch][cont] = {'Status': 'NI'}
                        dict_MeshesProc[process]['vmtk_CL'][ch][cont] = {'Status': 'NI'}
                        dict_MeshesProc[process]['buildCL'][ch][cont] = {'Status': 'NI'}
                        
        else: 
            if process == 'A-Create3DMesh':
                dict_MeshesProc[process][ch] = {'Status': 'NI'}

    for cont in ['tiss', 'int', 'ext']:
        if (ch, cont, 'whole') in item_ballooning:
            dict_MeshesProc['D-Ballooning'][ch] = {}
            dict_MeshesProc['D-Ballooning'][ch][cont] =  {'Status': 'NI'}

        if (ch, cont, 'whole') in item_thickness_intext:
            dict_MeshesProc['D-Thickness_int>ext'][ch] = {}
            dict_MeshesProc['D-Thickness_int>ext'][ch][cont] = {'Status': 'NI'}
            
        if (ch, cont, 'whole') in item_thickness_extint:
                dict_MeshesProc['D-Thickness_ext>int'][ch] = {}
                dict_MeshesProc['D-Thickness_ext>int'][ch][cont] = {'Status': 'NI'}
                                            
# Project status
for cutg in cut_segm: 
    dict_MeshesProc['E-Segments'][cutg] = {}
    for ch in ch_segm:
        dict_MeshesProc['E-Segments'][cutg][ch] = {}
        for cont in ['tiss', 'int', 'ext']:
            if (cutg, ch, cont, 'segm1') in segm_list:
                dict_MeshesProc['E-Segments'][cutg][ch][cont] = {'Status': 'NI'}
                # for segm in mH_segments[cutg]:
                #     dict_MeshesProc['E-Segments'][cutg][ch][cont][segm]={'Status': 'NI'}

for cutc in cut_sect: 
    dict_MeshesProc['E-Sections'][cutc] = {}
    for ch in ch_sect:
        dict_MeshesProc['E-Sections'][cutc][ch] = {}
        for cont in ['tiss', 'int', 'ext']:
            if (cutc, ch, cont, 'sect1') in sect_list:
                dict_MeshesProc['E-Sections'][cutc][ch][cont] = {'Status': 'NI'}
                # for sect in mH_sections[cutc]:
                #     dict_MeshesProc['E-Sections'][cutc][ch][cont][sect]={'Status': 'NI'}


settings =  {'mH': {'settings': {'no_chs': 1, 'name_chs': {'ch1': 'myocardium'}, 'chs_relation': {'ch1': 'external'}, 'color_chs': {'ch1': {'int': 'gold', 'tiss': 'lightseagreen', 'ext': 'crimson'}}, 'orientation': {'stack': 'anterior, ventral, left', 'roi': 'anterior, ventral, left'}, 'rotateZ_90': True, 'mask_ch': {'ch1': False}, 'chNS': False, 'segm': False, 'sect': False, 'chs_all': {'ch1': 'myocardium'}, 'params': {0: {'s': 'SA', 'l': 'surface area'}, 1: {'s': 'Vol', 'l': 'volume'}, 2: {'s': 'CL', 'l': 'centreline', 'measure': {'looped_length': True, 'linear_length': True}}, 3: {'s': 'th_i2e', 'l': 'thickness (int>ext)'}, 4: {'s': 'th_e2i', 'l': 'thickness (ext>int)'}, 5: {'s': 'ball', 'l': 'centreline>tissue (ballooning)', 'measure': {}}}}, 'params': {'SA': {'ch1:int:whole': False, 'ch1:tiss:whole': False, 'ch1:ext:whole': False}, 'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True}, 'CL': {'ch1:int:whole': False, 'ch1:ext:whole': False}, 'th_i2e': {'ch1:tiss:whole': True}, 'th_e2i': {'ch1:tiss:whole': False}, 'ball': {'ch1:int:whole': False, 'ch1:ext:whole': False}}}, 'mC': {'settings': None, 'params': None}}


