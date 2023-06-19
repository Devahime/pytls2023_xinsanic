from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Rectangle

def degree_range(n):
    start = np.linspace(0, 180, n+1, endpoint=True)[0:-1]
    end = np.linspace(0, 180, n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points


def rot_text(ang):
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation


def gauge(value, ranges=None, labels=['LOW', 'MEDIUM', 'HIGH', 'VERY HIGH', 'EXTREME'],
          colors='jet_r', title=None, bg_color='w'):

    N = len(labels)

    """
    if colors is a string, we assume it's a matplotlib colormap
    and we discretize in N discrete colors 
    """

    if isinstance(colors, str):
        cmap = cm.get_cmap(colors, N)
        cmap = cmap(np.arange(N))
        colors = cmap[::-1, :].tolist()
    if isinstance(colors, list):
        if len(colors) == N:
            colors = colors[::-1]
        else:
            raise Exception("\n\nnumber of colors {} not equal \
            to number of categories{}\n".format(len(colors), N))

    """
    begins the plotting
    """

    fig, ax = plt.subplots()

    """ 
    ranges=[0, 18.6, 25, 30, 48.59],
    -> calculate midpoints and angle ranges
    """

    if ranges == None:
        ang_range, mid_points = degree_range(N)
        max = 360
    else:
        max = ranges[len(ranges) - 1]

        ang_range = []
        mid_points = []
        for i in range(len(ranges) - 1):
            v_from = ranges[i]
            v_to = ranges[(i + 1)]

            # convert to angle ranges
            r_range = [v_from / max * 180, v_to / max * 180]

            ang_range.append(r_range)

            mid_points.append((r_range[0] + r_range[1]) / 2)

    labels = labels[::-1]

    """
    plots the sectors and the arcs
    """
    patches = []
    for ang, c in zip(ang_range, colors):
        # sectors
        patches.append(Wedge((0., 0.), .4, *ang, facecolor=bg_color, lw=2))
        # arcs
        patches.append(Wedge((0., 0.), .4, *ang, width=0.10,
                       facecolor=c, lw=2, alpha=0.5))

    [ax.add_patch(p) for p in patches]

    """
    set the labels (e.g. 'LOW','MEDIUM',...)
    """

    for mid, lab in zip(mid_points, labels):

        ax.text(0.45 * np.cos(np.radians(mid)), 0.45 * np.sin(np.radians(mid)), lab,
                horizontalalignment='center', verticalalignment='center', fontsize=14,
                fontweight='bold', rotation=rot_text(mid))

    """
    set the bottom banner and the title
    """
    if title != None:
        r = Rectangle((-0.4, -0.1), 0.8, 0.1, facecolor=bg_color, lw=2)
        ax.add_patch(r)

        ax.text(0, -0.05, title, horizontalalignment='center',
                verticalalignment='center', fontsize=22, fontweight='bold')

    """
    plots the arrow now
    """

    angle = 180 - (value / max * 180)

    print(angle, value, mid_points)

    ax.arrow(0, 0, 0.225 * np.cos(np.radians(angle)), 0.225 * np.sin(np.radians(angle)),
             width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')

    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor=bg_color, zorder=11))

    """
    removes frame and ticks, and makes axis equal and tight
    """

    ax.set_frame_on(False)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.axis('equal')
    ax.set_facecolor("#e3d0fc")
    plt.tight_layout()

    fig.set_facecolor("#e3d0fc")

    return fig