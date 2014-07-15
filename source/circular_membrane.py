# -*- coding: utf-8 -*-
# I'm using python2 because of a python3 bug under arch linux a saving the
# animation
from __future__ import unicode_literals, print_function, division
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D
# get bessel functions and root of the besselfunctions
from scipy.special import jn, jn_zeros


fig = plt.figure(figsize=(12.8, 7.2))
ax = fig.add_subplot(1,1,1, projection='3d')

radius=2

r, phi = np.meshgrid(np.linspace(0, radius, 50), np.linspace(0, 2*np.pi, 52))

x, y = r*np.cos(phi), r*np.sin(phi)

bessel_roots=np.array([jn_zeros(0,5), jn_zeros(1,5),jn_zeros(2,5),jn_zeros(3,5)])

def ani_welle(t):
    step = int(t/np.pi)

    l = (step//12)
    m = (step//4)%3

    z = jn(m,bessel_roots[m,l]*r/radius)*np.cos(m*phi)*np.sin(t)
    ax.cla()
    plot = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap="jet",vmin=-1, vmax=1, label="test", linewidth=0)
    ax.set_zlim(-1.1,1.1)
    ax.set_title("circular membrane: l={}, m={}-Mode".format(l+1,m))

anim = ani.FuncAnimation(fig, ani_welle, np.linspace(0, 36*np.pi, 1800 ))
anim.save('circular_membrane.mp4', dpi=100, bitrate=16384, fps=25 )
