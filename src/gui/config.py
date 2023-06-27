# -*- coding: utf-8 -*-
'''
morphoHeart_config

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''

class mH_Config():
    def __init__(self):
        self.version = '2.0.1'
        self.gui_sound = (True, 'All')
        self.theme = 'Light'
        self.heart_default = False

mH_config = mH_Config()

print('morphoHeart! - Loaded config')