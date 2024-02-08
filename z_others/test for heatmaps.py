import seaborn as sns
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
print(matplotlib.__version__)
import os

conda_env = os.environ['CONDA_DEFAULT_ENV']
print(conda_env)


#https://stackoverflow.com/questions/56942670/first-and-last-row-cut-in-half-of-heatmap-plot
#https://datascience.stackexchange.com/questions/57245/seaborn-heatmap-not-displaying-correctly

#dir_df = Path('Z:\Data\Juliana\B_DATA_PROCESSED\LS_Processed\LS_morphoHeart\R_LS52_F02_V_SR_1029\Results_LS52_F02_V_SR_1029\csv_all\LS52_F02_V_SR_1029_hm_unloopAtr_MyocTh.csv')
dir_df = 'D:\Documents JSP\Dropbox\Dropbox_Juliana\PhD_Thesis\Data_ongoing\LS_ongoing\A_LS_Analysis\im_morphoHeart2\R_testing4 - Before ThBall - Copy\R_testing4\LS52_F02\csv_all\LS52_F02_dfUnloop_th_i2e[ch1-tiss]_ventricle.csv'

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
c = ax.pcolor(heatmap, cmap='turbo',vmin=0, vmax=20)#, alpha=0.8)
cb = fig.colorbar(c, ax=ax)
cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=6)
# ax.axes.set_aspect('scaled')
ax.invert_yaxis()

# set the xtick labels
x_pos = ax.get_xticks()
print(x_pos)
# xlabels=np.linspace(heatmap.columns.min(), heatmap.columns.max(), len(x_pos)).round(3)
# print(xlabels)
# ax.set_xticks(ticks=x_pos, labels=xlabels)


x_pos_new = np.linspace(x_pos[0], x_pos[-1], 13)
x_lab_new = np.arange(-180,200,30)
ax.set_xticks(x_pos_new) 
ax.set_xticklabels(x_lab_new, rotation=30, fontsize=6)#, fontname='Arial')


y_pos = ax.get_yticks()
print(y_pos)
ylabels=np.linspace(heatmap.index.min(), heatmap.index.max(), len(y_pos)).round(2)
ax.set_yticks(ticks=y_pos, labels=ylabels)
print(ylabels)

# y_pos_new = np.linspace(y_pos[0], y_pos[-1], 11)
# y_labels = sorted([0,1])
# y_lab_new = np.linspace(y_labels[0],y_labels[1],11)

# # ax.set_yticks(ticks=y_pos_new, labels = y_lab_new)
# yticks = ax.get_yticks()
# ax.set_yticks(ticks=y_pos, labels=np.linspace(heatmap.index.min(), heatmap.index.max(), len(y_pos)).round(3))


y_pos = ax.get_yticks()
print(y_pos)
y_pos_new = np.linspace(y_pos[0], y_pos[-1], 11)
y_labels = sorted([0,1])
y_lab_new = np.linspace(y_labels[0],y_labels[1],11)
y_lab_new = [format(y,'.2f') for y in y_lab_new]
ax.set_yticks(y_pos_new)
ax.set_yticklabels(y_lab_new, rotation=0, fontsize=6)#, fontname='Arial') 

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)




# xticks = ax.get_xticks()
# xlabels = np.linspace(heatmap.columns.min(), heatmap.columns.max(), 8).round(3)
# ax.set_xticks(xticks, xlabels)

# # set the ytick labels
# ax.set_yticks(ticks=ax.get_yticks(), labels=np.linspace(heatmap.index.min(), heatmap.index.max(), 8).round(3))

# reverse the yaxis to emulate seaborn


# # b = sns.heatmap(heatmap, cmap='turbo', ax=ax)#, vmin = vmin, vmax = vmax)#, xticklabels=20, yticklabels=550)
# x_pos = ax.get_xticks()
# x_pos_new = np.linspace(x_pos[0], x_pos[-1], 19)
# x_lab_new = np.arange(-180,200,20)
# ax.set_xticks(x_pos_new) 

# y_pos = ax.get_yticks()
# y_pos_new = np.linspace(y_pos[0], y_pos[-1], 11)
# ax.set_yticks(y_pos_new) 

# plt.show()


fig, ax = plt.subplots(figsize=(16, 10))
b = sns.heatmap(heatmap, cmap='turbo', ax=ax)#, vmin = vmin, vmax = vmax)#, xticklabels=20, yticklabels=550)
print('x:',b.get_xlim())
print('y:',b.get_ylim())
b.set_ylim(sorted(b.get_xlim(), reverse=True))

b.set_xlim(-180,180)
# b.set_ylim(1,2)




plt.show()