# -*- coding: utf-8 -*-
'''
morphoHeart_config

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
import os
from pathlib import Path

class mH_Config():
    def __init__(self):
        self.version = '2.0.1'
        self.gui_sound = (True, 'All')
        self.theme = 'Light'
        self.heart_default = False

        #Config for vedo plots
        self.txt_font = 'Dalim'
        self.leg_font = 'LogoType' # 'Quikhand' 'LogoType'  'Dalim'
        self.leg_width = 0.18
        self.leg_height = 0.2
        self.txt_size = 0.8
        self.txt_color = '#696969'
        self.txt_slider_size = 0.8

        self.path_o = os.path.abspath(__file__)
        self.path_mHImages = Path(self.path_o).parent.parent.parent / 'images'
        self.dev = True

mH_config = mH_Config()

print('morphoHeart! - Loaded config')

