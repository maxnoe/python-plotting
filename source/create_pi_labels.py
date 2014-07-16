# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction

def create_pi_labels(a=0, b=2, step=0.5):
    values = np.arange(a, b+0.1*step, step)
    fracs = [Fraction(x) for x in values]
    ticks = values*np.pi

    labels = []

    for frac in fracs:
        if frac.numerator==0:
            labels.append(r"$0$")
        elif frac.numerator<0:
            if frac.denominator==1 and abs(frac.numerator)==1:
                labels.append(r"$-\pi$")
            elif frac.denominator==1:
                labels.append(r"$-{}\pi$".format(abs(frac.numerator)))
            else:
                labels.append(r"$-\frac{{{}}}{{{}}} \pi$".format(abs(frac.numerator), frac.denominator))
        else:
            if frac.denominator==1 and frac.numerator==1:
                labels.append(r"$\pi$")
            elif frac.denominator==1:
                labels.append(r"${}\pi$".format(frac.numerator))
            else:
                labels.append(r"$\frac{{{}}}{{{}}} \pi$".format(frac.numerator, frac.denominator))

    return ticks, labels

x = np.linspace(-np.pi, 2*np.pi, 1000)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title("Automatically create Labels as Multiples of $\pi$")

ax.plot(x, np.sin(x), 'r-', label=r"$\sin(x)$")
ax.plot(x, np.cos(x), 'b-', label=r"$\cos(x)$")

ax.grid()
ax.set_xlim(-np.pi, 2*np.pi)
ax.set_ylim(-1.1, 1.1)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$f(x)$")



ticks, labels = create_pi_labels(-1, 2, 0.5)
ax.set_xticks(ticks)
ax.set_xticklabels(labels)

ax.legend(loc="best")

fig.tight_layout()
fig.savefig("../images/create_pi_labels.png", dpi=300)
