
# change mH_settings out of gui to look like this
#then change the proj class to get info from this directly? check
# 
mH_settings = {'setup': 
                    {'no_chs': 2,
                    'channels': 
                            {'ch1': 
                                {'name_ch': 'myoc', 
                                'ch_relation': 'external',
                                'color_ch': 
                                    {'int': '', 
                                    'tiss': '',
                                    'ext': ''},
                                'mask_ch': True},
                            'ch2': 
                                {'name_ch': 'endo', 
                                'ch_relation': 'internal',
                                'color_ch': 
                                    {'int': '', 
                                    'tiss': '',
                                    'ext': ''},
                                'mask_ch': True},
                        'chNS': {'layer_btw_chs': True, 
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
                                                {'ch1': ['tiss', 'ext'], 
                                                'ch2': ['int', 'tiss'], 
                                                'chNS': ['tiss']}}, 
                                'measure': 
                                        {'volume': True, 
                                        'area': True, 
                                        'ellipsoids': True}}, 
                        'sect': {'cutLayersIn2Sections': True, 
                                'Cut1': 
                                    {'no_sections': 2, 
                                    'obj_segm': 'Centreline', 
                                    'name_segments':
                                            {'sect1': 'left',
                                            'sect2': 'right'}, 
                                    'ch_segments': 
                                            {'ch1': ['tiss'],
                                            'ch2': ['tiss'],
                                            'chNS': ['tiss']}}, 
                                'measure': 
                                        {'volume': True, 
                                        'area': False}},
                        'orientation': {},
                        'rotateZ_90': True}},
                'measure': {},
                'wf': {}}