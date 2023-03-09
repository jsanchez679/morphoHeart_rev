'''
morphoHeart_funcBasics

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% Imports 
import os
from pathlib import Path
from playsound import playsound
# import json
import numpy as np 
import flatdict
from functools import reduce  
import operator
from itertools import count
# from typing import Union

path_fcBasics = os.path.abspath(__file__)
print(path_fcBasics)

#%% morphoHeart Imports 
# from ...config import dict_gui
# from .mH_classes import Project, Organ, ImChannel, ImChannelNS, ContStack, Mesh_mH
import vedo as vedo

alert_all=True
heart_default=False
dict_gui = {'alert_all': alert_all,
            'heart_default': heart_default}

#%% -Functions
#%% func - alert
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
    mp3_basic = ['connection','woohoo']
    
    alert_all = True#dict_gui['allert_all']
    if alert_all or sound in mp3_basic:
        path_parentSounds = Path(path_fcBasics).parent.parent.parent
        # print(path_parentSounds)
        sound_mp3= sound +'.mp3'
        path = path_parentSounds / 'sounds' / sound_mp3
        # print(path,'-', type(path))
        playsound(str(path))

#%% func - ask4input
def ask4input(text:str, res:dict, type_response:type, keep=False):
    """
    Function that ask for user input and transforms it into the expected type

    Parameters
    ----------
    text : str
        Text asking the question and giving possible options.
    type_response : data types int/str/float/boolean
        data type of the expected response
    keep : Boolean
        If True, leaves the string as it is (with upper and lower cases), else, changes the whole string to lower case.

    Returns
    -------
    response : int/str/float/bool
        returns an object with the corresponding type_response given as input.

    """
    alert('error_beep')
    exit_now = False
    while exit_now == False:
        res_text = '> '+text+' \n\t'
        res_len = len(res)
        for n, r in enumerate(res.keys()): 
            if n != res_len-1:
                r_text = '['+str(r)+']: '+res[r] +'\n\t'
            else: 
                r_text = '['+str(r)+']: '+res[r] +' >> : '
            res_text += r_text
        response = input(res_text)
        if type_response == int:
            try:
                response = int(response)
                exit_now = True
            except:
                print('>> Error: -'+response+'- The number entered needs to be an integer!')
                alert('error_beep')
                pass
        elif type_response == float:
            try:
                response = float(response)
                exit_now = True
            except:
                print('>> Error: -'+response+'- The number entered needs to be a float!')
                alert('error_beep')
                pass
        elif type_response == str:
            if keep == False:
                response = response.lower()
            exit_now = True
        elif type_response == bool:
            try:
                if int(response) in [0,1]:
                    response = bool(int(response))
                    exit_now = True
            except:
                print('>> Error: -'+response+'- The number entered needs to be a [0]:no or [1]:yes!')
                alert('error_beep')
                pass

    return response

#%% func - ask4inputList
def ask4inputList(text, res, res_all=True):

    alert('error_beep')
    exit_now = False
    while not exit_now:
        res_text = '> '+text+' \n\t'
        res_len = len(res)
        for n, r in enumerate(res.keys()): 
            if n != res_len-1:
                r_text = '['+str(r)+']: '+res[r] +'\n\t'
            else:
                if res_all:
                    r_text = '['+str(r)+']: '+res[r] +'\n\t[all]: All >> : '
                else: 
                    r_text = '['+str(r)+']: '+res[r] +' >> : '
            res_text += r_text
        response = input(res_text).lower()
        
        if response == 'all':
            obj_num = list(range(0,len(res),1))
    
        else:
            obj_num = []
            comma_split = response.split(',')
    
            for string in comma_split:
                if '-' in string:
                    minus_split = string.split('-')
                    #print(minus_split)
                    for n in list(range(int(minus_split[0]),int(minus_split[1])+1,1)):
                        #print(n)
                        obj_num.append(n)
                else:
                    obj_num.append(int(string))
        exit_now = True

    return obj_num

#%% func - compare_dicts
def compare_dicts(dict_1, dict_2, dict_1_name, dict_2_name, path="", ignore_dir=False):
    """Compare two dictionaries recursively to find non mathcing elements
    https://stackoverflow.com/questions/27265939/comparing-python-dictionaries-and-nested-dictionaries

    Args:
        dict_1: dictionary 1
        dict_2: dictionary 2

    Returns:

    """
    from .mH_classes import Project, Organ, ImChannel, ImChannelNS, ContStack, Mesh_mH
    
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
                err += compare_dicts(dict_1[k],dict_2[k],'d1','d2', path)
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

#%% func - compare_nested_dicts
def compare_nested_dicts(dict_1, dict_2, dict_1_name, dict_2_name, path=""):
    
    res = compare_dicts(dict_1, dict_2, dict_1_name, dict_2_name, path="")
    if len(res) ==0:
        return '\tNo differences!'
    else: 
        return res
        
#%% func - get_by_path
def get_by_path(root_dict, items):
    """Access a nested object in root_dict by item sequence.
    by Martijn Pieters (https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """
    return reduce(operator.getitem, items, root_dict)

#%% func - set_by_path
def set_by_path(root_dict, items, value):
    """Set a value in a nested object in root_dict by item sequence.
    by Martijn Pieters (https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """
    get_by_path(root_dict, items[:-1])[items[-1]] = value
    
#%% func - del_by_path
def del_by_path(root_dict, items):
    """Delete a key-value in a nested object in root_dict by item sequence.
    by Martijn Pieters (https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys)
    """
    del get_by_path(root_dict, items[:-1])[items[-1]]

#%% func - make_Paths
def make_Paths(load_dict):
    
    flat_dict = flatdict.FlatDict(load_dict)
    # Make all paths into Path
    dir_keys = [key.split(':') for key in flat_dict.keys() if 'dir' in key]
    # print(dir_keys)
    for key in dir_keys:
        # print('key:', key)
        value = get_by_path(load_dict, key)
        # print('value:', value)
        if value != None and value != 'NotAssigned':
            set_by_path(load_dict, key, Path(value))
    
    return load_dict
            
#%% func - make_tuples
def make_tuples(load_dict, tuple_keys): 
    flat_dict = flatdict.FlatDict(load_dict)
    #Make all keys from input list into tuples
    separator = ':'
    for tup in tuple_keys:
        str_tup = separator.join(tup)
        if str_tup in flat_dict.keys(): 
            value = get_by_path(load_dict, tup)
            if value != None:
                set_by_path(load_dict, tup, tuple(value))
        
    return load_dict

#%% func - check_gral_loading
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
    
#%% func - load_npy_stack
    # def load_npy_stack(organ:Organ, name:str):
from collections import defaultdict        
class NestedDict(defaultdict):

    # def __getitem__(self,keytuple):
    #     # if key is not a tuple then access as normal
    #     if not isinstance(keytuple, tuple):
    #         return super(NestedDict,self).__getitem__(keytuple)
    #     d = self
    #     for key in keytuple:
    #         d = d[key]
    #     return d
    

    def __getitem__(self, key):
        if isinstance(key, list):
            d = self
            for i in key:
                d = defaultdict.__getitem__(d, i)
            return d
        else:
            return defaultdict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if isinstance(key, list):
            d = self[key[:-1]]
            defaultdict.__setitem__(d, key[-1], value)
        else:
            defaultdict.__setitem__(self, key, value)

def nested_dict(n, type):
    if n == 1:
        return NestedDict(type)
    else:
        return NestedDict(lambda: nested_dict(n-1, type))

#https://stackoverflow.com/questions/30648317/programmatically-accessing-arbitrarily-deeply-nested-values-in-a-dictionary
#https://stackoverflow.com/questions/13687924/setting-a-value-in-a-nested-python-dictionary-given-a-list-of-indices-and-value
#https://www.geeksforgeeks.org/python-update-nested-dictionary/


# terms = ['person', 'address', 'city'] 
# result = nested_dict(3, str)
# result[terms] = 'New York'  # as easy as it can be


# class NestedDict(dict):

#     def __getitem__(self,keytuple):
#         # if key is not a tuple then access as normal
#         if not isinstance(keytuple, tuple):
#             return super(NestedDict,self).__getitem__(keytuple)
#         d = self
#         print('d:', d)
#         for key in keytuple:
#             d = d[key]
#             print('key:',key, d)
#         return d
    
#     def __setitem__(self, keylist, value):
#         if isinstance(keylist, list):
#             d = self[keylist[:-1]]
#             super(NestedDict).__setitem__(d, key[-1], value)
        
    
#         return super().__setitem__(__key, __value)

# x = {
#      'key1' : 'value1',
#      'key2' : {
#                'key21' : {
#                           'key211': 'value211'
#                          },
#                'key22' : 'value22'
#               },
#      'key3' : 'value3'
#     }
    
# nd = NestedDict(x)
# nd['key2']





#%% Module loaded
print('morphoHeart! - Loaded funcBasics')