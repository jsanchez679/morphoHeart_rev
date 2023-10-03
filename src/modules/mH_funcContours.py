"""
morphoHeart_funcContours

Version: Feb 13, 2023
@author: Juliana Sanchez-Posada

"""
#%% ##### - Imports - ########################################################
from skimage import measure, io
import scipy.ndimage as ndimage
from scipy.spatial import ConvexHull, distance
from scipy.spatial.distance import cdist
from skimage.measure import label, regionprops
from skimage.draw import line_aa
import numpy as np
import matplotlib.pyplot as plt
import copy
plt.rcParams['figure.constrained_layout.use'] = True
# from PyQt6.QtCore import QObject, QThread, pyqtSignal
import cv2

#%% ##### - Other Imports - ##################################################
from .mH_funcBasics import ask4input, ask4inputList, get_by_path, alert
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

def set_tuples(slc_first, slc_last, slcs_per_im): 

    first_tuple = list(range(slc_first,slc_last+1,slcs_per_im))
    if first_tuple[-1] != slc_last:
        first_tuple.append(slc_last)
    final_tuples = []
    for nn in range(len(first_tuple[:-1])): 
        final_tuples.append((first_tuple[nn], first_tuple[nn+1]))
    print('final_tuples:', final_tuples)
    return final_tuples

# Interactive functions
def get_slices(lineEdit, slc_tuple, win):
    """
    Funtion that returns a list with the slice numbers to be processed/checked.
    """
    user_input = lineEdit.text()
    numbers = []
    if user_input == 'all': 
        numbers = list(range(slc_tuple[0],slc_tuple[1]+1,1))
    elif user_input == 'N' or user_input == 'n': 
        numbers = []
    elif user_input == '': 
        error_txt = '*Please select the slices you want to close within the given tuple.'
        win.tE_validate.setText(error_txt)
        return
    else: 
        user_input_comma = user_input.split(',')
        for numb in user_input_comma: 
            if '-' in numb: 
                st, end = numb.split('-')
                rg = list(range(int(st)-1,int(end)+1-1,1))
                numbers = numbers+rg
            else: 
                numbers.append(int(numb)-1)

    return numbers

#Draw functions
def close_draw(color_draw, win): #_closed, slc, chStr, color_draw, level, plot_show = True):
    """
    Function that collects clicks positions given by the user and connects them using a white or black line given as
    input by 'color_draw' parameter

    """
    if win.slc_py != None:
        slc_py = win.slc_py
        slc_user = slc_py+1
        ch_name = win.im_ch.channel_no
        level = win.gui_manual_close_contours[ch_name]['level']
        min_contour_len = win.gui_manual_close_contours[ch_name]['min_contour_len']

        #Get clicks of positions to close contours
        clicks = get_clicks([], win.myIm, scale=1, text='DRAWING SLICE ('+color_draw+')')
        # Draw white/black line following the clicked pattern
        win.myIm = draw_line(clicks, win.myIm, color_draw)
        #Plot image with closed contours
        params = {'myIm': copy.deepcopy(win.myIm), 'slc_user': slc_user, 'ch': ch_name, 
                    'level': level, 'min_contour_length': min_contour_len}
        win.add_thumbnail(function ='fcC.plot_contours_slc', params = params, 
                            name = 'Cont Slc '+str(slc_user))
        win.plot_contours_slc(params)
    else: 
        win.win_msg('*Please enter the slices you would like to close from the current slice tuple ('+str(win.slc_tuple[0]+1)+'-'+str(win.slc_tuple[1])+')')

def close_box(box, win):
    """
    Function that closes the contours of the input image using the cropNcloseCont function
    """
    if win.slc_py != None:
        slc_py = win.slc_py
        slc_user = slc_py+1
        ch_name = win.im_ch.channel_no
        level = win.gui_manual_close_contours[ch_name]['level']
        min_contour_len = win.gui_manual_close_contours[ch_name]['min_contour_len']

        clicks = get_clicks([], win.myIm, scale=1, text='CLOSING CONTOURS')
        #Close contours and get Image
        win.myIm = crop_n_close(clicks, win.myIm, box, level)
        #Plot image with closed contours
        params = {'myIm': copy.deepcopy(win.myIm), 'slc_user': slc_user, 'ch': ch_name, 
                    'level': level, 'min_contour_length': min_contour_len}
        win.add_thumbnail(function ='fcC.plot_contours_slc', params = params, 
                            name = 'Cont Slc '+str(slc_user))
        win.plot_contours_slc(params)
    else: 
        win.win_msg('*Please enter the slices you would like to close from the current slice tuple ('+str(win.slc_tuple[0]+1)+'-'+str(win.slc_tuple[1])+')')

def close_user(win): 
    try: 
        box_w = int(win.box_w.text())
    except: 
        win.win_msg("*Check the defined box's width for Close (User)")
        return
    try: 
        box_h = int(win.box_h.text())
    except: 
        win.win_msg("*Check the defined box's height for Close (User)")
        return
    close_box(box=(box_w, box_h), win=win)

def close_convex_hull(win): 
    """
    Function that closes the inlet/outlet of the input slice using convex hull
    """
    if win.slc_py != None:
        slc_py = win.slc_py
        slc_user = slc_py+1
        ch_name = win.im_ch.channel_no
        level = win.gui_manual_close_contours[ch_name]['level']
        min_contour_len = win.gui_manual_close_contours[ch_name]['min_contour_len']

        contours_or = get_contours(win.myIm, min_contour_length=min_contour_len, level=level)
        contours_or = sorted(contours_or, key = len, reverse=True)
        ind_contours = []
        for i, cont in enumerate(contours_or): 
            props = maskContour(win.myIm, cont)
            if props[2] > 15000:
                ind_contours.append(i)

        # print('ind_contours:', ind_contours)
        im_height, im_width = win.myIm.shape
        black_array = np.uint16(np.zeros((150,im_width), dtype=int))

        myIm_closed = np.vstack((black_array, win.myIm, black_array))
        myIm_closed = np.uint16(myIm_closed)

        contours_new = get_contours(myIm_closed, min_contour_length=min_contour_len, level=level)
        contours_new = sorted(contours_new, key = len, reverse=True)

        contours = []
        for index in ind_contours:
            contours.append(contours_new[index])
      
        xy_contours = xy_allContours(contours)

        clicks = []
        #Get click to use convex hull to close
        print("\n- Closing Inflow/Outflow tract - slice ", str(slc_user))
        # Get click for point to create convex hull from
        while len(clicks) == 0:
            clicks = get_clicks([],myIm_closed, scale=0.6, text='CONVEX HULL')
        clicks = clicks[-1]
            
        clicks_correct = False
        while not clicks_correct: 
            # Last point is considered the seed
            if len(clicks) > 0:
                y0, x0 = clicks
                point2add = np.array([[y0],[x0]])
                xy_contours_new = np.concatenate((xy_contours, np.transpose(point2add)))
                qg_num = 'QG'+str(len(xy_contours_new)-1)
                hull = ConvexHull(points=xy_contours_new,qhull_options=qg_num)
                merge = hull.simplices[hull.good]
                closing_pt1, closing_pt2 = selectHull (merge, xy_contours_new)
                if type(closing_pt1) == tuple and type(closing_pt2) == tuple: 
                    clicks_correct = True
                    break
                else: 
                    alert('error')
                    win.win_msg('*ALERT: Make sure you are clicking on a point outside the convex hull of the contours!')
                    clicks = get_clicks([],myIm_closed, scale=0.6, text='CONVEX HULL')
                    clicks = clicks[-1]

        rr, cc, val = line_aa(int(closing_pt1[0]), int(closing_pt1[1]),
                            int(closing_pt2[0]), int(closing_pt2[1]))
        myIm_closed[rr, cc] = val * 50000
        win.myIm = myIm_closed[150:150+im_height]
        win.im_proc[slc_py][:][:] = win.myIm

        #Plot image with closed contours
        params = {'myIm': copy.deepcopy(win.myIm), 'slc_user': slc_user, 'ch': ch_name, 
                    'level': level, 'min_contour_length': min_contour_len}
        win.add_thumbnail(function ='fcC.plot_contours_slc', params = params, 
                            name = 'Cont Slc '+str(slc_user))
        win.plot_contours_slc(params)

    else: 
        win.win_msg('*Please enter the slices you would like to close from the current slice tuple ('+str(win.slc_tuple[0]+1)+'-'+str(win.slc_tuple[1])+')')

def reset_img(rtype, win): 

    if win.slc_py != None:
        slc_py = win.slc_py
        slc_user = slc_py+1
        ch_name = win.im_ch.channel_no
        level = win.gui_manual_close_contours[ch_name]['level']
        min_contour_len = win.gui_manual_close_contours[ch_name]['min_contour_len']
        if rtype == 'autom': 
            win.myIm = copy.deepcopy(win.im_proc_o[slc_py][:][:])
        else: 
            im_ch = win.organ.obj_imChannels[ch_name]
            myIm = im_ch.im_proc()[slc_py][:][:]
            if rtype == 'masked': 
                if win.organ.mH_settings['setup']['mask_ch'][ch_name]: 
                    myMask = io.imread(str(im_ch.dir_mk))[slc_py][:][:]
                    myIm[myMask == False] = 0
                    win.myIm = copy.deepcopy(myIm)
                else: 
                    win.myIm = copy.deepcopy(myIm)
                    win.win_msg('*No mask for this channel ('+ch_name+'). Image was reset to RAW instead')
            else: #rtype = 'raw'
                win.myIm = copy.deepcopy(myIm)

        #Plot image with closed contours
        params = {'myIm': copy.deepcopy(win.myIm), 'slc_user': slc_user, 'ch': ch_name, 
                    'level': level, 'min_contour_length': min_contour_len}
        win.add_thumbnail(function ='fcC.plot_contours_slc', params = params, 
                            name = 'Cont Slc '+str(slc_user))
        win.plot_contours_slc(params)
    else: 
        win.win_msg('*Please enter the slices you would like to close from the current slice tuple ('+str(win.slc_tuple[0]+1)+'-'+str(win.slc_tuple[1])+')')
  
def get_clicks(clicks, myIm, scale, text):
    """
    Function to get clicks of prompted image slice.
    """

    print("- Getting clicks... Press ENTER when done")

    window_width = int(myIm.shape[1] * scale)
    window_height = int(myIm.shape[0] * scale)

    def on_mouse(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            #print ('\r    Seed: ' + str(y) + ', ' + str(x), myIm[y,x])
            clicks.append((y,x))
    text = text+' - Getting clicks... Press ENTER when done'
    cv2.namedWindow(text, cv2.WINDOW_NORMAL)#,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(text, window_width, window_height)
    cv2.setMouseCallback(text, on_mouse, 0, )
    cv2.imshow(text, myIm)
    cv2.waitKey()
    cv2.destroyAllWindows()

    return clicks

def draw_line(clicks, myIm, color_draw):
    """
    Function that draws white or black line connecting all the clicks received as input
    """

    for num, click in enumerate(clicks):
        if num < len(clicks)-1:
            pt1x, pt1y = click
            pt2x, pt2y = clicks[num+1]
            rr, cc, val = line_aa(int(pt1x), int(pt1y),
                                  int(pt2x), int(pt2y))
            rr1, cc1, val1 = line_aa(int(pt1x)+1, int(pt1y),
                                     int(pt2x)+1, int(pt2y))
            rr2, cc2, val2 = line_aa(int(pt1x)-1, int(pt1y),
                                     int(pt2x)-1, int(pt2y))
            if color_draw == "white" or color_draw == "":
                myIm[rr, cc] = val * 50000
            elif color_draw == "1":
                myIm[rr, cc] = 1
                myIm[rr1, cc1] = 1
                myIm[rr2, cc2] = 1
            elif color_draw == "0":
                myIm[rr, cc] = 0
                myIm[rr1, cc1] = 0
                myIm[rr2, cc2] = 0
            else: #"black"
                myIm[rr, cc] = val * 0
                myIm[rr1, cc1] = val1 * 0
                
    return myIm

def crop_n_close(clicks, myIm, box, level):
    """
    Function that crops a rectangular region of the input image centered by the click, gets the contours present in that
    region and connects the two closest contours with a white line

    """
    kw, kh = box
    wh = kw//2
    ww = kh//2

    for click in clicks:
        y0, x0 = click

        #Crop image in a square with center: click
        ymin = y0-wh
        xmin = x0-ww
        if ymin < 0:
            ymin = 0
        if xmin < 0:
            xmin = 0
        imCrop = myIm[ymin:y0+wh,xmin:x0+ww]

        #Get contours of the cropped image
        contours_crop = measure.find_contours(imCrop, level, 'high', 'high')
        #Organize contours in terms of number of points to get the two biggest
        contours_crop = sorted(contours_crop, key = len, reverse=True)
        
        if len(contours_crop) > 1:
            #Find euclidian distance beteen all points in contours
            dist = cdist(contours_crop[0],contours_crop[1])
            #Get indexes where distance is minimum (closest points)
            index4min = np.where(dist == np.amin(dist))

            index_ptCont0 = index4min[0][0]
            ptCont0 = contours_crop[0][index_ptCont0]
            index_ptCont1 = index4min[1][0]
            ptCont1 = contours_crop[1][index_ptCont1]

            rr, cc, val = line_aa(int(ptCont0[0]), int(ptCont0[1]), int(ptCont1[0]), int(ptCont1[1]))
            imCrop[rr, cc] = val * 50000

    return myIm

def xy_allContours(contours):
    """
    Function to create a unique array including all the points that make up a list of contours

    """
    coordsXY = []

    if len(contours) == 1:
        coordsXY = np.array(contours)[0]
    else:
        for num, cont in enumerate(contours):
            coords2add = cont
            if len(coordsXY) == 0:
                coordsXY = coords2add
            else:
                coordsXY = np.concatenate((coordsXY,coords2add))

    return coordsXY

def selectHull(merge, xy_contours):
    """
    Function that selects the longest good hull
    """

    eu_dist = []
    pts1 = []
    pts2 = []
    if len(merge) > 0:
        for num, pair in enumerate(merge):
            #print(num,pair)
            x1 = xy_contours[pair[0]][0]
            y1 = xy_contours[pair[0]][1]
            xy1 = (x1,y1)
    
            x2 = xy_contours[pair[1]][0]
            y2 = xy_contours[pair[1]][1]
            xy2 = (x2,y2)
    
            eu_dist.append(distance.euclidean(xy1,xy2))
            pts1.append(xy1)
            pts2.append(xy2)
    
            index4max = np.where(eu_dist == np.amax(eu_dist))
            closing_pt1 = pts1[index4max[0][0]]
            closing_pt2 = pts2[index4max[0][0]]
    else: 
        closing_pt1 = []
        closing_pt2 = []
    
    return closing_pt1, closing_pt2

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
        ax.plot(contour[:,1], contour[:,0], linewidth=0.25, color=win.contours_palette[num])
        # txt = "Cont"+str(num)
        # ax.text(txt_pos[num][0], txt_pos[num][1],#0.95,(0.97-0.035*(num+1)), 
        #         txt,
        #         verticalalignment='top', horizontalalignment='left',
        #         transform=ax.transAxes,
        #         color=win.contours_palette[num], fontsize=2, weight = 'semibold')
        ax.set_axis_off()

    win.fig_title.setText("Channel "+str(ch[-1])+" / Slice "+str(slc))

    # Grid where subplots of each contour will be placed
    all_grid = outer_grid[1].subgridspec(rows, cols, wspace=0, hspace=0)

    # Iterate through sorted contours
    for index, contList in enumerate(cont_plot):
        ax = fig11.add_subplot(all_grid[index])
        ax.imshow(myIm, cmap=plt.cm.gray)
        ax.plot(contList[:,1], contList[:,0], linewidth=0.15, color = win.contours_palette[index])
        ax.set_title("Contour "+str(index+1), fontsize=2, weight = 'semibold', 
                     color = win.contours_palette[index],  pad=0.15)
        ax.set_axis_off()

    win.canvas_plot.draw()

#%% Module loaded
print('morphoHeart! - Loaded funcContours')