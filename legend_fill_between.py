# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

"""
In physics you often want to show a one-sigma area around a graph, most likely
for a fit. This will be done with the fill_between function. However, matplotlib
does not support adding a fill_between to the legend directly via a label argument
or passing the artist instace which is returned by fill_between to the legend.
An easy solution is a so called proxy artist, a Rectangle without dimension but
using the same style options as the fill_between comman.
"""

x = np.linspace(0, 2*np.pi, 1000)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)


# the plot-command returns a list of the drawn lines
plot_sin = ax.plot(x, np.sin(x), 'b-')
ax.fill_between(x, 0.95*np.sin(x), 1.05*np.sin(x), color='b', alpha=0.3)

plot_cos = ax.plot(x, np.cos(x), 'r-')
ax.fill_between(x, 0.95*np.cos(x), 1.05*np.cos(x), color='r', alpha=0.3)

# Create Rectangles without height or width but with the same colors as your
# plot
rect_cos = Rectangle((0,0), 0,0, color='r', alpha=0.3)
rect_sin = Rectangle((0,0), 0,0, color='b', alpha=0.3)

# a list of Objects you want to have in the legend
objects = [plot_sin[0], rect_sin, plot_cos[0], rect_cos]
# a list of labels for yout objects
labels = [r"$\sin(x)$", r"$1\sigma$-area",r"$\cos(x)$", r"$1\sigma$-area"]

# create the legend
ax.legend(objects, labels, loc="best")

# no plot without labels on the axis

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$f(x)$")


ax.grid()
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.1, 1.1)

# always call tight_layout before saving ;)
fig.tight_layout()
fig.savefig("legend_fill_between.pdf", dpi=300)
