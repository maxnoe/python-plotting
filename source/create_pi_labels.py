# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction

def create_pi_labels(a, b, step):
    values = np.arange(a, b+step/10, step)
    fracs = [Fraction(x) for x in values]

    labels = []

    for frac in fracs:
        if frac.numerator==0:
            labels.append(r"$0$")
        elif frac.denominator==1 and frac.numerator==1:
            labels.append(r"$\pi$")
        elif frac.denominator==1:
            labels.append(r"${}\pi$".format(frac.numerator))
        else:
            labels.append(r"$\frac{{{}}}{{{}}} \pi$".format(frac.numerator, frac.denominator))

    return labels

x = np.linspace(0, 2*np.pi, 1000)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title("Automatically create Labels as Multiples of $\pi$")

ax.plot(x, np.sin(x), 'r-', label=r"$\sin(x)$")
ax.plot(x, np.cos(x), 'b-', label=r"$\cos(x)$")

ax.grid()
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.1, 1.1)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$f(x)$")


ax.set_xticks(np.arange(0, 2*np.pi+0.1, 0.25*np.pi))

labels = create_pi_labels(0, 2, 0.25)
ax.set_xticklabels(labels)

ax.legend(loc="best")

fig.tight_layout()
fig.savefig("../images/create_pi_labels.png", dpi=300)
