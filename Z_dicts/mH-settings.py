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
                        'measure': {'volume': True, 'area': True, 'ellipsoids': True}},
                'sect': {'cutLayersIn2Sections': True, 
                         'Cut1':
                                {'no_sections': 2, 
                                 'obj_segm': 'Centreline', 
                                 'name_segments': 
                                        {'sect1': 'left', 
                                         'sect2': 'right'}, 
                                'ch_segments': 
                                        {'ch2': ['int', 'tiss'], 
                                         'chNS': ['tiss'], 
                                         'ch1': ['tiss', 'ext']}}, 
                        'measure': {'volume': True, 'area': False}}}


segm_dict = mH_settings['segm']
if isinstance(segm_dict, dict): 
    if segm_dict['cutLayersIn2Segments']: 
        cuts = [key for key in segm_dict if 'Cut' in key]
        params_segm = [param for param in segm_dict['measure'].keys() if segm_dict['measure'][param]]

user_params= {'SA_ch1:int:whole': False, 
                        'Vol_ch1:int:whole': True, 
                        'CL_ch1:int:whole': True, 
                        'ball_ch1:int:whole': True, 
                        'LoopDir_ch1:int:whole': False,
                        'SA_ch1:tiss:whole': False, 
                        'Vol_ch1:tiss:whole': True, 
                        'th_i2e_ch1:tiss:whole': True, 
                        'th_e2i_ch1:tiss:whole': True, 
                        'LoopDir_ch1:tiss:whole': False,
                        'SA_ch1:ext:whole': False, 
                        'Vol_ch1:ext:whole': True,
                        'CL_ch1:ext:whole': False, 
                        'ball_ch1:ext:whole': True, 
                        'LoopDir_ch1:ext:whole': False, 
                        'SA_ch2:int:whole': False, 
                        'Vol_ch2:int:whole': True,
                        'CL_ch2:int:whole': False, 
                        'ball_ch2:int:whole': False, 
                        'LoopDir_ch2:int:whole': False,
                        'SA_ch2:tiss:whole': False, 
                        'Vol_ch2:tiss:whole': True, 
                        'th_i2e_ch2:tiss:whole': True,
                        'th_e2i_ch2:tiss:whole': False, 
                        'LoopDir_ch2:tiss:whole': False, 
                        'SA_ch2:ext:whole': False, 
                        'Vol_ch2:ext:whole': True, 
                        'CL_ch2:ext:whole': True, 
                        'ball_ch2:ext:whole': False, 
                        'LoopDir_ch2:ext:whole': False, 
                        'SA_chNS:int:whole': False, 
                        'Vol_chNS:int:whole': True, 
                        'CL_chNS:int:whole': False, 
                        'LoopDir_chNS:int:whole': False, 
                        'SA_chNS:tiss:whole': False, 
                        'Vol_chNS:tiss:whole': True, 
                        'th_i2e_chNS:tiss:whole': True, 
                        'th_e2i_chNS:tiss:whole': False, 
                        'LoopDir_chNS:tiss:whole': False, 
                        'SA_chNS:ext:whole': False, 
                        'Vol_chNS:ext:whole': True, 
                        'CL_chNS:ext:whole': False, 
                        'LoopDir_chNS:ext:whole': False, 

                        'Vol(segm)_ch2:int:Cut1-segm1': True, 
                        'Vol(segm)_ch2:int:Cut1-segm2': True, 
                        'SA(segm)_ch2:int:Cut1-segm1': True, 
                        'SA(segm)_ch2:int:Cut1-segm2': True, 
                        'Ellip(segm)_ch2:int:Cut1-segm1': True, 
                        'Ellip(segm)_ch2:int:Cut1-segm2': True, 
                        'Vol(segm)_ch2:tiss:Cut1-segm1': True, 
                        'Vol(segm)_ch2:tiss:Cut1-segm2': True, 
                        'SA(segm)_ch2:tiss:Cut1-segm1': True, 
                        'SA(segm)_ch2:tiss:Cut1-segm2': True, 
                        'Ellip(segm)_ch2:tiss:Cut1-segm1': True,
                        'Ellip(segm)_ch2:tiss:Cut1-segm2': True, 
                        'Vol(segm)_ch1:tiss:Cut1-segm1': True, 
                        'Vol(segm)_ch1:tiss:Cut1-segm2': True, 
                        'SA(segm)_ch1:tiss:Cut1-segm1': True, 
                        'SA(segm)_ch1:tiss:Cut1-segm2': True, 
                        'Ellip(segm)_ch1:tiss:Cut1-segm1': True, 
                        'Ellip(segm)_ch1:tiss:Cut1-segm2': True, 
                        'Vol(segm)_ch1:ext:Cut1-segm1': True, 
                        'Vol(segm)_ch1:ext:Cut1-segm2': True, 
                        'SA(segm)_ch1:ext:Cut1-segm1': True, 
                        'SA(segm)_ch1:ext:Cut1-segm2': True, 
                        'Ellip(segm)_ch1:ext:Cut1-segm1': True, 
                        'Ellip(segm)_ch1:ext:Cut1-segm2': True, 
                        'Vol(segm)_chNS:tiss:Cut1-segm1': True, 
                        'Vol(segm)_chNS:tiss:Cut1-segm2': True, 
                        'SA(segm)_chNS:tiss:Cut1-segm1': True, 
                        'SA(segm)_chNS:tiss:Cut1-segm2': True, 
                        'Ellip(segm)_chNS:tiss:Cut1-segm1': True,
                        'Ellip(segm)_chNS:tiss:Cut1-segm2': True, 

                        'Vol(sect)_ch2:tiss:Cut1-sect1': True, 
                        'Vol(sect)_ch2:tiss:Cut1-sect2': True, 
                        'Vol(sect)_ch1:tiss:Cut1-sect1': True, 
                        'Vol(sect)_ch1:tiss:Cut1-sect2': True, 
                        'Vol(sect)_chNS:tiss:Cut1-sect1': True,
                        'Vol(sect)_chNS:tiss:Cut1-sect2': True}

{'mH_projName': 'mH_Proj-202305051641', 
 'user_projName': 'testing_project', 
 'info': 
    {'mH_projName': 'mH_Proj-202305051641', 
     'user_projName': 'testing_project', 
     'user_projNotes': 'aaaaa notes', 
     'date_created': '2023-05-05', 
     'dirs': []}, 
'analysis': 
    {'morphoHeart': True, 
     'morphoCell': False,
    'morphoPlot': False}, 
'dir_proj': WindowsPath('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/R_testing project'), 
'organs': {}, 
'cellGroups': {}, 
'mH_settings': 
    {'setup': 
        {'no_chs': 2, 
         'name_chs': 
            {'ch1': 'myocardium', 
             'ch2': 'endocardium', 
             'chNS': 'cardiac jelly'}, 
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
            {'stack': 'anterior, ventral, left', 
             'roi': 'anterior, ventral, left'}, 
        'rotateZ_90': True, 
        'mask_ch': 
            {'ch1': False, 
             'ch2': False}, 
        'chNS': 
            {'layer_btw_chs': True, 
             'ch_ext': ('ch1', 'int'), 
             'ch_int': ('ch2', 'ext'), 
             'user_nsChName': 'cardiac jelly', 
             'color_chns': 
                {'int': 'greenyellow', 
                 'tiss': 'darkorange', 
                 'ext': 'powderblue'}}, 
        'segm': 
            {'cutLayersIn2Segments': True, 
             'Cut1': 
                {'no_segments': 2, 
                 'obj_segm': 'Disc', 
                 'no_cuts_4segments': 1, 
                 'name_segments': 
                    {'segm1': 'atrium', 
                     'segm2': 'ventricle'}, 
                'ch_segments': 
                    {'chNS': ['tiss'], 
                     'ch2': ['int', 'tiss'], 
                     'ch1': ['tiss', 'ext']}}, 
                'measure': {'Vol': True, 
                            'SA': True, 
                            'Ellip': True}}, 
        'sect': 
            {'cutLayersIn2Sections': True, 
             'Cut1':
                {'no_sections': 2, 
                 'obj_sect': 'Centreline', 
                 'name_sections': 
                    {'sect1': 'left', 
                     'sect2': 'right'}, 
                'ch_sections': 
                    {'chNS': ['tiss'], 
                     'ch2': ['tiss'], 
                     'ch1': ['tiss']}}, 
            'measure': {'Vol': True, 'SA': False}}, 
        'chs_all': 
            {'ch1': 'myocardium', 
             'ch2': 'endocardium', 
             'chNS': 'cardiac jelly'},
        'params': 
            {0: {'s': 'SA', 'l': 'surface area'}, 
             1: {'s': 'Vol', 'l': 'volume'}, 
             2: {'s': 'CL', 'l': 'centreline', 'measure': {'looped_length': True, 'linear_length': True}}, 
             3: {'s': 'th_i2e', 'l': 'thickness (int>ext)'}, 
             4: {'s': 'th_e2i', 'l': 'thickness (ext>int)'}, 
             5: {'s': 'ball', 'l': 'centreline>tissue (ballooning)', 'measure': {1: {'to_mesh': 'ch1', 'to_mesh_type': 'int', 'from_cl': 'ch2', 'from_cl_type': 'ext'}}}, 
             6: {'s': 'LoopDir', 'l': 'looping direction', 'description': "heart's looping direction", 'classes': ['dv', 'dex', 'sin']}}},

        'wf_info': {}, 
        'measure': {'SA': {}, 
                    'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True, 'ch2:int:whole': True, 'ch2:tiss:whole': True, 'ch2:ext:whole': True, 'chNS:int:whole': True, 'chNS:tiss:whole': True, 'chNS:ext:whole': True}, 
                    'CL': {'ch2:ext:whole': True}, 'th_i2e': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 
                    'th_e2i': {'ch1:tiss:whole': True}, 
                    'ball': {'ch1:int:whole': True}, 
                    'LoopDir': {'ch1:ext:whole': True}, 
                    'Vol(segm)': {'chNS:tiss:Cut1-segm1': True, 'chNS:tiss:Cut1-segm2': True, 'ch2:int:Cut1-segm1': True, 'ch2:int:Cut1-segm2': True, 'ch2:tiss:Cut1-segm1': True, 'ch2:tiss:Cut1-segm2': True, 'ch1:tiss:Cut1-segm1': True, 'ch1:tiss:Cut1-segm2': True, 'ch1:ext:Cut1-segm1': True, 'ch1:ext:Cut1-segm2': True}, 
                    'SA(segm)': {'chNS:tiss:Cut1-segm1': True, 'chNS:tiss:Cut1-segm2': True, 'ch2:int:Cut1-segm1': True, 'ch2:int:Cut1-segm2': True, 'ch2:tiss:Cut1-segm1': True, 'ch2:tiss:Cut1-segm2': True, 'ch1:tiss:Cut1-segm1': True, 'ch1:tiss:Cut1-segm2': True, 'ch1:ext:Cut1-segm1': True, 'ch1:ext:Cut1-segm2': True}, 
                    'Ellip(segm)': {'chNS:tiss:Cut1-segm1': True, 'chNS:tiss:Cut1-segm2': True, 'ch2:int:Cut1-segm1': True, 'ch2:int:Cut1-segm2': True, 'ch2:tiss:Cut1-segm1': True, 'ch2:tiss:Cut1-segm2': True, 'ch1:tiss:Cut1-segm1': True, 'ch1:tiss:Cut1-segm2': True, 'ch1:ext:Cut1-segm1': True, 'ch1:ext:Cut1-segm2': True}, 
                    'Vol(sect)': {'chNS:tiss:Cut1-sect1': True, 'chNS:tiss:Cut1-sect2': True, 'ch2:tiss:Cut1-sect1': True, 'ch2:tiss:Cut1-sect2': True, 'ch1:tiss:Cut1-sect1': True, 'ch1:tiss:Cut1-sect2': True}}}, 
        'mH_channels': 
            {'ch1': 'myocardium', 
             'ch2': 'endocardium', 
             'chNS': 'cardiac jelly'}, 
        'mH_segments': 
            {'Cut1': {'segm1': 'atrium', 'segm2': 'ventricle'}}, 
        'mH_sections': 
            {'Cut1': {'sect1': 'left', 'sect2': 'right'}}, 

        'mH_param2meas': {'SA': {}, 'Vol': {'ch1:int:whole': True, 'ch1:tiss:whole': True, 'ch1:ext:whole': True, 'ch2:int:whole': True, 'ch2:tiss:whole': True, 'ch2:ext:whole': True, 'chNS:int:whole': True, 'chNS:tiss:whole': True, 'chNS:ext:whole': True}, 'CL': {'ch2:ext:whole': True}, 'th_i2e': {'ch1:tiss:whole': True, 'ch2:tiss:whole': True, 'chNS:tiss:whole': True}, 'th_e2i': {'ch1:tiss:whole': True}, 'ball': {'ch1:int:whole': True}, 'LoopDir': {'ch1:ext:whole': True}, 'Vol(segm)': {'chNS:tiss:Cut1-segm1': True, 'chNS:tiss:Cut1-segm2': True, 'ch2:int:Cut1-segm1': True, 'ch2:int:Cut1-segm2': True, 'ch2:tiss:Cut1-segm1': True, 'ch2:tiss:Cut1-segm2': True, 'ch1:tiss:Cut1-segm1': True, 'ch1:tiss:Cut1-segm2': True, 'ch1:ext:Cut1-segm1': True, 'ch1:ext:Cut1-segm2': True}, 'SA(segm)': {'chNS:tiss:Cut1-segm1': True, 'chNS:tiss:Cut1-segm2': True, 'ch2:int:Cut1-segm1': True, 'ch2:int:Cut1-segm2': True, 'ch2:tiss:Cut1-segm1': True, 'ch2:tiss:Cut1-segm2': True, 'ch1:tiss:Cut1-segm1': True, 'ch1:tiss:Cut1-segm2': True, 'ch1:ext:Cut1-segm1': True, 'ch1:ext:Cut1-segm2': True}, 'Ellip(segm)': {'chNS:tiss:Cut1-segm1': True, 'chNS:tiss:Cut1-segm2': True, 'ch2:int:Cut1-segm1': True, 'ch2:int:Cut1-segm2': True, 'ch2:tiss:Cut1-segm1': True, 'ch2:tiss:Cut1-segm2': True, 'ch1:tiss:Cut1-segm1': True, 'ch1:tiss:Cut1-segm2': True, 'ch1:ext:Cut1-segm1': True, 'ch1:ext:Cut1-segm2': True}, 'Vol(sect)': {'chNS:tiss:Cut1-sect1': True, 'chNS:tiss:Cut1-sect2': True, 'ch2:tiss:Cut1-sect1': True, 'ch2:tiss:Cut1-sect2': True, 'ch1:tiss:Cut1-sect1': True, 'ch1:tiss:Cut1-sect2': True}}, 
        
        'mH_methods': ['A-Create3DMesh', 'B-TrimMesh', 'C-Centreline', 'D-Ballooning', 'D-Thickness_int>ext', 'D-Thickness_ext>int', 'E-Segments', 'E-Sections'], 
        'mC_settings': {}}
