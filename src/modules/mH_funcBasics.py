'''
morphoHeart_funcBasics

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% Imports 
from pathlib import Path
from playsound import playsound


#%% morphoHeart Imports 
from .mH_classes import Organ, Mesh_mH, ImChannel


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
        path = Path.cwd().parent
        sound_mp3= sound+'.mp3'
        path = path / 'sounds' / sound_mp3
        playsound(str(path))

#%% func - load_npy_stack
    # def load_npy_stack(organ:Organ, name:str):
        


#%% Module loaded
print('morphoHeart! - Loaded funcBasics')