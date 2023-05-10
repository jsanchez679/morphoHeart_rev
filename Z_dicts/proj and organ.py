from pathlib import Path
proj = {'mH_projName': 'mH_Proj-202305101220', 'user_projName': 'heart_tissue_morphology', 'info': {'mH_projName': 'mH_Proj-202305101220', 'user_projName': 'heart_tissue_morphology', 'user_projNotes': 'Analysis of heart tissue morphology in wild-type hearts at different developmental stages', 'date_created': '2023-05-10', 'dirs': {}, 'dir_proj': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology'), 'dir_info': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/settings/mH_heart_tissue_morphology_project.json')}, 'analysis': {'morphoHeart': True, 'morphoCell': False, 'morphoPlot': False}, 'dir_proj': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology'), 'organs': {}, 'cellGroups': {}, 'gui_custom_data': {'strain': [], 'stage': [], 'genotype': [], 'im_orientation': ['ventral', 'lateral-left', 'lateral-right', 'dorsal', 'custom'], 'im_res_units': ['um', 'mm', 'm']}, 'mH_settings': {'setup': {'no_chs': 2, 'name_chs': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'chs_relation': {'ch1': 'external', 
'ch2': 'internal'}, 'color_chs': {'ch1': {'int': 'gold', 'tiss': 'lightseagreen', 'ext': 'crimson'}, 'ch2': {'int': 'deepskyblue', 'tiss': 'darkmagenta', 'ext': 'deeppink'}}, 'orientation': {'stack': 'anterior, ventral, left', 'roi': 'anterior, ventral, left'}, 'rotateZ_90': True, 'mask_ch': {'ch1': True, 'ch2': True}, 'chNS': {'layer_btw_chs': True, 'ch_ext': ('ch1', 'int'), 'ch_int': ('ch2', 'ext'), 'operation': 'XOR', 'user_nsChName': 'cardiac jelly', 'color_chns': {'int': 'greenyellow', 'tiss': 'darkorange', 'ext': 'powderblue'}}, 'segm': {'cutLayersIn2Segments': True, 'Cut1': {'no_segments': 2, 'obj_segm': 'Disc', 'no_cuts_4segments': 1, 'name_segments': {'segm1': 'atrium', 'segm2': 'ventricle'}, 'ch_segments': {'ch1': ['tiss', 'ext'], 'ch2': ['int', 'tiss'], 'chNS': ['tiss']}}, 'measure': {'Vol': True, 'SA': False, 'Ellip': True}}, 'sect': {'cutLayersIn2Sections': True, 'Cut1': {'no_sections': 2, 'obj_sect': 'Centreline', 'name_sections': {'sect1': 'left', 'sect2': 'right'}, 'ch_sections': {'ch1': ['tiss'], 'ch2': ['tiss'], 'chNS': ['tiss']}}, 'measure': {'Vol': True, 'SA': False}}, 'chs_all': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'params': {0: {'s': 'SA', 'l': 'surface area'}, 1: {'s': 'Vol', 'l': 'volume'}, 2: {'s': 'CL', 'l': 'centreline', 'measure': {'looped_length': True, 'linear_length': True}}, 3: {'s': 'th_i2e', 'l': 'thickness (int>ext)'}, 4: {'s': 'th_e2i', 'l': 'thickness (ext>int)'}, 5: {'s': 'ball', 'l': 'centreline>tissue (ballooning)', 'measure': {1: {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch2', 'from_cl_type': 'ext'}, 2: {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch1', 'from_cl_type': 'int'}}}, 6: {'s': 'LoopDir', 'l': 'looping direction', 'description': "Heart's looping direction", 'classes': ['dv', 'sinistral', 'dextral']}}}, 'wf_info': {}, 'measure': {'SA': {}, 'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True, 'ch2:int:whole': True, 'ch2:tiss:whole': True, 'ch2:ext:whole': True, 'chNS:int:whole': True, 'chNS:tiss:whole': True, 'chNS:ext:whole': True}, 'CL': {'ch1:int:whole': True, 'ch2:ext:whole': True}, 'th_i2e': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'th_e2i': {'ch1:tiss:whole': True}, 'ball': {'ch1:int:whole': True}, 'LoopDir': {'ch1:ext:whole': True}, 'Vol(segm)': {'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True}, 'Ellip(segm)': {'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True}, 'Vol(sect)': {'Cut1:ch1:tiss:sect1': True, 'Cut1:ch1:tiss:sect2': True, 'Cut1:ch2:tiss:sect1': True, 'Cut1:ch2:tiss:sect2': True, 'Cut1:chNS:tiss:sect1': True, 'Cut1:chNS:tiss:sect2': True}}}, 'mH_channels': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'mH_segments': {'Cut1': {'segm1': 'atrium', 
'segm2': 'ventricle'}}, 'mH_sections': {'Cut1': {'sect1': 'left', 'sect2': 'right'}}, 'mH_param2meas': {'SA': {}, 'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True, 'ch2:int:whole': True, 'ch2:tiss:whole': True, 'ch2:ext:whole': True, 'chNS:int:whole': True, 'chNS:tiss:whole': True, 'chNS:ext:whole': True}, 'CL': {'ch1:int:whole': True, 'ch2:ext:whole': True}, 'th_i2e': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'th_e2i': {'ch1:tiss:whole': True}, 'ball': {'ch1:int:whole': True}, 'LoopDir': {'ch1:ext:whole': True}, 'Vol(segm)': {'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True}, 'Ellip(segm)': {'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True}, 'Vol(sect)': {'Cut1:ch1:tiss:sect1': True, 'Cut1:ch1:tiss:sect2': True, 'Cut1:ch2:tiss:sect1': True, 'Cut1:ch2:tiss:sect2': True, 'Cut1:chNS:tiss:sect1': True, 'Cut1:chNS:tiss:sect2': True}}, 'mH_methods': ['A-Create3DMesh', 'B-TrimMesh', 'C-Centreline', 'D-Ballooning', 'D-Thickness_int>ext', 'D-Thickness_ext>int', 'E-Segments', 'E-Sections'], 'mC_settings': {}, 'mC_channels': {}, 'mC_segments': {}, 'mC_sections': {}, 'mC_param2meas': {}, 'mC_methods': {}, 'workflow': {'morphoHeart': {'ImProc': {'Status': 'NI', 'ch1': {'Status': 'NI', 'A-MaskChannel': {'Status': 'NI'}, 'B-CloseCont': {'Status': 'NI', 'Steps': {'A-Autom': {'Status': 'NI'}, 'B-Manual': {'Status': 'NI'}, 'C-CloseInOut': {'Status': 'NI'}}}, 'C-SelectCont': {'Status': 'NI'}, 'D-S3Create': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-TrimS3': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}}, 'ch2': {'Status': 'NI', 'A-MaskChannel': {'Status': 'NI'}, 'B-CloseCont': {'Status': 'NI', 'Steps': {'A-Autom': {'Status': 'NI'}, 'B-Manual': {'Status': 'NI'}, 'C-CloseInOut': {'Status': 'NI'}}}, 'C-SelectCont': {'Status': 'NI'}, 'D-S3Create': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-CleanCh': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-TrimS3': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}}, 'chNS': {'Status': 'NI', 'D-S3Create': {'Status': 'NI'}}}, 'MeshesProc': {'Status': 'NI', 'A-Create3DMesh': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': 
{'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'chNS': {'Status': 'NI'}}, 'B-TrimMesh': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'C-Centreline': {'Status': 'NI', 'SimplifyMesh': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}, 'vmtk_CL': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}, 'buildCL': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}}, 'D-Ballooning': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}}, 'D-Thickness_int>ext': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}, 'D-Thickness_ext>int': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}}}, 'E-Segments': {'Status': 'NI', 'Cut1': {'ch1': {'tiss': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}}, 'E-Sections': {'Status': 'NI', 'Cut1': {'ch1': {'tiss': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}}, 'F-Measure': {'SA': {}, 'Vol': {'ch1': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}, 'ch2': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}, 'chNS': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}}, 'CL': {'ch1': {'int': {'whole': True}}, 'ch2': {'ext': 
{'whole': True}}}, 'th_i2e': {'ch1': {'tiss': {'whole': True}}, 'ch2': {'tiss': {'whole': True}}, 'chNS': {'tiss': {'whole': True}}}, 'th_e2i': {'ch1': {'tiss': {'whole': True}}}, 'ball': {'ch1': {'int': {'whole': True}}}, 'LoopDir': {'ch1': {'ext': {'whole': True}}}, 'Vol(segm)': {'Cut1': {'ch1': {'tiss': {'segm1': True, 'segm2': True}, 'ext': {'segm1': True, 'segm2': True}}, 'ch2': {'int': {'segm1': True, 'segm2': True}, 'tiss': {'segm1': True, 'segm2': True}}, 'chNS': {'tiss': {'segm1': True, 'segm2': True}}}}, 'Ellip(segm)': {'Cut1': {'ch1': {'tiss': {'segm1': True, 'segm2': True}, 'ext': {'segm1': True, 'segm2': True}}, 'ch2': {'int': {'segm1': True, 'segm2': True}, 'tiss': {'segm1': True, 'segm2': True}}, 'chNS': {'tiss': {'segm1': True, 'segm2': True}}}}, 'Vol(sect)': {'Cut1': {'ch1': {'tiss': {'sect1': True, 'sect2': True}}, 'ch2': {'tiss': {'sect1': True, 'sect2': True}}, 'chNS': {'tiss': {'sect1': True, 'sect2': True}}}}}}}, 'morphoCell': {}}, 'dir_info': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/settings/mH_heart_tissue_morphology_project.json')}

organ_dict = {'parent_project': proj, 'user_organName': 'LS52_F02', 'info': {'project': {'user': 'heart_tissue_morphology', 'mH': 'mH_Proj-202305101220', 'dict_dir_info': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/settings/mH_heart_tissue_morphology_project.json')}, 'user_organName': 'LS52_F02', 'user_organNotes': "Embryo's notes", 'im_orientation': 'ventral', 'custom_angle': '0', 'resolution': [0.22832596445005057, 0.22832596445005057, 0.75], 'im_res_units': ['um', 'um', 'um'], 'stage': 
'48-50hpf', 'strain': 'hapln1a s241/+; myl7:lifeActGFP; fli1a:AcTagRFP', 'genotype': 'wild-type', 'dirs': {'meshes': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/LS52_F02/meshes'), 'csv_all': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/LS52_F02/csv_all'), 'imgs_videos': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/LS52_F02/imgs_videos'), 's3_numpy': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/LS52_F02/s3_numpy'), 'centreline': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/LS52_F02/centreline'), 'settings': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/LS52_F02/settings')}}, 'img_dirs': {'ch1': {'image': {'path': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch0_EDC.tif'), 'shape': (288, 892, 892)}, 'mask': {'path': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch0_mask.tif'), 'shape': (288, 892, 892)}}, 'ch2': {'image': {'path': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_EDC.tif'), 'shape': (288, 892, 892)}, 'mask': {'path': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Im_LS52_F02_V_SR_1029/LS52_F02_V_SR_1029_ch1_mask.tif'), 'shape': (288, 892, 892)}}}, 'mH_organName': 'mH_Organ-202305101222', 'analysis': {'morphoHeart': True, 'morphoCell': False, 'morphoPlot': False}, 'mH_settings': {'setup': {'no_chs': 2, 'name_chs': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'chs_relation': {'ch1': 'external', 'ch2': 'internal'}, 'color_chs': {'ch1': {'int': 'gold', 'tiss': 'lightseagreen', 'ext': 'crimson'}, 'ch2': {'int': 'deepskyblue', 'tiss': 'darkmagenta', 'ext': 'deeppink'}}, 'orientation': {'stack': 'anterior, ventral, left', 'roi': 'anterior, ventral, left'}, 'rotateZ_90': True, 'mask_ch': {'ch1': True, 'ch2': True}, 'chNS': {'layer_btw_chs': True, 'ch_ext': ('ch1', 'int'), 'ch_int': ('ch2', 'ext'), 'operation': 'XOR', 'user_nsChName': 'cardiac jelly', 'color_chns': {'int': 'greenyellow', 'tiss': 'darkorange', 'ext': 'powderblue'}}, 'segm': {'cutLayersIn2Segments': True, 'Cut1': {'no_segments': 2, 'obj_segm': 'Disc', 'no_cuts_4segments': 1, 'name_segments': {'segm1': 'atrium', 'segm2': 'ventricle'}, 'ch_segments': {'ch1': ['tiss', 'ext'], 'ch2': ['int', 'tiss'], 'chNS': ['tiss']}}, 'measure': {'Vol': True, 'SA': False, 'Ellip': True}}, 'sect': {'cutLayersIn2Sections': True, 'Cut1': {'no_sections': 2, 'obj_sect': 'Centreline', 'name_sections': {'sect1': 'left', 'sect2': 'right'}, 'ch_sections': {'ch1': ['tiss'], 'ch2': ['tiss'], 'chNS': ['tiss']}}, 'measure': {'Vol': True, 'SA': False}}, 'chs_all': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'params': {0: {'s': 'SA', 'l': 'surface area'}, 1: {'s': 'Vol', 'l': 'volume'}, 2: {'s': 'CL', 'l': 'centreline', 'measure': {'looped_length': True, 'linear_length': True}}, 3: {'s': 'th_i2e', 'l': 'thickness (int>ext)'}, 4: {'s': 'th_e2i', 'l': 'thickness (ext>int)'}, 5: {'s': 'ball', 'l': 'centreline>tissue (ballooning)', 'measure': {1: {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch2', 'from_cl_type': 'ext'}, 2: {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch1', 'from_cl_type': 'int'}}}, 6: {'s': 'LoopDir', 'l': 'looping direction', 'description': "Heart's looping direction", 'classes': ['dv', 'sinistral', 'dextral']}}}, 'wf_info': {}, 'measure': {'SA': {}, 'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True, 'ch2:int:whole': True, 'ch2:tiss:whole': True, 'ch2:ext:whole': True, 'chNS:int:whole': True, 'chNS:tiss:whole': True, 'chNS:ext:whole': True}, 'CL': {'ch1:int:whole': True, 
'ch2:ext:whole': True}, 'th_i2e': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'th_e2i': {'ch1:tiss:whole': True}, 'ball': {'ch1:int:whole': True}, 'LoopDir': {'ch1:ext:whole': True}, 'Vol(segm)': {'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True}, 'Ellip(segm)': {'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True}, 'Vol(sect)': {'Cut1:ch1:tiss:sect1': True, 'Cut1:ch1:tiss:sect2': True, 'Cut1:ch2:tiss:sect1': True, 'Cut1:ch2:tiss:sect2': True, 'Cut1:chNS:tiss:sect1': True, 'Cut1:chNS:tiss:sect2': True}}}, 'imChannels': {}, 'obj_imChannels': {}, 'imChannelNS': {}, 'obj_imChannelNS': {}, 'meshes': {}, 'submeshes': {}, 'obj_meshes': {}, 'objects': {'KSplines': {'cut4cl': {'bottom': {}, 'top': {}}}, 'Spheres': {'cut4cl': {'bottom': {}, 'top': {}}}, 'Centreline': {}}, 'workflow': {'morphoHeart': {'ImProc': {'Status': 'NI', 'ch1': {'Status': 'NI', 'A-MaskChannel': {'Status': 'NI'}, 'B-CloseCont': {'Status': 'NI', 'Steps': {'A-Autom': {'Status': 'NI'}, 'B-Manual': {'Status': 'NI'}, 'C-CloseInOut': {'Status': 'NI'}}}, 'C-SelectCont': {'Status': 'NI'}, 'D-S3Create': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-TrimS3': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}}, 'ch2': {'Status': 'NI', 'A-MaskChannel': {'Status': 'NI'}, 'B-CloseCont': {'Status': 'NI', 'Steps': {'A-Autom': {'Status': 'NI'}, 'B-Manual': {'Status': 'NI'}, 'C-CloseInOut': {'Status': 'NI'}}}, 'C-SelectCont': {'Status': 'NI'}, 'D-S3Create': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-CleanCh': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-TrimS3': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}}, 'chNS': {'Status': 'NI', 'D-S3Create': {'Status': 'NI'}}}, 'MeshesProc': {'Status': 'NI', 'A-Create3DMesh': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'chNS': {'Status': 'NI'}}, 'B-TrimMesh': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'C-Centreline': {'Status': 'NI', 'SimplifyMesh': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}, 'vmtk_CL': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}, 'buildCL': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}}, 'D-Ballooning': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}}, 'D-Thickness_int>ext': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}, 'D-Thickness_ext>int': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}}}, 'E-Segments': {'Status': 'NI', 'Cut1': {'ch1': {'tiss': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}}, 'E-Sections': {'Status': 'NI', 'Cut1': {'ch1': {'tiss': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}}, 'F-Measure': {'SA': {}, 'Vol': {'ch1': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}, 'ch2': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}, 'chNS': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}}, 'CL': {'ch1': {'int': {'whole': True}}, 'ch2': {'ext': {'whole': True}}}, 'th_i2e': {'ch1': {'tiss': {'whole': True}}, 'ch2': {'tiss': {'whole': True}}, 'chNS': {'tiss': {'whole': True}}}, 'th_e2i': {'ch1': {'tiss': {'whole': True}}}, 'ball': {'ch1': {'int': {'whole': True}}}, 'LoopDir': {'ch1': {'ext': {'whole': True}}}, 'Vol(segm)': {'Cut1': {'ch1': {'tiss': {'segm1': True, 'segm2': True}, 'ext': {'segm1': True, 'segm2': True}}, 'ch2': {'int': {'segm1': True, 'segm2': True}, 'tiss': {'segm1': True, 'segm2': True}}, 'chNS': {'tiss': {'segm1': True, 'segm2': True}}}}, 'Ellip(segm)': {'Cut1': {'ch1': {'tiss': {'segm1': True, 'segm2': True}, 'ext': {'segm1': True, 'segm2': True}}, 'ch2': {'int': {'segm1': True, 'segm2': True}, 'tiss': {'segm1': 
True, 'segm2': True}}, 'chNS': {'tiss': {'segm1': True, 'segm2': True}}}}, 'Vol(sect)': {'Cut1': {'ch1': {'tiss': {'sect1': True, 'sect2': True}}, 'ch2': {'tiss': {'sect1': True, 'sect2': True}}, 'chNS': {'tiss': {'sect1': True, 'sect2': True}}}}}}}, 'morphoCell': {}}, 'dir_res': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart2/R_heart tissue morphology/LS52_F02')}


proj_new =  {'info': {'mH_projName': 'mH_Proj-202305101536', 'user_projName': 'hapln1a_morphology', 'user_projNotes': '', 'date_created': '2023-05-10', 'dirs': {}, 'dir_proj': 'D:\\Documents JSP\\Dropbox\\Dropbox_Juliana\\PhD_Thesis\\Data_ongoing\\LS_ongoing\\A_LS_Analysis\\im_morphoHeart2\\R_hapln1a morphology', 'dir_info': 'D:\\Documents JSP\\Dropbox\\Dropbox_Juliana\\PhD_Thesis\\Data_ongoing\\LS_ongoing\\A_LS_Analysis\\im_morphoHeart2\\R_hapln1a morphology\\settings\\mH_hapln1a_morphology_project.json'}, 'user_projName': 'hapln1a_morphology', 'mH_projName': 'mH_Proj-202305101536', 'analysis': {'morphoHeart': True, 'morphoCell': False, 'morphoPlot': False}, 'mH_settings': {'setup': {'no_chs': 2, 'name_chs': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'chs_relation': {'ch1': 'external', 'ch2': 'internal'}, 'color_chs': {'ch1': {'int': 'gold', 'tiss': 'lightseagreen', 'ext': 'crimson'}, 'ch2': {'int': 'deepskyblue', 'tiss': 'darkmagenta', 'ext': 'deeppink'}}, 'orientation': {'stack': 'anterior, ventral, left', 'roi': 'anterior, ventral, left'}, 'rotateZ_90': True, 'mask_ch': {'ch1': True, 'ch2': True}, 'chNS': {'layer_btw_chs': True, 'ch_ext': ['ch1', 'int'], 'ch_int': ['ch2', 'ext'], 'operation': 'XOR', 'user_nsChName': 'cardiac jelly', 'color_chns': {'int': 'greenyellow', 'tiss': 'darkorange', 'ext': 'powderblue'}}, 'segm': {'cutLayersIn2Segments': True, 'Cut1': {'no_segments': 2, 'obj_segm': 'Disc', 'no_cuts_4segments': 1, 'name_segments': {'segm1': 'atrium', 'segm2': 'ventricle'}, 'ch_segments': {'chNS': ['tiss'], 'ch2': ['int', 'tiss'], 'ch1': ['tiss', 'ext']}}, 'measure': {'Vol': True, 'SA': False, 'Ellip': True}}, 'sect': {'cutLayersIn2Sections': True, 'Cut1': {'no_sections': 2, 'obj_sect': 'Centreline', 'name_sections': {'sect1': 'left', 'sect2': 'right'}, 'ch_sections': {'chNS': ['tiss'], 'ch2': ['tiss'], 'ch1': ['tiss']}}, 'measure': {'Vol': True, 'SA': False}}, 'chs_all': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'params': {'0': {'s': 'SA', 'l': 'surface area'}, '1': {'s': 'Vol', 'l': 'volume'}, '2': {'s': 'CL', 'l': 'centreline', 'measure': {'looped_length': True, 'linear_length': True}}, '3': {'s': 'th_i2e', 'l': 'thickness (int>ext)'}, '4': {'s': 'th_e2i', 'l': 'thickness (ext>int)'}, '5': {'s': 'ball', 'l': 'centreline>tissue (ballooning)', 'measure': {'1': {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch2', 'from_cl_type': 'ext'}, '2': {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch1', 'from_cl_type': 'int'}}}, '6': {'s': 'LoopDir', 'l': 'looping direction', 'description': "Heart's looping direction", 'classes': ['dv', 'sin', 'dex']}}}, 'wf_info': {}, 'measure': {'SA': {}, 'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True, 'ch2:int:whole': True, 'ch2:tiss:whole': True, 'ch2:ext:whole': True, 'chNS:int:whole': True, 'chNS:tiss:whole': True, 'chNS:ext:whole': True}, 'CL': {'ch1:int:whole': True, 'ch2:ext:whole': True}, 'th_i2e': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'th_e2i': {'ch1:tiss:whole': True}, 'ball': {'ch1:int:whole': True}, 'LoopDir': {'ch1:ext:whole': True}, 'Vol(segm)': {'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True}, 'Ellip(segm)': {'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True}, 'Vol(sect)': {'Cut1:chNS:tiss:sect1': True, 'Cut1:chNS:tiss:sect2': True, 'Cut1:ch2:tiss:sect1': True, 'Cut1:ch2:tiss:sect2': True, 'Cut1:ch1:tiss:sect1': True, 'Cut1:ch1:tiss:sect2': True}}}, 'mH_channels': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'mH_segments': {'Cut1': {'segm1': 'atrium', 'segm2': 'ventricle'}}, 'mH_sections': {'Cut1': {'sect1': 'left', 'sect2': 'right'}}, 'mH_param2meas': {'SA': {}, 'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True, 'ch2:int:whole': True, 'ch2:tiss:whole': True, 'ch2:ext:whole': True, 'chNS:int:whole': True, 'chNS:tiss:whole': True, 'chNS:ext:whole': True}, 'CL': {'ch1:int:whole': True, 'ch2:ext:whole': True}, 'th_i2e': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'th_e2i': {'ch1:tiss:whole': True}, 'ball': {'ch1:int:whole': True}, 'LoopDir': {'ch1:ext:whole': True}, 'Vol(segm)': {'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True}, 'Ellip(segm)': {'Cut1:chNS:tiss:segm1': True, 'Cut1:chNS:tiss:segm2': True, 'Cut1:ch2:int:segm1': True, 'Cut1:ch2:int:segm2': True, 'Cut1:ch2:tiss:segm1': True, 'Cut1:ch2:tiss:segm2': True, 'Cut1:ch1:tiss:segm1': True, 'Cut1:ch1:tiss:segm2': True, 'Cut1:ch1:ext:segm1': True, 'Cut1:ch1:ext:segm2': True}, 'Vol(sect)': {'Cut1:chNS:tiss:sect1': True, 'Cut1:chNS:tiss:sect2': True, 'Cut1:ch2:tiss:sect1': True, 'Cut1:ch2:tiss:sect2': True, 'Cut1:ch1:tiss:sect1': True, 'Cut1:ch1:tiss:sect2': True}}, 'mC_settings': {}, 'mC_channels': {}, 'mC_segments': {}, 'mC_sections': {}, 'mC_param2meas': {}, 'workflow': {'morphoHeart': {'ImProc': {'Status': 'NI', 'ch1': {'Status': 'NI', 'A-MaskChannel': {'Status': 'NI'}, 'B-CloseCont': {'Status': 'NI', 'Steps': {'A-Autom': {'Status': 'NI'}, 'B-Manual': {'Status': 'NI'}, 'C-CloseInOut': {'Status': 'NI'}}}, 'C-SelectCont': {'Status': 'NI'}, 'D-S3Create': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-TrimS3': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}}, 'ch2': {'Status': 'NI', 'A-MaskChannel': {'Status': 'NI'}, 'B-CloseCont': {'Status': 'NI', 'Steps': {'A-Autom': {'Status': 'NI'}, 'B-Manual': {'Status': 'NI'}, 'C-CloseInOut': {'Status': 
'NI'}}}, 'C-SelectCont': {'Status': 'NI'}, 'D-S3Create': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-CleanCh': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'E-TrimS3': {'Status': 'NI', 'Info': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}}, 'chNS': {'Status': 'NI', 'D-S3Create': {'Status': 'NI'}}}, 'MeshesProc': {'Status': 'NI', 'A-Create3DMesh': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}, 'int': {'Status': 
'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'chNS': {'Status': 'NI'}}, 'B-TrimMesh': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}}, 'C-Centreline': {'Status': 'NI', 'SimplifyMesh': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}, 'vmtk_CL': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}, 'buildCL': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}, 'ch2': {'ext': {'Status': 'NI'}}}}, 'D-Ballooning': {'Status': 'NI', 'ch1': {'int': {'Status': 'NI'}}}, 'D-Thickness_int>ext': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}, 'D-Thickness_ext>int': {'Status': 'NI', 'ch1': {'tiss': {'Status': 'NI'}}}, 'E-Segments': {'Status': 'NI', 'Cut1': {'ch1': {'tiss': {'Status': 'NI'}, 'ext': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}, 'int': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}}, 'E-Sections': {'Status': 'NI', 'Cut1': {'ch1': {'tiss': {'Status': 'NI'}}, 'ch2': {'tiss': {'Status': 'NI'}}, 'chNS': {'tiss': {'Status': 'NI'}}}}, 'F-Measure': {'SA': {}, 'Vol': {'ch1': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}, 'ch2': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}, 'chNS': {'int': {'whole': True}, 'tiss': {'whole': True}, 'ext': {'whole': True}}}, 'CL': {'ch1': {'int': {'whole': True}}, 'ch2': {'ext': {'whole': True}}}, 'th_i2e': {'ch1': {'tiss': {'whole': True}}, 'ch2': {'tiss': {'whole': True}}, 'chNS': {'tiss': {'whole': True}}}, 'th_e2i': {'ch1': {'tiss': {'whole': True}}}, 'ball': {'ch1': {'int': {'whole': True}}}, 'LoopDir': {'ch1': {'ext': {'whole': True}}}, 'Vol(segm)': {'Cut1': {'chNS': {'tiss': {'segm1': True, 'segm2': True}}, 'ch2': {'int': {'segm1': True, 'segm2': True}, 'tiss': {'segm1': True, 'segm2': True}}, 'ch1': {'tiss': {'segm1': True, 'segm2': True}, 'ext': {'segm1': True, 'segm2': True}}}}, 'Ellip(segm)': {'Cut1': {'chNS': {'tiss': {'segm1': True, 'segm2': True}}, 'ch2': {'int': {'segm1': True, 'segm2': True}, 'tiss': {'segm1': True, 'segm2': True}}, 'ch1': {'tiss': {'segm1': True, 'segm2': True}, 'ext': {'segm1': True, 'segm2': True}}}}, 'Vol(sect)': {'Cut1': {'chNS': {'tiss': {'sect1': True, 'sect2': True}}, 'ch2': {'tiss': {'sect1': True, 'sect2': True}}, 'ch1': {'tiss': {'sect1': True, 'sect2': True}}}}}}}, 'morphoCell': {}}, 'mH_methods': ['A-Create3DMesh', 'B-TrimMesh', 'C-Centreline', 'D-Ballooning', 'D-Thickness_int>ext', 'D-Thickness_ext>int', 'E-Segments', 'E-Sections'], 'mC_methods': {}, 'organs': {}, 'cellGroups': {}, 'gui_custom_data': {'strain': [], 'stage': [], 'genotype': [], 'manipulation': [], 'im_orientation': ['ventral', 'lateral-left', 'lateral-right', 'dorsal'], 'im_res_units': ['um', 'mm', 'm']}, 'dir_proj': 'D:\\Documents JSP\\Dropbox\\Dropbox_Juliana\\PhD_Thesis\\Data_ongoing\\LS_ongoing\\A_LS_Analysis\\im_morphoHeart2\\R_hapln1a morphology', 'dir_info': 'D:\\Documents JSP\\Dropbox\\Dropbox_Juliana\\PhD_Thesis\\Data_ongoing\\LS_ongoing\\A_LS_Analysis\\im_morphoHeart2\\R_hapln1a morphology\\settings\\mH_hapln1a_morphology_project.json'}

# import re
# text = '/\d+\.?\d*/'
# r = re.compile(text)
# if r.match('1'): print ('it matches!')


# import PyQt5
# from PyQt5 import QtWidgets
# from qtwidgets import Toggle, AnimatedToggle

# class Window(QtWidgets.QMainWindow):

#     def __init__(self):
#         super().__init__()

#         toggle_1 = Toggle()
#         toggle_2 = AnimatedToggle(
#             checked_color="#FFB000",
#             pulse_checked_color="#44FFB000"
#         )

#         container = QtWidgets.QWidget()
#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(toggle_1)
#         layout.addWidget(toggle_2)
#         container.setLayout(layout)

#         self.setCentralWidget(container)


# app = QtWidgets.QApplication([])
# w = Window()
# w.show()
# app.exec_()


