"""
morphoHeart_funcContours

Version: Feb 13, 2023
@author: Juliana Sanchez-Posada

"""
#%% ##### - Imports - ########################################################
from skimage import measure, io
import scipy.ndimage as ndimage
from scipy.spatial.distance import cdist
from skimage.measure import label, regionprops
from skimage.draw import line_aa
import numpy as np
import matplotlib.pyplot as plt
import copy
plt.rcParams['figure.constrained_layout.use'] = True
from PyQt6.QtCore import QObject, QThread, pyqtSignal

#%% ##### - Other Imports - ##################################################
from .mH_funcBasics import ask4input, ask4inputList, get_by_path, alert, palette_rbg
from .mH_classes_new import ImChannel
from ..gui.config import mH_config

#%% - morphoHeart A functions
def autom_close_contours(stack, ch, gui_param, gui_plot, win):
    """
    Funtion that automatically closes the contours of the input slice between the range given by 'slices'

    """

    level = gui_plot['level']
    slc_first_py = gui_param['start_slc']
    slc_first = slc_first_py+1
    slc_last_py = gui_param['end_slc']
    slc_last = slc_last_py+1
    plot2d = gui_param['plot2d']
    n_slices = gui_param['n_slices']
    min_contour_len = gui_param['min_contour_len']
    min_int = gui_param['min_int']
    mean_int = gui_param['mean_int']
    min_dist = gui_param['min_dist']

    #Create a copy of the stack in which to make changes
    new_stack = copy.deepcopy(stack)

    print('\n')
    win.prog_bar_range(0, slc_last_py-slc_first_py)
    win.win_msg('Automatically closing contours ('+ch+', No. slices to close: '+str(slc_last-slc_first)+')')

    for index, slc_py in enumerate(range(slc_first_py, slc_last_py)):

        slc = slc_py+1 #Transformed user format
        myIm = stack[slc_py][:][:]
        # Get the contours of slice
        contours = get_contours(myIm, min_contour_length = min_contour_len, level = level)
        # Sort the contours by length (bigger to smaller)
        contours = sorted(contours, key = len, reverse=True)
        # Get properties of each contour
        props = get_cont_props(myIm, cont_sort = contours)
        # Plot contours
        if plot2d and (index % n_slices == 0):
            print("\n------------- Channel "+str(ch)+" / Slice "+str(slc)+" -------------")
            params_props = {'myIm': copy.deepcopy(myIm), 'ch': ch, 'slc':slc, 
                            'cont_sort': contours, 'win':win}
            plot_props(params_props)
            win.add_thumbnail(function='fcC.plot_props', params = params_props, 
                              name='Orig. Cont Slc'+str(slc))

        # Select only the contours that have a max intensity greater than min_int
        filt_cont, filt_props = filter_contours(contours, props, min_int = min_int, mean_int = mean_int)
        # Plot filtered contours
        # if plot2d and (index % n_slices == 0):
        #     params_props = {'myIm': myIm, 'ch': ch, 'slc':slc, 
        #                     'cont_sort': filt_cont, 'win':win}
        #     plot_props(params_props)
        #     win.add_thumbnail(function='fcC.plot_props', params = params_props, 
        #                       name='Filt Cont Slc'+str(slc))
            
        # Find distance between all contours and save information of those whose are at a distance less than minDist
        data_connect = dist_btw_allCont(contours = filt_cont, user_min_dist = min_dist)
        # Draw lines between closer contours
        myIm_closedCont = auto_draw_close_contours(myIm, data_connect)
        # Show new closed contours
        new_contours = get_contours(myIm_closedCont, min_contour_length = min_contour_len, level = level)
        # Sort the contours by length (bigger to smaller)
        new_contours = sorted(new_contours, key = len, reverse=True)
        # if plotshow:
        #     print('\n-> FINAL CONTOURS')
        if plot2d and (index % n_slices == 0):
            params_props = {'myIm': copy.deepcopy(myIm_closedCont), 'ch': ch, 'slc':slc, 
                            'cont_sort': new_contours, 'win':win}
            plot_props(params_props)
            win.add_thumbnail(function='fcC.plot_props', params = params_props, 
                              name='Final Cont. Slc'+str(slc))
        new_stack[slc_py][:][:] = myIm_closedCont

        #Update Bar
        win.prog_bar_update(value = slc_py-slc_first_py)
    
    win.prog_bar_update(value = slc_last-slc_first)
    
    #Plot slice range
    win.plot_all_slices(ch = ch, slice_range = (slc_first_py, slc_last_py))

    return new_stack

def manual_close_contours(stack, ch, gui_param, gui_plot, win):

    """
    Function used to manually close the contours of the stack

    """
    level = gui_param['level']
    slc_first_py = gui_param['start_slc']
    slc_first = slc_first_py+1
    slc_last_py = gui_param['end_slc']
    slc_last = slc_last_py+1
    no_slices = slc_last_py-slc_first_py

    n_rows = int(gui_plot['n_rows'])
    n_cols = int(gui_plot['n_cols'])
    slcs_per_im = n_rows*n_cols
    slices = list(range(slc_first_py,slc_last_py+1,slcs_per_im))
    if slices[-1] != slc_last_py+1:
        slices.append(slc_last_py+1)

    min_contour_len = gui_param['min_contour_len']

    win.prog_bar_range(0, slc_last_py-slc_first_py)
    win.win_msg('Manually closing contours ('+ch+', No. slices to close: '+str(slc_last-slc_first)+')')

    for nn in range(len(slices[:-1])):
        # plotSlcsRange(stack_closed, slc_tuple, 'INITIAL', slcs_per_im, level)
        slc_tuple = (slices[nn], slices[nn+1])
        params = {'stack': stack, 'slices_plot': slc_tuple, 
                    'text': 'Contours', 'slcs_per_im': slcs_per_im, 
                    'n_rows': n_rows, 'n_cols': n_cols,
                    'level': level, 'min_contour_length': min_contour_len}
        win.add_thumbnail(function ='plot_slc_range', params = params, 
                            name = 'Cont Slcs '+str(slc_tuple[0]+1)+'-'+str(slc_tuple[1]-1+1)+'')
        win.plot_slc_range(params)

        win.setup_get_slices_thread(slc_tuple, win)
        # while win.worker.status != 'DONE': 
        #     pass

        # print('Now it is DONE!')
        

        # # Open interpreter
        # getattr(win, 'close_contours_open').setChecked(False)
        # win.open_section(name = 'close_contours')
        # slc_list, slc_end = get_slices(slc_tuple, win)
        # print('AJA - slc_list:', slc_list)

    #     while len(slc_list) != 0:
    #         exit_code, slc_end, last_slc, stack_closed = manuallyCloseContoursTuple (slc_list, stack_closed, stack_o, 
    #                                                                                  stack_m, chStr, exit_code, level)

    #         if exit_code:
    #             alert('error',1)
    #             print("\n- Exit script - last slice ", last_slc)
    #             break

    #         plotSlcsRange(stack_closed, slc_tuple, 'CHECKING (after having closed)', slcs_per_im, level)
    #         q_done = str(input('> Are you done CLOSING the contours for this - tuple ('+ str(slc_tuple[0])+','+str(slc_tuple[1]-1)+')?: \n - [0]:no/[1/ ]:yes! >>>>> ')).lower()
    #         if q_done == '1' or q_done == '':
    #             # print('slc list: ', slc_list)
    #             break
    #         #     if i == len(slices_first)-1:
    #         #         q_not_done_all = str(input('> Do you want to close any other slices? [0]:no/[1/ ]:yes! >>>>> '))
    #         #         if q_not_done_all == '1' or q_not_done_all == '': 
    #         #             slc_list, slc_end = getSlices((0,stack_closed.shape[0]), 'you would like to close')
    #         #         else: 
    #         #             exit_code = True
    #         #             break
    #         #     else: 
    #         #         break
    #         elif q_done == '0':
    #             slc_list, slc_end = getSlices(slc_tuple, 'you would like to close')
            
    #     if exit_code:
    #         break

    # if slc_end == slices[1]:
    #     last_slc = slices[1]
        # alert('wohoo',1)
        # print("- All Done - Contours have been manually closed!")

    # return stack_closed, last_slc, exit_code

def manuallyCloseContoursTuple (slc_list, stack_closed, stack_o, stack_m, chStr, exit_code, level):
    """
    Function used to manually close the contours of the slices in the slc_list given as input

    Parameters
    ----------
    slc_list : list of int
        List of slices to be processed/checked.
    stack_closed : numpy array
        Input closed stack.
    stack_o : numpy array
        Copy of closed stack.
    stack_m : numpy array
        Copy of original masked stack to process.
    chStr : str
        Text indicating channel being processed ('ch0': myocardium/ 'ch1': endocardium).
    exit_code : boolean
        True if user wants to exit code, else False.
    level : float 
        Value along which to find contours in the array. Parameter for skimage.measure.find_contours

    Returns
    -------
    exit_code : boolean
        True if user wants to exit code, else False.
    slc : int
        Slice number being processed.
    last_slc : int
        Last processed slice
    stack_closed : numpy array
        Resulting closed stack.

    """
    select_process = 'esc'
    if len(slc_list) > 0: 
        for slc in slc_list:
            if exit_code:
                print('- EXIT! - slc: '+ str(slc)+' - Process: '+ select_process)
                break
    
            print("- Processing contours - slice ", str(slc))
            # Get image
    
            myIm = stack_closed[slc][:][:]
            # Get contours for that slice
            _ = getContExpCont_plt (myIm, slc, chStr, minLenContour=100, figSize=10, level = level)
            myIm_closed = myIm
    
            # closeContours per slice
            k_size = 60
            myIm_closed, done_close  = closeContoursSlc(myIm_closed, slc, chStr, k_size, k_size, level)
            if done_close == 'esc': #done_close in ['esc', 'n', 'N']
                last_slc = slc
                exit_code = True
                break
    
            last_slc = slc
            add_step = ['', '1']
            while not exit_code and done_close in add_step:   #exit_code == False:
                list_close = ['3', '4', '5']
                crop_size = [(120,120), (50,50), (100,300)]
                print('\n - Additional processes for - Slc '+str(slc)+':')
                print('   -[1]:draw black/clean slice\t\t-[2]:draw white')
                print('   -[3]:close (120x120)\t\t\t\t-[4]:close (50x50)')
                print('   -[5]:close (300x100)\t\t\t\t-[6]:close (user input size)')
                print('   -[7]:reset slice (to original after automatic contour closure)')
                print('   -[8]:reset slice (to original image - just masked)')
                print('   -[9/ ]:save (slice done!)\t\t-[esc]:exit')
                select_process = str(input('> Select: ')).lower()
    
                if select_process == 'esc':
                    done = select_process
                    last_slc = slc;
                    exit_code = True
                    break
                # Draw contour black/Clean contours
                elif select_process == '1':
                    myIm_closed, done = close_draw(myIm_closed, slc, chStr, 'black', level)
                # Draw contour white
                elif select_process == '2':
                    myIm_closed, done = close_draw(myIm_closed, slc, chStr, 'white', level)
                # Close contours
                elif select_process in list_close:
                    index_selected = list_close.index(select_process)
                    myIm_closed, done = closeContoursSlc(myIm_closed, slc, chStr, crop_size[index_selected][0], crop_size[index_selected][1], level)
                elif select_process == '6':
                    input_size = ask4input('Enter the rectangle size to crop and close contours separated by a comma - x,y -: ', str)
                    x_size, y_size = input_size.split(',')
                    myIm_closed, done = closeContoursSlc(myIm_closed, slc, chStr, int(y_size), int(x_size), level)
                # Done
                elif select_process == '9' or select_process == '':
                    done = 'OK'
                    stack_closed[slc][:][:] = myIm_closed
                    last_slc = slc
                    break
                #Reset slc
                elif select_process == '7':
                    myIm_closed = stack_o[slc][:][:]
                    done = 'reset_o_OK'
                    _ = getContExpCont_plt (myIm_closed, slc, chStr, 250, 10, level, True)
                    
                elif select_process == '8':
                    myIm_closed = stack_m[slc][:][:]
                    done = 'reset_m_OK'
                    _ = getContExpCont_plt (myIm_closed, slc, chStr, 250, 10, level, True)
                    
                else:
                    print('Error: Wrong input. Select only from the given options')
    
                if done == 'esc':
                    last_slc = slc
                    exit_code = True
                    break
    else: 
        exit_code = False
        last_slc = 0
        slc = 0

    return exit_code, slc, last_slc, stack_closed

def closeContours(organ, ch_name:str, close_done:dict, win):

    if close_done['A-MaskChannel'] != 'DONE':
        im_ch = organ.create_ch(ch_name=ch_name)
        win.win_msg('Masking Channel '+str(ch_name[-1]))
        im_ch.maskIm()
        win.win_msg('Channel '+str(ch_name[-1])+ ' was successfully masked!')
    else: 
        im_ch = ImChannel(organ=organ, ch_name=ch_name)#, new=False)      
        win.win_msg('Channel '+str(ch_name[-1])+ ' was successfully loaded!') 
    print(ch_name,':', im_ch.__dict__)
    win.update_ch_progress()     
            
    # if close_done['A-Autom'] != 'DONE':
    #     win.win_msg('Closing Contours of Channel '+str(ch_name[-1])+' Automatically')
    #     im_ch.closeContours_auto()
    #     win.win_msg('Contours of channel '+str(ch_name[-1])+ 'have been automatically closed!')
    # win.update_ch_progress() 
        
    # if close_done['B-Manual'] != 'DONE':
    #     win.win_msg('Closing Contours of Channel '+str(ch_name[-1])+' Manually')
    #     im_ch.closeContours_manual()
    #     win.win_msg('Contours of channel '+str(ch_name[-1])+ 'have been manually closed!')
    # win.update_ch_progress() 
        
    # if close_done['C-CloseInOut'] != 'DONE':
    #     win.win_msg('Closing Top and Bottom Contours of Channel '+str(ch_name[-1]))
    #     im_ch.closeInfOutf()
    #     win.win_msg('The top and bottom contours of channel '+str(ch_name[-1])+ 'have been succesfully closed!')
    # win.update_ch_progress() 

def checkWfCloseCont(workflow, ch_name):
    #Check if masking is part of the workflow
    if get_by_path(workflow, ['ImProc', ch_name, 'A-MaskChannel','Status']) != 'N/A': 
        close_done = {'A-MaskChannel': get_by_path(workflow, ['ImProc', ch_name, 'A-MaskChannel','Status'])}
    else: 
        close_done = {}

    for key_a in ['A-Autom', 'B-Manual', 'C-CloseInOut']:
        val = get_by_path(workflow, ['ImProc', ch_name, 'B-CloseCont','Steps', key_a, 'Status'])
        close_done[key_a] = val
    
    return close_done

def selectContours(organ, im_ch, win):
    
    layerDict = im_ch.selectContours()
    im_ch.create_chS3s(layerDict=layerDict, win=win)
    win.win_msg('Contour masks for channel '+str(im_ch.channel_no[-1])+ ' have been successfully created!')
    win.update_ch_progress() 

# Functions related to contours
def get_contours(myIm, min_contour_length, level):
    """
    Function that gets and returns the contours of a particular slice (slcNum)
    """
    # Create an empty array to save all the contours of each slice individually
    arr_contour_slc = []
    # Find all the contours of the image
    contours = measure.find_contours(myIm, level, 'high', 'high')
    # Go through all the contours
    for n, contour in enumerate(contours):
        # Get only the contours made up of more than the designated number of points
        if len(contour)>min_contour_length:
            # Append contour to the array
            arr_contour_slc.append(contour)
        
    return arr_contour_slc

def get_cont_props(myIm, cont_sort): 
     # Array to save the metrics of all the contours
    props_all = []
    # Iterate through sorted contours
    for contList in cont_sort:
        #-->>#2 [0. area, 1. centroid, 2. max_int, 3. mean_int, 4. lgth, 5. per, 6. sol, 7. bbox]
        props = maskContour(myIm, contList)
        props_all.append(props)

    return props_all

def maskContour(myIm, contour):
    """
    Function that measures the properties of the contour received as input

    Parameters
    ----------
    myIm : numpy array
        Imaged being processed
    contour : numpy array
        Coordinates of contour to use to mask image

    Returns
    -------
    props_all : list of numpy array
        List of arrays with values of properties associated to each of the contours found in slice
        -->>#2 [0. area, 1. centroid, 2. max_int, 3. mean_int, 4. lgth, 5. per, 6. sol, 7. bbox]

    """

    # Create an empty image to store the masked array
    r_mask = np.zeros_like(myIm, dtype='bool')
    # Create a contour masked image by using the contour coordinates rounded to their nearest integer value
    r_mask[np.round(contour[:, 1]).astype('int'), np.round(contour[:, 0]).astype('int')] = 1
    # Fill in the holes created by the contour boundary
    r_mask = ndimage.binary_fill_holes(r_mask)

    # Change the mask type to integer
    r_mask_int = r_mask.astype(int)

    # label image regions
    label_r_mask = label(r_mask_int)
    label_r_mask = np.transpose(label_r_mask)
    # print(label_r_mask.shape, myIm.shape)
    
    props = regionprops(label_r_mask, intensity_image = myIm)
    
    area = props[0].area
    centroid = props[0].centroid
    max_int = props[0].max_intensity
    mean_int = props[0].mean_intensity
    #cx_area = props[0].convex_area
    #ecc = props[0].eccentricity
    lgth = len(contour)
    per = props[0].perimeter
    sol = props[0].solidity
    bbox = props[0].bbox

    props_all = np.array([area, centroid, max_int, mean_int, lgth, per, sol, bbox], dtype=object)

    return props_all

def filter_contours(contours, props, min_int, mean_int):
    """
    Funtion that filters contours by minimum and mean intensities

    Parameters
    ----------
    contours : list of arrays
        list of numpy array with coordinates making up the contours of the slice being processed.
    props : list of numpy array
        List of arrays with values of properties associated to each of the contours found in slice
        -->>#2 [0. area, 1. centroid, 2. max_int, 3. mean_int, 4. lgth, 5. per, 6. sol, 7. bbox]
    min_expInt : int
        Minimum expected intensity value.
    printData : boolean
        True to print number of initial and final contours, else False

    Returns
    -------
    filt_cont : list of arrays
        Filtered list of numpy array with coordinates making up the contours of the slice being processed.
    filt_props : list of numpy array
        Filtered list of arrays with values of properties associated to each of the filtered contours found in slice
        -->>#2 [0. area, 1. centroid, 2. max_int, 3. mean_int, 4. lgth, 5. per, 6. sol, 7. bbox]

    """

    filt_cont = []
    filt_props = []
    for num, cont in enumerate(contours):
        if props[num][2] > min_int and props[num][3] > mean_int:
            filt_cont.append(cont)
            filt_props.append(props[num])

    # print('- Number of initial contours: ', len(contours))
    # print('- Number of final contours: ', len(filt_cont))

    return filt_cont, filt_props

def dist_btw_allCont(contours, user_min_dist):
    """
    Function used to find minimum distance between a list of input contours

    Parameters
    ----------
    contours : list of arrays
        list of numpy array with coordinates making up the contours of the slice being processed.
    minDist : int
        Minimum distance in pixels
    printData : boolean
        True to print the number of the contours to connect, else False

    Returns
    -------
    final_list : list of lists
        List with data to be used to join contours [i, j+1, min_dist, indA, ptA, indB, ptB].

    """

    mtx_dist = np.ones(shape = (len(contours), len(contours)))*10000
    np.fill_diagonal(mtx_dist, 0)

    ij_list = []
    final_list = []

    for i, contA in enumerate(contours):
        # print('i:',i)
        for j, contB in enumerate(contours[i+1:]):
            # print('j:',j+1)
            #Get minimum distance between contA and contB
            data_func = min_dist_btw_contsAB(contA, contB)
            min_dist, indA, ptA, indB, ptB = data_func
            data_func = i, j+1, min_dist, indA, ptA, indB, ptB
            mtx_dist[i,i+j+1] = min_dist

            if min_dist <= user_min_dist:
                ij_tuple = (i,i+j+1)
                ij_list.append(ij_tuple)
                final_list.append(data_func)
                print('- Contours to connect: ', ij_tuple, ' / Distance [px]: ', format(min_dist, '.2f'))

    return final_list

def min_dist_btw_contsAB (contourA, contourB):
    """
    Function that measues the actual distance in pixels between contourA and contourB

    Parameters
    ----------
    contourA : numpy array
        Array with coordinates of contour A.
    contourB : numpy array
        Array with coordinates of contour B.

    Returns
    -------
    min_dist : float
        Minimum distance found between contours A and B.
    index_ptContA : int
        Index of point within array of contour A that results in minimum distance
    ptContA : numpy array
        Coordinates of point A
    index_ptContB : int
        Index of point within array of contour B that results in minimum distance
    ptContB : numpy array
        Coordinates of point B

    """

    # Find euclidian distance beteen all points in contours
    dist = cdist(contourA,contourB)
    # Get indexes where distance is minimum (closest points)
    min_dist = np.amin(dist)
    index4min = np.where(dist == min_dist)

    index_ptContA = index4min[0][0]
    ptContA = contourA[index_ptContA]
    index_ptContB = index4min[1][0]
    ptContB = contourB[index_ptContB]

    return min_dist, index_ptContA, ptContA, index_ptContB, ptContB

def auto_draw_close_contours(myIm, data_Connect):
    """
    Function that connects contours using the data2Connect given as input - (return of distBtwAllCont)

    Parameters
    ----------
    myIm : numpy array
        Imaged being processed
    data2Connect  :list of lists
        List with data to be used to join contours [i, j+1, min_dist, indA, ptA, indB, ptB].

    Returns
    -------
    myIm : numpy array
        Resulting processed imaged with connected contours

    """

    for connection in data_Connect:
        ptAx = int(connection[4][0])
        ptAy = int(connection[4][1])
        ptBx = int(connection[6][0])
        ptBy = int(connection[6][1])

        rr, cc, val = line_aa(ptAx, ptAy, ptBx, ptBy)
        myIm[rr, cc] = val * 50000

    return myIm

# Interactive functions
def get_slices(slc_tuple, win):
    """
    Funtion that returns a list with the slice numbers to be processed/checked.
    """

    slc_list = []
    q_text = 'Select the slices you would like to close from -('+str(slc_tuple[0])+','+str(slc_tuple[1]-1)+')- \n(e.g. to close slices 5, 9, 10, and 11 type: 5,9-11), [all/ ]:all, [N/n]:none)'
    options = ['int', 'all','', 'N', 'n']
    win.emit_question(q_text, options)

    # if input_slc == 'all' or input_slc == '':
    #     slc_list = list(range(slc_tuple[0],slc_tuple[1],1))
    #     # print(slc_list)
    # elif input_slc in ['n', 'N']:
    #     slc_list = []
    # else:
    #     slc_list = []
    #     comma_split = input_slc.split(',')

    #     for string in comma_split:
    #         if '-' in string:
    #             minus_split = string.split('-')
    #             #print(minus_split)
    #             for n in list(range(int(minus_split[0]),int(minus_split[1])+1,1)):
    #                 #print(n)
    #                 slc_list.append(n)
    #         elif string == '':
    #             pass
    #         else:
    #             slc_list.append(int(string))

    # slc_end = slc_tuple[1]

    # return slc_list, slc_end

#Draw functions
def getClicks (clicks, myIm, scale, text):
    """
    Function to get clicks of prompted image slice.

    Parameters
    ----------
    clicks : list of tuples with coordinates (clicks)
        Initialised list of clicks coordinates.
    myIm : numpy array
        Imaged being processed
    scale : float
        Number that scales the image to be prompted.
    text : str
        Title of prompted window with image indicating the process being performed (cleaning/closing/etc...).

    Returns
    -------
    clicks : list of tuples with coordinates (clicks)
        Final list of clicks coordinates.

    """

    print("- Getting clicks... Press ENTER when done")

    window_width = int(myIm.shape[1] * scale)
    window_height = int(myIm.shape[0] * scale)

    def on_mouse(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            #print ('\r    Seed: ' + str(y) + ', ' + str(x), myIm[y,x])
            clicks.append((y,x))

    cv2.namedWindow(text, cv2.WINDOW_NORMAL)#,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(text, window_width, window_height)
    cv2.setMouseCallback(text, on_mouse, 0, )
    cv2.imshow(text, myIm)
    cv2.waitKey()
    cv2.destroyAllWindows()

    return clicks

def close_draw (myIm_closed, slc, chStr, color_draw, level, plot_show = True):
    """
    Function that collects clicks positions given by the user and connects them using a white or black line given as
    input by 'color_draw' parameter

    Parameters
    ----------
    myIm_closed : numpy array
        Image to close drawing
    slc : int
        Slice number being processed.
    chStr : str
        Text indicating channel being processed ('ch0': myocardium/ 'ch1': endocardium).
    color_draw : str
        Color used when drawing line between clicks ('b'/'black': black, 'w'/'white': white)
    level : float 
        Value along which to find contours in the array. Parameter for skimage.measure.find_contours
    plot_show : boolean, optional
        True to show plot, else False. The default is True.

    Returns
    -------
    myIm_closed : numpy array
        Closed/cleaned image
    done_draw : boolean
        True if drawing is done, else False.

    """

    while True:
        #Get clicks of positions to close contours
        clicks = getClicks([], myIm_closed, scale=1, text='DRAWING SLICE ('+color_draw+')')
        # Draw white/black line following the clicked pattern
        myIm_closed = drawLine(clicks, myIm_closed, color_draw)
        _ = getContExpCont_plt (myIm_closed, slc, chStr, 250, 10, level, plot_show)

        if plot_show:
            print("- Are you done drawing ("+color_draw+") the contours for this - slice "+ str(slc)+"?: ")
            done_draw = str(input('>  - [0]:no/[1/ ]:yes!/[esc]:exit >>>>> ')).lower()
            if done_draw == '1' or done_draw == 'esc' or done_draw == '':
                break
        else:
            done_draw = ''
            break

    return myIm_closed, done_draw

#Plot contour functions
def plot_props(params):

    myIm = params['myIm']
    ch = params['ch']
    slc = params['slc']
    cont_sort = params['cont_sort']
    win = params['win']
    num_contours = len(cont_sort)

    # Define the figure properties (columns, rows, image size)
    cols = 5
    # Limit the number of contours to plot to 30
    if num_contours > 30:
        num_contours = 30
        cont_plot = cont_sort[0:30]
    else:
        cont_plot = cont_sort

    rows = num_contours // cols
    if num_contours%cols != 0:
        rows = rows + 1
    if rows == 0: 
        rows = 1
    # print('rows:', rows)
    fig11 = win.figure#plt.figure(figsize=(cols*imSize+colorImSize, rows*imSize), constrained_layout=True)
    fig11.clear()
    
    # gridspec inside gridspec
    outer_grid = fig11.add_gridspec(nrows=1, ncols=2, width_ratios=[1,2])
    outer_grid.update(left=0.1,right=0.9,top=0.95,bottom=0.05,wspace=0,hspace=0)
    # Grid where color image will be placed
    color_grid = outer_grid[0].subgridspec(nrows=1, ncols=1, wspace=0, hspace=0)
    ax = fig11.add_subplot(color_grid[0])
    ax.imshow(myIm, cmap=plt.cm.gray)

    #Text positions
    # xlin = np.linspace(0.1,0.9, cols)
    # ylin = np.linspace(-0.1,-0.9, rows)
    # txt_pos = []
    # for y in ylin: 
    #     for x in xlin:
    #         txt_pos.append((x,y))

    # Go through all the contours
    for num, contour in enumerate(cont_plot):
        ax.plot(contour[:,1], contour[:,0], linewidth=0.25, color=palette[num])
        # txt = "Cont"+str(num)
        # ax.text(txt_pos[num][0], txt_pos[num][1],#0.95,(0.97-0.035*(num+1)), 
        #         txt,
        #         verticalalignment='top', horizontalalignment='left',
        #         transform=ax.transAxes,
        #         color=palette[num], fontsize=2, weight = 'semibold')
        ax.set_axis_off()

    win.fig_title.setText("Channel "+str(ch[-1])+" / Slice "+str(slc))

    # Grid where subplots of each contour will be placed
    all_grid = outer_grid[1].subgridspec(rows, cols, wspace=0, hspace=0)

    # Iterate through sorted contours
    for index, contList in enumerate(cont_plot):
        ax = fig11.add_subplot(all_grid[index])
        ax.imshow(myIm, cmap=plt.cm.gray)
        ax.plot(contList[:,1], contList[:,0], linewidth=0.15, color = palette[index])
        ax.set_title("Contour "+str(index+1), fontsize=2, weight = 'semibold', 
                     color = palette[index],  pad=0.15)
        ax.set_axis_off()

    win.canvas_plot.draw()

def plot_contours_slc(params):
    """
    # getContExpCont_plt
    Function that gets and returns the contours of a particular slice (slcNum) plotting the image with an overlay
    of the contours
    """

    myIm = params['myIm']
    slc = params['slc']
    ch = params['ch']
    level = params['level']
    min_contour_length = params['min_contour_length']
    win = params['win']

    # Create an empty array to save all the contours of each slice individually
    arr_contours = []
    #Find all the contours of the image
    contours = measure.find_contours(myIm, level, 'high', 'high')

    # Display the image and plot an overlay of all contours found that have
    # more than min_contour_length points
    fig11 = win.figure
    fig11.clear()
    ax = fig11.add_subplot(111)
    ax.imshow(myIm, cmap=plt.cm.gray)

    # Go through all the contours
    for index, contour in enumerate(contours):
        # Get only the contours made up of more than the designated number of points
        if len(contour)>min_contour_length:
            # Append contour to the array
            arr_contours.append(contour)
            # plot the contour
            ax.plot(contour[:, 1], contour[:, 0], linewidth=0.3, color = palette[index])

    win.fig_title.setText("Channel "+str(ch[-1])+" / Slice "+str(slc))
    ax.set_axis_off()
    win.canvas_plot.draw()

    return arr_contours

palette =  palette_rbg('bright', 30, False)*20
#%% Module loaded
print('morphoHeart! - Loaded funcContours')