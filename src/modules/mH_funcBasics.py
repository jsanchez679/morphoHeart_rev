'''
morphoHeart_funcBasics

@author: Juliana Sanchez-Posada
'''
#%% Imports - ########################################################
import os
from pathlib import Path, PurePath
from playsound import playsound
import numpy as np 
import flatdict
from functools import reduce  
import operator
from itertools import count
import vedo as vedo
import copy
import pandas as pd
import seaborn as sns

path_fcBasics = os.path.abspath(__file__)

#%% morphoHeart Imports - ##################################################
from ..gui.config import mH_config

alert_all=True
heart_default=False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}

#%% - morphoHeart Basic General Functions 
def alert(sound:str):
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
    # print('alert: ', mH_config.gui_sound)
    mp3_basic = ['connection','woohoo', 'error_beep', 'error']
    
    if mH_config.gui_sound[0]: 
        if mH_config.gui_sound[1] == 'Minimal' and sound in mp3_basic:
            sound_on = True
        elif mH_config.gui_sound[1] == 'Minimal' and sound not in mp3_basic:
            sound_on = False
        else: 
            sound_on = True
    else: 
        sound_on = False
    try: 
        if sound_on: 
            path_parentSounds = Path(path_fcBasics).parent.parent.parent
            sound_mp3= sound +'.mp3'
            path = path_parentSounds / 'sounds' / sound_mp3
            playsound(str(path))
            if sound == 'error_beep': 
                print('EEERROR')
    except:# playsound.PlaysoundException: 
        print('sound not played: ', sound)
        pass

def input_range(response):
    try: 
        obj_num = []
        comma_split = response.split(',')
        print(comma_split)
        for string in comma_split:
            if '-' in string:
                minus_split = string.split('-')
                print(minus_split)
                for n in list(range(int(minus_split[0]),int(minus_split[1])+1,1)):
                    obj_num.append(n)
                    print('Appended: ', str(n))
            else:
                obj_num.append(int(string))
                print('Appended2: ', string)
        return obj_num
    except: 
        obj_num = 'error'

# Dataframes
def df_reset_index(df:pd.DataFrame, mult_index:list): 

    df_new = df.reset_index()
    # print(df_new.head(10))
    df_new = df_new.set_index(mult_index)
    # print(df_new.head(10), '\n', df_new.index)

    return df_new

def df_add_value(df:pd.DataFrame, index:tuple, value):

    df.loc[index, 'Value'] = value
    print('New value: ',df.loc[index, 'Value'])

    return df

# Dictionaries
def compare_dicts(dict_1, dict_2, dict_1_name, dict_2_name, path="", ignore_dir=False):
    """Compare two dictionaries recursively to find non mathcing elements
    https://stackoverflow.com/questions/27265939/comparing-python-dictionaries-and-nested-dictionaries

    Args:
        dict_1: dictionary 1
        dict_2: dictionary 2

    Returns:

    """
    from .mH_classes_new import Project, Organ, ImChannel, ImChannelNS, ContStack, Mesh_mH
    
    err = ''
    key_err = ''
    value_err = ''
    old_path = path
    for k in dict_1.keys():
        path = old_path + "[%s]" % k
        if not k in dict_2:
            key_err += "\tKey %s%s not in %s\n" % (dict_1_name, path, dict_2_name)
        else:
            if isinstance(dict_1[k], dict) and isinstance(dict_2[k], dict):
                err += compare_dicts(dict_1[k],dict_2[k], dict_1_name, dict_2_name, path)#'d1','d2', path)
            else:
                if 'dir' in k: 
                    if str(dict_1[k]) != str(dict_2[k]):
                        value_err += "Value of %s%s (%s) not same as \n\t %s%s (%s)\n"\
                            % (dict_1_name, path, dict_1[k], dict_2_name, path, dict_2[k])
                            
                elif isinstance(dict_1[k], np.ndarray) or isinstance(dict_2[k], np.ndarray):
                    # print(k)
                    if not isinstance(dict_1[k], np.ndarray):
                        dd1 = np.array(dict_1[k])
                    else: 
                        dd1 = dict_1[k]
                        
                    if not isinstance(dict_2[k], np.ndarray):
                        dd2 = np.array(dict_2[k])
                    else: 
                        dd2 = dict_2[k]

                    comparison = dd1 == dd2
                    equal_arrays = comparison.all()
                    if not equal_arrays: 
                        value_err += "Value of %s%s (%s) not same as \n\t %s%s (%s)\n"\
                            % (dict_1_name, path, dict_1[k], dict_2_name, path, dict_2[k])
                            
                else: 
                    if not isinstance(dict_1[k], (Project, Organ, ImChannel, ImChannelNS, ContStack, Mesh_mH, vedo.Mesh)):
                        # print(k)
                        if dict_1[k] != dict_2[k]:
                            value_err += "Value of %s%s (%s) not same as \n\t %s%s (%s)\n"\
                                % (dict_1_name, path, dict_1[k], dict_2_name, path, dict_2[k])
                    # else: 
                    #     print(type(dict_1[k]))


    for k in dict_2.keys():
        path = old_path + "[%s]" % k
        if not k in dict_1:
            key_err += "\tKey %s%s not in %s\n" % (dict_2_name, path, dict_1_name)

    res = key_err + value_err + err
    return res

def compare_nested_dicts(dict_1, dict_2, dict_1_name, dict_2_name, path=""):
    
    res = compare_dicts(dict_1, dict_2, dict_1_name, dict_2_name, path="")
    if len(res) ==0:
        return '\tNo differences!'
    else: 
        return res
    
def update_gui_set(loaded:dict, current:dict): 
    flat_loaded = flatdict.FlatDict(loaded)
    flat_current = flatdict.FlatDict(current)
    current_keys = flat_current.keys()

    changed = False
    final_dict = copy.deepcopy(loaded)
    for key in current_keys: 
        # print('>>', key)
        value_current = get_by_path(current, key.split(':'))
        # print('current:',value_current)
        try: 
            value_loaded = get_by_path(loaded, key.split(':'))
            # print('loaded:',value_loaded)

            if value_current != value_loaded:
                print('value_current != value_loaded:', value_current, value_loaded, '- key: ', key)
                if value_current == {} and isinstance(value_loaded, dict): 
                    print('>> NOT Changed')
                    pass
                else: 
                    set_by_path(final_dict, key.split(':'),value_current)
                    changed = True
        except: 
            # print('add key to loaded!')
            changed = True
            try: 
                set_by_path(final_dict, key.split(':'), value_current)
            except KeyError as e: 
                key_error = e.args[0]
                #Get the position of that key in the flat key
                split_key = key.split(':')
                len_all_keys = len(split_key)
                index = split_key.index(key_error)
                #Get the length of the keys that need to be added
                len_key = len(split_key[index:])
                for num in range(len_key):
                    # print(split_key, index+num)
                    key2add = split_key[:index+num+1]
                    # print('key2add:', key2add)
                    if num != len_key-1:
                        set_by_path(final_dict, key2add, {})
                    else:
                        set_by_path(final_dict, key2add, value_current)
    
    print('GUI:', current)
    print('Loaded_o: ',loaded)
    print('Loaded_f: ',final_dict)

    return final_dict, changed
        
def get_by_path(root_dict, items):
    """Access a nested object in root_dict by item sequence.
    by Martijn Pieters (https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """
    return reduce(operator.getitem, items, root_dict)

def set_by_path(root_dict, items, value, add=False):
    """Set a value in a nested object in root_dict by item sequence.
    by Martijn Pieters (https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """    
    get_by_path(root_dict, items[:-1])[items[-1]] = value

def del_by_path(root_dict, items):
    """Delete a key-value in a nested object in root_dict by item sequence.
    by Martijn Pieters (https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """
    del get_by_path(root_dict, items[:-1])[items[-1]]

def make_Paths(load_dict):
    
    flat_dict = flatdict.FlatDict(copy.deepcopy(load_dict))
    # Make all paths into Path
    dir_keys = [key.split(':') for key in flat_dict.keys() if 'dir' in key and 'direction' not in key]
    # print(dir_keys)
    for key in dir_keys:
        # print('key:', key)
        value = get_by_path(load_dict, key)
        # print('value:', value)
        if isinstance(value, dict) and len(value) == 0: 
            pass
        elif value != None and value != 'NotAssigned' and not isinstance(value, bool):
            set_by_path(load_dict, key, Path(value))
    
    return load_dict
            
def make_tuples(load_dict, tuple_keys): 
    flat_dict = flatdict.FlatDict(copy.deepcopy(load_dict))
    #Make all keys from input list into tuples
    separator = ':'
    for tup in tuple_keys:
        str_tup = separator.join(tup)
        if str_tup in flat_dict.keys(): 
            value = get_by_path(load_dict, tup)
            if value != None:
                set_by_path(load_dict, tup, tuple(value))
        
    return load_dict

def check_gral_loading(proj, proj_name, dir_proj, organ=[], organ_name=''):
    
    from .mH_classes import Project, Organ
    
    proj_new = Project(new = False, name = proj_name, dir_proj = dir_proj)
    print('>> Check Project: \n',compare_nested_dicts(proj.__dict__,proj_new.__dict__,'proj','new'))
   
    if isinstance(organ, Organ):
        organ_new = proj_new.load_organ(user_organName = organ_name)   
        print('>> Check Organ: \n',compare_nested_dicts(organ.__dict__,organ_new.__dict__,'organ','new'))  
        
        for ch in organ.obj_imChannels: 
            ch_m = organ.obj_imChannels[ch]
            ch_mn = organ_new.obj_imChannels[ch]
            print('>> Check ',ch,': \n',compare_nested_dicts(ch_m.__dict__,ch_mn.__dict__,'orig','new'))  
        
        for chNS in organ.obj_imChannelNS: 
            chNS_m = organ.obj_imChannelNS[chNS]
            chNS_mn = organ_new.obj_imChannelNS[chNS]
            print('>> Check ',chNS,': \n',compare_nested_dicts(chNS_m.__dict__,chNS_mn.__dict__,'orig','new'))  
        
        if len(organ.obj_meshes) != len(organ_new.obj_meshes):
            print('organ.obj_meshes: ', organ.obj_meshes)
            print('organ_new.obj_meshes: ', organ_new.obj_meshes)
            
        for obj in organ.obj_meshes: 
            obj_m = organ.obj_meshes[obj]
            obj_mn = organ_new.obj_meshes[obj]
            print('>> Check ',obj,': \n',compare_nested_dicts(obj_m.__dict__,obj_mn.__dict__,'orig','new'))  
        
        del organ_new
        
    del proj_new
    
# Color palette as RGB
def palette_rbg(name:str, num:int, rgb=True):
    rgb_colors = []
    palette =  sns.color_palette(name, num)
    if rgb: 
        for color in palette:
            tup = []
            for value in color:
                tup.append(round(value*255))
            rgb_colors.append(tuple(tup))
    else: 
        rgb_colors = palette

    return rgb_colors

#%% Module loaded
print('morphoHeart! - Loaded funcBasics')