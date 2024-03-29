# -*- coding: utf-8 -*-
'''
morphoHeart_config
Version: Nov 9, 2023

@author: Juliana Sanchez-Posada
'''
#%% Imports - ########################################################
import os
from pathlib import Path

#%% ##### - Authorship - #####################################################
__author__     = 'Juliana Sanchez-Posada'
__license__    = 'MIT'
__maintainer__ = 'J. Sanchez-Posada'
__email__      = 'julianasanchezposada@gmail.com'
__website__    = 'https://github.com/jsanchez679/morphoHeart'

#%% config class
class mH_Config():
    def __init__(self):
        self.version = '2.0.8'
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
        self.dev = False
        self.dev_plots = False
        self.dev_hm3d2d = False

mH_config = mH_Config()

print('morphoHeart! - Loaded config')

