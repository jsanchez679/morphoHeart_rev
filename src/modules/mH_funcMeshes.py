'''
morphoHeart_funcBasics

Version: Dec 01, 2022
@author: Juliana Sanchez-Posada

'''
#%% ##### - Imports - ########################################################
import vedo as vedo


#%% ##### - morphoHeart Imports - ##################################################
# from .mH_funcBasics import *
# from .mH_classes import *


#%%
man = vedo.Mesh(vedo.dataurl+'man.vtk').c('white').lighting('glossy')

p1 = vedo.Point([1,0,1], c='y')
p2 = vedo.Point([0,0,2], c='r')
p3 = vedo.Point([-1,-0.5,-1], c='b')
p4 = vedo.Point([0,1,0], c='k')

# Add light sources at the given positions
l1 = vedo.Light(p1, c='y') # p1 can simply be [1,0,1]
l2 = vedo.Light(p2, c='r')
l3 = vedo.Light(p3, c='b')
l4 = vedo.Light(p4, c='w', intensity=0.5)

# vedo.show(man, l1, l2, l3, l4, p1, p2, p3, p4, __doc__, axes=1, viewup='z').close()

plt = vedo.Plotter(axes=1)
plt += [man, p1, p2, p3, p4, l1, l2, l3, l4]
plt.show(viewup='z')

#%% Module loaded
print('morphoHeart! - Loaded funcMeshes')