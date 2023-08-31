import seaborn as sns
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
print(matplotlib.__version__)


#dir_df = Path('Z:\Data\Juliana\B_DATA_PROCESSED\LS_Processed\LS_morphoHeart\R_LS52_F02_V_SR_1029\Results_LS52_F02_V_SR_1029\csv_all\LS52_F02_V_SR_1029_hm_unloopAtr_MyocTh.csv')
dir_df = 'D:\Documents JSP\Dropbox\Dropbox_Juliana\PhD_Thesis\Data_ongoing\LS_ongoing\A_LS_Analysis\im_morphoHeart2\R_testing4 - Before ThBall - Copy\R_testing4\LS52_F02\csv_all\LS52_F02_dfUnloop_th_i2e[ch1-tiss]_atrium.csv'

df = pd.read_csv(str(dir_df))
print(df.sample(10))
df = df.drop(['taken'], axis=1)
print(df.sample(10))
df.astype('float16').dtypes

val = 'th_i2e[ch1-tiss]'
heatmap = pd.pivot_table(df, values= val, columns = 'theta', index='z_plane', aggfunc=np.max)
heatmap.astype('float16').dtypes
print(heatmap.sample(10))

fig, ax = plt.subplots(figsize=(16, 10))
b = sns.heatmap(heatmap, cmap='turbo', ax=ax)#, vmin = vmin, vmax = vmax)#, xticklabels=20, yticklabels=550)
x_pos = ax.get_xticks()
x_pos_new = np.linspace(x_pos[0], x_pos[-1], 19)
x_lab_new = np.arange(-180,200,20)
ax.set_xticks(x_pos_new) 

y_pos = ax.get_yticks()
y_pos_new = np.linspace(y_pos[0], y_pos[-1], 11)
ax.set_yticks(y_pos_new) 

plt.show()