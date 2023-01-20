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
# from .mH_classes import Organ, Mesh_mH, ImChannel

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
        path_parentSounds = Path(path_fcBasics).parent.parent.parent
        # print(path_parentSounds)
        sound_mp3= sound +'.mp3'
        path = path_parentSounds / 'sounds' / sound_mp3
        # print(path,'-', type(path))
        playsound(str(path))

#%% func - ask4input
def ask4input(text:str, type_response:type, keep=False):
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
        response = input('> '+text+' ')
        if type_response == int:
            try:
                response = int(response)
                exit_now = True
            except:
                print('ERROR: -'+response+'- The number entered needs to be an integer!')
                pass
        elif type_response == float:
            try:
                response = float(response)
                exit_now = True
            except:
                print('ERROR: -'+response+'- The number entered needs to be a float!')
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
                print('ERROR: -'+response+'- The number entered needs to be a [0]:no or [1]:yes!')
                pass

    return response

#%% func - compare_dictionaries
def compare_dictionaries(dict_1, dict_2, dict_1_name, dict_2_name, path=""):
    """Compare two dictionaries recursively to find non mathcing elements
    https://stackoverflow.com/questions/27265939/comparing-python-dictionaries-and-nested-dictionaries

    Args:
        dict_1: dictionary 1
        dict_2: dictionary 2

    Returns:

    """
    err = ''
    key_err = ''
    value_err = ''
    old_path = path
    for k in dict_1.keys():
        path = old_path + "[%s]" % k
        if not k in dict_2:
            key_err += "Key %s%s not in %s\n" % (dict_1_name, path, dict_2_name)
        else:
            if isinstance(dict_1[k], dict) and isinstance(dict_2[k], dict):
                err += compare_dictionaries(dict_1[k],dict_2[k],'d1','d2', path)
            else:
                if dict_1[k] != dict_2[k]:
                    value_err += "Value of %s%s (%s) not same as %s%s (%s)\n"\
                        % (dict_1_name, path, dict_1[k], dict_2_name, path, dict_2[k])

    for k in dict_2.keys():
        path = old_path + "[%s]" % k
        if not k in dict_1:
            key_err += "Key %s%s not in %s\n" % (dict_2_name, path, dict_1_name)

    res = key_err + value_err + err
    return res

#%% 

# def save_mHProject(dicts:list, organ:Organ):
#     jsonDict_name = 'mH_'+organ.user_organName+'_project.json'
#     json2save_dir = organ.dir_res / jsonDict_name

#     with open(str(json2save_dir), "w") as write_file:
#         json.dump(str(organ.dir_res), write_file, cls=NumpyArrayEncoder)
#         print('\t>> Dictionary saved correctly!\n\t>> File: '+jsonDict_name)
#         alert('countdown')

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