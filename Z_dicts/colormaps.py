#https://matplotlib.org/stable/tutorials/colors/colormaps.html
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from colorspacious import cspace_converter

x = np.linspace(0.0, 1.0, 100)
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

def plot_color_gradients2(name):
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(4, 2))
    print(axs)
    fig.subplots_adjust(#top=0.95, bottom=0.01, left=0.2, right=0.99,
                        wspace=0.05)
    # fig.suptitle(cmap_category + ' colormaps', fontsize=14, y=1.0, x=0.6)

    print(name)
    # Get RGB values for colormap.
    rgb = mpl.colormaps[name](x)[np.newaxis, :, :3]

    # Get colormap in CAM02-UCS colorspace. We want the lightness.
    lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
    L = lab[0, :, 0]
    L = np.float32(np.vstack((L, L, L)))

    axs[0].imshow(gradient, aspect='auto', cmap=mpl.colormaps[name])
    axs[0].set_axis_off()
    axs[1].imshow(L, aspect='auto', cmap='binary_r', vmin=0., vmax=100.)
    axs[1].set_axis_off()
    # pos = list(axs[0].get_position().bounds)
    # x_text = pos[0] - 0.01
    # y_text = pos[1] + pos[3]/2.
    # fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)

    plt.savefig(name+'.svg', dpi=300, format='svg', bbox_inches='tight', pad_inches=0.01)
    plt.savefig(name+'.png', dpi=300, format='png', bbox_inches='tight', pad_inches=0.01)
    plt.show()

def plot_color_gradients(name):
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(3, 2))
    print(axs)
    fig.subplots_adjust(#top=0.95, bottom=0.01, left=0.2, right=0.99,
                        wspace=0.05)
    # fig.suptitle(cmap_category + ' colormaps', fontsize=14, y=1.0, x=0.6)

    print(name)
    # Get RGB values for colormap.
    rgb = mpl.colormaps[name](x)[np.newaxis, :, :3]

    # Get colormap in CAM02-UCS colorspace. We want the lightness.
    lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
    L = lab[0, :, 0]
    L = np.float32(np.vstack((L, L, L)))

    axs.imshow(gradient, aspect='auto', cmap=mpl.colormaps[name])
    axs.set_axis_off()

    # pos = list(axs[0].get_position().bounds)
    # x_text = pos[0] - 0.01
    # y_text = pos[1] + pos[3]/2.
    # fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)

    plt.savefig(name+'.svg', dpi=300, format='svg', bbox_inches='tight', pad_inches=0.01)
    plt.savefig(name+'.png', dpi=300, format='png', bbox_inches='tight', pad_inches=0.01)
    plt.show()


cmap_list = ['turbo','viridis', 'jet', 'magma', 'inferno', 'plasma']
for name in cmap_list: 
    plot_color_gradients(name)


# cmaps = {}
# gradient = np.linspace(0, 1, 256)
# gradient = np.vstack((gradient, gradient))

# def plot_color_gradients(category, cmap_list):
#     # Create figure and adjust figure height to number of colormaps
#     nrows = len(cmap_list)
#     figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
#     fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
#     fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
#                         left=0.2, right=0.99)
#     axs[0].set_title(f'{category} colormaps', fontsize=14)

#     for ax, name in zip(axs, cmap_list):
#         ax.imshow(gradient, aspect='auto', cmap=mpl.colormaps[name])
#         ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=10,
#                 transform=ax.transAxes)

#     # Turn off *all* ticks & spines, not just the ones with colormaps.
#     for ax in axs:
#         ax.set_axis_off()

#     # Save colormap list for later.
#     cmaps[category] = cmap_list

# plot_color_gradients('Perceptually Uniform Sequential',
#                      ['viridis', 'plasma', 'inferno', 'magma', 'cividis'])

# plot_color_gradients('Sequential',
#                      ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
#                       'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
#                       'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'])

# mpl.rcParams.update({'font.size': 14})
# # Indices to step through colormap.
# x = np.linspace(0.0, 1.0, 100)
# gradient = np.linspace(0, 1, 256)
# gradient = np.vstack((gradient, gradient))

# def plot_color_gradients(cmap_category, cmap_list):
#     fig, axs = plt.subplots(nrows=len(cmap_list), ncols=2)
#     fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99,
#                         wspace=0.05)
#     # fig.suptitle(cmap_category + ' colormaps', fontsize=14, y=1.0, x=0.6)

#     for ax, name in zip(axs, cmap_list):
#         print(name)
#         # Get RGB values for colormap.
#         rgb = mpl.colormaps[name](x)[np.newaxis, :, :3]

#         # Get colormap in CAM02-UCS colorspace. We want the lightness.
#         lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
#         L = lab[0, :, 0]
#         L = np.float32(np.vstack((L, L, L)))

#         ax[0].imshow(gradient, aspect='auto', cmap=mpl.colormaps[name])
#         ax[1].imshow(L, aspect='auto', cmap='binary_r', vmin=0., vmax=100.)
#         pos = list(ax[0].get_position().bounds)
#         x_text = pos[0] - 0.01
#         y_text = pos[1] + pos[3]/2.
#         fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)

#     # Turn off *all* ticks & spines, not just the ones with colormaps.
#     for ax in axs.flat:
#         ax.set_axis_off()

#     plt.show()

# for cmap_category, cmap_list in cmaps.items():
#     print(cmap_category, cmap_list)
#     plot_color_gradients(cmap_category, cmap_list)