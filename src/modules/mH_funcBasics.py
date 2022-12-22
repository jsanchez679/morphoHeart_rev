'''
morphoHeart_funcBasics

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% Imports 
import os
from pathlib import Path
from playsound import playsound
import json
import numpy as np 

path_fcBasics = os.path.abspath(__file__)
print(path_fcBasics)

#%% morphoHeart Imports 
from .mH_classes import Organ, Mesh_mH, ImChannel

#%% class - NumpyArrayEncoder
# Definition of class to save dictionary
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)

#%% -Functions
#%% func - alert
def alert(sound:str, alert_all=True):
    '''
    bubble:
    clown:
    connection:
    countdown:
    error:
    error_beep:
    frog: 
    jump:
    whistle:
    woohoo:
    '''
    mp3_basic = ['connection','woohoo']
    
    if alert_all or sound in mp3_basic:
        path = Path(path_fcBasics).parent.parent.parent
        print(path)
        sound_mp3= sound+'.mp3'
        path = path / 'sounds' / sound_mp3
        playsound(str(path))


def save_mHProject(dicts:list, organ:Organ):
    jsonDict_name = 'mH_'+organ.user_organName+'_project.json'
    json2save_dir = organ.dir_res / jsonDict_name

    with open(str(json2save_dir), "w") as write_file:
        json.dump(str(organ.dir_res), write_file, cls=NumpyArrayEncoder)
        print('\t>> Dictionary saved correctly!\n\t>> File: '+jsonDict_name)
        alert('countdown')

#%% func - load_npy_stack
    # def load_npy_stack(organ:Organ, name:str):
        


#%% Module loaded
print('morphoHeart! - Loaded funcBasics')