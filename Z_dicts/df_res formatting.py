dict_segm = {'cB_segm_Cut1_ch1_int': False, 'cB_segm_Cut1_ch1_tiss': True, 'cB_segm_Cut1_ch1_ext': True, 'cB_segm_Cut1_ch2_int': True, 'cB_segm_Cut1_ch2_tiss': True, 'cB_segm_Cut1_ch2_ext': False, 'cB_segm_Cut1_chNS_int': False, 'cB_segm_Cut1_chNS_tiss': True, 'cB_segm_Cut1_chNS_ext': False, 'cB_segm_Cut2_ch1_int': False, 'cB_segm_Cut2_ch1_tiss': True, 'cB_segm_Cut2_ch1_ext': False, 'cB_segm_Cut2_ch2_int': False, 'cB_segm_Cut2_ch2_tiss': False, 'cB_segm_Cut2_ch2_ext': False, 'cB_segm_Cut2_chNS_int': False, 'cB_segm_Cut2_chNS_tiss': False, 'cB_segm_Cut2_chNS_ext': False}
dict_sect = {'cB_sect_Cut1_ch1_int': False, 'cB_sect_Cut1_ch1_tiss': True, 'cB_sect_Cut1_ch1_ext': False, 'cB_sect_Cut1_ch2_int': True, 'cB_sect_Cut1_ch2_tiss': True, 'cB_sect_Cut1_ch2_ext': False, 'cB_sect_Cut1_chNS_int': False, 'cB_sect_Cut1_chNS_tiss': True, 'cB_sect_Cut1_chNS_ext': False}

from pathlib import Path
import numpy as np

mH_settings = {'setup': {'no_chs': 2, 'name_chs': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'ECM'}, 'chs_relation': {'ch1': 'external', 'ch2': 'internal'}, 'color_chs': {'ch1': {'int': 'gold', 'tiss': 'lightseagreen', 'ext': 'crimson'}, 'ch2': {'int': 'deepskyblue', 'tiss': 'darkmagenta', 'ext': 'deeppink'}}, 'orientation': {'stack': 'anterior, ventral, left', 'roi': 'anterior, ventral, left'}, 'rotateZ_90': True, 'mask_ch': {'ch1': True, 'ch2': True}, 'all_contained': True, 'one_contained': False, 'chNS': {'layer_btw_chs': True, 'ch_ext': ('ch1', 'int'), 'ch_int': ('ch2', 'ext'), 'operation': 'XOR', 'user_nsChName': 'ECM', 'color_chns': {'int': 'greenyellow', 'tiss': 'darkorange', 'ext': 'powderblue'}, 'keep_largest': {'tiss': False, 'int': True, 'ext': True}, 'alpha': {'tiss': 0.05, 'int': 0.05, 'ext': 0.05}, 'plot_settings': [False, None]}, 'segm': {'cutLayersIn2Segments': True, 'Cut1': {'no_segments': 2, 'obj_segm': 'Disc', 'no_cuts_4segments': 1, 'name_segments': {'segm1': 'atrium', 'segm2': 'ventricle'}, 'ch_segments': {'ch1': ['int', 'tiss', 'ext'], 'ch2': ['int', 'tiss', 'ext'], 'chNS': ['tiss']}, 'colors': {'segm1': [247, 113, 137], 'segm2': [220, 137, 50]}}, 'measure': {'Vol': True, 'SA': False, 'Ellip': True}}, 'sect': {'cutLayersIn2Sections': True, 'Cut1': {'no_sections': 2, 'obj_sect': 'Centreline', 'name_sections': {'sect1': 'left', 'sect2': 'right'}, 'ch_sections': {'ch1': ['tiss'], 'ch2': ['tiss'], 'chNS': ['tiss']}, 'colors': {'sect1': [102, 194, 165], 'sect2': [252, 141, 98]}}, 'Cut2': {'no_sections': 2, 'obj_sect': 'Centreline', 'name_sections': {'sect1': 'dorsal', 'sect2': 'ventral'}, 'ch_sections': {'ch1': ['tiss'], 'ch2': ['tiss'], 'chNS': ['tiss']}, 'colors': {'sect1': [141, 160, 203], 'sect2': [231, 138, 195]}}, 'measure': {'Vol': True, 'SA': False}}, 'chs_all': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'ECM'}, 'params': {'0': {'s': 'SA', 'l': 'Surface Area'}, '1': {'s': 'Vol', 'l': 'Volume'}, '2': {'s': 'CL', 'l': 'Centreline', 'measure': {'looped_length': True, 'linear_length': True}}, '3': {'s': 'th_i2e', 'l': 'Thickness Heatmap (int>ext*)'}, '4': {'s': 'th_e2i', 'l': 'Thickness Heatmap (ext>int*)'}, '5': {'s': 'ball', 'l': 'Centreline>Tissue (Ballooning)', 'measure': {'1': {'to_mesh': 'ch1', 'to_mesh_type': 'ext', 
'from_cl': 'ch1', 'from_cl_type': 'int'}, '2': {'to_mesh': 'ch1', 'to_mesh_type': 'ext', 'from_cl': 'ch2', 'from_cl_type': 'ext'}, '3': {'to_mesh': 'ch2', 'to_mesh_type': 'ext', 'from_cl': 'ch2', 'from_cl_type': 'ext'}}}, '6': {'s': 'LoopDir', 'l': 'Looping Direction', 'description': '', 'type': 'categorical', 'categories': ['dloop', 'sloop', 'dvloop']}}, 'keep_largest': {'ch1': {'int': True, 'tiss': True, 'ext': True}, 'ch2': {'int': True, 'tiss': True, 'ext': True}}, 'alpha': {'ch1': {'int': 0.05, 'tiss': 0.05, 'ext': 0.05}, 'ch2': {'int': 0.05, 'tiss': 0.05, 'ext': 0.05}}}, 'wf_info': {'keep_largest': {'ch1': {'int': True, 'tiss': True, 'ext': True}, 'ch2': {'int': True, 'tiss': True, 'ext': True}}, 'cleanup': {'ch2': {'cont': ['int', 'tiss', 'ext'], 'with_ch': 'ch1', 'with_cont': 'int', 'inverted': True}, 'plot2d': False}, 'trimming': {'top': {'chs': {'ch1': {'int': True, 'tiss': True, 'ext': True}, 'ch2': {'int': True, 'tiss': True, 'ext': True}}, 'object': 'Plane', 'plane_info_mesh': {'pl_normal': [0.0, 0.7495431902766063, -0.661955441030563], 'pl_centre': [109.36814022064188, -8.724057338274235, 54.31639880977799]}, 'plane_info_image': {'pl_normal': [-0.7495431902766064, 0.0, -0.6619554410305631], 'pl_centre': [8.724057338274237, 109.3681402206419, 54.31639880977801]}}, 'bottom': 
{'chs': {'ch1': {'int': True, 'tiss': True, 'ext': True}, 'ch2': {'int': True, 'tiss': True, 'ext': True}}, 'object': 'Plane', 'plane_info_mesh': {'pl_normal': [0.0031863666649780205, 0.9968034549983764, -0.07982931272894528], 'pl_centre': [108.79834848331649, -183.31396761097068, 108.23176550199149]}, 'plane_info_image': {'pl_normal': [-0.9968034549983766, 0.0031863666649780214, -0.07982931272894529], 'pl_centre': [183.3139676109707, 108.79834848331652, 108.23176550199152]}}}, 'orientation': {'stack': {'axis': 'anterior, ventral, left', 'planar_views': {'anterior': {'color': [255, 215, 0, 200], 'idcell': 4, 'pl_normal': [0.0, 0.0, -0.9999999403953552]}, 'ventral': {'color': [0, 0, 205, 200], 'idcell': 3, 'pl_normal': [0.0, 1.0, 0.0]}, 'left': {'color': [255, 0, 0, 200], 'idcell': 1, 'pl_normal': [1.0, 0.0, -0.0]}}, 'stack_cube': {'pos': [107.65694275768884, -97.9726166651186, 99.5046940806983], 'side': 194.76205444335938, 'color': [152, 251, 152], 'rotateY': False}}, 'roi': {'axis': 'anterior, ventral, left', 'reorient': True, 'method': 'Centreline', 'centreline': 'myocardium (ch1_int)', 'plane_orient': 'YZ', 'vector_orient': 'Y+', 'planar_views': {'anterior': {'color': [255, 215, 0, 200], 'idcell': 4, 'pl_normal': [0.0, 0.6866674423217773, -0.7269716858863831]}, 'ventral': {'color': [0, 0, 205, 200], 'idcell': 3, 'pl_normal': [-0.0, 0.7269716858863831, 0.6866674423217773]}, 'left': {'color': [255, 0, 0, 200], 'idcell': 1, 'pl_normal': [0.9999999403953552, 0.0, -0.0]}}, 'roi_cube': {'pos': [108.00353054658893, -98.51430151849954, 100.17562469666241], 'side': 194.76205444335938, 'color': [152, 251, 152], 'rotate_x': 43.36688268023689}, 'settings': {'proj_plane': 'YZ', 'ref_vect': 'Y+', 'ref_vectF': [[0, 1, 0], [0, 0, 0]], 'orient_vect': [[0.0, -38.75894546508789, 23.04160499572754], [0.0, -176.57174682617188, 153.2139129638672]], 'angle_deg': 43.36688268023689}}}, 'chNS': {'plot2d': False}, 'centreline': {'SimplifyMesh': {'plane_cuts': {'bottom': {'dir': True, 'pl_dict': {'pl_normal': [0.0031863666649780205, 0.9968034549983764, -0.07982931272894528], 'pl_centre': [108.79834848331649, -180.7342138772441, 108.23176550199149]}}, 'top': {'dir': False, 'pl_dict': {'pl_normal': [0.0, 0.7495431902766063, -0.661955441030563], 'pl_centre': [109.36814022064188, -10.718546489407998, 54.31639880977799]}}}, 'tol': 2.0}, 'vmtk_CL': {'voronoi': False}, 'buildCL': {'nPoints': 300, 'connect_cl': {'ch1_int': 'Option 1-Point in meshesCut4Cl', 'ch2_ext': 'Option 1-Point in meshesCut4Cl'}}, 'dirs': {'ch1': {'int': {'dir_cleanMesh': Path('LS23_F06_ch1_int_cut4cl.stl'), 'dir_meshLabMesh': Path('LS23_F06_ch1_int_cut4clML.stl')}}, 'ch2': {'ext': {'dir_cleanMesh': Path('LS23_F06_ch2_ext_cut4cl.stl'), 'dir_meshLabMesh': Path('LS23_F06_ch2_ext_cut4clML.stl')}}}}, 'heatmaps': {'th_i2e[ch1-tiss]': {'default': False, 'min_val': 0.0, 'max_val': 20.0, 'colormap': 'turbo', 'd3d2': True}, 'th_i2e[ch2-tiss]': {'default': False, 'min_val': 0.0, 'max_val': 20.0, 'colormap': 'turbo', 'd3d2': True}, 'th_i2e[chNS-tiss]': {'default': False, 'min_val': 0.0, 'max_val': 20.0, 'colormap': 'turbo', 'd3d2': True}, 'ball[ch1-ext(CL.ch1-int)]': {'default': False, 'min_val': 0.0, 'max_val': 70.0, 'colormap': 'turbo', 'd3d2': True}, 'ball[ch1-ext(CL.ch2-ext)]': {'default': False, 'min_val': 0.0, 'max_val': 70.0, 'colormap': 'turbo', 'd3d2': True}, 'ball[ch2-ext(CL.ch2-ext)]': {'default': False, 'min_val': 0.0, 'max_val': 70.0, 'colormap': 'turbo', 'd3d2': True}}, 'segments': {'radius': {'Cut1': 60}, 'use_centreline': True, 'centreline': 'myocardium (ch1_int)', 'setup': {'Cut1': {'ch_info': {'ch1': {'int': 'cut_with_ext-ext', 'tiss': 'cut_with_ext-ext', 'ext': 'ext-ext'}, 'ch2': {'int': 'cut_with_other_ext-ext', 'tiss': 'cut_with_other_ext-ext', 'ext': 'cut_with_other_ext-ext'}, 'chNS': {'tiss': 'cut_with_other_ext-ext'}}, 'measure': {'ch1': {'int': {}, 'tiss': {}, 'ext': {}}, 'ch2': {'int': {}, 'tiss': {}, 'ext': {}}, 'chNS': {'tiss': {}}}, 'dirs': {'ch1': {'int': {'segm1': Path('LS23_F06_Cut1_ch1_int_segm1.vtk'), 'segm2': Path('LS23_F06_Cut1_ch1_int_segm2.vtk')}, 'tiss': {}, 'ext': {'segm1': Path('LS23_F06_Cut1_ch1_ext_segm1.vtk'), 'segm2': Path('LS23_F06_Cut1_ch1_ext_segm2.vtk')}}, 'ch2': {'int': {}, 'tiss': {'segm1': Path('LS23_F06_Cut1_ch2_tiss_segm1.vtk'), 'segm2': Path('LS23_F06_Cut1_ch2_tiss_segm2.vtk')}, 'ext': {'segm1': Path('LS23_F06_Cut1_ch2_ext_segm1.vtk'), 'segm2': Path('LS23_F06_Cut1_ch2_ext_segm2.vtk')}}, 'chNS': {'tiss': {'segm1': Path('LS23_F06_Cut1_chNS_tiss_segm1.vtk'), 'segm2': Path('LS23_F06_Cut1_chNS_tiss_segm2.vtk')}}}, 'names': {'segm1': 'Cut1_ch1_ext_segm1', 'segm2': 'Cut1_ch1_ext_segm2'}, 'cut_info': {'Disc No.0': {'radius': 70, 'normal_unit': [-8.953277151450006, 1.8505357613110403, -4.051462161421751], 'pl_centre': [94.97468750186152, -100.62606927455202, 103.8687565120911], 'height': 0.45, 'color': 'purple', 'res': [0.22832596445005057, 0.22832596445005057, 0.46972965900571756]}}}}}}, 'measure': {'Vol(segm)': {'Cut1_ch1_int_segm1': 1026263.6682457177, 'Cut1_ch1_int_segm2': 502518.4665165625, 'Cut1_ch1_tiss_segm1': True, 'Cut1_ch1_tiss_segm2': True, 'Cut1_ch1_ext_segm1': 1217239.8473997868, 'Cut1_ch1_ext_segm2': 750104.1440213979, 'Cut1_ch2_int_segm1': True, 'Cut1_ch2_int_segm2': True, 'Cut1_ch2_tiss_segm1': 158680.0113253534, 'Cut1_ch2_tiss_segm2': 171255.81167165047, 'Cut1_ch2_ext_segm1': 696405.551346254, 'Cut1_ch2_ext_segm2': 450966.70804834936, 'Cut1_chNS_tiss_segm1': 329803.01532814425, 'Cut1_chNS_tiss_segm2': 46792.05463174141}, 'Ellip(segm)': {'Cut1_ch1_int_segm1': True, 'Cut1_ch1_int_segm2': True, 'Cut1_ch1_tiss_segm1': True, 'Cut1_ch1_tiss_segm2': True, 'Cut1_ch1_ext_segm1': True, 'Cut1_ch1_ext_segm2': True, 'Cut1_ch2_int_segm1': True, 'Cut1_ch2_int_segm2': True, 'Cut1_ch2_tiss_segm1': True, 'Cut1_ch2_tiss_segm2': True, 'Cut1_ch2_ext_segm1': True, 'Cut1_ch2_ext_segm2': True, 'Cut1_chNS_tiss_segm1': True, 'Cut1_chNS_tiss_segm2': True}, 'Vol(sect)': {'Cut1_ch1_tiss_sect1': True, 'Cut1_ch1_tiss_sect2': True, 'Cut1_ch2_tiss_sect1': True, 'Cut1_ch2_tiss_sect2': True, 'Cut1_chNS_tiss_sect1': True, 'Cut1_chNS_tiss_sect2': True, 'Cut2_ch1_tiss_sect1': True, 'Cut2_ch1_tiss_sect2': True, 'Cut2_ch2_tiss_sect1': True, 'Cut2_ch2_tiss_sect2': True, 'Cut2_chNS_tiss_sect1': True, 'Cut2_chNS_tiss_sect2': True}, 'SA': {}, 'Vol': {'ch1_int_whole': 1532652.3355905353, 'ch1_tiss_whole': 440917.6207903193, 'ch1_ext_whole': 1973605.2113114528, 'ch2_int_whole': 826054.9236657482, 'ch2_tiss_whole': 331162.01017873926, 'ch2_ext_whole': 1149048.2415037625, 'chNS_int_whole': 1149048.2415037625, 'chNS_tiss_whole': 382776.5852857098, 'chNS_ext_whole': 1532652.3355905353}, 'CL': {'ch1_int_whole': {'looped_length': 288.38489726465195, 'lin_length': 192.48130798339844}, 'ch2_ext_whole': 
{'looped_length': 286.2414221651852, 'lin_length': 193.7996826171875}}, 'th_i2e': {'ch1_tiss_whole': {'range_o': {'min_val': 0.0, 'max_val': 12.298886313341892}, 'range_user': {'min_val': 0.0, 'max_val': 20.0}, 'colormap': 'turbo'}, 'ch2_tiss_whole': {'range_o': {'min_val': -1.0539671592559017, 'max_val': 24.197131536474014}, 'range_user': {'min_val': 0.0, 'max_val': 20.0}, 'colormap': 'turbo'}, 'chNS_tiss_whole': {'range_o': {'min_val': -1.7124646059499976e-06, 'max_val': 20.183471102385848}, 'range_user': {'min_val': 0.0, 'max_val': 20.0}, 'colormap': 'turbo'}}, 'th_e2i': {}, 'ball': {'ch1_ext_(ch1_int)': True, 'ch1_ext_(ch2_ext)': {'range_o': 
{'min_val': 0.7076867391951892, 'max_val': 81.08640949025072}, 'range_user': {'min_val': 0.0, 'max_val': 70.0}, 'colormap': 'turbo'}, 'ch2_ext_(ch2_ext)': True}, 'LoopDir': {'roi': True}, 'hm3Dto2D': {'ch2_ext': True}}}

mH_settings =  {'setup': {'no_chs': 2, 'name_chs': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'chs_relation': {'ch1': 'external', 'ch2': 'internal'}, 'color_chs': {'ch1': {'int': 'gold', 'tiss': 'lightseagreen', 'ext': 'crimson'}, 'ch2': {'int': 'deepskyblue', 'tiss': 'darkmagenta', 'ext': 'deeppink'}}, 'orientation': {'stack': 'anterior, ventral, left', 'roi': 'anterior, ventral, left'}, 'rotateZ_90': True, 'mask_ch': {'ch1': False, 'ch2': False}, 'all_contained': True, 'one_contained': False, 'chNS': {'layer_btw_chs': True, 'ch_ext': ('ch1', 'int'), 'ch_int': ('ch2', 'ext'), 'operation': 'XOR', 'user_nsChName': 'cardiac jelly', 'color_chns': {'int': 'greenyellow', 'tiss': 'darkorange', 'ext': 'powderblue'}, 'keep_largest': {'tiss': False, 'int': True, 'ext': True}, 'alpha': {'tiss': 0.05, 'int': 0.05, 'ext': 0.05}, 'plot_settings': [False, None]}, 'segm': {'cutLayersIn2Segments': True, 'Cut1': {'no_segments': 2, 'obj_segm': 'Disc', 'no_cuts_4segments': 1, 'name_segments': {'segm1': 'atrium', 'segm2': 'ventricle'}, 'ch_segments': {'ch2': ['int', 'tiss'], 'chNS': ['tiss'], 'ch1': ['tiss', 'ext']}, 'colors': {'segm1': [247, 113, 137], 'segm2': [220, 137, 50]}}, 'measure': {'Vol': True, 'SA': False, 'Ellip': True, 'Angles': True}}, 'sect': {'cutLayersIn2Sections': True, 'Cut1': {'no_sections': 2, 'obj_sect': 'Centreline', 'name_sections': {'sect1': 'left', 'sect2': 'right'}, 'ch_sections': {'ch2': ['tiss'], 'chNS': ['tiss'], 'ch1': ['tiss']}, 'colors': {'sect1': [102, 194, 165], 'sect2': [252, 141, 98]}}, 'Cut2': {'no_sections': 2, 'obj_sect': 'Centreline', 'name_sections': {'sect1': 'dorsal', 'sect2': 'ventral'}, 'ch_sections': {'ch2': ['tiss'], 'chNS': ['tiss'], 'ch1': ['tiss']}, 'colors': {'sect1': [141, 160, 203], 'sect2': [231, 138, 195]}}, 'measure': {'Vol': True, 'SA': False}}, 'segm-sect': {'cutLayersIn2SegmSect': True, 'sCut1': {'Cut1': {'ch_segm_sect': ['ch1_tiss', 'chNS_tiss']}, 'Cut2': {'ch_segm_sect': ['ch2_tiss', 'chNS_tiss']}}, 'measure': {'Vol': True, 'SA': False}}, 'chs_all': {'ch1': 'myocardium', 'ch2': 'endocardium', 'chNS': 'cardiac jelly'}, 'params': {'0': {'s': 'SA', 'l': 'Surface Area'}, '1': {'s': 'Vol', 'l': 'Volume'}, '2': {'s': 'CL', 'l': 'Centreline', 'measure': {'looped_length': True, 'linear_length': True}}, '3': {'s': 'th_i2e', 'l': 'Thickness Heatmap (int>ext*)'}, '4': {'s': 'th_e2i', 'l': 'Thickness Heatmap (ext>int*)'}, '5': {'s': 'ball', 'l': 'Centreline>Tissue (Ballooning)', 'measure': {'1': {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch1', 'from_cl_type': 'int'}}}, '6': {'s': 'LoopDir', 'l': 'Looping Direction', 'description': '', 'type': 'categorical', 'categories': ['dorsoventral', 'dextral', 'sinistral']}}, 'keep_largest': {'ch1': {'int': True, 'tiss': False, 'ext': True}, 'ch2': {'int': True, 'tiss': False, 'ext': True}}, 'alpha': {'ch1': {'int': 0.05, 'tiss': 0.05, 'ext': 0.05}, 'ch2': {'int': 0.05, 'tiss': 0.05, 'ext': 0.05}}}, 'wf_info': {'keep_largest': {'ch1': {'int': True, 'tiss': False, 'ext': True}, 'ch2': {'int': True, 'tiss': False, 'ext': True}}, 'cleanup': {'ch2': {'cont': ['int', 'tiss', 'ext'], 'with_ch': 'ch1', 'with_cont': 'int', 'inverted': True}, 'plot2d': False}, 'orientation': {'stack': {'axis': 'anterior, ventral, left', 'planar_views': {'anterior': {'color': [255, 215, 0, 200], 'idcell': 3, 'pl_normal': [0.0, 1.0, 0.0]}, 'ventral': {'color': [0, 0, 205, 200], 'idcell': 5, 'pl_normal': [0.0, -0.0, 1.0]}, 'left': {'color': [255, 0, 0, 200], 'idcell': 1, 'pl_normal': [1.0, -0.0, -0.0]}}, 'stack_cube': {'pos': [104.11133310446859, -95.64685952862841, 111.28608846731674], 'side': 213.0, 'color': [152, 251, 152], 'rotateY': False}}, 'roi': {'axis': 'anterior, ventral, left', 'reorient': True, 'method': 'Centreline', 'centreline': 'myocardium (ch1_int)', 'plane_orient': 'YZ', 'vector_orient': 'Y+'}}, 'chNS': {'plot2d': False}}, 'measure': {'SA': {}, 'Vol': {'ch1_int_whole': 1339021.681832008, 'ch1_tiss_whole': 486483.03241369675, 'ch1_ext_whole': 1825785.097088925, 'ch2_int_whole': 734429.141889463, 'ch2_tiss_whole': 358974.1787526688, 'ch2_ext_whole': 1093248.9604772246, 'chNS_int_whole': 1093248.9604772246, 'chNS_tiss_whole': 244728.70615242305, 'chNS_ext_whole': 1339021.681832008}, 'CL': {'ch1_int_whole': True}, 'th_i2e': {'ch1_tiss_whole': True, 'ch2_tiss_whole': True, 'chNS_tiss_whole': True}, 'th_e2i': {'ch1_tiss_whole': True}, 'ball': {'ch1_int_(ch1_int)': True}, 'LoopDir': {'roi': True}, 'hm3Dto2D': {'ch1_int': True}, 'Vol(segm)': {'Cut1_ch2_int_segm1': True, 'Cut1_ch2_int_segm2': True, 'Cut1_ch2_tiss_segm1': True, 'Cut1_ch2_tiss_segm2': True, 'Cut1_chNS_tiss_segm1': True, 'Cut1_chNS_tiss_segm2': True, 'Cut1_ch1_tiss_segm1': True, 'Cut1_ch1_tiss_segm2': True, 'Cut1_ch1_ext_segm1': True, 'Cut1_ch1_ext_segm2': True}, 'Ellip(segm)': {'Cut1_ch2_int_segm1': True, 'Cut1_ch2_int_segm2': True, 'Cut1_ch2_tiss_segm1': True, 'Cut1_ch2_tiss_segm2': True, 'Cut1_chNS_tiss_segm1': True, 'Cut1_chNS_tiss_segm2': True, 'Cut1_ch1_tiss_segm1': True, 'Cut1_ch1_tiss_segm2': True, 'Cut1_ch1_ext_segm1': True, 'Cut1_ch1_ext_segm2': True}, 'Angles(segm)': {'Cut1_ch2_int_segm1': True, 'Cut1_ch2_int_segm2': True, 'Cut1_ch2_tiss_segm1': True, 'Cut1_ch2_tiss_segm2': True, 'Cut1_chNS_tiss_segm1': True, 'Cut1_chNS_tiss_segm2': True, 'Cut1_ch1_tiss_segm1': True, 'Cut1_ch1_tiss_segm2': True, 'Cut1_ch1_ext_segm1': True, 'Cut1_ch1_ext_segm2': True}, 'Vol(sect)': {'Cut1_ch2_tiss_sect1': True, 'Cut1_ch2_tiss_sect2': True, 'Cut1_chNS_tiss_sect1': True, 'Cut1_chNS_tiss_sect2': True, 'Cut1_ch1_tiss_sect1': True, 'Cut1_ch1_tiss_sect2': True, 'Cut2_ch2_tiss_sect1': True, 'Cut2_ch2_tiss_sect2': True, 'Cut2_chNS_tiss_sect1': True, 'Cut2_chNS_tiss_sect2': True, 'Cut2_ch1_tiss_sect1': True, 'Cut2_ch1_tiss_sect2': True}, 'Vol(segm-sect)': {'sCut1_Cut1_ch1_tiss_segm1_sect1': True, 'sCut1_Cut1_ch1_tiss_segm1_sect2': True, 'sCut1_Cut1_ch1_tiss_segm2_sect1': True, 'sCut1_Cut1_ch1_tiss_segm2_sect2': True, 'sCut1_Cut1_chNS_tiss_segm1_sect1': True, 'sCut1_Cut1_chNS_tiss_segm1_sect2': True, 'sCut1_Cut1_chNS_tiss_segm2_sect1': True, 'sCut1_Cut1_chNS_tiss_segm2_sect2': True, 'sCut1_Cut2_ch2_tiss_segm1_sect1': True, 'sCut1_Cut2_ch2_tiss_segm1_sect2': True, 'sCut1_Cut2_ch2_tiss_segm2_sect1': True, 'sCut1_Cut2_ch2_tiss_segm2_sect2': True, 'sCut1_Cut2_chNS_tiss_segm1_sect1': True, 'sCut1_Cut2_chNS_tiss_segm1_sect2': True, 'sCut1_Cut2_chNS_tiss_segm2_sect1': True, 'sCut1_Cut2_chNS_tiss_segm2_sect2': True}}}

measurements = {'SA': {}, 'Vol': {'ch1_int_whole': 1339021.681832008, 'ch1_tiss_whole': 486483.03241369675, 'ch1_ext_whole': 1825785.097088925, 'ch2_int_whole': 734429.141889463, 'ch2_tiss_whole': 358974.1787526688, 'ch2_ext_whole': 1093248.9604772246, 'chNS_int_whole': 1093248.9604772246, 'chNS_tiss_whole': 244728.70615242305, 'chNS_ext_whole': 1339021.681832008}, 'CL': {'ch1_int_whole': True}, 'th_i2e': {'ch1_tiss_whole': True, 'ch2_tiss_whole': True, 'chNS_tiss_whole': True}, 'th_e2i': {'ch1_tiss_whole': True}, 'ball': {'ch1_int_(ch1_int)': True}, 'LoopDir': {'roi': True}, 'hm3Dto2D': {'ch1_int': True}, 'Vol(segm)': {'Cut1_ch2_int_segm1': True, 'Cut1_ch2_int_segm2': True, 'Cut1_ch2_tiss_segm1': True, 'Cut1_ch2_tiss_segm2': True, 'Cut1_chNS_tiss_segm1': True, 'Cut1_chNS_tiss_segm2': True, 'Cut1_ch1_tiss_segm1': True, 'Cut1_ch1_tiss_segm2': True, 'Cut1_ch1_ext_segm1': True, 'Cut1_ch1_ext_segm2': True}, 'Ellip(segm)': {'Cut1_ch2_int_segm1': True, 'Cut1_ch2_int_segm2': True, 'Cut1_ch2_tiss_segm1': True, 'Cut1_ch2_tiss_segm2': True, 'Cut1_chNS_tiss_segm1': True, 'Cut1_chNS_tiss_segm2': True, 'Cut1_ch1_tiss_segm1': True, 'Cut1_ch1_tiss_segm2': True, 'Cut1_ch1_ext_segm1': True, 'Cut1_ch1_ext_segm2': True}, 'Angles(segm)': {'Cut1_ch2_int_segm1': True, 'Cut1_ch2_int_segm2': True, 'Cut1_ch2_tiss_segm1': True, 'Cut1_ch2_tiss_segm2': True, 'Cut1_chNS_tiss_segm1': True, 'Cut1_chNS_tiss_segm2': True, 'Cut1_ch1_tiss_segm1': True, 'Cut1_ch1_tiss_segm2': True, 'Cut1_ch1_ext_segm1': True, 'Cut1_ch1_ext_segm2': True}, 'Vol(sect)': {'Cut1_ch2_tiss_sect1': True, 'Cut1_ch2_tiss_sect2': True, 'Cut1_chNS_tiss_sect1': True, 'Cut1_chNS_tiss_sect2': True, 'Cut1_ch1_tiss_sect1': True, 'Cut1_ch1_tiss_sect2': True, 'Cut2_ch2_tiss_sect1': True, 'Cut2_ch2_tiss_sect2': True, 'Cut2_chNS_tiss_sect1': True, 'Cut2_chNS_tiss_sect2': True, 'Cut2_ch1_tiss_sect1': True, 'Cut2_ch1_tiss_sect2': True}, 'Vol(segm-sect)': {'sCut1_Cut1_ch1_tiss_segm1_sect1': True, 'sCut1_Cut1_ch1_tiss_segm1_sect2': True, 'sCut1_Cut1_ch1_tiss_segm2_sect1': True, 'sCut1_Cut1_ch1_tiss_segm2_sect2': True, 'sCut1_Cut1_chNS_tiss_segm1_sect1': True, 'sCut1_Cut1_chNS_tiss_segm1_sect2': True, 'sCut1_Cut1_chNS_tiss_segm2_sect1': True, 'sCut1_Cut1_chNS_tiss_segm2_sect2': True, 'sCut1_Cut2_ch2_tiss_segm1_sect1': True, 'sCut1_Cut2_ch2_tiss_segm1_sect2': True, 'sCut1_Cut2_ch2_tiss_segm2_sect1': True, 'sCut1_Cut2_ch2_tiss_segm2_sect2': True, 'sCut1_Cut2_chNS_tiss_segm1_sect1': True, 'sCut1_Cut2_chNS_tiss_segm1_sect2': True, 'sCut1_Cut2_chNS_tiss_segm2_sect1': True, 'sCut1_Cut2_chNS_tiss_segm2_sect2': True}}
import pandas as pd

params = mH_settings['setup']['params']
dict_names = {}
for pp in params:
    var = params[pp]
    dict_names[var['s']] = var['l']
dict_names['Ellip'] = 'Ellipsoid'
dict_names['Angles'] = 'Angles'

df_index = pd.DataFrame.from_dict(measurements, orient='index')
vars2drop = ['th_e2i', 'th_i2e', 'ball', 'hm3Dto2D']
vars = list(df_index.index)
for var in vars: 
    if var in vars2drop: 
        df_index = df_index.drop(var)
cols = list(df_index.columns)

#Add column with actual names of variables
var_names = []
for index, row in df_index.iterrows(): 
    try: 
        var_names.append(dict_names[index])
    except: 
        var, typpe = index.split('(')
        if typpe == 'segm)': 
            name = 'Segment'
        elif typpe == 'segm-sect)': 
            name = 'Segm-Reg'
        else: 
            name == 'Region'
        var_names.append(dict_names[var]+': '+name)

df_index['Parameter'] = var_names
df_index = df_index.reset_index()
df_index = df_index.drop(['index'], axis=1)
df_melt = pd.melt(df_index, id_vars = ['Parameter'],  value_vars=cols, value_name='Value')
df_melt = df_melt.rename(columns={"variable": "Tissue-Contour"})
df_meltf = df_melt.dropna()
mult_index= ['Parameter', 'Tissue-Contour']
df_multi = df_meltf.set_index(mult_index)

df_new = df_multi.copy(deep=True)
key_cl = {'lin_length': 'Linear Length', 'looped_length': 'Looped Length'}
if 'CL' in vars:
    dict_CL = {}
    df_CL = df_multi.loc[[dict_names['CL']]]
    for index, row in df_CL.iterrows():
        # print(index, row['Value'])
        if isinstance(row['Value'], dict): 
            merge = True
            df_new.drop(index, axis=0, inplace=True)
            for key, item in row['Value'].items():
                # print(key, item) 
                new_index = 'Centreline: '+key_cl[key]
                new_variable = index[1]
                dict_CL[(new_index, new_variable)] = item

    # print('dict_CL:',  dict_CL)
    if len(dict_CL) != 0: 
        df_CL = pd.DataFrame(dict_CL, index =[0])
        # print('df_CL:', df_CL)
        df_CL_melt = pd.melt(df_CL, var_name=mult_index,value_name='Value')
        df_CL_melt = df_CL_melt.set_index(mult_index)
        df_final = pd.concat([df_new, df_CL_melt])
        df_final = df_final.sort_values(by=['Parameter'])
    else: 
        df_final = df_new.sort_values(by=['Parameter'])

# key_ellip = {'lin_length': 'Linear Length', 'looped_length': 'Looped Length'}

#Change True Values to TBO
values_updated = []
for index, row in df_final.iterrows(): 
    # print(index, type(row['Value']))
    if isinstance(row['Value'], bool): 
        values_updated.append('TBO')
    else: 
        values_updated.append(row['Value'])

#Add column with better names
user_tiss_cont = []
name_chs = mH_settings['setup']['name_chs']
if isinstance(mH_settings['setup']['segm'], dict):
    name_segm = {}
    for cut in [key for key in mH_settings['setup']['segm'] if 'Cut' in key]:
        name_segm[cut] = mH_settings['setup']['segm'][cut]['name_segments']
if isinstance(mH_settings['setup']['sect'], dict):
    name_sect = {}
    for cut in [key for key in mH_settings['setup']['sect'] if 'Cut' in key]:
        name_sect[cut] = mH_settings['setup']['sect'][cut]['name_sections']
name_cont = {'int': 'internal', 'tiss': 'tissue', 'ext': 'external'}

for index, _ in df_final.iterrows(): 
    param, tiss_cont = index
    split_name = tiss_cont.split('_')
    # print(split_name, len(split_name))
    if len(split_name) == 1 and tiss_cont == 'roi': 
        namef = 'Organ/ROI'
    elif len(split_name) == 3: 
        ch, cont, _ = split_name
        namef = name_chs[ch]+ ' ('+name_cont[cont]+')'
    elif len(split_name) == 4: 
        # print('split_name:', split_name)
        cut, ch, cont, subm = split_name
        if 'segm' in subm: 
            namef = cut+': '+name_chs[ch]+ '-'+name_cont[cont]+' ('+name_segm[cut][subm]+')'
        else: 
            namef = cut+': '+name_chs[ch]+ '-'+name_cont[cont]+' ('+name_sect[cut][subm]+')'
        # print(namef)
    elif len(split_name) == 6: #Intersections
        # print('split_name:', split_name)
        scut, rcut, ch, cont, segm, sect = split_name
        namef = scut[1:]+'-'+rcut+': '+name_chs[ch]+ '-'+name_cont[cont]+' ('+name_segm[scut[1:]][segm]+'-'+name_sect[rcut][sect]+')'
    else: 
        print(index, len(split_name))
        namef = 'Check: '+tiss_cont
    
    # print(index, namef.title())
    nameff = namef.title()
    user_tiss_cont.append(nameff)

df_final['Value'] = values_updated
df_final['User (Tissue-Contour)'] = user_tiss_cont
df_finalf = df_final.reset_index()
df_finalf = df_finalf.set_index(mult_index+['User (Tissue-Contour)'])

df_finalf = df_finalf.sort_values(['Parameter','Tissue-Contour'],
                                        ascending = [True, True])

print('df_finalf: ', df_finalf)
self.df_res = df_finalf