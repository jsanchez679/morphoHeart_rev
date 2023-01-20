# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 11:47:08 2023

@author: bi1jsa
"""

"""Hover mouse onto an object
to pop a flag-style label"""
from vedo import *

b = Mesh(dataurl+'bunny.obj').color('m')
c = Cube(side=0.1).compute_normals().alpha(0.8).y(-0.02).lighting("off").lw(1)

fp = b.flagpole('A flag pole descriptor\nfor a rabbit', font='Quikhand')
fp.scale(0.5).color('v').use_bounds() # tell camera to take fp bounds into account

c.caption('2d caption for a cube\nwith face indices', point=[0.044, 0.03, -0.04],
          size=(0.3,0.06), font="VictorMono", alpha=1)

# create a new object made of polygonal text labels to indicate the cell numbers
flabs = c.labels('id', on="cells", font='Theemim', scale=0.02, c='k')
vlabs = c.clone().clean().labels2d(font='ComicMono', scale=3, bc='orange7')

# create a custom entry to the legend
b.legend('Bugs the bunny')
c.legend('The Cube box')
lbox = LegendBox([b,c], font="Quikhand", width=0.15)#font="Bongas", width=0.25)

show(b, c, fp, flabs, vlabs, lbox, __doc__, axes=11, bg2='linen').close()

"""A flag-post style marker"""
from vedo import ParametricShape, precision, color_map, show

s = ParametricShape("RandomHills").cmap("coolwarm")

pts = s.clone().decimate(n=10).points()

fss = []
for p in pts:
    col = color_map(p[2], name="coolwarm", vmin=0, vmax=0.7)
    ht = precision(p[2], 3)
    fs = s.flagpost(f"Heigth:\nz={ht}m", p, c=col)
    fss.append(fs)

show(s, *fss, __doc__, bg="bb", axes=1, viewup="z")

"""Customizing a legend box"""
from vedo import *

s = Sphere()
c = Cube().x(2)
e = Ellipsoid().x(4)
h = Hyperboloid().x(6).legend('The description for\nthis one is quite long')

lb = LegendBox([s,c,e,h], width=0.3, height=0.4, markers='s').font("Kanopus")

cam = dict( # press C in window to get these numbers
    position=(10.4414, -7.62994, 4.18818),
    focal_point=(4.10196, 0.335224, -0.148651),
    viewup=(-0.252830, 0.299657, 0.919936),
    distance=11.0653,
    clipping_range=(3.69605, 21.2641),
)

show(s, c, e, h, lb, __doc__,
     axes=1, bg='lightyellow', bg2='white', size=(1400,800), camera=cam
).close()


"""Make a icon to indicate orientation
and place it in one of the 4 corners
within the same renderer"""
from vedo import *

plt = Plotter(axes=5)

plt += Text3D(__doc__).bc('tomato')

elg = Picture(dataurl+"images/embl_logo.jpg")

plt.add_icon(elg, pos=2, size=0.06)
plt.add_icon(VedoLogo(), pos=1, size=0.06)

plt.show().close()
