# from scipy.interpolate import RegularGridInterpolator

# import numpy as np

# x, y = np.array([-2, 0, 4]), np.array([-2, 0, 2, 5])

# def ff(x, y):
#     print('x:',x,'y:', y)

#     return x**2 + y**2

# xg, yg = np.meshgrid(x, y, indexing='ij')

# data = ff(xg, yg)

# interp = RegularGridInterpolator((x, y), data,

#                                  bounds_error=False, fill_value=None)

# import matplotlib.pyplot as plt

# fig = plt.figure()

# ax = fig.add_subplot(projection='3d')

# ax.scatter(xg.ravel(), yg.ravel(), data.ravel(),

#            s=60, c='k', label='data')

# xx = np.linspace(-4, 9, 31)

# yy = np.linspace(-4, 9, 31)

# X, Y = np.meshgrid(xx, yy, indexing='ij')

# from vedo import *
# m1 = Mesh(dataurl+'bunny.obj')#.add_gaussian_noise(0.1)
# pts = m1.points()
# ces = m1.cell_centers()
# m1.pointdata["xvalues"] = np.power(pts[:,0], 3)
# m1.celldata["yvalues"]  = np.power(ces[:,1], 3)
# m2 = Mesh(dataurl+'bunny.obj')
# m2.resample_arrays_from(m1)
# # print(m2.pointdata["xvalues"])
# show(m1, m2 , N=2, axes=1)

# import numpy as np
# from scipy.interpolate import LinearNDInterpolator
# from scipy.interpolate import RegularGridInterpolator
# import matplotlib.pyplot as plt

# #original data
# x = np.linspace(0, 1, num=20)
# y = np.linspace(1, 2, num=10)
# X, Y = np.meshgrid(x, y)
# values = np.random.rand(20, 10)
# points = np.column_stack((X.flatten(), Y.flatten()))
# values_flat = values.flatten()

# #LinearNDInterpolation
# interfunc = LinearNDInterpolator(points, values_flat)
# x1 = np.linspace(0, 1, num=3000)
# y1 = np.linspace(1, 2, num=3000)
# X1, Y1 = np.meshgrid(x1, y1)
# interpolated_values = interfunc(np.column_stack((X1.flatten(), Y1.flatten())))
# interpolated_values = interpolated_values.reshape(X1.shape)
# fig, ax = plt.subplots()
# linear = ax.contourf(X1, Y1, interpolated_values.T)
# fig.colorbar(linear, ax=ax)

# #RegularGridInterpolation
# fig2, ax2 = plt.subplots()
# x2 = np.linspace(0, 1, num=3000)
# y2 = np.linspace(1, 2, num=3000)
# X2, Y2 = np.meshgrid(x2, y2)
# points_grid = (x, y)
# interfunc_grid = RegularGridInterpolator(points_grid, values, method="linear")
# interpolated_values_grid = interfunc_grid(np.column_stack((X2.flatten(), Y2.flatten())))
# interpolated_values_grid = interpolated_values_grid.reshape(X2.shape)
# d = ax2.contourf(X2, Y2, interpolated_values_grid.T)
# fig2.colorbar(d, ax=ax2)
# plt.show()


# import numpy as np
# from matplotlib import pyplot as plt

# data = '''0.615   5.349
#     0.615   5.413
#     0.617   6.674
#     0.617   6.616
#     0.63    7.418
#     0.642   7.809
#     0.648   8.04
#     0.673   8.789
#     0.695   9.45
#     0.712   9.825
#     0.734   10.265
#     0.748   10.516
#     0.764   10.782
#     0.775   10.979
#     0.783   11.1
#     0.808   11.479
#     0.849   11.951
#     0.899   12.295
#     0.951   12.537
#     0.972   12.675
#     1.038   12.937
#     1.098   13.173
#     1.162   13.464
#     1.228   13.789
#     1.294   14.126
#     1.363   14.518
#     1.441   14.969
#     1.545   15.538
#     1.64    16.071
#     1.765   16.7
#     1.904   17.484
#     2.027   18.36
#     2.123   19.235
#     2.149   19.655
#     2.172   20.096
#     2.198   20.528
#     2.221   20.945
#     2.265   21.352
#     2.312   21.76
#     2.365   22.228
#     2.401   22.836
#     2.477   23.804'''

# data = np.array([line.split() for line in data.split('\n')],dtype=float)

# x,y = data.T
# xd = np.diff(x)
# yd = np.diff(y)
# dist = np.sqrt(xd**2+yd**2)
# u = np.cumsum(dist)
# u = np.hstack([[0],u])

# t = np.linspace(0,u.max(),10)
# xn = np.interp(t, u, x)
# yn = np.interp(t, u, y)

"""Modify a spline interactively.
- Drag points with mouse
- Add points by clicking on the line
- Remove them by selecting&pressing DEL
--- PRESS q TO PROCEED ---"""
from vedo import Circle, KSpline, show
import numpy as np

cl_pts = np.array([[64.11766,-52.123386,19.028566],
[64.38801,-52.36957,19.964714],
[64.633965,-52.586224,20.893393],
[64.856125,-52.774246,21.814817],
[65.055084,-52.93455,22.729187],
[65.231415,-53.068054,23.636715],
[65.38571,-53.17566,24.537603],
[65.51856,-53.258274,25.432062],
[65.63055,-53.31682,26.320297],
[65.72226,-53.352196,27.202518],
[65.79429,-53.36532,28.078928],
[65.84721,-53.357094,28.949738],
[65.88164,-53.328438,29.815151],
[65.898125,-53.280254,30.675377],
[65.897285,-53.21346,31.530622],
[65.879684,-53.12896,32.381096]])

# Create a set of points in space
# pts = Circle(res=8).extrude(zshift=0.5).ps(4)
pts = KSpline(cl_pts, res=50)

# Visualize the points
plt = show(pts, __doc__, interactive=False, axes=1)

# Add the spline tool using the same points and interact with it
sptool = plt.add_spline_tool(pts, closed=True)
plt.interactive()

# Switch off the tool
sptool.off()

# Extract and visualize the resulting spline
sp = sptool.spline().lw(4)
show(sp, "My spline is ready!", interactive=True, resetcam=False).close()



        #Text
        text = '>> Modify Extended Centreline - Instructions: \n  -Drag extreme centreline points with mouse\n  -Remove them by selecting and pressing -Delete-\n  -Press q when ready to proceed.'
        txt = vedo.Text2D(text, c=txt_color, font=txt_font, s=txt_size)

        #Make the user define the final points for the centreline
        vp = vedo.Plotter(N=1, axes=1)
        vp.add_icon(logo, pos=(0.9,1), size=0.25)
        vp.show(mesh, kspl_o, txt, interactive=False, at=0)
        # Add the spline tool using the same points and interact with it
        sptool = vp.add_spline_tool(kspl_o, closed=False)
        vp.interactive()
        # Switch off the tool
        sptool.off()
        # Extract and visualize the resulting spline
        sp = sptool.spline().lw(4)
        vp.close()

        text = '> Final extended centreline/ribbon. \n  Close window to continue.'
        txt = vedo.Text2D(text, c=txt_color, font=txt_font, s=txt_size)
        vp2 = vedo.Plotter(N=1, axes=1)
        vp2.add_icon(logo, pos=(0.9,1), size=0.25)
        vp2.show(mesh, sp, txt, interactive=True, at=0)