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


user_param = {'SA:ch1:int:whole': True, 
              'Vol:ch1:int:whole': True, 
              'CL:ch1:int:whole': True, 
              'CLlin:ch1:int:whole': True, 
              'CLloop:ch1:int:whole': True, 
              'th_i2e:ch1:int:whole': False, 
              'th_e2i:ch1:int:whole': False, 
              'ball:ch1:int:whole': True, 
              'LoopDir:ch1:int:whole': False, 
              'SA:ch1:tiss:whole': True, 
              'Vol:ch1:tiss:whole': True, 
              'CL:ch1:tiss:whole': False, 
              'CLlin:ch1:tiss:whole': False, 
              'CLloop:ch1:tiss:whole': False, 
              'th_i2e:ch1:tiss:whole': True, 
              'th_e2i:ch1:tiss:whole': True, 
              'ball:ch1:tiss:whole': False, 
              'LoopDir:ch1:tiss:whole': False, 
              'SA:ch1:ext:whole': True, 'Vol:ch1:ext:whole': True, 'CL:ch1:ext:whole': True, 'CLlin:ch1:ext:whole': False, 'CLloop:ch1:ext:whole': False, 'th_i2e:ch1:ext:whole': False, 'th_e2i:ch1:ext:whole': False, 'ball:ch1:ext:whole': True, 'LoopDir:ch1:ext:whole': False, 'SA:ch2:int:whole': True, 'Vol:ch2:int:whole': True, 'CL:ch2:int:whole': True, 'CLlin:ch2:int:whole': False, 'CLloop:ch2:int:whole': False, 'th_i2e:ch2:int:whole': False, 'th_e2i:ch2:int:whole': False, 'ball:ch2:int:whole': False, 'LoopDir:ch2:int:whole': False, 'SA:ch2:tiss:whole': True, 'Vol:ch2:tiss:whole': True, 'CL:ch2:tiss:whole': False, 'CLlin:ch2:tiss:whole': False, 'CLloop:ch2:tiss:whole': False, 'th_i2e:ch2:tiss:whole': True, 'th_e2i:ch2:tiss:whole': True, 'ball:ch2:tiss:whole': False, 'LoopDir:ch2:tiss:whole': False, 'SA:ch2:ext:whole': True, 'Vol:ch2:ext:whole': True, 'CL:ch2:ext:whole': False, 'CLlin:ch2:ext:whole': False, 'CLloop:ch2:ext:whole': False, 'th_i2e:ch2:ext:whole': False, 'th_e2i:ch2:ext:whole': False, 'ball:ch2:ext:whole': False, 'LoopDir:ch2:ext:whole': False, 'SA:chNS:int:whole': True, 'Vol:chNS:int:whole': True, 'CL:chNS:int:whole': False, 'CLlin:chNS:int:whole': False, 'CLloop:chNS:int:whole': False, 'th_i2e:chNS:int:whole': False, 'th_e2i:chNS:int:whole': False, 'ball:chNS:int:whole': False, 'LoopDir:chNS:int:whole': False, 'SA:chNS:tiss:whole': True, 'Vol:chNS:tiss:whole': True, 'CL:chNS:tiss:whole': False, 'CLlin:chNS:tiss:whole': False, 'CLloop:chNS:tiss:whole': False, 'th_i2e:chNS:tiss:whole': True, 'th_e2i:chNS:tiss:whole': True, 'ball:chNS:tiss:whole': False, 'LoopDir:chNS:tiss:whole': False, 'SA:chNS:ext:whole': True, 'Vol:chNS:ext:whole': True, 'CL:chNS:ext:whole': False, 'CLlin:chNS:ext:whole': False, 'CLloop:chNS:ext:whole': False, 'th_i2e:chNS:ext:whole': False, 'th_e2i:chNS:ext:whole': False, 'ball:chNS:ext:whole': False, 'LoopDir:chNS:ext:whole': False}