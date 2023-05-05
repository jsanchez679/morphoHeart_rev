from pathlib import Path
#  (set_meas_param)
mH_settings =  {'no_chs': 2, 
                'name_chs': 
                        {'ch1': 'myocardium',
                        'ch2': 'endocardium'}, 
                'chs_relation': 
                        {'ch1': 'external', 
                        'ch2': 'internal'}, 
                'color_chs': 
                        {'ch1':
                                {'int': 'gold', 
                                  'tiss': 'lightseagreen', 
                                  'ext': 'crimson'},
                        'ch2': 
                                {'int': 'deepskyblue', 
                                 'tiss': 'darkmagenta', 
                                 'ext': 'deeppink'}}, 
                'orientation': 
                        {'stack': 'aaa,bbb,ccc', 
                         'roi': 'anterior, ventral, left'}, 
                'rotateZ_90': True, 
                'mask_ch': 
                        {'ch1': True,
                          'ch2': True}, 
                'chNS': 
                        {'layer_btw_chs': True, 
                         'ch_ext': ('ch1', 'int'), 
                         'ch_int': ('ch2', 'ext'), 
                         'user_nsChName': 'cardiac jelly', 
                         'color_chns': 
                                {'int': 'greenyellow', 
                                 'tiss': 'darkorange', 
                                 'ext': 'powderblue'}}, 
                'segm': {'cutLayersIn2Segments': True, 
                         'Cut1': 
                                {'no_segments': 2, 
                                 'obj_segm': 'Disc', 
                                 'no_cuts_4segments': 1, 
                                 'name_segments':
                                         {'segm1': 'atrium', 
                                          'segm2': 'ventricle'}, 
                                'ch_segments': 
                                        {'ch2': ['int', 'tiss'], 
                                         'chNS': ['tiss'], 
                                         'ch1': ['tiss', 'ext']}}, 
                        'measure': {'Vol': True, 'SA': True, 'Ellip': True}},
                'sect': {'cutLayersIn2Sections': True, 
                         'Cut1':
                                {'no_sections': 2, 
                                 'obj_sect': 'Centreline', 
                                 'name_sections': 
                                        {'sect1': 'left', 
                                         'sect2': 'right'}, 
                                'ch_sections': 
                                        {'ch2': ['int', 'tiss'], 
                                         'chNS': ['tiss'], 
                                         'ch1': ['tiss', 'ext']}}, 
                        'measure': {'Vol': True, 'SA': False}}}

proj = {'mH_projName': 'mH_Proj-202305031103', 
        'user_projName': 'Test_Juliana', 
        'info':
                 {'mH_projName': 'mH_Proj-202305031103', 
                  'user_projName': 'Test_Juliana', 
                  'user_projNotes': 'Juliana', 
                  'date_created': '2023-05-03', 
                  'dirs': []}, 
        'analysis':
                 {'morphoHeart': True, 
                  'morphoCell': False, 
                  'morphoPlot': False}, 
        'dir_proj': Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/morphoHeart_rev/vedo_changes/R_Test Juliana'), 
        'organs': {}, 
        'cellGroups': {}}

self.params= {0: {'s': 'SA', 'l': 'surface area'},
                1: {'s': 'Vol', 'l': 'volume'},
                 2: {'s': 'CL', 'l': 'centreline'},
                   3: {'s': 'th_i2e', 'l': 'thickness (int>ext)'},
                     4: {'s': 'th_e2i', 'l': 'thickness (ext>int)'},
                       5: {'s': 'ball', 'l': 'centreline>tissue (ballooning)'},
                         6: {'s': 'LoopDir', 'l': 'looping direction', 'description': 'nfnjfjdnfjknkj dnjsjkf', 'classes': ['dv', 'sin', 'dex']}}
self.centreline: {'looped_length': True, 'linear_length': True}


self.ballooning: {1: {'to_mesh': 'ch1', 'to_mesh_type': 'ext', 'from_cl': 'ch2', 'from_cl_type': 'ext'}, 2: {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch2', 'from_cl_type': 'ext'}}

self.user_params= {'SA': 
                        {'ch1:int:whole': False, 
                        'ch1:tiss:whole': False, 
                        'ch1:ext:whole': False, 
                        'ch2:int:whole': False, 
                        'ch2:tiss:whole': False, 
                        'ch2:ext:whole': False, 
                        'chNS:int:whole': False, 
                        'chNS:tiss:whole': False, 
                        'chNS:ext:whole': False}, 
                'Vol': 
                        {'ch1:int:whole': True, 
                        'ch1:tiss:whole': True, 
                        'ch1:ext:whole': True, 
                        'ch2:int:whole': True, 
                        'ch2:tiss:whole': True, 
                        'ch2:ext:whole': True, 
                        'chNS:int:whole': True, 
                        'chNS:tiss:whole': True, 
                        'chNS:ext:whole': True}, 
                'CL': 
                        {'ch1:int:whole': True, 
                       'ch1:ext:whole': False, 
                       'ch2:int:whole': False, 
                       'ch2:ext:whole': True, 
                       'chNS:int:whole': False, 
                       'chNS:ext:whole': False},
                'th_i2e': 
                        {'ch1:tiss:whole': True, 
                         'ch2:tiss:whole': True, 
                         'chNS:tiss:whole': True}, 
                'th_e2i':
                         {'ch1:tiss:whole': True, 
                          'ch2:tiss:whole': False, 
                          'chNS:tiss:whole': False}, 
                'ball':
                        {'ch1:int:whole': True, 
                         'ch1:ext:whole': True, 
                         'ch2:int:whole': False, 
                         'ch2:ext:whole': False},
                'LoopDir': 
                        {'ch1:int:whole': False, 
                         'ch1:tiss:whole': False, 
                         'ch1:ext:whole': True, 
                         'ch2:int:whole': False, 
                         'ch2:tiss:whole': False, 
                         'ch2:ext:whole': False, 
                         'chNS:int:whole': False, 
                         'chNS:tiss:whole': False, 
                         'chNS:ext:whole': False}, 
                'Vol(segm)': 
                        {'ch1:tiss:Cut1-segm1': True, 
                         'ch1:tiss:Cut1-segm2': True, 
                         'ch1:ext:Cut1-segm1': True, 
                         'ch1:ext:Cut1-segm2': True, 
                         'chNS:tiss:Cut1-segm1': True, 
                         'chNS:tiss:Cut1-segm2': True, 
                         'ch2:int:Cut1-segm1': True, 
                         'ch2:int:Cut1-segm2': True, 
                         'ch2:tiss:Cut1-segm1': True, 
                         'ch2:tiss:Cut1-segm2': True}, 
                'SA(segm)': 
                        {'ch1:tiss:Cut1-segm1': True, 
                         'ch1:tiss:Cut1-segm2': True, 
                         'ch1:ext:Cut1-segm1': True, 
                         'ch1:ext:Cut1-segm2': True, 
                         'chNS:tiss:Cut1-segm1': True, 
                         'chNS:tiss:Cut1-segm2': True, 
                         'ch2:int:Cut1-segm1': True, 
                         'ch2:int:Cut1-segm2': True, 
                         'ch2:tiss:Cut1-segm1': True, 
                         'ch2:tiss:Cut1-segm2': True}, 
                'Ellip(segm)': 
                        {'ch1:tiss:Cut1-segm1': True, 
                         'ch1:tiss:Cut1-segm2': True, 
                         'ch1:ext:Cut1-segm1': True, 
                         'ch1:ext:Cut1-segm2': True, 
                         'chNS:tiss:Cut1-segm1': True, 
                         'chNS:tiss:Cut1-segm2': True, 
                         'ch2:int:Cut1-segm1': True, 
                         'ch2:int:Cut1-segm2': True, 
                         'ch2:tiss:Cut1-segm1': True,
                        'ch2:tiss:Cut1-segm2': True},   
                'Vol(sect)': 
                        {'ch1:tiss:Cut1-sect1': True, 
                         'ch1:tiss:Cut1-sect2': True, 
                         'chNS:tiss:Cut1-sect1': True, 
                         'chNS:tiss:Cut1-sect2': True, 
                         'ch2:tiss:Cut1-sect1': True, 
                         'ch2:tiss:Cut1-sect2': True}}
