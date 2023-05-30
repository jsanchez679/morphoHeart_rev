# -*- coding: utf-8 -*-
'''
morphoHeart_config

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''

class mH_Config():
    def __init__(self):
        self.gui_sound = (True, 'All')
        self.theme = 'Light'

mH_config = mH_Config()

print('morphoHeart! - Loaded config')