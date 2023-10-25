from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import copy

path_src = Path('D:/Documents JSP/Dropbox/Dropbox_Juliana/PhD_Thesis/Data_ongoing/LS_ongoing/A_LS_Analysis/im_morphoHeart/LS52_F02_V_SR_1029_2A/Results_LS52_F02_V_SR_1029/txt_npy')
dir_ch1_int = path_src / Path('LS52_F02_V_SR_1029_s3_ch0_int.npy')
dir_ch1_tiss = path_src / Path('LS52_F02_V_SR_1029_s3_ch0_all.npy')
dir_ch1_ext = path_src / Path('LS52_F02_V_SR_1029_s3_ch0_ext.npy')

dir_ch2_int = path_src / Path('LS52_F02_V_SR_1029_s3_ch1_int.npy')
dir_ch2_tiss = path_src / Path('LS52_F02_V_SR_1029_s3_ch1_all.npy')
dir_ch2_ext = path_src / Path('LS52_F02_V_SR_1029_s3_ch1_ext.npy')


ch1_int = np.load(dir_ch1_int)
ch1_tiss = np.load(dir_ch1_tiss)
ch1_ext = np.load(dir_ch1_ext)

ch2_int = np.load(dir_ch2_int)
ch2_tiss = np.load(dir_ch2_tiss)
ch2_ext = np.load(dir_ch2_ext)

def plot_slc(int, tiss, ext, slc): 
    im_int = int[:,:,slc]
    im_tiss = tiss[:,:,slc]
    im_ext = ext[:,:,slc]
    plot(im_int, im_tiss, im_ext, slc)

def plot(imIntFilledCont, imExtFilledCont, imAllFilledCont, slcNum): 
        
    figR, axR = plt.subplots(1,3, figsize=(10, 3.5))
    axR[0].imshow(imIntFilledCont)
    axR[0].set_title("Filled Internal Contours", fontsize=10)
    axR[0].set_xticks([])
    axR[0].set_yticks([])

    axR[1].imshow(imExtFilledCont)
    axR[1].set_title("Filled External Contours", fontsize=10)
    axR[1].set_xticks([])
    axR[1].set_yticks([])

    axR[2].imshow(imAllFilledCont)
    axR[2].set_title("Filled All Contours", fontsize=10)
    axR[2].set_xticks([])
    axR[2].set_yticks([])

plot_slc(ch1_int, ch1_tiss, ch1_ext, 100)
plot_slc(ch2_int, ch2_tiss, ch2_ext, 100)

#Cardiac jelly
s3 = copy.deepcopy(ch1_int)
s3_mask = copy.deepcopy(ch2_ext)
s3_bits = np.zeros_like(ch1_int, dtype='uint8')
s3_new =  np.zeros_like(ch1_int, dtype='uint8')
operation = 'AND-XOR'

for slc in range(s3.shape[2]):
    mask_slc = s3_mask[:,:,slc]
    toClean_slc = s3[:,:,slc]
    # Keep ch to use as mask as it is
    inv_slc = np.copy(mask_slc)
    if operation == 'XOR': 
        # inverted_mask or mask AND ch1_2clean
        toRemove_slc = np.logical_and(toClean_slc, inv_slc)
        # Keep only the clean bit
        cleaned_slc = np.logical_xor(toClean_slc, toRemove_slc)

    s3_bits[:,:,slc] = toRemove_slc
    s3_new[:,:,slc] = cleaned_slc
        
plot_slc(ch1_int, ch2_ext, s3_new, 100)
plot_slc(ch1_int, ch2_ext, s3_bits, 100)

#Create a channel including cardiac jelly and ch1
ch1_HA = np.zeros_like(ch1_int, dtype='uint8')
for slc in range(s3.shape[2]):
    ch_HA = np.logical_or(ch1_tiss[:,:,slc], s3_new[:,:,slc])
    ch1_HA[:,:,slc] = ch_HA

plot_slc(ch1_tiss, s3_new, ch1_HA, 100)


#Ch1+HA -CH1
s3 = copy.deepcopy(ch1_tiss)
s3_mask = copy.deepcopy(ch1_HA)
s3_HA = np.zeros_like(s3, dtype='uint8')
operation = 'XOR'

for slc in range(s3.shape[2]):
    s3_slc = s3[:,:,slc]
    mask_slc = s3_mask[:,:,slc]
    res_slc = np.logical_xor(s3_slc, mask_slc)

    s3_HA[:,:,slc] = res_slc

plot_slc(ch1_tiss, ch1_HA, s3_HA, 150)

